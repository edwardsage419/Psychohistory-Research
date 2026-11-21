"""Exercise a fictional decision in real Chromium against the built loopback app."""

from contextlib import contextmanager
from decimal import Decimal
import json
import os
from pathlib import Path
import re
import shutil
import socket
import subprocess
import sys
import tempfile
from time import monotonic, sleep
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import urlopen

from playwright.sync_api import expect, sync_playwright


PROJECT = Path(__file__).resolve().parents[1]
API = '/api/v4/decisions'
STAY = '留在当前的产品分析岗位'
MOVE = '接受新公司的产品运营岗位'
STARTUP = '加入创业公司的产品负责人岗位'
QUESTION = f'我该{STAY}，还是{MOVE}？我想在三个月内决定，重视学习机会和收入稳定，也不能每周工作超过四十五小时。'
HOURS = '周工时上限'
GROWTH = '学习机会'
STABILITY = '收入稳定'
SOURCE = '虚构职业选择案例的合成数据'
OBSERVATION = '虚构回访：在选择的岗位参加了一次跨组培训。'


@contextmanager
def loopback_service(data):
    if not (PROJECT / 'web/dist/index.html').is_file():
        raise RuntimeError('Build the console first with npm --prefix web run build')
    with socket.socket() as listener:
        listener.bind(('127.0.0.1', 0))
        port = listener.getsockname()[1]
    url = f'http://127.0.0.1:{port}'
    env = {**os.environ, 'PYTHONPATH': str(PROJECT / 'src')}
    process = subprocess.Popen([
        sys.executable, '-m', 'psychohistory.cli', '--data', str(data),
        '--repo', str(PROJECT.parents[1]), 'serve', '--port', str(port),
    ], cwd=PROJECT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        deadline = monotonic() + 12
        while monotonic() < deadline and process.poll() is None:
            try:
                with urlopen(f'{url}/api/v1/health', timeout=1) as response:
                    if response.status == 200 and (data / 'token').is_file():
                        break
            except (URLError, TimeoutError):
                pass
            sleep(0.05)
        else:
            raise RuntimeError(f'Loopback service did not become ready (exit code {process.poll()})')
        yield url, (data / 'token').read_text(encoding='utf-8').strip()
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=8)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


def button(page, name):
    return page.get_by_role('button', name=name, exact=True)


def field(page, name):
    return page.get_by_label(name, exact=True)


def combobox(page, name):
    return page.get_by_role('combobox', name=name, exact=True)


def posted(page, path, act, *, state_matches=None):
    def matches(response):
        return (urlsplit(response.url).path == f'{API}/{path}'
                and response.request.method == 'POST'
                and (state_matches is None or state_matches(response.request.post_data_json['state'])))

    with page.expect_response(matches) as pending:
        act()
    response = pending.value
    assert response.ok, f'{path} returned HTTP {response.status}'
    return response.json()


def quantity(page, label, lower, upper):
    combobox(page, f'{label}数据性质').select_option('synthetic')
    field(page, f'{label}下界').fill(lower)
    field(page, f'{label}上界').fill(upper)
    field(page, f'{label}来源').fill(SOURCE)


def method(analysis, method_id):
    return next(entry for entry in analysis['methods'] if entry['model_id'] == method_id)


def bounds(analysis, a, b, expected):
    entry = method(analysis, 'c034_joint_robustness')
    assert entry['status'] == 'EXECUTED', entry['reasons']
    pair, = entry['result']['pairs']
    assert (pair['a'], pair['b']) == (a, b)
    actual = Decimal(pair['lower']), Decimal(pair['upper'])
    assert actual == tuple(map(Decimal, expected)), actual
    return entry


def show_charts(page, entry):
    card = page.locator(f'[data-model-id="{entry["model_id"]}"]')
    charts = entry['result']['charts']
    assert charts, f'{entry["model_id"]} returned no chart'
    for chart in charts:
        title = chart['title']
        name = f'{title} · {chart["unit"]}' if chart['unit'] else title
        expect(card.get_by_role('img', name=name, exact=True)).to_be_visible()
        combobox(card, f'查看 {title} 的区间').select_option('0')
        row = chart['rows'][0]
        expect(card.get_by_role('status').filter(has_text=row['label'])).to_contain_text(
            f'{row["lower"]} 至 {row["upper"]}'
        )


