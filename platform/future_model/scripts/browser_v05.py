"""Run three fictional workbench decisions and a genuine v0.4 recovery in Chromium."""

from datetime import UTC, datetime
from decimal import Decimal
from io import BytesIO
import json
import os
from contextlib import contextmanager
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from urllib.parse import urlsplit

from playwright.sync_api import expect, sync_playwright

from browser_v04 import PROJECT, button, combobox, field, loopback_service, research_navigation


V5 = '/api/v5/decisions'
V04_RELEASE = '2ecc6433d9ec0819b0fe71ff965e0ee6b71a5f4d'
SOURCE = '虚构验收记录 · 2026-11-21'
SCORE_BASIS = '共同基数效用，越高越好，允许目标补偿并确认所填权重。'
SCENARIO_BASIS = '同一决策时限的综合基数效用，越高越好。'
REVIEW = '虚构观察：只核对了实际选择的第一阶段表现。'


def post(page, endpoint, act, *, request_matches=None, prefix=V5):
    def matches(response):
        return (urlsplit(response.url).path == f'{prefix}/{endpoint}' and response.request.method == 'POST'
                and (request_matches is None or request_matches(response.request.post_data_json)))

    with page.expect_response(matches) as pending:
        act()
    response = pending.value
    assert response.ok, f'{endpoint} returned HTTP {response.status}'
    return response.json()


def edit_analysis(page, edit, state_matches):
    return post(page, 'analyze', edit, request_matches=lambda payload: state_matches(payload['state']))


def assert_plan(analysis):
    plan = analysis['plan']
    assert {'UNDERSTAND', 'FEASIBILITY', 'COMPARE', 'TIMING', 'REVIEW'} <= {step['stage'] for step in plan['steps']}
    assert all({'model_id', 'title'} <= method.keys() for method in plan['can_run'])
    assert all({'category', 'action', 'priority', 'prompt', 'reason', 'target', 'evidence_status'} <= item.keys()
               for item in plan['items'])
    assert analysis['execution'] == {'available': False, 'authorization': 'NOT_REQUESTED',
                                      'action_endpoint': 'OBSERVATION_ONLY'}
    return plan


def method(analysis, identity, status='EXECUTED'):
    entry = next(item for item in analysis['methods'] if item['model_id'] == identity)
    assert entry['status'] == status, (identity, entry['status'], entry.get('reasons'))
    return entry


def connect(page, url, token, *, version=None):
    version = version or os.environ.get('PH_BROWSER_WORKFLOW')
    page.goto(f'{url}?workflow={version}' if version else url)
    field(page, '本地访问令牌').fill(token)
    button(page, '连接工作空间').click()
    expect(page.get_by_text('工作空间已连接', exact=True)).to_be_visible()
    button(page, '个人决策工作台').click()


def tab(page, name):
    target = button(page, name)
    if not target.is_visible():
        button(page, '显示全部编辑项').click()
    target.click()


def open_question(page, question, deadline, labels):
    field(page, '你的决策问题').fill(question)
    started = post(page, 'start', button(page, '开始澄清').click)
    assert started['state']['question'] == question and started['state']['confirmed'] is False
    assert started['understanding']['mode'] == 'GUIDED_CONFIRMATION'
    assert not started['state']['options'] and not started['state']['weights']
    assert not assert_plan(started)['can_run']
    prompts = {item['field']: item['prompt'] for item in started['questions']}
    assert {'objectives', 'options', 'deadline', 'constraints', 'confirmed'} <= prompts.keys()
    expect(page.get_by_text(prompts['deadline'], exact=True)).to_be_visible()
    button(page, '问题与时限').click()
    field(page, '决策时限').fill(deadline)
    tab(page, '决策意图与证据')
    page.get_by_role('textbox', name='决策意图', exact=True).fill(question)
    button(page, '底线与方案').click()
    found = {item['value'] for item in started['understanding']['suggestions'] if item['field'] == 'options'}
    for index, label in enumerate(labels):
        if label in found:
            suggestion = page.get_by_role('listitem').filter(has_text=f'{label} · 原文片段')
            button(suggestion, '采用为方案').click()
            expect(field(page, '方案名称').nth(index)).to_have_value(label)
        else:
            button(page, '添加候选方案').click()
            field(page, '方案名称').nth(index).fill(label)
    return started['state']['decision_id']


def interval(page, label, low, high, source=SOURCE):
    combobox(page, f'{label}数据性质').select_option('synthetic')
    field(page, f'{label}下界').fill(str(low))
    field(page, f'{label}上界').fill(str(high))
    field(page, f'{label}来源').fill(source)


def constraint(page, title, operator, threshold, unit, measurements):
    button(page, '添加硬约束').click()
    card = page.get_by_role('group').filter(has=field(page, '底线名称')).last
    field(card, '底线名称').fill(title)
    combobox(card, '比较符号').select_option(operator)
    field(card, '阈值').fill(str(threshold))
    field(card, '底线单位').fill(unit)
    field(card, '底线依据').fill(SOURCE)
    for label, low, high in measurements:
        interval(page, f'{label} · {title}', low, high)


