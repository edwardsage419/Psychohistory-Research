"""Real loopback browser acceptance. Token stays in memory; never written to report."""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

url=os.environ.get('PH_TEST_URL','http://127.0.0.1:8765')
token=Path(os.environ.get('PH_TEST_DATA','/tmp/psychohistory-web-check'),'token').read_text().strip()
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
    page=browser.new_page(viewport={'width':1440,'height':1000})
    errors=[]
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.goto(url)
    page.get_by_label('本地访问令牌').fill(token,timeout=3000)
    page.get_by_role('button',name='连接工作空间',exact=True).click()
    page.get_by_text('工作空间已连接',exact=True).wait_for()
    page.get_by_role('button',name='实验工作台',exact=True).click()
    page.get_by_label('随机种子').fill('123')
    page.get_by_label('模拟轮次').fill('6')
    page.get_by_label('合成人口').fill('16')
    page.get_by_role('button',name='提交合成实验',exact=True).click()
    page.get_by_role('button',name='批准合成执行',exact=True).first.click()
    page.get_by_text('COMPLETED',exact=True).first.wait_for(timeout=15000)
    page.get_by_role('heading',name='两条独立情景分支',exact=True).wait_for()
    assert page.get_by_text('不代表真实因果效应',exact=False).count()>0
    assert page.get_by_text('individual@1.0.0',exact=False).count()>0
    page.get_by_role('button',name='审批与证据',exact=True).click()
    page.get_by_role('button',name='只读登记来源',exact=True).click()
    page.get_by_text('R_SERIES_ORIGINAL',exact=False).first.wait_for()
    page.get_by_role('button',name='模型注册',exact=True).click()
    page.get_by_role('heading',name='individual',exact=True).wait_for()
    page.get_by_role('button',name='情景历史',exact=True).click()
    page.get_by_role('heading',name='两条独立情景分支',exact=True).wait_for()
    output=Path(os.environ.get('PH_BROWSER_REPORT','/tmp/psychohistory-browser.json'))
    page.screenshot(path=str(output.with_suffix('.png')),full_page=True)
    assert not errors,errors
    output.write_text(json.dumps({'status':'PASS','flow':['connect','submit','approve','completed','branches','versions','evidence-discovery','models','history'],'browser_errors':errors},ensure_ascii=False,indent=2))
    print('Browser functional flow: PASS (9 steps, no page errors)')
    browser.close()