def save_revision(page, analysis):
    expect(page.get_by_text(analysis['input_hash'], exact=True)).to_have_count(1)
    saved = posted(page, 'save', button(page, '保存当前决策').click)
    assert saved['revision'] == analysis['revision']
    assert saved['analysis']['input_hash'] == analysis['input_hash']
    assert saved['state']['question'] == QUESTION
    expect(page.get_by_text('已保存当前修订', exact=True)).to_be_visible()
    return saved


def connect(page, url, token):
    page.goto(f"{url}/?workflow=v04")
    field(page, '本地访问令牌').fill(token)
    button(page, '连接工作空间').click()
    expect(page.get_by_text('工作空间已连接', exact=True)).to_be_visible()
    button(page, '个人决策工作台').click()
    expect(page.get_by_text('导出的备份文件未经加密', exact=False)).to_be_visible()


def career_decision(page):
    field(page, '你的决策问题').fill(QUESTION)
    started = posted(page, 'start', button(page, '开始澄清').click)
    draft = started['state']
    assert draft['question'] == QUESTION and not draft['confirmed'] and not draft['options']
    understanding = started['understanding']
    assert understanding['mode'] == 'GUIDED_CONFIRMATION'
    assert [item['value'] for item in understanding['suggestions']] == [STAY, MOVE]
    assert {item['field'] for item in started['questions']} >= {
        'options', 'objectives', 'deadline', 'constraints', 'confirmed',
    }
    for item in started['questions']:
        expect(page.get_by_text(item['prompt'], exact=True)).to_be_visible()

    deadline_prompt = next(item['prompt'] for item in started['questions'] if item['field'] == 'deadline')
    button(page.get_by_role('listitem').filter(has_text=deadline_prompt), '填写问题与时限').click()
    expect(page.get_by_role('region', name='澄清与确认').get_by_text(QUESTION, exact=True).first).to_be_visible()
    field(page, '决策时限').fill('三个月内')
    button(page, '底线与方案').click()
    button(page, '添加硬约束').click()
    field(page, '底线名称').fill(HOURS)
    combobox(page, '比较符号').select_option('<=')
    field(page, '阈值').fill('45')
    field(page, '底线单位').fill('小时/周')
    field(page, '底线依据').fill('虚构决策者确认的工作时间底线')
    for index, (option, low, high) in enumerate(((STAY, '39', '42'), (MOVE, '44', '47'), (STARTUP, '51', '56'))):
        if index < 2:
            suggestion = page.get_by_role('listitem').filter(has_text=f'{option} · 原文片段')
            button(suggestion, '采用为方案').click()
            expect(field(page, '方案名称').nth(index)).to_have_value(option)
        else:
            button(page, '添加候选方案').click()
            field(page, '方案名称').nth(index).fill(option)
        quantity(page, f'{option} · {HOURS}', low, high)
    field(page, '我确认底线清单完整（也可确认没有硬约束）').check()

    button(page, '目标与权重').click()
    for index, (objective, low, high) in enumerate(((GROWTH, '0.60', '0.65'), (STABILITY, '0.35', '0.40'))):
        button(page, '添加目标').click()
        field(page, '目标名称').nth(index).fill(objective)
        field(page, '目标单位').nth(index).fill('效用')
        field(page, f'{objective}权重下界').fill(low)
        field(page, f'{objective}权重上界').fill(high)
    field(page, '我确认使用下列权重区间').check()

    button(page, '评分与误差').click()
    combobox(page, '评分误差依赖').select_option('rectangle')
    field(page, '评分误差依赖依据').fill('虚构条件：评分误差区间端点可独立组合。')
    page.get_by_text('共享误差与评分变换', exact=True).click()
    combobox(page, '评分变换').select_option('identity')
    score_points = ((STAY, GROWTH, '0.80'), (STAY, STABILITY, '0.40'),
                    (MOVE, GROWTH, '0.50'), (MOVE, STABILITY, '0.80'))
    for option, objective, score in score_points:
        quantity(page, f'{option} · {objective}', score, score)

    gated = posted(page, 'analyze', button(page, '确认并分析').click)
    assert [(item['label'], item['status']) for item in gated['feasibility']] == [
        (STAY, 'ACCEPT'), (MOVE, 'UNRESOLVED'), (STARTUP, 'REJECT'),
    ]
    assert gated['conditional_scope']
    results = page.get_by_role('region', name='当前分析')
    expect(results).to_be_visible()
    expect(results.get_by_role('row').filter(has_text=MOVE).get_by_text('待核实', exact=True)).to_be_visible()

    button(page, '底线与方案').click()
    relaxed = posted(page, 'analyze', lambda: field(page, '阈值').fill('47'),
                     state_matches=lambda state: Decimal(state['constraints'][0]['threshold']) == 47)
    a, b, rejected = relaxed['feasibility']
    assert [x['status'] for x in (a, b, rejected)] == ['ACCEPT', 'ACCEPT', 'REJECT']
    a, b = a['option_id'], b['option_id']
    assert relaxed['input_hash'] != gated['input_hash']
    assert method(relaxed, 'c034_joint_robustness')['status'] == 'INELIGIBLE'

    button(page, '评分与误差').click()
    basis = '同一 0 至 1 基数效用刻度，越高越好。允许目标之间补偿，并确认权重区间。'
    strict = posted(page, 'analyze', lambda: field(page, '评分量表与比较依据').fill(basis),
                    state_matches=lambda state: state['score_basis'] == basis)
    strict_model = bounds(strict, a, b, ('0.02', '0.055'))
    assert strict_model['result']['pairs'][0]['relation'] == 'A_STRICT'
    assert strict_model['result']['leaders'] == [a]
    assert strict['revision'] == 1
    expect(page.get_by_text('方法审计', exact=True)).to_be_visible()
    show_charts(page, strict_model)

    consent = posted(page, 'consent', button(page, '授权本地保存').click)
    assert consent['authorized'] and consent['epoch']
    original = save_revision(page, strict)
    growth_id, stability_id = [item['id'] for item in original['state']['objectives']]

    button(page, '目标与权重').click()

    def edit_weights():
        field(page, f'{GROWTH}权重下界').fill('0.55')
        field(page, f'{STABILITY}权重上界').fill('0.45')

    weighted = posted(page, 'analyze', edit_weights, state_matches=lambda state: (
        Decimal(state['weights'][growth_id]['lower']) == Decimal('0.55')
        and Decimal(state['weights'][stability_id]['upper']) == Decimal('0.45')
    ))
    assert not bounds(weighted, a, b, ('-0.015', '0.055'))['result']['leaders']
    assert weighted['input_hash'] != strict['input_hash']

    button(page, '评分与误差').click()

    def edit_errors():
        for option, objective, score in score_points:
            label = f'{option} · {objective}'
            field(page, f'{label}下界').fill(str(Decimal(score) - Decimal('0.03')))
            field(page, f'{label}上界').fill(str(Decimal(score) + Decimal('0.03')))

    widened = posted(page, 'analyze', edit_errors, state_matches=lambda state: (
        Decimal(state['options'][1]['scores'][stability_id]['upper']) == Decimal('0.83')
    ))
    widened_model = bounds(widened, a, b, ('-0.075', '0.115'))
    assert not widened_model['result']['leaders']
    assert widened['input_hash'] != weighted['input_hash']
    expect(page.get_by_text(widened['input_hash'], exact=True)).to_have_count(1)
    show_charts(page, widened_model)

    button(page, '情景与参考').click()
    field(page, '情景效用的共同量表').fill('同一三个月的综合基数效用，0 最差，1 最好。')
    combobox(page, '情景效用依赖').select_option('rectangle')
    field(page, '情景效用依赖依据').fill('虚构条件：各单元格效用端点可独立组合。')
    field(page, '反转检验半径').fill('0.03')
    combobox(page, '参考方案').select_option(label=STAY)

    def add_scenario(index, label, stay, move):
        button(page, '添加情景').click()
        field(page, '情景名称').nth(index).fill(label)
        combobox(page, '情景性质').nth(index).select_option('synthetic')
        field(page, '情景来源或假设').nth(index).fill(SOURCE)
        quantity(page, f'{label} · {STAY}效用', stay, stay)
        quantity(page, f'{label} · {MOVE}效用', move, move)

    add_scenario(0, '业务增长', '0.95', '0.55')
    final = posted(page, 'analyze', lambda: add_scenario(1, '招聘收缩', '0.30', '0.65'),
                   state_matches=lambda state: (
                       len(state['scenarios']) == 2
                       and state['scenarios'][1]['utilities'].get(b, {}).get('source') == SOURCE
                       and all(item['probability'] is None for item in state['scenarios'])
                   ))
    regret_model = method(final, 'C029')
    assert regret_model['status'] == 'EXECUTED', regret_model['reasons']
    regret = regret_model['result']
    assert regret['leaders'] == [a] and regret['maximin_leaders'] == [b]
    assert {key: Decimal(value) for key, value in regret['worst_regret'].items()} == {
        a: Decimal('0.35'), b: Decimal('0.40'),
    }
    assert final['input_hash'] != widened['input_hash']
    assert final['decision_id'] == draft['decision_id']
    assert final['revision'] == 2
    expect(page.get_by_text(final['input_hash'], exact=True)).to_have_count(1)
    show_charts(page, regret_model)
    current = save_revision(page, final)
    return consent['epoch'], (original, current), (a, b, rejected['option_id'])