def constraints_complete(page):
    field(page, '我确认底线清单完整（也可确认没有硬约束）').check()


def objectives(page, labels, weights=None):
    tab(page, '目标与权重')
    for index, label in enumerate(labels):
        button(page, '添加目标').click()
        field(page, '目标名称').nth(index).fill(label)
        field(page, '目标单位').nth(index).fill('效用')
    if weights:
        for label, (low, high) in zip(labels, weights, strict=True):
            field(page, f'{label}权重下界').fill(str(low))
            field(page, f'{label}权重上界').fill(str(high))
        field(page, '我确认使用下列权重区间').check()


def scores(page, rows):
    tab(page, '评分与误差')
    field(page, '评分量表与比较依据').fill(SCORE_BASIS)
    combobox(page, '评分误差依赖').select_option('rectangle')
    field(page, '评分误差依赖依据').fill(SOURCE)
    page.get_by_text('共享误差与评分变换', exact=True).click()
    combobox(page, '评分变换').select_option('identity')
    for option, objective, value in rows:
        interval(page, f'{option} · {objective}', value, value)


def scenarios(page, cases):
    tab(page, '情景与参考')
    field(page, '情景效用的共同量表').fill(SCENARIO_BASIS)
    combobox(page, '情景效用依赖').select_option('rectangle')
    field(page, '情景效用依赖依据').fill(SOURCE)
    for index, (label, values) in enumerate(cases):
        button(page, '添加情景').click()
        field(page, '情景名称').nth(index).fill(label)
        combobox(page, '情景性质').nth(index).select_option('synthetic')
        field(page, '情景来源或假设').nth(index).fill(SOURCE)
        for option, value in values:
            interval(page, f'{label} · {option}效用', value, value)


def confirm(page, decision_id):
    analysis = post(page, 'analyze', button(page, '确认并分析').click,
                    request_matches=lambda request: request['state']['confirmed'])
    assert analysis['decision_id'] == decision_id
    assert_plan(analysis)
    expect(page.get_by_role('region', name='当前分析')).to_be_visible()
    return analysis


def clear_current(page):
    button(page, '开始新决策').click()
    expect(field(page, '你的决策问题')).to_have_value('')


def decimal_pair(analysis, values):
    result = method(analysis, 'c034_joint_robustness')['result']
    pair, = result['pairs']
    assert (Decimal(pair['lower']), Decimal(pair['upper'])) == tuple(map(Decimal, values))
    return result


def assert_revision(page, analysis):
    expect(page.get_by_text(analysis['input_hash'], exact=True)).to_have_count(1)


def cutoff(page, label, day, source=SOURCE):
    field(page, f'{label}时点').fill(str(day))
    combobox(page, f'{label}数据性质').select_option('synthetic')
    field(page, f'{label}来源').fill(source)


def timing(page, horizon, deadline, wait, *, prediction=None, status_quo=None):
    tab(page, '时机与行动')
    button(page, '启用时机分析').click()
    field(page, '时机单位').fill('天')
    field(page, '时间原点').fill('收到虚构通知当日')
    cutoff(page, '分析期限', horizon)
    cutoff(page, '决策截止', deadline)
    interval(page, '等待时长', wait, wait)
    if prediction is not None:
        interval(page, '预计完成时点', prediction, prediction, '虚构调查进度估计 · 从通知当日计')
    if status_quo:
        combobox(page, '维持现状方案').select_option(label=status_quo)
        combobox(page, '备用方案').select_option(label=status_quo)


def timing_action(page, option, day, cost, scenario_labels, *, delay=0):
    page.get_by_text(f'{option}的行动时机', exact=True).click()
    cutoff(page, f'{option}截止', day)
    interval(page, f'{option}切换成本', cost, cost)
    for scenario in scenario_labels:
        interval(page, f'{option} · {scenario}延迟损失', delay, delay)


def confirm_timing(page):
    return edit_analysis(page, lambda: field(page, '确认时机假设').check(),
                         lambda state: (state.get('timing') or {}).get('confirmed') is True)


