"""Real Chromium acceptance for the conversational workbench and frozen fictional cases."""

from functools import partial
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import shutil
import sys
from tempfile import TemporaryDirectory
from urllib.parse import urlsplit

from playwright.sync_api import expect, sync_playwright

from browser_v04 import button, combobox, field
from browser_v05 import assert_browser_memory_only, browser_export, browser_session, post, preview_backup, recover
from v07_offline_check import CHOICE, JOINT, NIGHT, SCENARIOS, resource_fixtures, session


API = '/api/v7/decisions'
V5 = '/api/v5/decisions'
send = partial(post, prefix=API)
CASE_FILE = Path(__file__).with_name('browser_v06_cases.json')
CASE_HASH = 'e67d6d0493d80882ff306e3e25d4f595a87f36d994290681b3fba622044eac82'
EVAL_DOMAINS = {'work', 'learning', 'budget', 'living', 'moving', 'risk'}
TECHNICAL = re.compile(r'EVSI|EVPI|C0(?:28|29|30|31|34)|SHA-256|JSON|Pydantic|联合稳健性|最小最大后悔值')


def frozen_cases():
    source = CASE_FILE.read_bytes()
    assert sha256(source).hexdigest() == CASE_HASH, 'The frozen engineering cases changed'
    rows = json.loads(source)['cases']
    assert len(rows) == len(EVAL_DOMAINS) and {row['id'] for row in rows} == EVAL_DOMAINS
    return rows


def connect(page, url, token, version="v07"):
    response = page.goto(f'{url}/?workflow={version}' if version else f'{url}/')
    assert response is not None and response.ok
    field(page, '本地访问令牌').fill(token)
    button(page, '连接工作空间').click()
    expect(page.get_by_text('工作空间已连接', exact=True)).to_be_visible()
    personal = button(page, '个人决策工作台')
    if personal.is_visible() and not field(page, '你的决策问题').is_visible():
        personal.click()
    expect(field(page, '你的决策问题')).to_be_visible()


def start(page, question):
    page.get_by_role('textbox', name='你的决策问题', exact=True).fill(question)
    return send(page, 'start', button(page, '开始对话').click)


def turn(page, text, previous):
    page.get_by_role('textbox', name='补充或修正', exact=True).fill(text)
    result = send(page, 'turn', button(page, '发送').click, request_matches=lambda request: (
        request['session_id'] == previous['session_id'] and request['revision'] == previous['revision']
    ))
    assert result['session_id'] == previous['session_id']
    assert result['revision'] > previous['revision']
    return result


def confirm(page, previous):
    scope = field(page, '我已说明本次目的和硬约束')
    if scope.is_visible():
        scope.check()
    field(page, '我已核对本组理解').check()
    result = send(page, 'confirm', button(page, '确认本组理解').click, request_matches=lambda request: (
        request['session_id'] == previous['session_id'] and request['revision'] == previous['revision']
    ))
    assert result['session_id'] == previous['session_id']
    return result


def compare(page, previous):
    return send(page, 'analyze', button(page, '计算并比较').click, request_matches=lambda request: (
        request['session_id'] == previous['session_id'] and request['revision'] == previous['revision']
    ))


def direct(page, url, token, endpoint, body, *, prefix=API):
    return page.request.post(f'{url}{prefix}/{endpoint}', data=body,
                             headers={'Authorization': f'Bearer {token}'}, timeout=10000)


def report_write(report, data):
    report.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def no_probabilities(result):
    state = result.get('state') or {}
    assert all(item.get('probability') is None for item in state.get('scenarios', ()))
    information = state.get('information') or {}
    assert not information.get('prior') and not information.get('likelihoods')


def conversational_view(page, result):
    area = page.locator('#decision-conversation')
    expect(area).to_be_visible()
    expect(area).to_have_attribute('data-conversation-revision', str(result['revision']))
    expect(page.get_by_role('textbox', name='补充或修正', exact=True)).to_be_visible()
    followup = area.get_by_role('region', name='待回答的问题', exact=True)
    question = result['summary']['question']
    expect(followup).to_have_count(int(bool(question)))
    if question:
        expect(followup).to_have_text(question)
        assert followup.inner_text().count('？') + followup.inner_text().count('?') <= 1

    advanced = area.locator('details').filter(has=area.get_by_text('高级输入与审计', exact=True)).first
    if advanced.count():
        assert advanced.get_attribute('open') is None
    forbidden = ('决策时限', '底线名称', '评分量表与比较依据', '调查成本单位', '调查完成模型')
    visible_fields = [name for name in forbidden if field(area, name).first.is_visible()]
    assert not visible_fields, visible_fields
    assert not TECHNICAL.search(area.inner_text()), 'Technical analysis vocabulary leaked into the primary view'
    no_probabilities(result)
    return followup.count()