def preview_backup(page, backup_bytes):
    field(page, '选择备份文件').set_input_files({
        'name': 'fictional-career-backup.json', 'mimeType': 'application/json', 'buffer': backup_bytes,
    })
    return posted(page, 'restore', button(page, '预览备份').click)


def review_and_recover(page, token, records_db, snapshots, options):
    a, b, rejected = options
    details = page.get_by_role('region', name='决策记录详情')
    expect(details.get_by_text(re.compile(r'^修订 2 · '))).to_be_visible()
    combobox(page, '实际选择').select_option(label=MOVE)
    action = posted(page, 'action', button(page, '记录实际行动').click)
    assert action['option_id'] == b and action['revision'] == 2
    assert action['coverage'] == {a: 'UNOBSERVED', b: 'CHOSEN', rejected: 'UNOBSERVED'}
    expect(details.get_by_text(f'未观察：{STAY}、{STARTUP}', exact=True)).to_be_visible()
    field(page, '观察结果').fill(OBSERVATION)
    combobox(page, '回访性质').select_option('synthetic')
    review = posted(page, 'review', button(page, '追加回访').click)
    assert review['option_id'] == b and review['kind'] == 'synthetic'
    assert review['observation'] == OBSERVATION
    expect(page.get_by_text(OBSERVATION, exact=True)).to_be_visible()

    with page.expect_download() as pending:
        button(page, '导出本地备份').click()
    backup_bytes = pending.value.path().read_bytes()
    assert token.encode() not in backup_bytes, 'Export contained the local access credential'
    backup = json.loads(backup_bytes)
    record, = json.loads(backup['payload'])['decisions']
    assert record['action'] == action and record['reviews'] == [review]
    assert [item['revision'] for item in record['snapshots']] == [1, 2]
    assert [item['analysis']['input_hash'] for item in record['snapshots']] == [
        item['analysis']['input_hash'] for item in snapshots
    ]
    assert [item['probability'] for item in record['snapshots'][1]['state']['scenarios']] == [None, None]

    expect(page.get_by_text('已导出本地备份', exact=True)).to_be_visible()
    # Rehearse content loss in the disposable workspace while preserving its consent ledger.
    records_db.unlink()
    preview = preview_backup(page, backup_bytes)
    assert preview == {'mode': 'preview', 'isolated': True, 'eligible': True, 'decision_count': 1, 'reason': None}
    assert not records_db.exists()
    expect(button(page, '确认恢复')).to_be_enabled()
    recovered = posted(page, 'restore', button(page, '确认恢复').click)
    assert recovered == {'mode': 'restored', 'isolated': False, 'decision_count': 1}
    assert records_db.is_file()
    loaded = posted(page, 'record', button(page, QUESTION).click)
    assert loaded['decision_id'] == record['decision_id']
    assert loaded['action'] == action and loaded['reviews'] == [review]
    assert [item['state'] for item in loaded['snapshots']] == [item['state'] for item in snapshots]
    assert all(item['analysis'] is None and item['analysis_status'] == 'RECOMPUTE_REQUIRED'
               for item in loaded['snapshots'])
    first_revision = details.locator('details.decision-snapshot').filter(has_text=re.compile(r'^修订 1 · '))
    first_revision.get_by_text(re.compile(r'^修订 1 · ')).click()
    expect(first_revision.get_by_text('恢复后需要重新计算', exact=True)).to_be_visible()
    expect(details.get_by_text(OBSERVATION, exact=True)).to_be_visible()
    return backup_bytes


