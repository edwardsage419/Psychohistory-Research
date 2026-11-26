"""Verify actual Chromium interaction against the instance-bound local API."""

from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlsplit
import argparse
import shutil

from playwright.sync_api import expect, sync_playwright

from browser_v06 import browser_session, connect, report_write


API = "/api/v8/decisions"
QUESTION = "预算最多3000元。A：费用4000元。B：费用2000元。我不能确定是否必须搬家。"


def post_ui(page, operation, click):
    with page.expect_response(lambda response: response.request.method == "POST"
                              and urlsplit(response.url).path == f"{API}/{operation}") as pending:
        click()
    response = pending.value
    assert response.ok, response.text()
    return response.json(), response.request.post_data_json


def button(page, label):
    return page.get_by_role("button", name=label, exact=True)


def session(view):
    return {key: view[key] for key in ("session_id", "session_instance", "revision")}


def run(report, chromium):
    with TemporaryDirectory(prefix="ph-v08-browser-") as temp, sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=chromium, headless=True,
                                             args=["--no-sandbox", "--disable-dev-shm-usage"])
        try:
            with browser_session(browser, Path(temp) / "workspace") as (page, url, token, requests):
                connect(page, url, token, version=None)
                area = page.locator("#decision-conversation")
                expect(area).to_have_attribute("data-workflow", "v08")
                page.get_by_role("textbox", name="你的决策问题", exact=True).fill(QUESTION)
                first, start_request = post_ui(page, "start", button(page, "开始对话").click)
                assert first["conversation_version"] == "0.8.0"
                assert first["cancel_nonce"] == start_request["cancel_nonce"] != first["session_id"]
                page.get_by_label("我已说明本次目的和硬约束", exact=True).check()
                page.get_by_label("我已核对本组理解", exact=True).check()
                confirmed, confirm_request = post_ui(page, "confirm", button(page, "确认本组理解").click)
                assert all(confirm_request[key] == value for key, value in session(first).items())
                assert confirmed["phase"] == "CLARIFY" and confirmed["analysis"] is None
                assert confirmed["partial_analysis"]["authority"] == "NONE"
                partial = page.get_by_role("region", name="已核对的局部分析")
                expect(partial).to_contain_text("4000")
                assert not page.request.post(f"{url}{API}/analyze", data=session(first),
                                             headers={"Authorization": f"Bearer {token}"}).ok
                with page.expect_request(lambda request: urlsplit(request.url).path == f"{API}/discard") as ended:
                    button(page, "结束本地会话").click()
                assert ended.value.post_data_json == session(confirmed)
                expect(partial).to_have_count(0)
                assert QUESTION not in page.content()
                assert f"{API}/start" in requests and f"{API}/confirm" in requests
                browser_version = browser.version
        finally:
            browser.close()
    report_write(report, {"status": "PASS", "protocol": "0.8.0", "chromium": browser_version,
                          "checks": ["instance-bound real HTTP and UI", "read-only partial analysis",
                                     "obsolete revision rejected", "session end and UI cleanup",
                                     "zero off-loopback requests and page errors"]})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=Path("/tmp/psychohistory-browser-v08.json"))
    parser.add_argument("--chromium", default=shutil.which("chromium"))
    arguments = parser.parse_args()
    run(arguments.report, arguments.chromium)
