"""Synthetic role classification probe. Native upstream option-extraction baseline."""
import json,re,sys,hashlib,runpy
from pathlib import Path

# Case families are development data, not independent tests.
FAMILIES = [
 ('career',('留在原公司','接受新岗位'),('工资','通勤时间')),
 ('housing',('续租旧房','搬去新房'),('房租','搬家成本')),
 ('learning',('报名网课','自学教材'),('学习时间','考试成绩')),
 ('transport',('坐地铁','骑自行车'),('通勤时间','交通费用')),
 ('consumption',('买新电脑','继续用旧电脑'),('价格','维修费')),
 ('schedule',('保持早班','换夜班'),('睡眠时间','每周工时')),
 ('family',('留在本地','搬去外地'),('陪伴时间','生活成本')),
 ('saving',('继续租房','买房'),('首付','月供')),
 ('work',('接受全职','选择兼职'),('收入','工作稳定性')),
 ('exercise',('报名健身课','在家锻炼'),('运动时间','受伤风险')),
 ('travel',('坐火车','乘飞机'),('票价','旅行时间')),
 ('study',('读研','继续工作'),('学习成本','就业概率')),
]
TEMPLATES = ['我想比较{}和{}','我在考虑{}还是{}','我在权衡{}与{}','我纠结{}还是{}']
EXTRA = [
 ('ambiguous','我想比较A和B',None),
 ('ambiguous','我在权衡甲与乙',None),
 ('ambiguous','我想比较线上和线下',None),
 ('ambiguous','我纠结稳定和自由',None),
 ('ambiguous','我想比较近一点和远一点',None),
 ('ambiguous','我想比较长期和短期',None),
 ('criteria','我该优先考虑工资还是通勤时间',None),
 ('criteria','我想比较搬家成本和学习时间',None),
 ('criteria','我想比较租房成本和买房成本',None),
 ('criteria','我想比较去公司的时间和在家工作的收入',None),
 ('reported','朋友在考虑留在原公司还是接受新岗位',None),
 ('reported','假设我比较留在原公司和接受新岗位',None),
 ('reported','之前我纠结续租旧房还是搬去新房',None),
 ('reported','我不想比较续租旧房和搬去新房',None),
 ('action','我想比较方案A和方案B',('方案A','方案B')),
 ('action','我在考虑远程还是到办公室',('远程','到办公室')),
 ('action','我纠结全职工作还是兼职工作',('全职工作','兼职工作')),
 ('action','我想比较步行和骑车',('步行','骑车')),
 ('action','我想比较咖啡店和图书馆',('咖啡店','图书馆')),
 ('action','我想比较保留现状和推迟决定',('保留现状','推迟决定')),
]
METRIC = re.compile(r'(?:工资|通勤时间|房租|成本|时间|成绩|费用|价格|维修费|工时|首付|月供|收入|稳定性|风险|票价|概率)$')
ACTION = re.compile(r'^(?:留在|留下|接受|续租|搬去|报名|自学|坐|骑|买|继续|保持|换|选择|在家|乘|读研|远程|到办公室|全职|兼职|步行|保留|推迟)')
LABEL = re.compile(r'^(?:方案|选项|岗位|工作|课程|房源|计划)[A-Za-z甲乙丙丁0-9]+$')
CONTEXT = re.compile(r'^(?:朋友|假设|之前|我不想比较)')

def fixtures():
    rows=[]
    for group,actions,metrics in FAMILIES:
        for i,t in enumerate(TEMPLATES):
            rows += [dict(group=group,role='action',text=t.format(*actions),expected=list(actions)),dict(group=group,role='criteria',text=t.format(*metrics),expected=[])]
    for i,(role,text,expected) in enumerate(EXTRA):
        rows.append(dict(group='extra',role=role,text=text,expected=list(expected or [])))
    return rows

def propose(text,options,revision=1):
    # Only a role gate over native options, not general language inference.
    if CONTEXT.search(text): return 'reported',[]
    if len(options)!=2: return 'ambiguous',[]
    if revision==2: options=[re.sub(r'^我纠结(?=.)','',x) for x in options]
    if all(METRIC.search(x) for x in options): return 'criteria',[]
    if all((ACTION.search(x) or LABEL.fullmatch(x)) and not METRIC.search(x) for x in options): return 'action',options
    return 'ambiguous',[]

def run(ns):
    records=[]
    for case in fixtures():
        text=case['text']; opts=ns['_options']([m[0].strip() for m in ns['_SENTENCES'].finditer(text) if m[0].strip()],'')
        role,p=propose(text,opts,1)
        role2,p2=propose(text,opts,2)
        records.append({**case,'baseline':opts,'candidateRole':role,'candidate':p,'revisedRole':role2,'revised':p2})
    def stats(key):
        return dict(action_cases=sum(x['role']=='action' for x in records),action_exact=sum(x['role']=='action' and x[key]==x['expected'] for x in records),false_action_cases=sum(x['role']!='action' and bool(x[key]) for x in records),wrong_action_cases=sum(x['role']=='action' and bool(x[key]) and x[key]!=x['expected'] for x in records),action_abstain=sum(x['role']=='action' and not x[key] for x in records))
    return dict(cases=len(records),groups=len(FAMILIES),baseline=stats('baseline'),candidate=stats('candidate'),revised=stats('revised'),role_exact=sum(x['role']==x['candidateRole'] for x in records),revised_role_exact=sum(x['role']==x['revisedRole'] for x in records),records=records)

if __name__=='__main__':
    ns=runpy.run_path(sys.argv[1]);print(json.dumps(run(ns),ensure_ascii=False,indent=2))
