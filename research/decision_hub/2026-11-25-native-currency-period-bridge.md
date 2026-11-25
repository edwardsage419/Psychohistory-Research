# 第55轮：真实语言解析与硬约束计算的币种、费用周期连接审查
2026-11-25。固定main 7ab23d84e837b9fdb05dee09335057a31f5f3709，PR #61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e open Draft。核对v3.1、AGENTS、同步规程、近期提交、开放PR、唯一交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07、第6/30/35/53/54轮。上一轮共享参数强调正确单位及时间语义，本轮实际执行原生语言片段和硬约束函数，非新合成数学枚举。container git ls-remote DNS失败；Python 3.13.5/Pydantic 2.13.5，项目此前锁定Python>=3.12,<3.13及Pydantic2.13.4，未能执行完整应用。无Qwen、真实设备或独立验收。
## 固定源码及实际复现
PR源码 decision_language.py blob fff9d6c8e20c6a57c4ae9756bf5d6fe0e81f61b4，原生片段 lines38-78、108-178、302-313、321-403，分别FNV1a UTF16去尾空白 e7d32c19、c3cb5d3f、ee37bc70、58a938a5。decision_feasibility.py blob 6181d6c578c7ef251e9708d0ffcf65e95d35f88f，lines7-30 a7463ac5。实际将5段逐字复制入本机probe.py，核对全部FNV一致；不是整个文件的原始字节哈希。原生函数体未修改；使用re/unicodedata/operator/Decimal及SimpleNamespace夹具。decision_conversation.py f505aeab2d9e5e0a9c8957ce6e039dea174918a7 _project/_compute真实流程另读，未执行build_state、完整interpret、ledger、Pydantic、对话确认、hub或前端。subject、context、focus由夹具给定；原生_numeric_claims直接接收原文子句，非完整白话问题的端到端语义准确率。原生check_constraint收到人工适配的字段；模拟双方来源有效、已核对、共同horizon，未证明真实完整流程可达。
## 缺陷
A55-01：_NON_CNY未列韩元等若干显式币种；已有USD、EUR等使用双侧单词边界，数字紧邻英文代码时也可绕过。_numeric_claims金额后缀可为空，仍将金额标成yuan或yuan/month。实际“预算最多3000韩元”“预算最多3000 KRW”“每月工资300万韩元”原生均生成错误币种声明。A55-02：每天、每日、按天、每小时、按小时、按季等费用周期不完整地排除；原生“每天费用200元”输出yuan而非有明确日周期的量。仅为已复现子句级解析错误，不能推断全系统实际用户事故或用户已确认错误声明。另一些输入被原生拒绝生成声明；不声称完整对话一定静默遗漏。
四项人工适配桥接原生硬约束见证：
|原始底线|原始测量|错误口径传入原生筛查|候选拦截|
|---|---|---|---|
|预算最多3000韩元|费用2000人民币|CERTAIN_PASS|BLOCKED_BY_ADAPTER|
|预算最多3000人民币|费用4000韩元|CERTAIN_FAIL|BLOCKED_BY_ADAPTER|
|预算最多3000人民币|每天费用200元|CERTAIN_PASS|BLOCKED_BY_ADAPTER|
|每天预算最多3000元|费用4000人民币|CERTAIN_FAIL|BLOCKED_BY_ADAPTER|
正确合同：无合格汇率、单位或时间覆盖依据时INCOMPARABLE/UNKNOWN；不能给出可行与否的现实判断。未计算任何现实汇率，不使用个人数据。原生硬约束本身按其收到的标签正确工作，错误来自上游语义。
## 修正候选与实际结果
非CNY或不支持周期的明确标记保留原始来源、VERIFY_CURRENCY/VERIFY_PERIOD和阻止完整建议义务，不静默删掉底线，也不擅自换算。对原生未解析的候选保留UNPARSED。本候选仅用于具有已识别金额线索的单子句实验，不能直接用于全部语言，不支持任意币种或混合条件、上下文继承/否定、任意币种符号、真正单位转换、周期聚合、真实权限或完整账本。保守拦截所有已识别金额异常可能导致额外澄清；生产应细化至相关义务及局部结果，另测缺省币种、含糊“元”、明确外币对外币同币种比较、跨期和多币种，不将正则列表当完整解决方案。
实际首次候选测试失败：货币代码使用双侧\b，紧贴数字时不匹配；改为两侧仅排除ASCII字母，并包含既有英文代码列表，原生源段未改。最终72个外币模板（18种币种词/符号/代码×4）、24个不支持周期模板（12周期×2），原生误标60+12=72，未生成声明12+12=24；候选96/96保留待核对，10/10正常人民币总量/月度及工时到岗控制保持原声明，4/4人工适配错误筛查见证候选阻止。不是独立留出、不是准确率或真实产品错误率。无CI或完整回归。实际本机probe.py SHA256 49ebfd9c83b17bf4d62cfe88d1e43cf9e2038726ecd19578dbd42cb472237a9d；完整results.json SHA256 f56c4993319598beccb14307fb48d6fe9e992485db739f83aa792fbe07404dba。本机文件未直接上传；下方提供等价可复跑源码抽取和测试，源代码不重复归档。下方复跑器未在完整仓库运行；实际本机使用已验证逐字片段。
## 复跑器
从固定PR提交工作树运行 python probe.py /path/to/repo/platform/future_model/src/psychohistory，普通非优化模式。校验两个完整原始Git blob及5段FNV，抽取原生函数；不执行完整应用。
```python
import re, unicodedata, operator, json, hashlib, sys
from decimal import Decimal
from types import SimpleNamespace as NS
from pathlib import Path

def fnv(s):
    h=2166136261
    b=s.encode('utf-16-le')
    for i in range(0,len(b),2):
        h=((h^(b[i]+256*b[i+1]))*16777619)&0xffffffff
    return f'{h:08x}'

def load(name,blob,ranges):
    b=(Path(sys.argv[1])/name).read_bytes()
    if hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()!=blob:
        raise RuntimeError('wrong source blob')
    ls=b.decode('utf-8').splitlines()
    for start,end,expected in ranges:
        s='\n'.join(ls[start-1:end]).rstrip()
        if fnv(s)!=expected: raise RuntimeError('wrong fragment')
        exec(compile(s,name,'exec'),globals())

load('decision_language.py','fff9d6c8e20c6a57c4ae9756bf5d6fe0e81f61b4',[(38,78,'e7d32c19'),(108,178,'c3cb5d3f'),(302,313,'ee37bc70'),(321,403,'58a938a5')])
load('decision_feasibility.py','6181d6c578c7ef251e9708d0ffcf65e95d35f88f',[(7,30,'a7463ac5')])

_FOREIGN_EXTRA = r'韩元|韩币|韓元|韓幣|韩圆|卢比|盧比|泰铢|泰銖|瑞士法郎|越南盾|印尼盾|马来西亚林吉特|(?<![A-Za-z])(?:KRW|INR|THB|CHF|VND|IDR|MYR|USD|AUD|HKD|SGD|CAD|EUR|GBP|JPY|TWD)(?![A-Za-z])|[₩₹฿]'
_UNSUPPORTED_PERIOD = r'每天|每日|按天|每小时|按小时|每周|每星期|每年|每季|每季度|按年|按季|[/／]\s*(?:天|日|小时|周|星期|年|季)'

def safe_numeric(clause, subject, source, context='', focus=''):
    is_money=bool(re.search(_COST,clause) or re.search(_INCOME,clause) or focus in {'income','income_min','cost','cost_max'})
    if is_money and re.search(rf'{_NON_CNY}|{_FOREIGN_EXTRA}',clause,re.I):
        return {'status':'VERIFY_CURRENCY','claims':[],'source':source,'block_full_recommendation':True}
    if is_money and re.search(_UNSUPPORTED_PERIOD,clause):
        return {'status':'VERIFY_PERIOD','claims':[],'source':source,'block_full_recommendation':True}
    claims=_numeric_claims(clause,subject,source,context,focus)
    return {'status':'PROVISIONAL' if claims else 'UNPARSED','claims':claims,'source':source,'block_full_recommendation':not bool(claims)}

def fixture_gate(limit,measurement):
    if not limit or not measurement:return 'BLOCKED_BY_ADAPTER'
    c=NS(source=limit['source'],unit=limit['unit'],horizon='fixture',operator='<=',threshold=Decimal(limit['value']))
    v=NS(source=measurement['source'],unit=measurement['unit'],horizon='fixture',kind='fact',lower=Decimal(measurement['value']),upper=Decimal(measurement['value']))
    return check_constraint(c,v,'fixture')[0]

stats={'currency_cases':0,'currency_mislabeled':0,'currency_blocked_original':0,'period_cases':0,'period_mislabeled':0,'period_blocked_original':0,'candidate_blocked':0,'supported_controls':0,'gate_witnesses':[]}
for currency in ['韩元','韩币','KRW','₩','卢比','INR','泰铢','THB','瑞士法郎','CHF','越南盾','VND','美元','USD','日元','JPY','欧元','EUR']:
    for fmt,sub in [('预算最多3000{}',''),('费用2000{}','A'),('每月工资3000{}','A'),('每月预算最多3000{}','')]:
        s=fmt.format(currency); old=_numeric_claims(s,sub,s,'',''); new=safe_numeric(s,sub,s)
        assert new['status']=='VERIFY_CURRENCY' and new['block_full_recommendation'] and not new['claims']
        stats['currency_cases']+=1;stats['candidate_blocked']+=1
        stats['currency_mislabeled']+=bool(old);stats['currency_blocked_original']+=not bool(old)
for period in ['每天','每日','按天','每小时','按小时','每周','每星期','每年','每季','每季度','按年','按季']:
    for fmt,sub in [('{}费用200元','A'),('{}预算最多3000元','')]:
        s=fmt.format(period);old=_numeric_claims(s,sub,s,'','');new=safe_numeric(s,sub,s)
        assert new['status']=='VERIFY_PERIOD' and new['block_full_recommendation'] and not new['claims']
        stats['period_cases']+=1;stats['candidate_blocked']+=1
        stats['period_mislabeled']+=bool(old);stats['period_blocked_original']+=not bool(old)
for s,sub in [('预算最多3000元',''),('预算最多3000人民币',''),('每月预算最多3000元',''),('费用2000人民币','A'),('每月费用2000元','A'),('每月工资3000元','A'),('每周到岗2天','A'),('每周工时40小时','A'),('每周最多到岗3天',''),('每周工时最多45小时','')]:
    old=_numeric_claims(s,sub,s,'','');new=safe_numeric(s,sub,s)
    assert old and new['status']=='PROVISIONAL' and new['claims']==old
    stats['supported_controls']+=1
for lim,meas,expected in [('预算最多3000韩元','费用2000人民币','CERTAIN_PASS'),('预算最多3000人民币','费用4000韩元','CERTAIN_FAIL'),('预算最多3000人民币','每天费用200元','CERTAIN_PASS'),('每天预算最多3000元','费用4000人民币','CERTAIN_FAIL')]:
    a=_numeric_claims(lim,'',lim,'','');b=_numeric_claims(meas,'A',meas,'','')
    old=fixture_gate(a[0],b[0]);assert old==expected
    x=safe_numeric(lim,'',lim);y=safe_numeric(meas,'A',meas)
    new=fixture_gate((x['claims'] or [None])[0],(y['claims'] or [None])[0]);assert new=='BLOCKED_BY_ADAPTER'
    stats['gate_witnesses'].append({'limit':lim,'measurement':meas,'old':old,'candidate':new,'correct_contract':'INCOMPARABLE_WITHOUT_QUALIFIED_CONVERSION_OR_HORIZON'})
print(json.dumps(stats,ensure_ascii=False,indent=2))
```
## 后续
B02/B05/B06/B07/B08/B11优先修复候选。应在正式支持环境执行完整interpret、原文义务提取、ledger确认、build_state、hub、API与UI，验证明确外币及周期即使不产生数值声明仍保留必要待核对义务；不能只扩充_NON_CNY正则而忽略无声明情况下的覆盖。用户可确认币种和周期、按实际范围比较，不强制手填全部参数。当前未修改PR生产源码：安全修复涉及未支持语义的账本与投影，不能将局部wrapper当完整修复；本轮已交付可复算候选与明确反例，实际生产修复和回归待授权完整任务或有足够运行证据的定向修复。未启动Codex、CI、训练、合并、部署、冻结协议变更或新增费用。