def career_case(page):
    current = '留在现有产品分析岗位'
    offer, rejected = '接受星桥长期产品岗位', '接受潮汐长期增长岗位'
    question = f'我该{offer}，还是{rejected}？我也可以{current}。两周内看长期发展，收入底线和工时都不能越过。'
    decision_id = open_question(page, question, '两周内', (current, offer, rejected))
    income, hours = '月收入底线', '每周工时上限'
    constraint(page, income, '>=', 10000, '元/月', [(current, 10500, 11200)])
    constraint(page, hours, '<=', 45, '小时/周', [(current, 40, 43), (offer, 41, 44), (rejected, 51, 54)])
    constraints_complete(page)
    growth, stability = '长期成长', '收入稳定性'
    objectives(page, (growth, stability), [('.60', '.65'), ('.35', '.40')])
    scores(page, [(current, growth, '.80'), (current, stability, '.40'),
                  (offer, growth, '.50'), (offer, stability, '.80')])
    baseline = confirm(page, decision_id)
    by_label = {x['label']: x for x in baseline['feasibility']}
    assert [by_label[label]['status'] for label in (current, offer, rejected)] == ['ACCEPT', 'UNRESOLVED', 'REJECT']
    reasons = assert_plan(baseline)['items']
    pivotal = next(item for item in reasons if item['priority'] == 'HIGH'
                   and item['target'].get('option_id') == by_label[offer]['option_id'])
    deferred = next(item for item in reasons if item['priority'] == 'DEFERRED'
                    and item['target'].get('option_id') == by_label[rejected]['option_id'])
    assert deferred['proof']['witness_constraint_id'] != deferred['target']['constraint_id']
    guide = page.get_by_role('region', name='下一步计划')
    deferred_card = guide.locator(f'[data-plan-item="{deferred["id"]}"]')
    expect(deferred_card).to_have_count(0)
    guide.get_by_role('button', name=re.compile('^查看暂缓事项')).click()
    expect(deferred_card).to_be_visible()
    pivotal_card = guide.locator(f'[data-plan-item="{pivotal["id"]}"]')
    button(pivotal_card, '前往填写').click()
    expect(combobox(page, f'{offer} · {income}数据性质')).to_be_focused()

    def revise_income():
        card = page.get_by_role('group', name=income, exact=True)
        field(card, '阈值').fill('9500')
        interval(page, f'{offer} · {income}', 9500, 9800, '虚构书面薪酬区间 · 2026-11-21')

    admitted = edit_analysis(page, revise_income, lambda state: (
        Decimal(state['constraints'][0]['threshold']) == 9500
        and state['options'][1]['measurements'].get(state['constraints'][0]['id'], {}).get('source')
    ))
    assert [item['status'] for item in admitted['feasibility']] == ['ACCEPT', 'ACCEPT', 'REJECT']
    assert decimal_pair(admitted, ('.02', '.055'))['leaders'] == [by_label[current]['option_id']]
    assert admitted['input_hash'] != baseline['input_hash']

    button(page, '目标与权重').click()

    def revise_growth():
        field(page, f'{growth}权重下界').fill('.55')
        field(page, f'{stability}权重上界').fill('.45')

    revised = edit_analysis(page, revise_growth, lambda state: (
        Decimal(state['weights'][state['objectives'][0]['id']]['lower']) == Decimal('.55')
        and Decimal(state['weights'][state['objectives'][1]['id']]['upper']) == Decimal('.45')
    ))
    assert not decimal_pair(revised, ('-.015', '.055'))['leaders']
    assert revised['input_hash'] != admitted['input_hash']
    assert_revision(page, revised)

    worlds = ('增长顺利', '增长延迟')
    scenarios(page, [(worlds[0], [(current, 6), (offer, 8)]), (worlds[1], [(current, 6), (offer, 7)])])
    timing(page, 14, 10, 4, prediction=4, status_quo=current)
    interval(page, '希望行动时点', 2, 2)
    timing_action(page, current, 10, 0, worlds)
    timing_action(page, offer, 3, 0, worlds)
    calendar = confirm_timing(page)
    result = method(calendar, 'timing_actions')['result']
    offer_id = by_label[offer]['option_id']
    assert result['time_inputs']['prediction_vs_action_cutoffs'][offer_id] == 'AFTER'
    assert any(item['type'] == 'wait' and item['option_id'] == offer_id and item['status'] == 'EXPIRED'
               for item in result['strategies'])
    assert_revision(page, calendar)
    return question, calendar


