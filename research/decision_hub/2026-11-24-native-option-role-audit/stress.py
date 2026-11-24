import json,runpy
from probe import propose
# Written after v2 was frozen; no further tuning. Same researcher, development challenge.
CASES=[
 ('reported','我朋友想比较留在原公司和接受新岗位',[]),
 ('reported','如果只是替同事比较续租旧房和搬去新房',[]),
 ('reported','昨天我还在考虑买新电脑还是继续用旧电脑',[]),
 ('reported','我已经不再考虑报名网课还是自学教材',[]),
 ('reported','这是假设：我想比较接受全职和选择兼职',[]),
 ('criteria','我想比较租房的便利性和买房的安全感',[]),
 ('criteria','我想比较买车和租车的成本',[]),
 ('criteria','我想比较学习的难度和工作的压力',[]),
 ('criteria','我想比较去办公室的频率和在家办公的效率',[]),
 ('ambiguous','我纠结买车还是价格',[]),
 ('action','我想比较打车和坐公交',['打车','坐公交']),
 ('action','我想比较开车和骑车',['开车','骑车']),
 ('action','我想比较找室友和自己住',['找室友','自己住']),
 ('action','我想比较读研还是直接就业',['读研','直接就业']),
 ('action','我想比较去外地工作还是留在本地',['去外地工作','留在本地']),
 ('action','我想比较接受工作A还是接受工作B',['接受工作A','接受工作B']),
]
def run(ns):
 rows=[]
 for role,text,expected in CASES:
  opts=ns['_options']([m[0].strip() for m in ns['_SENTENCES'].finditer(text) if m[0].strip()],'')
  typ,p=propose(text,opts,2)
  rows.append(dict(role=role,text=text,expected=expected,baseline=opts,candidateRole=typ,candidate=p))
 return dict(cases=len(rows),roleExact=sum(r['role']==r['candidateRole'] for r in rows),baselineFalse=sum(r['role']!='action' and bool(r['baseline']) for r in rows),candidateFalse=sum(r['role']!='action' and bool(r['candidate']) for r in rows),actionCases=sum(r['role']=='action' for r in rows),actionExact=sum(r['role']=='action' and r['expected']==r['candidate'] for r in rows),records=rows)
if __name__=='__main__':
 import sys
 print(json.dumps(run(runpy.run_path(sys.argv[1])),ensure_ascii=False,indent=2))
