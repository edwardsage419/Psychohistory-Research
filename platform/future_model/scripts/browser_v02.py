"""Exercise the v0.2 research workflow in Chromium against a real loopback service."""
import json
import os
from pathlib import Path
import re
import shutil
import sys

from playwright.sync_api import expect, sync_playwright


def posted(page, button, path, *, status=None):
    with page.expect_response(
        lambda response: response.url.endswith(f'/api/v2/{path}')
        and response.request.method == 'POST'
    ) as pending:
        button.click()
    response = pending.value
    assert (response.ok if status is None else response.status == status), (
        f'{path} returned {response.status}: {response.text()}'
    )
    return response.json()


def run():
    url = os.environ.get('PH_TEST_URL', 'http://127.0.0.1:8765')
    data = Path(os.environ.get('PH_TEST_DATA', '/tmp/psychohistory-web-check'))
    report = Path(os.environ.get('PH_BROWSER_REPORT', '/tmp/psychohistory-browser-v02.json'))
    token = (data / 'token').read_text().strip()
    headers = {'Authorization': f'Bearer {token}'}
    seed = os.environ.get('PH_TEST_SEED', '207')
    executable = os.environ.get('PH_CHROMIUM_EXECUTABLE') or shutil.which('chromium')
    args = ['--no-sandbox', '--disable-dev-shm-usage'] if sys.platform.startswith('linux') else []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=executable, headless=True, args=args)
        page = browser.new_page(viewport={'width': 1440, 'height': 1000})
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto(url)
        page.get_by_label('本地访问令牌').fill(token)
        page.get_by_role('button', name='连接工作空间', exact=True).click()
        expect(page.get_by_text('工作空间已连接', exact=True)).to_be_visible()
        page.get_by_role('button', name='研究工作流', exact=True).click(timeout=3500)

        catalog = page.get_by_role('combobox', name='科研来源目录', exact=True)
        register = page.get_by_role('button', name='登记来源', exact=True)
        catalog.select_option('R123')
        source = posted(page, register, 'sources')
        assert source['origin'] == 'MAIN', source['origin']
        source_id = source['source_id']
        sources = page.get_by_role('region', name='科研来源')
        source_card = sources.get_by_role('article').filter(has_text=source_id)
        expect(source_card.get_by_text('MAIN', exact=True)).to_be_visible()
        expect(source_card.get_by_text('BROWSE_ONLY', exact=True)).to_be_visible()
        verified = posted(page, source_card.get_by_role('button', name='校验来源'), f'sources/{source_id}/verify')
        assert verified['commit'] == source['commit']
        source_card.get_by_text('查看原始科研记录', exact=True).click()
        expect(source_card.locator('pre').filter(has_text='R123').first).to_be_visible()

        page.get_by_role('combobox', name='协议来源', exact=True).select_option(source_id)
        page.get_by_role('combobox', name='模型版本', exact=True).select_option('r123-degroot@1.0.0')
        page.get_by_label('协议随机种子', exact=True).fill(seed)
        protocol = posted(page, page.get_by_role('button', name='创建版本化协议'), 'protocols')
        protocol_id = protocol['protocol_id']
        protocol_card = page.get_by_role('article').filter(has_text=protocol_id)
        assert protocol['source_id'] == source_id and protocol['spec']['seed'] == int(seed)
        posted(page, protocol_card.get_by_role('button', name='批准协议'), f'protocols/{protocol_id}/approve')
        original = posted(page, protocol_card.get_by_role('button', name='提交研究实验'), 'experiments')
        assert original['status'] == 'PENDING', 'Use a fresh test data root or PH_TEST_SEED'
        original_id = original['id']
        current = page.get_by_role('region', name='所选研究实验')
        expect(current.get_by_text(original_id, exact=True)).to_be_visible()
        canceled = posted(page, current.get_by_role('button', name='取消研究实验'), f'experiments/{original_id}/cancel')
        assert canceled['status'] == 'CANCELED'
        expect(current.get_by_text('CANCELED', exact=True)).to_be_visible()

        retry = posted(page, current.get_by_role('button', name='重试研究实验'), f'experiments/{original_id}/retry')
        run_id = retry['id']
        assert run_id != original_id and retry['status'] == 'PENDING'
        expect(current.get_by_text(run_id, exact=True)).to_be_visible()
        posted(page, current.get_by_role('button', name='批准研究执行'), f'experiments/{run_id}/approve')
        terminal = current.get_by_text(re.compile(r'^(COMPLETED|FAILED|CANCELED|BLOCKED)$'))
        expect(terminal).to_be_visible(timeout=25000)
        assert terminal.inner_text() == 'COMPLETED', current.inner_text()

        results = page.get_by_role('region', name='不可变研究结果')
        expect(results.get_by_text('UNKNOWN', exact=True)).to_be_visible()
        expect(results.get_by_role('heading', name='可比指标')).to_be_visible()
        expect(results.get_by_role('heading', name='逐来源评分')).to_be_visible()
        expect(results.get_by_role('heading', name='权重敏感性')).to_be_visible()
        artifact = results.get_by_label('结果工件 SHA-256')
        expect(artifact).to_have_text(re.compile(r'^[0-9a-f]{64}$'))
        artifact_hash = artifact.inner_text()
        artifact_response = page.request.get(f'{url}/api/v2/experiments/{run_id}/result', headers=headers)
        assert artifact_response.ok, artifact_response.status
        artifact_record = artifact_response.json()
        assert artifact_record['artifact_sha256'] == artifact_hash
        output = artifact_record['result']
        for model in ('r123-degroot', 'train-prevalence'):
            metric_row = results.get_by_role('table').first.get_by_role('row').filter(has_text=model)
            expect(metric_row.get_by_role('cell').nth(1)).to_have_text(str(output['metrics'][model]['brier']))
            expect(metric_row.get_by_role('cell').nth(2)).to_have_text(str(output['metrics'][model]['log_loss']))
        for study in output['study_results']:
            expect(results.get_by_role('article', name=study['study_label'], exact=True).get_by_text('train-prevalence')).to_be_visible()
        for scenario in output['weight_sensitivity']:
            expect(results.get_by_role('article', name=scenario['label'], exact=True).get_by_text('r123-degroot')).to_be_visible()
        assert len(output['study_results']) == 2 and len(output['weight_sensitivity']) == 3
        expect(results.get_by_role('heading', name='适用边界与局限')).to_be_visible()
        expect(results.get_by_text(output['provenance']['input_sha256'], exact=True)).to_be_visible()
        expect(results.get_by_text(output['provenance']['protocol_sha256'], exact=True)).to_be_visible()
        expect(results.get_by_text(protocol_id, exact=True)).to_be_visible()
        expect(results.get_by_text(source_id, exact=True)).to_be_visible()
        expect(results.get_by_text(source['commit'], exact=True)).to_be_visible()
        history = page.get_by_role('region', name='研究实验历史')
        canceled_row = history.get_by_role('row').filter(has_text=original_id)
        expect(canceled_row.get_by_text('CANCELED', exact=True)).to_be_visible()
        canceled_row.get_by_role('button', name=original_id).click()
        expect(results).to_have_count(0)
        page.get_by_label('实验完整 ID', exact=True).fill(run_id)
        page.get_by_role('button', name='按 ID 查找实验', exact=True).click()
        expect(results.get_by_label('结果工件 SHA-256')).to_have_text(artifact_hash)

        candidate_id = os.environ.get('PH_TEST_CANDIDATE_ID')
        candidate_commit = os.environ.get('PH_TEST_CANDIDATE_COMMIT')
        assert bool(candidate_id) == bool(candidate_commit), 'Configure both candidate ID and commit'
        if candidate_id and candidate_commit:
            catalog.select_option(candidate_id)
            page.get_by_label('来源提交 SHA', exact=True).fill(candidate_commit)
            candidate = posted(page, register, 'sources')
            assert candidate['origin'] == 'CANDIDATE'
            candidate_card = sources.get_by_role('article').filter(has_text=candidate['source_id'])
            expect(candidate_card.get_by_text('CANDIDATE', exact=True)).to_be_visible()
            expect(candidate_card.get_by_text('BROWSE_ONLY', exact=True)).to_be_visible()
            posted(page, candidate_card.get_by_role('button', name='校验来源'), f"sources/{candidate['source_id']}/verify")
            assert candidate['source_id'] not in page.get_by_role('combobox', name='协议来源', exact=True).locator('option').evaluate_all(
                '(options) => options.filter(option => !option.disabled).map(option => option.value)'
            )
            denied = page.request.post(f'{url}/api/v2/protocols', headers=headers, data={
                'source_id': candidate['source_id'], 'seed': int(seed),
                'model_id': 'r123-degroot', 'model_version': '1.0.0',
            })
            assert denied.status == 403, denied.status

        assert not errors, errors
        page.evaluate('window.scrollTo(0, 0)')
        page.screenshot(path=str(report.with_suffix('.png')), full_page=True)
        report.write_text(json.dumps({
            'status': 'PASS',
            'source_id': source_id,
            'protocol_id': protocol_id,
            'canceled_run_id': original_id,
            'completed_run_id': run_id,
            'artifact_sha256': artifact_hash,
            'candidate_checked': bool(candidate_id),
            'page_errors': errors,
        }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        browser.close()
    print('Chromium v0.2 research workflow: PASS')


if __name__ == '__main__':
    run()