def learning_case(page):
    now, wait, reserve = '立即报名数据训练', '等下一轮课程', '保留学习预算'
    question = f'我该{now}，还是{wait}？也可以{reserve}。六周内用有限时间和资金学习，额外消息有机会成本。'
    decision_id = open_question(page, question, '六周内', (now, wait, reserve))
    constraint(page, '支出预算', '<=', 600, '元', [(now, 520, 600), (wait, 100, 500), (reserve, 0, 0)])
    constraint(page, '每周时间', '<=', 8, '小时/周', [(now, 6, 8), (wait, 2, 6), (reserve, 0, 0)])
    constraints_complete(page)
    objectives(page, ('技能提升与机会成本',))
    first, second = '岗位需求扩大', '岗位需求平稳'
    scenarios(page, [(first, [(now, 10), (wait, 6), (reserve, 5)]),
                     (second, [(now, 0), (wait, 6), (reserve, 5)])])
    unknown = confirm(page, decision_id)
    method(unknown, 'voi_point', 'INELIGIBLE')
    regret = method(unknown, 'C029')['result']
    assert regret['leaders'] and len(unknown['feasibility']) == 3

    tab(page, '信息价值')
    button(page, '启用信息价值分析').click()
    field(page, '调查成本单位').fill('效用')
    interval(page, '调查成本', '.5', '.5')
    field(page, '所有通过硬约束的方案在收到信号后仍可选择').check()
    field(page, '调查后行动可用性依据').fill('虚构训练：即时信号时三种方案都存在，较晚行动按各自截止核对。')
    field(page, '调查不改变行动时机的依据').fill('虚构即时反馈，无额外耗时。')
    positive_signal, negative_signal = '推荐', '不推荐'
    for index, signal in enumerate((positive_signal, negative_signal)):
        button(page, '添加信号').click()
        field(page, '信号名称').nth(index).fill(signal)
    interval(page, f'{first}先验概率', '.5', '.5')
    interval(page, f'{second}先验概率', '.5', '.5')
    for label, high, low in ((first, '.9', '.1'), (second, '.3', '.7')):
        interval(page, f'{label} · {positive_signal}条件概率', high, high)
        if label == first:
            interval(page, f'{label} · {negative_signal}条件概率', low, low)

    last = f'{second} · {negative_signal}条件概率'

    def complete_probabilities(state):
        information = state['information']
        scenario_id = state['scenarios'][1]['id']
        signal_id = information['signals'][1]['id']
        return information['likelihoods'].get(scenario_id, {}).get(signal_id, {}).get('source') == SOURCE

    positive = edit_analysis(page, lambda: interval(page, last, '.7', '.7'), complete_probabilities)
    value = method(positive, 'voi_point')['result']
    assert (Decimal(value['evsi']), Decimal(value['evpi']), Decimal(value['net_value'])) == (
        Decimal('.9'), Decimal('2'), Decimal('.4'),
    )
    assert value['decision'] == 'POSITIVE'
    assert_revision(page, positive)

    revised_fee = edit_analysis(page, lambda: interval(page, '调查成本', '.95', '.95'),
                                lambda state: Decimal(state['information']['cost']['upper']) == Decimal('.95'))
    value = method(revised_fee, 'voi_point')['result']
    assert Decimal(value['net_value']) == Decimal('-.05') and value['decision'] == 'NEGATIVE'

    timing(page, 42, 20, 5, prediction=5, status_quo=reserve)
    for option in (now, wait, reserve):
        timing_action(page, option, 10 if option == now else 20, 0, (first, second))
    button(page, '添加调查时机').click()
    combobox(page, '调查完成模型').select_option('deterministic')
    combobox(page, '调查时机数据性质').select_option('synthetic')
    field(page, '调查时机依据').fill(SOURCE)
    interval(page, '时机分析中的调查成本', '.5', '.5')
    interval(page, '确定调查时长', 5, 5)
    before = confirm_timing(page)
    now_id = next(item['option_id'] for item in before['feasibility'] if item['label'] == now)
    assert method(before, 'timing_actions')['result']['time_inputs']['prediction_vs_action_cutoffs'][now_id] == 'WITHIN'
    before_investigation = method(before, 'timing_investigation')['result']
    assert before_investigation['status'] == 'INVESTIGATE' and Decimal(before_investigation['net_value']) == Decimal('.4')
    deadline_edit = edit_analysis(page, lambda: field(page, f'{now}截止时点').fill('4'),
                                  lambda state: Decimal(state['timing']['actions'][now_id]['cutoff']['at']) == 4)
    assert method(deadline_edit, 'timing_actions')['result']['time_inputs']['prediction_vs_action_cutoffs'][now_id] == 'AFTER'
    late_investigation = method(deadline_edit, 'timing_investigation')['result']
    assert late_investigation['status'] == 'ACT_NOW' and Decimal(late_investigation['net_value']) == Decimal('-.5')
    assert now_id not in {option for branch in late_investigation['policy'] for option in branch['eligible_option_ids']}
    assert_revision(page, deadline_edit)

    tab(page, '信息价值')
    source = field(page, f'{last}来源')
    expect(source).not_to_have_value('')

    def clear_probability_source():
        source.press('ControlOrMeta+A')
        source.press('Backspace')
        expect(source).to_have_value('')

    refreshed = edit_analysis(page, clear_probability_source,
                              lambda state: not complete_probabilities(state))
    method(refreshed, 'voi_point', 'INELIGIBLE')
    method(refreshed, 'timing_investigation', 'INELIGIBLE')
    assert method(refreshed, 'C029')['result']['leaders'] == regret['leaders']
    return question


