"""Run synthetic decision cases through the real v0.7 JSON-lines CLI with egress denied."""

from datetime import UTC, datetime, timedelta
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory


# Blocks every socket operation in the child, including DNS and loopback.
OFFLINE_BOOTSTRAP = """
import runpy
import sys

def deny_socket(event, arguments):
    if event.startswith("socket."):
        raise RuntimeError("network disabled for offline acceptance")

sys.addaudithook(deny_socket)
runpy.run_module("psychohistory.cli", run_name="__main__")
"""

JOINT = ("房租和停车费合计每月最多3000元。A：每月房租2600元，停车费每月500元。"
         "B：每月房租2600元，停车费每月300元。C：每月房租2600元，停车费300。")
NIGHT = ("我不接受夜班。A：老板说没有夜班。B：当前实际排班有夜班。"
         "C：当前实际排班没有夜班。D：承诺不安排夜班。")
CHOICE = "我该选「方案甲」，还是「方案乙」？"
SCENARIOS = (CHOICE + "情景平常：方案甲得10分，方案乙得6分。情景变动：方案甲得0分，方案乙得7分。"
             "都比较未来30天，分差可比较，分数越高越好。")


def session(view):
    return {key: view[key] for key in ("session_id", "revision")}


def confirm(call, view, **kwargs):
    pending = [item["id"] for item in view["claims"] if item["status"] == "PROVISIONAL"]
    options = [item["id"] for item in view["options"]]
    return call("confirm", {**session(view), "claim_ids": pending, "option_ids": options,
                            "accept_context": True, **kwargs})


def gate(view):
    return {row["label"]: row["status"] for row in view["analysis"]["feasibility"]}


def resource_fixtures(view):
    now = datetime.now(UTC).date()
    tomorrow = (now + timedelta(days=1)).isoformat()
    today = now.isoformat()
    keys = {item["label"]: item["id"] for item in view["options"]}
    cash = {"as_of": today, "cash": {"currency": "CNY", "opening_balance": "1000", "opening_date": today,
                                   "covered_through": today, "source": "虚构期初余额",
                                   "events": [
                                       {"kind": "actual_expense", "id": "paid", "amount": "400", "date": today, "source": "虚构已付款"},
                                       {"kind": "actual_refund", "id": "received", "amount": "150", "date": today, "source": "虚构已到账", "refund_of": "paid"},
                                       {"kind": "estimated_income", "id": "forecast", "amount": "1000", "date": today, "source": "虚构未到账"},
                                   ]},
            "options": [{"option_id": keys["方案甲"], "future_cost": "800"},
                        {"option_id": keys["方案乙"], "future_cost": "700"}]}
    time = {"as_of": today, "capacity": [{"date": today, "minutes": 0}, {"date": tomorrow, "minutes": 120}],
            "shared_tasks": [{"id": "old-plan", "label": "虚构旧计划", "total_minutes": 150,
                              "completed_minutes": 60, "deadline": tomorrow, "mode": "splittable",
                              "source": "虚构进度", "prior_plan_id": "old-decision"}],
            "options": [{"option_id": keys["方案甲"], "tasks": [{"id": "new-a", "label": "虚构新事项", "total_minutes": 25,
                         "completed_minutes": 0, "deadline": tomorrow, "mode": "splittable", "source": "虚构计划"}]},
                        {"option_id": keys["方案乙"], "tasks": [{"id": "new-b", "label": "虚构连续事项", "total_minutes": 20,
                         "completed_minutes": 0, "deadline": tomorrow, "mode": "continuous", "source": "虚构计划"}]}]}
    return cash, time


def exercise(call):
    status = call("status", {})
    assert status["cognition"]["network"] == "OFFLINE"
    joint = call("start", {"question": JOINT, "use_local_model": True})
    assert joint["local_model_status"] == "LEGACY_REQUEST_RETIRED"
    assert joint["analysis"] is None
    joint_view = confirm(call, joint)
    assert gate(joint_view) == {"A": "REJECT", "B": "ACCEPT", "C": "UNRESOLVED"}
    night = confirm(call, call("start", {"question": NIGHT}))
    assert gate(night) == {"A": "UNRESOLVED", "B": "REJECT", "C": "ACCEPT", "D": "UNRESOLVED"}
    risk = confirm(call, call("start", {"question": SCENARIOS}))
    regret = next(row for row in risk["analysis"]["methods"] if row["model_id"] == "C029")
    assert regret["status"] == "EXECUTED"
    assert all(row["probability"] is None for row in risk["state"]["scenarios"])
    selected = [item["label"] for item in risk["options"] if item["id"] in regret["result"]["leaders"]]
    assert selected == ["方案乙"]
    resource = confirm(call, call("start", {"question": CHOICE}))
    cash, timing = resource_fixtures(resource)
    updated = call("update_resources", {**session(resource), "resources": cash, "confirmed": True})
    assert gate(updated) == {"方案甲": "REJECT", "方案乙": "ACCEPT"}
    assert updated["resources"]["result"]["cash"]["balance"] == "750.00"
    timed = call("update_resources", {**session(updated), "resources": timing, "confirmed": True})
    assert gate(timed) == {"方案甲": "ACCEPT", "方案乙": "UNRESOLVED"}
    timing["shared_tasks"][0]["completed_minutes"] = 30
    delayed = call("update_resources", {**session(timed), "resources": timing, "confirmed": True})
    assert gate(delayed) == {"方案甲": "REJECT", "方案乙": "REJECT"}
    assert call("analyze", session(timed))["status"] == "REJECTED"
    call("end", {"session_id": delayed["session_id"]})
    assert call("analyze", session(delayed))["status"] == "REJECTED"
    return {"candidate": status["conversation_version"], "math_version": status["engine_version"],
            "joint": {"question": JOINT, "feasibility": gate(joint_view)},
            "night": {"question": NIGHT, "feasibility": gate(night)},
            "risk": {"question": SCENARIOS, "executed": regret["model_id"], "leaders": selected},
            "cash": {"snapshot": cash, "balance": "750.00", "feasibility": gate(updated)},
            "time": {"revised_snapshot": timing, "before": gate(timed), "after": gate(delayed)},
            "obsolete_revision": "REJECTED", "ended_session": "REJECTED"}


def main():
    source = Path(__file__).resolve().parents[1] / "src"
    environment = {**os.environ, "PYTHONPATH": str(source), "PSYCHOHISTORY_LOCAL_AI": "1",
                   "PSYCHOHISTORY_LOCAL_MODEL": "obsolete-fixture", "OLLAMA_HOST": "http://127.0.0.1:11434"}
    with TemporaryDirectory(prefix="ph-v07-offline-") as directory, subprocess.Popen(
        [sys.executable, "-c", OFFLINE_BOOTSTRAP, "--data", str(Path(directory) / "workspace"), "decision-v07"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, encoding="utf-8", env=environment,
    ) as process:
        def call(operation, data):
            process.stdin.write(json.dumps({"operation": operation, "data": data}, ensure_ascii=False) + "\n")
            process.stdin.flush()
            return json.loads(process.stdout.readline())

        try:
            result = exercise(call)
        finally:
            process.stdin.close()
        assert process.wait(timeout=10) == 0
    output = {"status": "PASS", "entry": "decision-v07 JSON lines", "socket_audit": "ALL_SOCKET_OPERATIONS_DENIED", **result}
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
