# v0.7 语义候选略过后的同文重新提议及确认恢复审计
2026-11-25。SOURCE_FRAGMENT_REPRODUCED / SYNTHETIC_DEVELOPMENT / NATIVE_FULL_NOT_RUN / INDEPENDENT_NOT_RUN。起始main b8f25e0be9917f33c0d26b63e055c4dabcb762bc；固定Draft #62候选 e61bbad10932edabc9a87483e5407fdae6c751cc，仍待审。核对近期12提交、14开放PR、v3.2/同步规程/唯一产品交接前22行（交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07）。检索projection/confirmed semantics/quantity/obligation/conditional/repair/fingerprint/dismiss/deduplication/duplicate claim/occurrence identity/repeated input，审阅R1 a93cc28fab6dec01e3eec14aad85053a17814c10、R6 3db4324e40d29fae21afa3641cb38517c81d10be、R55 3383346cad3e2420c30e9c7f7f660875e34ca78e、R57 dd45037da2fe04dbb7687d110e75c2eda2eeb4ad合同前段。已有硬约束覆盖与语义修订研究，不重做币种/归属问题。本轮专门审查用户略过一条候选后再次提交相同声明的可恢复性；全库查重有限。
## 固定源码
platform/future_model/src/psychohistory/ 下：
decision_evidence.py b45932af6346fb0df072ffb6cb13ef0cd6991b7a，_duplicate_key lines84–89 FNV1a UTF16 ca0a4346，draft_claims lines242–259 e4fb3c60；
decision_semantics.py c7158c996f82c208b4d142b2863ddc3e27efa267，_covered_fingerprints lines123–137 64dcac0b，blocking_obligations lines149–176 56c04606；另逐字转录_repair_key和必要常量。
decision_conversation.py ed1c5aa8407f53ef3dfc1484ba1a18ef1edabcad，public_claims 113–129、_ingest 262–299、confirm 331–368、_project 395–425。实际源级审阅：dismiss只向row.dismissed添加ID，public_claims用DISMISSED覆盖状态，confirm只允许PROVISIONAL；_ingest对同一来源的候选使用固定source_identity current_user、channel user_self_report、version PARSER_VERSION，调用draft_claims时未传dismissed；_project调用blocking_obligations。另读decision_conversation_math.py de49b71a3c8bb63c81539dd9c69b3c02b3e94c23、decision_language.py 4e6733499f74db505e2cedaff84cf8c5eae207d1（未执行）。
## 机制及范围
draft_claims的known集合排除被supersede的条目，却不感知会话dismissed集合。若原候选仍在账本、未被替代、重复输入生成完全相同的duplicate key，重复输入不会增加可确认条目。旧条目public状态仍DISMISSED，原生confirm入口拒绝非PROVISIONAL。对需要确认的硬义务，原生blocking_obligations在没有合格指纹时保留待核对；拒绝用户误操作不应取消真实底线，也不能因无法恢复而默认通过。用户重述为不同source可能获得新的候选，或开启新会话；本轮没有测试这些路径，不宣称所有输入必然阻塞或不可恢复。发现属于精确输入条件下的接口可恢复性缺口，非真实用户事故或错误数学放行。
## 实际运行
容器Python标准库执行/tmp/ph_dismiss_probe.py。四个固定函数逐字转录，inspect.getsource去尾空白，FNV1a以ASCII片段UTF16码元计算，四个指纹与连接器一致；FNV仅用于转录比对，非原始文件完整Git blob验证。ClaimInput.model_validate/SourceMetadata/EvidenceLedger/EvidenceEntry/claim_id/time使用极简夹具，pub模拟单一不冲突组的状态覆盖，sem人工给出两个相同的硬义务与匹配候选；未调用真实interpret/完整Pydantic账本/confirm/ConversationHub/_project/API/CLI/App。原生confirm拒绝由源码审阅确认，未实际调用。9组由cost_max/hours_max/onsite_max及3种值构成；候选规则只在显式重新提议且相同载荷条目全已略过时生成新ID，普通重复仍走原draft_claims；新ID未确认前仍阻塞，确认后原blocking_obligations对两个相同指纹均视为覆盖（仅夹具已知同义务，不证明任意同文同义）。每组四个控制：新待确认条目存在时重复不增长、非显式重新提议不增长、未略过候选保持去重、原确认有效的重复义务保持覆盖。实测：
```json
{"cases":9,"native_no_new_proposal":9,"native_no_confirmable":9,"native_blocked":9,"candidate_new_proposal":9,"candidate_still_blocked_before_confirmation":9,"candidate_unblocked_after_confirmation":9,"controls":36}
```
## 可复算代码
下列等价复算方式从固定源码提取函数而非重新实现，使用本轮同样的有限夹具（本轮实际执行的是逐字转录版，以下提取版尚未单独运行）。将三份固定源码文件放到同一目录，运行Python3；不需导入产品依赖。
```python
from __future__ import annotations
from dataclasses import dataclass
from types import SimpleNamespace as NS
from typing import Iterable
import unicodedata,re,ast,json
from unicodedata import normalize
from pathlib import Path

def snippet(file,name,cls=None):
    src=Path(file).read_text()
    tree=ast.parse(src)
    nodes=tree.body if cls is None else next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name==cls).body
    n=next(n for n in nodes if isinstance(n,ast.FunctionDef) and n.name==name)
    return "\n".join(src.splitlines()[n.lineno-1:n.end_lineno])
def fnv(s):
    h=2166136261
    b=s.encode("utf-16-le")
    for i in range(0,len(b),2):
        h=((h^(b[i]+256*b[i+1]))*16777619)&0xffffffff
    return f"{h:08x}"
CONFIRMED={'USER_CONFIRMED','EXTERNALLY_VERIFIED'}
CLAIM_KEYS=('kind','field','subject','value','unit','source')
CNY=r'人民币|(?<![A-Za-z])(?:CNY|RMB)(?![A-Za-z])|[¥￥]|(?<![美韩港澳日欧台泰加新])元|块钱?'
MONTH=r'每个自然月|每个月|每月|按月|[\/／]\s*月|月租'
MAX_CLAIMS=100
ClaimOrigin=str
SourceMetadata=lambda: NS(**dict.fromkeys(('version','observed_at','population','scope','channel','source_identity','published_date','retrieved_at'),''))
def _normalized(value):
    return unicodedata.normalize('NFC',value or '').strip()
class ClaimInput:
    def __init__(self,item):
        self.__dict__.update(item)
    @classmethod
    def model_validate(cls,item):
        return cls(item)
@dataclass
class EvidenceEntry:
    claim_id:str
    claim:ClaimInput
    origin:str
    recorded_at:str
    supersedes:str|None=None
@dataclass
class EvidenceLedger:
    entries:tuple=()
def _claim_id(claim,position): return str(position)
def _now(): return 'fixture'
import textwrap
s=snippet('decision_evidence.py','_duplicate_key','ClaimInput')
assert fnv(s)=='ca0a4346'
exec(textwrap.dedent(s))
ClaimInput._duplicate_key=_duplicate_key
for f,n,h in [('decision_evidence.py','draft_claims','e4fb3c60'),('decision_semantics.py','_covered_fingerprints','64dcac0b'),('decision_semantics.py','blocking_obligations','56c04606')]:
    s=snippet(f,n)
    assert fnv(s)==h
    exec(s)
exec(snippet('decision_semantics.py','_repair_key'))
def raw(field,value,source,unit='yuan',role='constraint'):
    md=SourceMetadata();md.version='0.7.0';md.channel='user_self_report';md.source_identity='current_user'
    return dict(kind='fact',field=field,subject='',value=str(value),unit=unit,source=source,role=role,metadata=md)
def pub(ledger,dismissed,confirmed):
    return [dict(id=e.claim_id,**{k:(e.claim.role if k=='kind' else getattr(e.claim,k)) for k in CLAIM_KEYS},status='DISMISSED' if e.claim_id in dismissed else 'USER_CONFIRMED' if e.claim_id in confirmed else 'PROVISIONAL',supersedes=e.supersedes) for e in ledger.entries]
def sem(item):
    fp={k:(item['role'] if k=='kind' else item[k]) for k in CLAIM_KEYS}
    return {'obligations':[dict(hard=True,source=item['source'],repair=None,status='PROVISIONAL',matches=[fp],operator='<=',condition=None)]}
def repropose(ledger,item,dismissed,explicit):
    claim=ClaimInput.model_validate(item);key=claim._duplicate_key()
    same=[e for e in ledger.entries if e.claim._duplicate_key()==key]
    if not explicit or not same or any(e.claim_id not in dismissed for e in same):
        return draft_claims(ledger,[item])
    return EvidenceLedger((*ledger.entries,EvidenceEntry(_claim_id(claim,len(ledger.entries)+1),claim,'USER',_now())))
out={'cases':0,'native_no_new_proposal':0,'native_no_confirmable':0,'native_blocked':0,'candidate_new_proposal':0,'candidate_still_blocked_before_confirmation':0,'candidate_unblocked_after_confirmation':0,'controls':0}
for field,unit,template in [('cost_max','yuan','预算最多{}元'),('hours_max','hours/week','每周最多工作{}小时'),('onsite_max','days/week','每周最多到岗{}天')]:
    for value in [1,2,3]:
        item=raw(field,value,template.format(value),unit);initial=draft_claims(EvidenceLedger(),[item]);old=initial.entries[0].claim_id;d={old};turns=[sem(item),sem(item)]
        replay=draft_claims(initial,[item]);p=pub(replay,d,set())
        assert len(replay.entries)==1;out['native_no_new_proposal']+=1
        assert not any(x['status']=='PROVISIONAL' for x in p);out['native_no_confirmable']+=1
        assert len(blocking_obligations(turns,p,[]))==2;out['native_blocked']+=1
        new=repropose(initial,item,d,True);assert len(new.entries)==2;out['candidate_new_proposal']+=1
        assert len(blocking_obligations(turns,pub(new,d,set()),[]))==2;out['candidate_still_blocked_before_confirmation']+=1
        assert not blocking_obligations(turns,pub(new,d,{new.entries[-1].claim_id}),[]);out['candidate_unblocked_after_confirmation']+=1
        assert len(repropose(new,item,d,True).entries)==2;out['controls']+=1
        assert len(repropose(initial,item,d,False).entries)==1;out['controls']+=1
        assert len(repropose(initial,item,set(),True).entries)==1;out['controls']+=1
        assert not blocking_obligations(turns,pub(initial,set(),{old}),[]);out['controls']+=1
        out['cases']+=1
print(json.dumps(out,ensure_ascii=False))
```
## 下一版本候选接口
区分输入事件幂等、内容相同、同一语义义务、候选历史ID、重新提议ID和确认资格。显式恢复须绑定当前会话实例、原候选、原文出现ID、当前条件/主体/用途及修订；不可默默清除旧dismissed或把重复文字自动视为授权。新候选保持待确认、保留原历史，确认后只覆盖可信绑定的同一义务；若不同语境或目标应保持独立，不能仅凭相同文本复用旧确认。上面的研究原型未实现原生限额、修订链冲突、跨会话、认证、持久化、恶意输入或完整语义，不能直接上线。验收须使用原生start/turn/confirm/compute、准确原文回放、同文重提/不同义务/未确认/明确修订/重复请求/过期状态、全部历史回归与独立留出，避免再次用人工候选替代实际语言入口。现有v0.7开放语义限制保持；产品轨维护唯一交接。研究者自行选择三个字段、有限夹具及显式重提策略；未新增真实数据、训练、源码修改、CI、PR合并、部署、费用或冻结变更。