def status_quo_case(page):
    stay, reversible, irreversible = '继续原有社区班次', '试行可撤回的新班次', '签订不可撤回的全年班次'
    question = f'我该{reversible}，还是{irreversible}？还可以{stay}。最迟一周内决定，不接受过大损失，偏好还没有定。'
    decision_id = open_question(page, question, '七天内', (stay, reversible, irreversible))
    constraint(page, '损失上限', '<=', 5, '效用', [(stay, 0, 0), (reversible, 1, 3), (irreversible, 8, 10)])
    constraints_complete(page)
    objectives(page, ('活动便利', '安排稳定'))
    scores(page, [(stay, '活动便利', '.5'), (stay, '安排稳定', '.9'),
                  (reversible, '活动便利', '.8'), (reversible, '安排稳定', '.6')])
    cases = [('正常排班', [(stay, 6), (reversible, 8)]), ('志愿者减少', [(stay, 6), (reversible, 8)])]
    scenarios(page, cases)
    analysis = confirm(page, decision_id)
    assert [item['status'] for item in analysis['feasibility']] == ['ACCEPT', 'ACCEPT', 'REJECT']
    method(analysis, 'c034_joint_robustness', 'INELIGIBLE')
    assert method(analysis, 'C029')['result']['leaders'] == [analysis['feasibility'][1]['option_id']]
    timing(page, 7, 7, 2, status_quo=stay)
    worlds = [case[0] for case in cases]
    timing_action(page, stay, 7, 0, worlds, delay=1)
    timing_action(page, reversible, 5, 3, worlds)
    for option, description in ((reversible, '试行后可逐周退出'), (irreversible, '签订后全年固定')):
        if option == irreversible:
            page.get_by_text(f'{option}的行动时机', exact=True).click()
        field(page, f'{option}可逆性说明').fill(description)
        combobox(page, f'{option}可逆性数据性质').select_option('synthetic')
        field(page, f'{option}可逆性来源').fill(SOURCE)
    timed = confirm_timing(page)
    timing_result = method(timed, 'timing_actions')['result']
    stay_id = timed['feasibility'][0]['option_id']
    assert timing_result['undominated_strategies'] == [{'type': 'status_quo', 'option_id': stay_id}]
    method(timed, 'c034_joint_robustness', 'INELIGIBLE')
    assert_revision(page, timed)
    return question, stay, timed


def preview_backup(page, archive):
    field(page, '选择备份文件').set_input_files({
        'name': 'fictional-decisions.json', 'mimeType': 'application/json', 'buffer': archive,
    })
    return post(page, 'restore', button(page, '预览备份').click)


def legacy_archive(research):
    """Build a signed v0.4 export with its historical implementation and consent ledger."""
    archive = subprocess.run(['git', 'archive', V04_RELEASE, 'platform/future_model/src'],
                             cwd=PROJECT.parents[1], capture_output=True, check=True).stdout
    legacy = research.parent / 'v04-source'
    with tarfile.open(fileobj=BytesIO(archive), mode='r:') as tar:
        tar.extractall(legacy, filter='data')
    source = legacy / 'platform/future_model/src'

    def invoke(action, payload=None):
        completed = subprocess.run([sys.executable, '-m', 'psychohistory.cli', '--data', str(research),
                                    'decision', action], cwd=source, env={**os.environ, 'PYTHONPATH': str(source)},
                                   input=json.dumps(payload) if payload is not None else '', text=True,
                                   capture_output=True)
        assert completed.returncode == 0, f'v0.4 CLI {action} returned {completed.returncode}'
        return json.loads(completed.stdout)

    epoch = invoke('grant')['epoch']
    question = '虚构旧版本恢复：应该继续图书整理，还是转为图书登记？'
    state = invoke('start', {'question': question})['state']
    state.update(confirmed=True, deadline='一个月', constraints_confirmed=True,
                 options=[{'id': 'sort', 'label': '继续图书整理'}, {'id': 'catalog', 'label': '转为图书登记'}],
                 objectives=[{'id': 'use', 'label': '使用便利程度', 'unit': '效用', 'direction': 'max'}])
    saved = invoke('save', {'epoch': epoch, 'state': state})
    assert saved['analysis']['hub_version'] == '0.4.0'
    record = {'epoch': epoch, 'decision_id': state['decision_id']}
    action = invoke('action', {**record, 'option_id': 'sort', 'occurred_at': datetime.now(UTC).isoformat(), 'revision': 1})
    review = invoke('review', {**record, 'observation': REVIEW, 'observed_at': datetime.now(UTC).isoformat(), 'kind': 'synthetic'})
    backup = invoke('export', {'epoch': epoch})
    return question, saved, action, review, json.dumps(backup, ensure_ascii=False).encode()


def save(page, analysis):
    assert_revision(page, analysis)
    snapshot = post(page, 'save', button(page, '保存当前决策').click)
    assert snapshot['analysis']['input_hash'] == analysis['input_hash']
    assert snapshot['analysis']['hub_version'] == '0.5.0'
    expect(page.get_by_text('已保存当前修订', exact=True)).to_be_visible()
    return snapshot


def filter_candidates(page, analysis):
    result = page.get_by_role('region', name='当前分析')
    options = combobox(page, '选择方案显示范围')
    methods = combobox(page, '选择方法显示范围')
    option_ids = [entry['option_id'] for entry in analysis['feasibility']]
    rows = result.locator('[data-option-id]')
    expect(rows).to_have_count(3)
    options.select_option('ACCEPT')
    expect(rows).to_have_count(2)
    expect(result.locator(f'[data-option-id="{option_ids[-1]}"]')).to_have_count(0)
    methods.select_option('EXECUTED')
    expect(page.locator('[data-model-id="c034_joint_robustness"]')).to_have_count(0)
    methods.select_option('all')
    options.select_option('all')
    expect(rows).to_have_count(3)
    assert rows.evaluate_all('rows => rows.map(row => row.dataset.optionId)') == option_ids
    assert_revision(page, analysis)