def autonomous_runtime(page, url, token):
    connect(page, url, token)
    status = page.request.get(f'{url}{API}/status', headers={'Authorization': f'Bearer {token}'})
    assert status.ok
    config = status.json()
    assert config['cognition']['coverage'] == 'BOUNDED_RULES' and config['cognition']['network'] == 'OFFLINE'
    assert config['external_verification'] == 'NOT_CONNECTED' and config['execution_available'] is False
    assert config['local_model']['enabled'] is False
    assert all(not config['purpose_consent'][purpose]['authorized'] for purpose in
               ('save', 'personalization', 'research', 'training'))
    page.get_by_text('理解方式与用途', exact=True).click()
    expect(page.get_by_role('checkbox', name='允许本轮使用本地模型辅助理解')).to_have_count(0)
    old = direct(page, url, token, 'start', {'question': '虚构旧客户端', 'use_local_model': True})
    assert old.ok and old.json()['local_model_status'] == 'LEGACY_REQUEST_RETIRED'
    assert old.json()['local_model_receipt']['notice']
    opened = start(page, '虚构本地理解回退：我该保留现有书桌，还是修好备用书桌？')
    assert opened['session_id'] and opened['revision'] > 0
    assert opened['analysis'] is None
    assert opened['local_model_status'] in {'LOCAL_AI_DISABLED', 'MODEL_NOT_ALLOWLISTED'}
    conversational_view(page, opened)
    return opened


def incomplete_workflow(page, url, token):
    connect(page, url, token)
    opened = start(page, '我有个决定一直想不清楚，能帮我梳理一下吗？')
    conversational_view(page, opened)
    assert not opened['options'] and opened['analysis'] is None
    confirmed = confirm(page, opened)
    assert not confirmed['state']['confirmed'] and confirmed['analysis'] is None
    expect(button(page, '计算并比较')).to_have_count(0)


def evaluate_cases(page, url, token, requests):
    results = []
    previous_posts = len(requests)
    for case in frozen_cases():
        connect(page, url, token)
        result = start(page, case['question'])
        assert result['session_id'] and result['revision'] > 0, case['id']
        assert result['state']['question'] == case['question'], case['id']
        assert result.get('analysis') is None, case['id']
        questions = [conversational_view(page, result)]
        for message in case['turns']:
            result = turn(page, message, result)
            assert result.get('analysis') is None, case['id']
            questions.append(conversational_view(page, result))
        assert len(questions) == len(case['turns']) + 1
        supplied = [case['question'], *case['turns']]
        assert [message['text'] for message in result['dialogue'] if message['role'] == 'user'] == supplied
        assert all(claim['source'] and any(claim['source'] in text for text in supplied) for claim in result['claims'])
        observed = json.dumps({key: result.get(key) for key in ('summary', 'claims', 'options')}, ensure_ascii=False)
        results.append({
            'domain': case['id'],
            'user_turns': len(questions),
            'maximum_visible_follow_ups': max(questions),
            'forced_technical_inputs': 0,
            'anchors_visible_in_structured_reply': [text for text in case['anchors'] if text in observed],
            'anchors_expected': len(case['anchors']),
            'candidate_count': len(result.get('options') or []),
            'claim_count': len(result.get('claims') or []),
            'extracted_fields': sorted({claim['field'] for claim in result['claims']}),
            'assessment_limit': 'This case evaluates conversation and grounding without a confirmed model comparison.',
        })
    allowed = {f'{API}/start', f'{API}/turn', f'{API}/end'}
    assert set(requests[previous_posts:]) <= allowed, 'An unconfirmed conversation performed a decision write'
    return results


INTEGRATION_QUESTION = (
    '我在比较两个工作岗位。方案甲：每周到岗一天，不需要搬家；方案乙：每周到岗三天，不需要搬家。'
    '每周最多到岗两天。我的目标是积累管理经验，周五之前必须决定。'
)
CORRECTION = '我原来每周最多到岗两天，现在把上限从两天改为三天。'


def hard_gate(result):
    return {row['label']: row['status'] for row in result['analysis']['feasibility']}