def withdraw_and_reject(page, url, token, epoch, backup_bytes):
    button(page, '撤回保存授权').click()
    withdrawn = posted(page, 'revoke', button(page, '确认撤回授权').click)
    assert withdrawn['authorized'] is False and withdrawn['epoch'] is None
    expect(page.get_by_text('已撤回保存授权', exact=True)).to_be_visible()
    expect(field(page, '你的决策问题')).to_have_value('')

    headers = {'Authorization': f'Bearer {token}'}
    assert page.request.post(f'{url}{API}/history', data={'epoch': epoch}, headers=headers).status == 403
    assert page.evaluate('''credential => [localStorage, sessionStorage].every(
        storage => Object.values(storage).every(value => !value.includes(credential)))''', token)
    connect(page, url, token)
    fresh = posted(page, 'consent', button(page, '授权本地保存').click)
    assert fresh['authorized'] is True and fresh['epoch'] != epoch

    preview = preview_backup(page, backup_bytes)
    assert preview['mode'] == 'preview' and preview['isolated'] is True and preview['eligible'] is False
    assert preview['reason']
    expect(button(page, '确认恢复')).to_be_disabled()
    expect(page.get_by_text(QUESTION, exact=True)).to_have_count(0)
    rejected_restore = page.request.post(f'{url}{API}/restore', headers=headers, data={
        'epoch': fresh['epoch'], 'backup': json.loads(backup_bytes), 'confirm': True,
    })
    assert rejected_restore.status in (403, 422), rejected_restore.status
    history = page.request.post(f'{url}{API}/history', data={'epoch': fresh['epoch']}, headers=headers)
    assert history.ok and history.json() == []