def session_reset(page, *markers):
    expect(field(page, '本地访问令牌')).to_have_value('')
    expect(page.get_by_text('本地会话未连接', exact=True)).to_be_visible()
    expect(page.locator('.decision-workbench')).to_have_count(0)
    assert all(marker not in page.content() for marker in markers)


def assert_browser_memory_only(page, *markers):
    assert page.evaluate('''async markers => {
      const stored = [...Object.values(localStorage), ...Object.values(sessionStorage)];
      return stored.every(value => markers.every(marker => !value.includes(marker)))
        && (await indexedDB.databases()).length === 0;
    }''', list(markers))
    assert not page.context.cookies()


def session_boundaries(page, url, token, question):
    assert_browser_memory_only(page, token, question)
    research_navigation(page)
    expect(page.locator('.decision-workbench')).to_have_count(0)
    assert question not in page.url and question not in page.content()
    button(page, '个人决策工作台').click()
    expect(field(page, '你的决策问题')).to_have_value('')

    marker = f'{question}虚构后退标记'
    field(page, '你的决策问题').fill(marker)
    post(page, 'start', button(page, '开始澄清').click)
    expect(page.get_by_text(marker, exact=True).first).to_be_visible()
    forward = page.goto(f'{url}/?session-check=history')
    assert forward is not None and forward.ok, f'Forward navigation returned {forward.status if forward else None}'
    back = page.go_back()
    assert back is None or back.ok, f'Back navigation returned {back.status} at {urlsplit(back.url).path}'
    session_reset(page, marker)

    connect(page, url, token)
    field(page, '你的决策问题').fill(f'{question}虚构刷新标记')
    page.reload()
    session_reset(page, '虚构刷新标记')

    connect(page, url, token)
    field(page, '你的决策问题').fill(f'{question}虚构退出标记')
    post(page, 'start', button(page, '开始澄清').click)
    expect(page.get_by_text(f'{question}虚构退出标记', exact=True).first).to_be_visible()
    button(page, '结束本地会话').click()
    session_reset(page, '虚构退出标记')
    assert_browser_memory_only(page, token, question)
    connect(page, url, token)
    expect(field(page, '你的决策问题')).to_have_value('')


def browser_export(page, token):
    with page.expect_download() as download:
        button(page, '导出本地备份').click()
    backup = download.value.path().read_bytes()
    assert token.encode() not in backup
    expect(page.get_by_text('已导出本地备份', exact=True)).to_be_visible()
    return backup


def recover(page, path, archive, question, snapshots, action, reviews, *, count=1):
    # Only the disposable personal content file is removed. The signing ledger stays put.
    expect(button(page, question)).to_be_visible()
    path.unlink()
    preview = preview_backup(page, archive)
    assert preview == {'mode': 'preview', 'isolated': True, 'eligible': True, 'decision_count': count, 'reason': None}
    assert not path.exists()
    restored = post(page, 'restore', button(page, '确认恢复').click)
    assert restored == {'mode': 'restored', 'isolated': False, 'decision_count': count}
    assert path.is_file()
    record = post(page, 'record', button(page, question).click)
    assert record['action'] == action and record['reviews'] == reviews
    assert [entry['state'] for entry in record['snapshots']] == [entry['state'] for entry in snapshots]
    assert all(entry['analysis'] is None and entry['analysis_status'] == 'RECOMPUTE_REQUIRED'
               for entry in record['snapshots'])
    return record


def withdraw(page, url, token, epoch, archive, *questions):
    button(page, '撤回保存授权').click()
    status = post(page, 'revoke', button(page, '确认撤回授权').click)
    assert status['authorized'] is False and status['epoch'] is None
    expect(page.get_by_text('已撤回保存授权', exact=True)).to_be_visible()
    expect(field(page, '你的决策问题')).to_have_value('')
    assert all(question not in page.content() for question in questions)
    headers = {'Authorization': f'Bearer {token}'}
    lost = page.request.post(f'{url}{V5}/history', data={'epoch': epoch}, headers=headers)
    assert lost.status == 403
    fresh = post(page, 'consent', button(page, '授权本地保存').click)
    assert fresh['authorized'] and fresh['epoch'] != epoch
    denied = preview_backup(page, archive)
    assert denied['isolated'] and not denied['eligible'] and denied['reason']
    expect(button(page, '确认恢复')).to_be_disabled()
    forced = page.request.post(f'{url}{V5}/restore', headers=headers, data={
        'epoch': fresh['epoch'], 'backup': json.loads(archive), 'confirm': True,
    })
    assert forced.status in (403, 422)
    empty = page.request.post(f'{url}{V5}/history', headers=headers, data={'epoch': fresh['epoch']})
    assert empty.ok and empty.json() == []


