"""Regression: >200 later terminal runs cannot hide old work or selected history.
Use a dedicated synthetic fixture root created by --prepare before starting API.
"""
import argparse
import json
import os
import sys
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--data',type=Path,required=True)
parser.add_argument('--url',default='http://127.0.0.1:8874')
parser.add_argument('--prepare',action='store_true')
parser.add_argument('--report',type=Path,default=Path('/tmp/pr40-browser-history.json'))
args=parser.parse_args()
if args.prepare:
    if args.data.exists():raise ValueError('Use a new dedicated synthetic fixture root')
    from psychohistory.storage import Store
    from psychohistory.engine import run_experiment
    store=Store(args.data)
    store.create_run('old-pending',{'seed':7,'rounds':1,'population':2,'intervention':.2})
    store.create_run('old-completed',{'seed':7,'rounds':1,'population':2,'intervention':.2})
    store.update_run('old-completed',status='APPROVED');store.update_run('old-completed',status='RUNNING')
    store.update_run('old-completed',status='COMPLETED',result_hash=store.put(run_experiment(rounds=1,population=2)))
    for i in range(201):
        store.create_run(f'terminal-{i}',{'seed':i,'rounds':1});store.update_run(f'terminal-{i}',status='CANCELED')
    print('Prepared synthetic pagination fixture (203 runs)')
else:
    from playwright.sync_api import sync_playwright
    token=(args.data/'token').read_text().strip()
    with sync_playwright() as p:
        linux = sys.platform.startswith('linux')
        executable = os.environ.get('PH_CHROMIUM_EXECUTABLE') or ('/usr/bin/chromium' if linux else None)
        launch_args = ['--no-sandbox', '--disable-dev-shm-usage'] if linux else []
        browser = p.chromium.launch(executable_path=executable, headless=True, args=launch_args)
        page=browser.new_page(viewport={'width':1440,'height':1000});errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(args.url);page.get_by_label('本地访问令牌').fill(token)
        page.get_by_role('button',name='连接工作空间',exact=True).click()
        page.get_by_text('工作空间已连接',exact=True).wait_for()
        page.get_by_role('button',name='实验工作台',exact=True).click()
        old=page.get_by_role('row').filter(has=page.get_by_role('button',name='old-pending',exact=True))
        old.get_by_role('button',name='取消',exact=True).click()
        heading=page.get_by_role('heading',name='所选实验 old-pending')
        page.locator('section').filter(has=heading).get_by_text('CANCELED',exact=True).wait_for()
        # Old completed run is on history page 5, independently of the live feed.
        for index in range(2,6):
            page.get_by_role('button',name='较早一页',exact=True).click()
            page.get_by_text(f'历史第 {index} 页 · 活动任务始终显示',exact=True).wait_for()
        page.get_by_role('button',name='old-complete',exact=True).click()
        page.get_by_role('heading',name='两条独立情景分支',exact=True).wait_for()
        # Current selection/result survives navigation to a page not containing it.
        page.get_by_role('button',name='较新一页',exact=True).click()
        page.get_by_text('历史第 4 页 · 活动任务始终显示',exact=True).wait_for()
        page.get_by_role('heading',name='两条独立情景分支',exact=True).wait_for()
        page.get_by_role('button',name='情景历史',exact=True).click()
        assert page.get_by_label('历史实验').input_value()=='old-completed'
        page.get_by_role('heading',name='两条独立情景分支',exact=True).wait_for()
        assert not errors,errors
        args.report.write_text(json.dumps({'status':'PASS','fixture_runs':203,'old_pending_canceled':True,'old_completed_retrieved':True,'history_pages':5,'selection_survived_page_change':True,'page_errors':errors},ensure_ascii=False,indent=2))
        page.screenshot(path=str(args.report.with_suffix('.png')),full_page=True)
        browser.close();print('Old live tasks, 5-page history and stable selection: PASS')
