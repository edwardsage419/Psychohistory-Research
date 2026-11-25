# 第56轮：否定比较符的方向反转与硬约束保留
2026-11-25。固定main 3383346cad3e2420c30e9c7f7f660875e34ca78e，PR #61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e open Draft。已核对v3.1、AGENTS、同步规程、近期提交、开放PR、唯一产品交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07、第35/55轮。沿用第55轮本机原生片段并实际重验五个FNV指纹：decision_language.py blob fff9d6c8e20c6a57c4ae9756bf5d6fe0e81f61b4 lines38-78 e7d32c19、108-178 c3cb5d3f、302-313 ee37bc70、321-403 58a938a5；decision_feasibility.py blob 6181d6c578c7ef251e9708d0ffcf65e95d35f88f lines7-30 a7463ac5。读取最新PR decision_conversation_math.py blob aca1b4aa5cf4b4fd5b476e078b6e2aa9af197d30，BOUNDS、evidence_number及build_state中strict_constraint映射。当前Python3.13.5非项目支持环境。真实执行_numeric_claims与check_constraint，人工适配subject/context/focus、源、单位与时域；BOUNDS及strict映射是源码审阅后的手工等价投影，未执行build_state、完整interpret/ledger/confirm/hub/API/UI/Qwen。复用片段，不重新验证完整Git原始字节；第55轮环境限制仍未解除。与A55-01/02币种周期、第35轮条件义务不同，聚焦否定比较方向。
## 发现
A56-01：_UPPER_STRICT和_LOWER_STRICT使用仅排除紧前字符“不”的否定向后检查；“不能少于”“不得少于”“不可以少于”等多字符否定未被充分覆盖。对现有上限字段可能误标严格上限，而原句要求下限；反向收入上限亦可能误标严格下限。“预算不少于3000元”还因budget标记产生非严格上限。原句作为明确硬约束的人工标注测试意图是下限；真实预算可有其他语义，仍需用户确认对象与用途。BOUNDS仅允许cost_max/hours_max/onsite_max与income_min等固定方向，strict_constraint只收紧相应方向，不可表达任意反向约束。缺失声明并非证明完整会话一定丢失底线。
## 修正候选
有限完整匹配语法：4指标×5否定前缀×7比较词×固定整数及单位，先识别完整否定运算，推导“不少于/不低于/不小于”为>=，“不多于/不高于/不大于/不超过”为<=；若方向与当前对话字段相符，生成待确认候选，否则显式保留UNSUPPORTED_DIRECTION、原始语句、阈值、方向、单位和阻止完整建议的义务，不能自动舍弃或用相反比较替代。真实系统应利用通用Constraint.operator四方向输入，并让可信宿主完成角色及来源确认；此处不实施生产改造。OUT_OF_GRAMMAR必须保留为待解析，不授权直接回退或放行；如条件、否定、范围、比较主体或时态不明确，仍需验证。非通用语言解析、非独立留出、无真人。
## 实际结果
140条专项语句：25条原生正确，71条未生成硬约束，44条反向，0条仅严格性不符。原生有可投影硬约束69条×3点=207次人工桥接原生筛查，44次错误放行、87次错误拒绝。每次测试使用阈值-1、阈值、阈值+1三个测量点；无声明的71条未擅自模拟为无底线。候选75条生成待确认声明、65条保留不支持方向；75×3=225次原生gate检查，与人工真值全一致。44条反向原声明全部被候选隔离。14项对照：8条原有支持语法正确且在候选语法之外、6条外币/多条件/非法量值/不明条件/估计句未被候选错误接收。原生例：“每周工时不能少于40小时”=>hours_max strict_constraint；“每月工资不能多于3000元”=>income_min strict_constraint。人工门见证：预算不少于3000元，测量2999，原生按<=给CERTAIN_PASS，预期>=为CERTAIN_FAIL；预算不能少于3000元，测量3000，原生按<给CERTAIN_FAIL，预期>=为CERTAIN_PASS。计数是开发模板非真实发生率，不可当用户总体准确率。本机实际脚本SHA256 9f2798ada20b86317b176549ee3efacee379e80815dfc1c3dda0fa0f485b6388，结果JSON SHA256 0366288e855df178c10e4774a7d0ade88f2b4640a04f7d6abd9ba01302593202。本机脚本复用第55轮probe.py，下面给出等价独立提取复算器（完整仓库路径运行仍待执行）。无实际生产修改，保留原始PR。
## 复算
```python
import sys,re,json,operator,unicodedata,hashlib
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace as NS
def fnv(s):
    h=2166136261
    b=s.encode('utf-16-le')
    for i in range(0,len(b),2):
        h=((h^(b[i]+256*b[i+1]))*16777619)&0xffffffff
    return f'{h:08x}'
def load(name,blob,ranges):
    b=(Path(sys.argv[1])/name).read_bytes()
    if hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()!=blob:raise RuntimeError('source identity')
    ls=b.decode('utf-8').splitlines()
    for a,z,h in ranges:
        s='\n'.join(ls[a-1:z]).rstrip()
        if fnv(s)!=h:raise RuntimeError('fragment identity')
        exec(compile(s,name,'exec'),globals())
load('decision_language.py','fff9d6c8e20c6a57c4ae9756bf5d6fe0e81f61b4',[(38,78,'e7d32c19'),(108,178,'c3cb5d3f'),(302,313,'ee37bc70'),(321,403,'58a938a5')])
load('decision_feasibility.py','6181d6c578c7ef251e9708d0ffcf65e95d35f88f',[(7,30,'a7463ac5')])
METRICS={'预算':('cost_max','yuan','元',3000,'<='),'每周工时':('hours_max','hours/week','小时',40,'<='),'每周到岗':('onsite_max','days/week','天',3,'<='),'每月工资':('income_min','yuan/month','元',3000,'>=')}
NEG=['不','不能','不得','不可','不可以']
REL={'少于':'>=','低于':'>=','小于':'>=','多于':'<=','高于':'<=','大于':'<=','超过':'<='}
def candidate(s):
    m=re.fullmatch(r'(预算|每周工时|每周到岗|每月工资)(不可以|不能|不得|不可|不)(少于|低于|小于|多于|高于|大于|超过)([0-9]+)(元|小时|天)',s)
    if not m:return {'status':'OUT_OF_GRAMMAR','source':s,'claim':None,'operator':None}
    metric,neg,rel,n,suffix=m.groups();field,unit,expected,_,direction=METRICS[metric];op=REL[rel]
    if suffix!=expected or int(n)>100000000000 or (field=='onsite_max' and int(n)>7):return {'status':'VERIFY_VALUE','source':s,'claim':None,'operator':op}
    if op!=direction:return {'status':'UNSUPPORTED_DIRECTION','source':s,'claim':None,'operator':op,'threshold':n,'unit':unit,'blocking_obligation':True}
    return {'status':'PROVISIONAL','source':s,'claim':{'field':field,'kind':'constraint','subject':'','value':n,'unit':unit,'source':s},'operator':op}
def gate(op,n,x):
    c=NS(source='synthetic limit',unit='u',horizon='fixture',operator=op,threshold=Decimal(n))
    v=NS(source='synthetic measurement',unit='u',horizon='fixture',kind='fact',lower=Decimal(x),upper=Decimal(x))
    return check_constraint(c,v,'fixture')[0]
def old_op(claim,metric):
    if not claim:return None
    if len(claim)!=1 or claim[0]['field']!=METRICS[metric][0] or claim[0]['kind'] not in ('constraint','strict_constraint'):return None
    op=METRICS[metric][-1]
    return op[0] if claim[0]['kind']=='strict_constraint' else op
stats={'cases':0,'correct_old':0,'no_constraint_old':0,'reversed_old':0,'strictness_old':0,'candidate_provisional':0,'candidate_unsupported':0,'old_gate_checks':0,'old_false_pass':0,'old_false_fail':0,'candidate_gate_checks':0,'candidate_gate_mismatch':0,'candidate_blocked_wrong_old':0,'controls':0}
for metric,(field,unit,suffix,n,direction) in METRICS.items():
 for neg in NEG:
  for rel,expected in REL.items():
   s=f'{metric}{neg}{rel}{n}{suffix}';old=_numeric_claims(s,'',s,'','');o=old_op(old,metric);new=candidate(s);stats['cases']+=1
   bucket='correct_old' if o==expected else 'no_constraint_old' if o is None else 'reversed_old' if o[0]!=expected[0] else 'strictness_old';stats[bucket]+=1
   assert new['operator']==expected
   if expected==direction:
    assert new['status']=='PROVISIONAL' and new['claim']['value']==str(n);stats['candidate_provisional']+=1
   else:
    assert new['status']=='UNSUPPORTED_DIRECTION' and new['blocking_obligation'] and new['claim'] is None;stats['candidate_unsupported']+=1
    if o is not None:stats['candidate_blocked_wrong_old']+=1
   for x in [n-1,n,n+1]:
    truth='CERTAIN_PASS' if (x>=n if expected=='>=' else x<=n) else 'CERTAIN_FAIL'
    if o is not None:
     got=gate(o,n,x);stats['old_gate_checks']+=1
     if got!=truth:stats['old_false_pass' if got=='CERTAIN_PASS' else 'old_false_fail']+=1
    if new['claim']:
     got=gate(new['operator'],n,x);stats['candidate_gate_checks']+=1
     if got!=truth:stats['candidate_gate_mismatch']+=1
for metric,(_,_,suffix,n,direction) in METRICS.items():
 for phrase,expected in ([('最多','<='),('少于','<')] if direction=='<=' else [('至少','>='),('超过','>')]):
  s=f'{metric}{phrase}{n}{suffix}';assert old_op(_numeric_claims(s,'',s,'',''),metric)==expected;assert candidate(s)['status']=='OUT_OF_GRAMMAR';stats['controls']+=1
for s in ['预算不能少于3000韩元','预算不能少于3000元或必须超过5000元','每周到岗不能少于8天','每周工时不能少于40元','如果预算不能少于3000元','预算大约不能少于3000元']:
 assert candidate(s)['status'] in ('OUT_OF_GRAMMAR','VERIFY_VALUE');stats['controls']+=1
assert stats['cases']==sum(stats[k] for k in ['correct_old','no_constraint_old','reversed_old','strictness_old'])
assert stats['candidate_gate_mismatch']==0
print(json.dumps(stats,ensure_ascii=False,indent=2))
```
实际统计：{"cases":140,"correct_old":25,"no_constraint_old":71,"reversed_old":44,"strictness_old":0,"candidate_provisional":75,"candidate_unsupported":65,"old_gate_checks":207,"old_false_pass":44,"old_false_fail":87,"candidate_gate_checks":225,"candidate_gate_mismatch":0,"candidate_blocked_wrong_old":44,"controls":14}。
## 接入与后续
B02/B05/B06/B07/B11增量；与A55币种周期共享输入义务账本，优先在受支持环境完整验证自然语言=>证据=>确认=>通用Constraint.operator=>原生数学=>建议，以及未知义务和跨轮修订。不能把局部正则通过当生产修复。现有正式范围保持12项完整，不拆零碎Codex任务。没有真实Qwen/设备/完整测试/独立验收，无新增费用、CI、Codex、训练、合并、部署或冻结协议修改。