def parity(page, url, token, result):
    expected = direct(page, url, token, 'analyze', {'state': result['state']}, prefix=V5)
    assert expected.ok, expected.status
    legacy = expected.json()
    analysis = result['analysis']
    for field_name in ('input_hash', 'feasibility', 'methods', 'trace'):
        assert analysis[field_name] == legacy[field_name], f'Calculation differs from v0.5 at {field_name}'
    assert analysis.get('execution', {}).get('available') is False
    return analysis


def claim_by_value(result, value, field_name):
    return next(claim for claim in result['claims'] if claim.get('field') == field_name and str(claim.get('value')) == value)


def revision_workflow(page, url, token, requests):
    connect(page, url, token)
    draft = start(page, INTEGRATION_QUESTION)
    conversational_view(page, draft)
    assert draft['analysis'] is None
    assert {item['label'] for item in draft['options']} == {'方案甲', '方案乙'}
    verified = confirm(page, draft)
    baseline = compare(page, verified)
    assert hard_gate(baseline) == {'方案甲': 'ACCEPT', '方案乙': 'REJECT'}
    analysis = parity(page, url, token, baseline)
    method_statuses = {entry['model_id']: entry['status'] for entry in analysis['methods']}
    assert method_statuses['c028_interval_feasibility'] == 'EXECUTED'
    assert method_statuses['voi_point'] == 'INELIGIBLE'
    assert method_statuses['c034_joint_robustness'] == 'INELIGIBLE'
    assert not analysis.get('execution', {}).get('available')
    old_claim = claim_by_value(baseline, '2', 'onsite_max')

    revised_draft = turn(page, CORRECTION, baseline)
    assert revised_draft['analysis'] is None
    stale = direct(page, url, token, 'analyze', {
        'session_id': baseline['session_id'], 'revision': baseline['revision'],
    })
    assert stale.status in (409, 422), stale.status
    new_claim = claim_by_value(revised_draft, '3', 'onsite_max')
    assert new_claim['source'] in CORRECTION
    assert new_claim['id'] != old_claim['id']
    claim_card = page.locator(f'[data-claim-id="{new_claim["id"]}"]')
    combobox(claim_card, '用此项替换此前内容').select_option(old_claim['id'])
    accepted = confirm(page, revised_draft)
    assert any('方案乙' in change and '通过底线' in change for change in accepted['changes'])
    revised = compare(page, accepted)
    assert hard_gate(revised) == {'方案甲': 'ACCEPT', '方案乙': 'ACCEPT'}
    corrected = parity(page, url, token, revised)
    assert corrected['input_hash'] != analysis['input_hash']
    old = next(claim for claim in revised['claims'] if claim['id'] == old_claim['id'])
    new = next(claim for claim in revised['claims'] if claim['id'] == new_claim['id'])
    assert old['status'] == 'SUPERSEDED' and new['supersedes'] == old_claim['id']
    no_probabilities(revised)
    assert {f'{API}/select', f'{API}/plan', f'{API}/save', f'{V5}/action'}.isdisjoint(requests)
    advanced = page.get_by_text('高级输入与审计', exact=True)
    advanced.click()
    expect(page.get_by_text(corrected['input_hash'], exact=True).first).to_have_count(1)
    advanced.click()
    return revised