def write_hindsight(page, snapshot, stay_id, requests):
    details = page.get_by_role('region', name='决策记录详情')
    field(details, '观察结果').fill(REVIEW)
    combobox(details, '回访性质').select_option('synthetic')
    details.get_by_text('记录事后证据与当前偏好', exact=True).click()
    evidence, applicability = '虚构排班记录显示原班次在实际阶段可用。', '未来社区活动排班'
    process_quality = '事前核对了不可接受损失和切换代价，保留偏好未知。'
    field(details, '事前流程质量').fill(process_quality)
    field(details, '事后新证据').fill(evidence)
    button(details, '填写回访时的偏好').click()
    for label, value in (('偏好适用范围', applicability), ('偏好来源', SOURCE),
                         ('偏好名称', '稳定性'), ('偏好内容', '安排变动时，优先考虑可撤回。')):
        field(details, label).fill(value)
    review = post(page, 'review', button(details, '追加回访').click)
    assert review['kind'] == 'synthetic' and review['option_id'] == stay_id and review['observation'] == REVIEW
    assert review['hindsight']['evidence'] == evidence
    assert review['hindsight']['process_quality'] == process_quality
    assert review['hindsight']['current_preferences']['applicability'] == applicability
    expect(details.get_by_text(REVIEW, exact=True)).to_be_visible()
    expect(details.get_by_text(process_quality, exact=False)).to_be_visible()
    assert not any(path.endswith('/adopt-preferences') for path in requests)

    button(details, '保留此偏好供将来使用').click()
    assert not any(path.endswith('/adopt-preferences') for path in requests)
    adoption = post(page, 'adopt-preferences', button(details, '确认采纳为未来偏好').click)
    assert adoption['decision_id'] == snapshot['decision_id'] and adoption['review_index'] == 1
    assert adoption['preferences'] == review['hindsight']['current_preferences']
    expect(details.get_by_text('已采纳为未来可选偏好', exact=True)).to_be_visible()
    return {**review, 'adopted_preferences': adoption}, adoption


def use_preference_in_new_draft(page, adoption):
    clear_current(page)
    question = '虚构未来偏好验证：下个月怎样安排公共活动？'
    field(page, '你的决策问题').fill(question)
    new = post(page, 'start', button(page, '开始澄清').click)
    assert new['state']['preferences'] is None and not new['state']['weights']
    preference_region = page.get_by_role('region', name='未来可选偏好')
    show = button(preference_region, '查看已采纳偏好')
    if show.is_visible():
        post(page, 'preferences', show.click)
    applicability = adoption['preferences']['applicability']
    preference_region.get_by_text(re.compile(f'^{re.escape(applicability)} · ')).click()
    button(preference_region, '选用此偏好').click()
    button(preference_region, '确认用于本次决策').wait_for()
    analysis = edit_analysis(page, button(preference_region, '确认用于本次决策').click,
                             lambda state: not state['weights'] and
                             (state.get('preferences') or {}).get('adopted_version_id') == adoption['version_id'])
    assert analysis['decision_id'] == new['state']['decision_id'] and analysis['status'] == 'CLARIFY'
    return question


def record_current_case(page, url, token, root, requests):
    career_question, career = career_case(page)
    consent = post(page, 'consent', button(page, '授权本地保存').click)
    assert consent['authorized'] and consent['epoch']
    save(page, career)
    clear_current(page)

    learning_question = learning_case(page)
    session_boundaries(page, url, token, learning_question)

    life_question, stay, life = status_quo_case(page)
    filter_candidates(page, life)
    stay_id = life['feasibility'][0]['option_id']
    tab(page, '时机与行动')
    combobox(page, '计划选择').select_option(label=stay)
    field(page, '行动计划说明').fill('仅记录拟议方案，是否实际行动另行记录。')
    plan = edit_analysis(page, button(page, '确认行动计划').click,
                         lambda state: state.get('intended_option_id') == stay_id)
    assert_plan(plan)
    expect(page.locator('[data-authorization="NOT_REQUESTED"]')).to_contain_text('未授权')
    assert not any(path == f'{V5}/action' for path in requests)
    snapshot = save(page, plan)
    assert snapshot['state']['intended_option_id'] == stay_id
    history_row = button(page, life_question)
    expect(history_row).to_be_enabled()
    # Defer the request to exercise editing during a pending record reload.
    page.evaluate('''() => {
      const original = window.fetch.bind(window);
      window.fetch = (...args) => {
        if (!String(args[0]).endsWith('/decisions/record')) return original(...args);
        window.fetch = original;
        return new Promise(resolve => {
          window.releaseRecordFixture = () => {
            delete window.releaseRecordFixture;
            resolve(original(...args));
          };
        });
      };
    }''')
    history_row.click()
    page.wait_for_function('typeof window.releaseRecordFixture === "function"', timeout=10000)
    choice = combobox(page, '实际选择')
    try:
        expect(choice).to_be_disabled()
    finally:
        with page.expect_response(lambda reply: urlsplit(reply.url).path == f'{V5}/record') as reloaded:
            page.evaluate('window.releaseRecordFixture()')
    expect(choice).to_be_enabled()
    assert reloaded.value.ok
    record = reloaded.value.json()
    assert record['action'] is None and not record['reviews']
    assert set(item['label'] for item in record['snapshots'][-1]['state']['options']) == {
        item['label'] for item in life['feasibility']
    }
    assert not any(path == f'{V5}/action' for path in requests)

    choice.select_option(label=stay)
    action = post(page, 'action', button(page, '记录实际行动').click)
    assert action['option_id'] == stay_id and action['revision'] == snapshot['revision']
    assert {key: value for key, value in action['coverage'].items() if key != stay_id} == {
        item['option_id']: 'UNOBSERVED' for item in life['feasibility'][1:]
    }
    review, adoption = write_hindsight(page, snapshot, stay_id, requests)
    archive = browser_export(page, token)
    recovered = recover(page, root / 'research-personal-v04/records.sqlite3', archive,
                        life_question, (snapshot,), action, [review], count=2)
    assert recovered['snapshots'][0]['state']['intended_option_id'] == stay_id
    assert recovered['snapshots'][0]['state']['preferences'] is None
    future_question = use_preference_in_new_draft(page, adoption)
    assert not any(path.endswith(('/execute', '/approve')) for path in requests)
    withdraw(page, url, token, consent['epoch'], archive, career_question, life_question, future_question)
    page.set_viewport_size({'width': 390, 'height': 844})
    expect(field(page, '你的决策问题')).to_be_visible()
    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')


