"""Exercise v0.3 in headless Chromium against the built Web and loopback API."""

import json
import os
from pathlib import Path
import re
import shutil
import sys

from playwright.sync_api import expect, sync_playwright


def posted(page, button, path, *, denied=False):
    with page.expect_response(lambda response: response.url.endswith(f'/api/{path}')
                              and response.request.method == 'POST') as pending:
        button.click()
    response = pending.value
    assert (response.status in (400, 422) if denied else response.ok), (
        f'{path} returned {response.status}: {response.text()}'
    )
    return response.json()


def run():
    url = os.environ.get('PH_TEST_URL', 'http://127.0.0.1:8765')
    data = Path(os.environ.get('PH_TEST_DATA', '/tmp/psychohistory-v03-web'))
    report = Path(os.environ.get('PH_BROWSER_REPORT', '/tmp/psychohistory-browser-v03.json'))
    token = (data / 'token').read_text(encoding='utf-8').strip()
    executable = os.environ.get('PH_CHROMIUM_EXECUTABLE') or shutil.which('chromium')
    args = ['--no-sandbox', '--disable-dev-shm-usage'] if sys.platform.startswith('linux') else []
    expect.set_options(timeout=15000)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=executable, headless=True, args=args)
        page = browser.new_page(viewport={'width': 1440, 'height': 1000})
        page_errors = []
        page.on('pageerror', lambda error: page_errors.append(str(error)))
        page.goto(url)
        page.get_by_label('本地访问令牌').fill(token)
        page.get_by_role('button', name='连接工作空间', exact=True).click()
        expect(page.get_by_text('工作空间已连接', exact=True)).to_be_visible()
        page.get_by_role('button', name='机制实验', exact=True).click(timeout=3500)
        expect(page.get_by_role('heading', name='机制实验', exact=True)).to_be_visible()

        registration = page.get_by_role('region', name='模型与来源')
        model = registration.get_by_label('实验模型')
        source_picker = registration.get_by_label('固定科研来源')
        setup = page.get_by_role('region', name='合成参数')
        current = page.get_by_role('region', name='所选机制实验')
        results = page.get_by_role('region', name='不可变机制结果')
        result_hash = results.get_by_label('结果工件 SHA-256')
        history = page.get_by_role('region', name='机制实验历史')
        compare = page.get_by_role('region', name='轨迹比较')

        def register(model_key, research_id):
            model.select_option(model_key)
            source = posted(page, registration.get_by_role('button', name='登记固定来源'), 'v2/sources')
            assert source['research_id'] == research_id and source['origin'] == 'MAIN'
            expect(source_picker).to_have_value(source['source_id'])
            verified = posted(page, registration.get_by_role('button', name='校验固定来源'),
                              f"v2/sources/{source['source_id']}/verify")
            assert verified['source_id'] == source['source_id']
            expect(registration.get_by_text(source['commit'], exact=True)).to_be_visible()
            return source

        def submit(model_id, source_id, *, branch_from=None):
            pending = posted(page, setup.get_by_role('button', name='提交机制实验'), 'v3/experiments')
            assert pending['status'] == 'PENDING', pending
            assert pending['config']['model_id'] == model_id, pending['config']
            assert pending['config']['source_id'] == source_id, pending['config']
            assert pending['config'].get('branch_from') == branch_from, pending['config']
            expect(current.get_by_text('PENDING', exact=True)).to_be_visible()
            return pending['id']

        def complete(run_id):
            posted(page, current.get_by_role('button', name='批准机制执行'),
                   f'v3/experiments/{run_id}/approve')
            expect(result_hash).to_have_text(re.compile('^[a-f0-9]{64}$'))
            expect(current.get_by_text('COMPLETED', exact=True)).to_be_visible()
            response = page.request.get(f'{url}/api/v3/experiments/{run_id}/result',
                                        headers={'Authorization': f'Bearer {token}'})
            assert response.ok, response.status
            artifact = response.json()
            expect(result_hash).to_have_text(artifact['artifact_sha256'])
            expect(results.get_by_text('UNKNOWN', exact=True)).to_be_visible()
            expect(results.get_by_role('img', name='机制状态随时间的变化')).to_be_visible()
            assert artifact['result']['trajectory'], artifact
            return artifact

        replicator_id, degroot_id = 'r132-replicator', 'r123-degroot'
        r132 = register(f'{replicator_id}@1.0.0', 'R132')
        setup.get_by_label('动力学方法').select_option('eq3')
        setup.get_by_label('步数').fill('4')
        expect(setup.get_by_label('积分步长')).to_have_count(0)
        exact_id = submit(replicator_id, r132['source_id'])
        exact = complete(exact_id)
        assert exact['result']['time_kind'] == 'discrete-generation', exact['result']['time_kind']
        assert exact['result']['trajectory'][0]['values'] == ['1/4', '3/4']
        expect(results.get_by_role('table', name='精确轨迹').get_by_text('1/4', exact=True)).to_be_visible()
        provenance = results.get_by_text('查看来源文件与固定输入', exact=True)
        provenance.click()
        expect(results.get_by_role('table', name='来源文件').get_by_text(r132['files'][0]['blob'], exact=True)).to_be_visible()
        provenance.click()

        setup.get_by_label('动力学方法').select_option('euler')
        setup.get_by_label('积分步长').fill('1/40')
        setup.get_by_label('步数').fill('40')
        euler_id = submit(replicator_id, r132['source_id'])
        euler = complete(euler_id)
        setup.get_by_label('动力学方法').select_option('rk4')
        rk4_id = submit(replicator_id, r132['source_id'])
        rk4 = complete(rk4_id)
        assert euler['result']['time_kind'] == rk4['result']['time_kind'] == 'continuous-ode'

        left = compare.get_by_label('左侧实验')
        right = compare.get_by_label('右侧实验')
        metric = compare.get_by_label('比较指标')
        compare_button = compare.get_by_role('button', name='比较已完成实验')
        left.select_option(euler_id)
        right.select_option(rk4_id)
        comparison = posted(page, compare_button, 'v3/compare')
        assert comparison['samples'] > 0 and comparison['max_abs_difference'] > 0, comparison
        expect(compare.get_by_label('最大绝对差', exact=True)).to_have_text(comparison['max_abs_difference_decimal'])

        history.get_by_role('button', name=euler_id, exact=True).click()
        expect(result_hash).to_have_text(euler['artifact_sha256'])
        results.get_by_role('button', name='从此快照创建分支').click()
        expect(setup.get_by_text(euler_id, exact=True)).to_be_visible()
        setup.get_by_label('步数').fill('4')
        branch_id = submit(replicator_id, r132['source_id'], branch_from=euler_id)
        branch = complete(branch_id)
        assert branch['result']['trajectory'][0]['time'] == euler['result']['trajectory'][-1]['time']
        assert branch['result']['trajectory'][0]['values'] == euler['result']['trajectory'][-1]['values']
        assert branch['result']['snapshot']['content_hash'] != euler['result']['snapshot']['content_hash']
        history.get_by_role('button', name=euler_id, exact=True).click()
        expect(result_hash).to_have_text(euler['artifact_sha256'])

        setup.get_by_label('合成预设').select_option('hawk-dove')
        setup.get_by_label('动力学方法').select_option('euler')
        setup.get_by_label('积分步长').fill('4')
        setup.get_by_label('步数').fill('1')
        hawk_id = submit(replicator_id, r132['source_id'])
        hawk = complete(hawk_id)
        expect(results.get_by_text('数值警告：伪灭绝', exact=True)).to_be_visible()
        assert 'FALSE_EXTINCTION' in json.dumps(hawk['result']['diagnostics']), hawk['result']['diagnostics']

        r123 = register(f'{degroot_id}@1.0.0', 'R123')
        setup.get_by_label('初始意见').fill('0, 1')
        setup.get_by_label('权重矩阵').fill('1/2, 1/2\n1/4, 3/4')
        setup.get_by_label('步数').fill('3')
        canceled_id = submit(degroot_id, r123['source_id'])
        posted(page, current.get_by_role('button', name='取消机制实验'), f'v3/experiments/{canceled_id}/cancel')
        expect(current.get_by_text('CANCELED', exact=True)).to_be_visible()
        degroot_run_id = submit(degroot_id, r123['source_id'])
        degroot = complete(degroot_run_id)
        assert degroot['result']['time_kind'] == 'discrete-round', degroot['result']['time_kind']
        assert degroot['result']['trajectory'][1]['values'] == ['1/2', '3/4']

        left.select_option(euler_id)
        right.select_option(degroot_run_id)
        rejected = posted(page, compare_button, 'v3/compare', denied=True)
        expect(compare.get_by_role('alert')).to_be_visible()
        right.select_option(exact_id)
        clock_rejected = posted(page, compare_button, 'v3/compare', denied=True)
        expect(compare.get_by_role('alert')).to_be_visible()
        right.select_option(rk4_id)
        metric.select_option('brier')
        brier_rejected = posted(page, compare_button, 'v3/compare', denied=True)
        expect(compare.get_by_role('alert')).to_be_visible()
        expect(compare.get_by_label('最大绝对差', exact=True)).to_have_count(0)

        page.get_by_label('机制实验完整 ID').fill(exact_id)
        page.get_by_role('button', name='按 ID 查看机制实验').click()
        expect(result_hash).to_have_text(exact['artifact_sha256'])
        expect(history.get_by_role('row').filter(has_text=canceled_id).get_by_text('CANCELED', exact=True)).to_be_visible()
        assert not page_errors, page_errors
        page.get_by_role('heading', name='不可变机制结果').scroll_into_view_if_needed()
        page.screenshot(path=str(report.with_suffix('.png')), full_page=True)
        report.write_text(json.dumps({
            'status': 'PASS',
            'source_ids': [r132['source_id'], r123['source_id']],
            'runs': {'eq3': exact_id, 'euler': euler_id, 'rk4': rk4_id, 'branch': branch_id,
                     'hawk_dove': hawk_id, 'degroot': degroot_run_id, 'canceled': canceled_id},
            'artifact_sha256': {name: artifact['artifact_sha256'] for name, artifact in (
                ('eq3', exact), ('euler', euler), ('rk4', rk4), ('branch', branch), ('degroot', degroot), ('hawk_dove', hawk))},
            'numerical_warning': 'FALSE_EXTINCTION',
            'comparison': {key: comparison[key] for key in (
                'max_abs_difference', 'max_abs_difference_decimal', 'samples')},
            'rejected_comparisons': {'cross_model': rejected, 'incompatible_clocks': clock_rejected, 'brier': brier_rejected},
            'page_errors': page_errors,
        }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        browser.close()
    print('Chromium v0.3 mechanism workflow: PASS')


if __name__ == '__main__':
    run()