def native_v07_cases(page, url, token):
    observations = {}
    for key, prompt, expected in (
        ('joint', JOINT, {'A': 'REJECT', 'B': 'ACCEPT', 'C': 'UNRESOLVED'}),
        ('night', NIGHT, {'A': 'UNRESOLVED', 'B': 'REJECT', 'C': 'ACCEPT', 'D': 'UNRESOLVED'}),
    ):
        connect(page, url, token)
        opened = start(page, prompt)
        verified = confirm(page, opened)
        assert hard_gate(verified) == expected
        parity(page, url, token, verified)
        observations[key] = {'question': prompt, 'gate': expected, 'version': verified['conversation_version']}
    connect(page, url, token)
    risk = confirm(page, start(page, SCENARIOS))
    point = next(item for item in risk['analysis']['methods'] if item['model_id'] == 'C029')
    assert point['status'] == 'EXECUTED'
    assert [item['label'] for item in risk['options'] if item['id'] in point['result']['leaders']] == ['方案乙']
    no_probabilities(risk)
    observations['risk'] = {'question': SCENARIOS, 'method': 'C029@' + point['version'], 'leader': '方案乙'}

    connect(page, url, token)
    base = confirm(page, start(page, CHOICE))
    cash, timing = resource_fixtures(base)
    page.get_by_text('共同资源与进度', exact=True).click()

    def apply(payload):
        field(page, '共同资源数据').fill(json.dumps(payload, ensure_ascii=False))
        field(page, '我已核对资源、日期和来源').check()
        return send(page, 'update_resources', button(page, '应用资源并重新计算').click)

    settled = apply(cash)
    assert hard_gate(settled) == {'方案甲': 'REJECT', '方案乙': 'ACCEPT'}
    assert settled['resources']['result']['cash']['balance'] == '750.00'
    expect(page.get_by_text('可用余额 750.00 CNY', exact=True)).to_be_visible()
    timed = apply(timing)
    assert hard_gate(timed) == {'方案甲': 'ACCEPT', '方案乙': 'UNRESOLVED'}
    timing['shared_tasks'][0]['completed_minutes'] = 30
    amended = apply(timing)
    assert hard_gate(amended) == {'方案甲': 'REJECT', '方案乙': 'REJECT'}
    stale = direct(page, url, token, 'analyze', session(timed))
    assert stale.status in (409, 422)
    observations['resources'] = {'cash': settled['resources']['result']['cash']['balance'],
                                 'cash_gate': hard_gate(settled), 'time_gate': hard_gate(timed),
                                 'revised_time_gate': hard_gate(amended), 'stale_status': stale.status}

    docs = direct(page, url, token, 'knowledge', {'query': 'C028 interval hard constraint feasibility', 'limit': 3})
    assert docs.ok and docs.json()['hits']
    assert all(hit['card']['decision_evidence'] == 'NOT_QUALIFIED' for hit in docs.json()['hits'])
    observations['knowledge'] = {'hits': len(docs.json()['hits']), 'authority': docs.json()['authority']}
    return observations


def local_history(page):
    disclosure = page.get_by_text('本地记录与隐私', exact=True)
    panel = page.locator('details').filter(has=disclosure).last
    if panel.get_attribute('open') is None:
        disclosure.click()
    return page.get_by_role('region', name='本地决策记录')


def choose_and_plan(page, result, requests):
    first = next(item for item in result['options'] if item['label'] == '方案甲')
    option_card = page.locator(f'article[data-option-id="{first["id"]}"]')
    button(option_card, '选择此方案').click()
    chosen = send(page, 'select', button(page, '确认选择').click)
    assert chosen['selected_option_id'] == first['id']
    trigger = '收到书面的到岗安排后再决定是否实际行动。'
    field(page, '触发条件').fill(trigger)
    planned = send(page, 'plan', button(page, '确认条件计划').click)
    assert planned['selected_plan'] == {'option_id': first['id'], 'trigger': trigger, 'status': 'USER_PLAN_ONLY'}
    assert {f'{V5}/action', f'{API}/save', f'{API}/execute'}.isdisjoint(requests)
    return planned


def privacy_workflow(page, url, token, root, result, requests):
    result = choose_and_plan(page, result, requests)
    history = local_history(page)
    assert_browser_memory_only(page, token, INTEGRATION_QUESTION, CORRECTION)
    content = root / 'research-personal-v04/records.sqlite3'
    save_request = {'session_id': result['session_id'], 'revision': result['revision']}
    denied = direct(page, url, token, 'save', {**save_request, 'epoch': '0' * 32, 'save_confirmed': True})
    assert denied.status in (403, 422) and not content.exists()
    consent = post(page, 'consent', button(history, '授权本地保存').click)
    epoch = consent['epoch']
    denied = direct(page, url, token, 'save', {**save_request, 'epoch': epoch, 'save_confirmed': False})
    assert denied.status in (403, 422) and not content.exists()

    save_button = button(history, '保存当前决策')
    expect(save_button).to_be_disabled()
    field(history, '我确认保存本次已核对的决策').check()
    saved = send(page, 'save', save_button.click, request_matches=lambda payload: (
        payload['epoch'] == epoch and payload['save_confirmed'] is True
    ))
    assert saved['state']['question'] == INTEGRATION_QUESTION
    saved_trace = saved['analysis']['conversation']
    assert saved_trace['selection'] == result['selected_option_id'] and saved_trace['plan'] == result['selected_plan']
    assert [claim['value'] for claim in saved_trace['confirmed_sources'] if claim['field'] == 'onsite_max'] == ['3']
    assert content.is_file()
    expect(button(history, INTEGRATION_QUESTION)).to_be_visible()
    record = post(page, 'record', button(history, INTEGRATION_QUESTION).click)
    assert record['action'] is None and not record['reviews']
    assert record['snapshots'][0]['state'] == saved['state']

    backup = browser_export(page, token)
    recover(page, content, backup, INTEGRATION_QUESTION, (saved,), None, [])
    button(history, '撤回保存授权').click()
    revoked = post(page, 'revoke', button(history, '确认撤回授权').click)
    assert revoked['authorized'] is False and revoked['epoch'] is None
    old_history = direct(page, url, token, 'history', {'epoch': epoch}, prefix=V5)
    assert old_history.status == 403
    history = local_history(page)
    expect(button(history, INTEGRATION_QUESTION)).to_have_count(0)
    fresh = post(page, 'consent', button(history, '授权本地保存').click)
    assert fresh['authorized'] is True and fresh['epoch'] != epoch
    denied = preview_backup(page, backup)
    assert denied['isolated'] and denied['eligible'] is False
    expect(button(history, '确认恢复')).to_be_disabled()
    attempted = direct(page, url, token, 'restore', {
        'epoch': fresh['epoch'], 'backup': json.loads(backup), 'confirm': True,
    }, prefix=V5)
    assert attempted.status in (403, 422)
    assert f'{V5}/action' not in requests and f'{API}/execute' not in requests