@contextmanager
def browser_session(browser, data):
    with loopback_service(data) as (url, token):
        context = browser.new_context(viewport={'width': 1440, 'height': 1000}, service_workers='block')
        posts, outside, errors = [], [], []

        def local(route):
            address = urlsplit(route.request.url)
            if address.scheme == 'http' and address.netloc == urlsplit(url).netloc:
                if route.request.method == 'POST':
                    posts.append(address.path)
                route.continue_()
            else:
                outside.append(True)
                route.abort()

        context.route('**/*', local)
        page = context.new_page()
        page.set_default_timeout(10000)
        page.on('pageerror', lambda error: errors.append(str(error)))
        try:
            yield page, url, token, posts
            assert not errors, errors
            assert not outside, 'The application requested a resource outside loopback'
        except Exception as error:
            sanitized = AssertionError(str(error).replace(token, '[redacted]'))
            raise sanitized.with_traceback(error.__traceback__) from None
        finally:
            context.close()


def run():
    report = Path(os.environ.get('PH_BROWSER_REPORT', '/tmp/psychohistory-browser-v05.json'))
    executable = os.environ.get('PH_CHROMIUM_EXECUTABLE') or shutil.which('chromium')
    args = ['--no-sandbox', '--disable-dev-shm-usage'] if sys.platform.startswith('linux') else []
    expect.set_options(timeout=12000)
    with tempfile.TemporaryDirectory(prefix='psychohistory-browser-v05-') as tmp, sync_playwright() as playwright:
        root = Path(tmp).resolve()
        browser = playwright.chromium.launch(executable_path=executable, headless=True, args=args,
                                             ignore_default_args=['--disable-back-forward-cache'])
        try:
            with browser_session(browser, root / 'research') as (page, url, token, requests):
                connect(page, url, token)
                record_current_case(page, url, token, root, requests)
                assert requests.count(f'{V5}/start') >= 3
                assert not any(path.startswith('/api/v4/decisions/') for path in requests)

            legacy = root / 'legacy-research'
            question, snapshot, action, review, archive = legacy_archive(legacy)
            with browser_session(browser, legacy) as (page, url, token, requests):
                connect(page, url, token)
                recover(page, root / 'legacy-research-personal-v04/records.sqlite3', archive,
                        question, (snapshot,), action, [review])
                connect(page, url, token, version='v04')
                old_record = post(page, 'record', button(page, question).click, prefix='/api/v4/decisions')
                assert old_record['snapshots'][0]['state'] == snapshot['state']
                assert old_record['action'] == action and old_record['reviews'] == [review]
            browser_version = browser.version
        finally:
            browser.close()
    report.write_text(json.dumps({
        'status': 'PASS', 'chromium': browser_version,
        'career': ['pivotal income gap and independently disqualified option', 'income and weight edits',
                   'expected evidence arrives after the offer expires'],
        'learning': ['unknown and sourced probability cases', 'positive and negative EVSI net of cost',
                     'deadline edit reverses expected investigation value and changes available actions'],
        'life': ['unknown preference and competing calculations', 'status quo after switching costs',
                 'display filters leave candidate set intact', 'plan confers no execution authority'],
        'privacy': ['research navigation, browser back, refresh and explicit session end',
                    'choice-only observation and locked edits while reloading a record', 'export and isolated v0.5 and historical v0.4 recovery',
                    'separate process quality, hindsight and explicitly adopted preferences',
                    'old archive rejected after withdrawal', '390px layout', 'loopback and zero page errors'],
        'v04_fixture_commit': V04_RELEASE,
    }, indent=2) + '\n', encoding='utf-8')
    print('Chromium v0.5 three fictional decisions and v0.4 recovery: PASS')


if __name__ == '__main__':
    run()