def research_navigation(page):
    for section, heading in (('研究看板', '近期实验与真实状态'),
                             ('研究工作流', '科研来源'), ('机制实验', '模型与来源')):
        button(page, section).click()
        expect(page.get_by_role('heading', name=section, exact=True, level=1)).to_be_visible()
        expect(page.get_by_role('heading', name=heading, exact=True)).to_be_visible()


def narrow_viewport(page):
    page.set_viewport_size({'width': 390, 'height': 844})
    button(page, '个人决策工作台').click()
    expect(field(page, '你的决策问题')).to_be_visible()
    expect(page.get_by_role('region', name='本地决策记录')).to_be_visible()
    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')


def run():
    report = Path(os.environ.get('PH_BROWSER_REPORT', '/tmp/psychohistory-browser-v04.json'))
    executable = os.environ.get('PH_CHROMIUM_EXECUTABLE') or shutil.which('chromium')
    args = ['--no-sandbox', '--disable-dev-shm-usage'] if sys.platform.startswith('linux') else []
    expect.set_options(timeout=15000)
    with tempfile.TemporaryDirectory(prefix='psychohistory-browser-v04-') as workspace:
        with loopback_service(Path(workspace) / 'research') as (url, token), sync_playwright() as playwright:
            browser = playwright.chromium.launch(executable_path=executable, headless=True, args=args)
            try:
                context = browser.new_context(viewport={'width': 1440, 'height': 1000}, service_workers='block')
                external_requests = []

                def local_requests(route):
                    address = urlsplit(route.request.url)
                    if address.scheme == 'http' and address.netloc == urlsplit(url).netloc:
                        route.continue_()
                    else:
                        external_requests.append(True)
                        route.abort()

                context.route('**/*', local_requests)
                page = context.new_page()
                page.set_default_timeout(10000)
                page_errors = []
                page.on('pageerror', lambda error: page_errors.append(str(error)))
                connect(page, url, token)
                epoch, snapshots, options = career_decision(page)
                records_db = Path(workspace) / 'research-personal-v04/records.sqlite3'
                backup = review_and_recover(page, token, records_db, snapshots, options)
                withdraw_and_reject(page, url, token, epoch, backup)
                research_navigation(page)
                narrow_viewport(page)
                assert not page_errors, page_errors
                assert not external_requests, 'The application requested a resource outside loopback'
                browser_version = browser.version
            except Exception as error:
                sanitized = AssertionError(str(error).replace(token, '[redacted]'))
                raise sanitized.with_traceback(error.__traceback__) from None
            finally:
                browser.close()
    report.write_text(json.dumps({
        'status': 'PASS',
        'chromium': browser_version,
        'fixture': 'fictional career decision',
        'checks': [
            'open question and targeted clarification', 'confirmed hard constraint and exact boundary change',
            'joint comparison waits for a declared scale', 'weight and score interval recomputation',
            'interactive chart selection', 'probability-free scenario and conflicting comparison rules',
            'explicit consent and two immutable snapshots', 'actual choice and synthetic review coverage',
            'local export and isolated recovery after temporary content loss', 'restored analysis requires recomputation',
            'withdrawal, revoked archive preview and restore refusal',
            'v0.1, v0.2 and v0.3 research navigation', '390px viewport and no horizontal document overflow',
            'same-origin requests and no page errors',
        ],
    }, indent=2) + '\n', encoding='utf-8')
    print('Chromium v0.4 fictional career workflow: PASS')


if __name__ == '__main__':
    run()