def close_session(page, url, token):
    connect(page, url, token)
    marker = '我想记录虚构橡木架：该保留它，还是回收？'
    result = start(page, marker)
    # The UI clears the connection immediately. Observe the keepalive request
    # without requiring the logging-out page to read its response body.
    with page.expect_request(lambda request: request.method == 'POST'
                             and urlsplit(request.url).path == f'{API}/end', timeout=5000) as pending:
        button(page, '结束本地会话').click()
    assert pending.value.post_data_json == {'session_id': result['session_id']}
    expect(field(page, '本地访问令牌')).to_have_value('')
    assert marker not in page.content()
    closed = direct(page, url, token, 'turn', {
        'session_id': result['session_id'], 'revision': result['revision'], 'text': '虚构记录已结束。',
    })
    assert closed.status in (404, 409, 410), closed.status
    assert_browser_memory_only(page, token, marker)


def run():
    report = Path(os.environ.get('PH_BROWSER_REPORT', '/tmp/psychohistory-browser-v06.json'))
    executable = os.environ.get('PH_CHROMIUM_EXECUTABLE') or shutil.which('chromium')
    args = ['--no-sandbox', '--disable-dev-shm-usage'] if sys.platform.startswith('linux') else []
    expect.set_options(timeout=12000)
    with TemporaryDirectory(prefix='psychohistory-browser-v06-') as tmp, sync_playwright() as playwright:
        root = Path(tmp).resolve()
        browser = playwright.chromium.launch(executable_path=executable, headless=True, args=args,
                                             ignore_default_args=['--disable-back-forward-cache'])
        try:
            with browser_session(browser, root / 'research') as (page, url, token, requests):
                autonomous_runtime(page, url, token)
                holdout = evaluate_cases(page, url, token, requests)
                incomplete_workflow(page, url, token)
                revised = revision_workflow(page, url, token, requests)
                privacy_workflow(page, url, token, root, revised, requests)
                close_session(page, url, token)
                native_cases = native_v07_cases(page, url, token)
                connect(page, url, token)
                page.set_viewport_size({'width': 390, 'height': 844})
                expect(page.get_by_role('textbox', name='你的决策问题', exact=True)).to_be_visible()
                assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
                browser_version = browser.version
        finally:
            browser.close()
    report_write(report, {
        'status': 'PASS', 'chromium': browser_version, 'engineering_case_sha256': CASE_HASH,
        'evaluation_scope': 'Fictional engineering cases frozen before implementation review. No scientific or user study.',
        'cross_domain': holdout,
        'native_v07_cases': native_cases,
        'checks': ['plain-language conversation without forced technical inputs', 'single clarification per reply',
                   'no invented probability evidence', 'offline autonomous path and retired model flag compatibility',
                   'verified correction and stale-state refusal', 'v0.5 calculation, gate and trace parity',
                   'unsupported methods remain ineligible', 'confirmed choice and plan grant no execution',
                   'separate storage and record consent', 'isolated recovery and withdrawn backup refusal',
                   'explicit local session end and narrow viewport', 'loopback and zero page errors'],
    })
    print('Chromium v0.7 conversation, six fictional domains, trace and recovery: PASS')


if __name__ == '__main__':
    run()
