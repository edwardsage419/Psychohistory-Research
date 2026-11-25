# v0.7 语义确认、修订、参数投影及结果当前性批量接口审计
2026-11-25。SOURCE_FRAGMENT_REPRODUCED / SYNTHETIC_INTERFACE_STRESS / NATIVE_FULL_NOT_RUN / INDEPENDENT_NOT_RUN。起始main 7977339db6133957bb4ff7140a1ca9fad2353b79；固定Draft #62 head e61bbad10932edabc9a87483e5407fdae6c751cc，尚未合并。核对15近期提交、14开放PR、v3.2及同步规程前22行、唯一产品交接前22行blob 5e74f4f0b37141d631740e844ad8bbbfed232e07；检索revision/supersede/constraint projection/scope/dismiss/receipt/resource date/stale resource/correction role/semantic revision/estimate/evidence conflict。已有R1投影覆盖、R57主体、R64修订身份、R107发布事务、前轮略过重提审计，不能重复计入新成果。此次新增四个边界的源函数复算及统一合同；查重为关键词/已有研究范围，非全库证明。容器git ls-remote直接连接GitHub DNS失败，不能恢复完整仓库。Python3.13.5/Pydantic2.13.5（非正式项目支持环境）；实际代码仅标准库、未导入Pydantic。无产品源码修改。
## 固定源码及转录校验
platform/future_model/src/psychohistory/ 下，固定上述候选：
- decision_evidence.py b45932af6346fb0df072ffb6cb13ef0cd6991b7a：_validate_correction 137–148 af3132b2；_group 220–239 eae6382b；_key/_comparison_scope/_supported另转录（未单独指纹）。
- decision_semantics.py c7158c996f82c208b4d142b2863ddc3e27efa267：occurrence 109–120 fc5cf5fe；fingerprint 105–106 fcf4a607；沿用前轮_covered_fingerprints 123–137 64dcac0b、blocking_obligations 149–176 56c04606。
- decision_conversation.py ed1c5aa8407f53ef3dfc1484ba1a18ef1edabcad：active_claims 132–135 0435aa15；_check_resource_date 476–478 e26f59f5；_view 571–591 b6503f7c；源读turn 301–329、confirm 331–368、_project/_compute 395–443、update_resources及reuse 445–474、select/plan/save 480–528、_read/_update 216–236。
- decision_conversation_math.py de49b71a3c8bb63c81539dd9c69b3c02b3e94c23：sourced_key 66–67 3f7ab4ef；_active_evidence 99–107 f0480b1b；源读build_state测量分支、估计排除、硬约束跳过及_ operator。
- decision_feasibility.py 6181d6c578c7ef251e9708d0ffcf65e95d35f88f：check_constraint 11–28 d454863e。
- decision_language.py 4e6733499f74db505e2cedaff84cf8c5eae207d1：源读_qualify/_numeric_claims lines323–421；decision_scenarios.py 0a18c9c203ec9d4c8e712b4ad1c82c8336da4399，读完整函数，未执行。
实际在/tmp/ph_batch_semantic.py运行10个新增固定函数（FNV1a UTF16去尾空白指纹一致），另外执行前轮/tmp/ph_dismiss_probe.py并复核4个指纹。FNV不是密码学身份或完整文件Git字节哈希。两个实际文件SHA256分别3377981d804d7e3d764a477737f97326553791658a4a364d2ca530d6acb76e03、6db05c9c576bbd5ea4a2b6155de327ad124dc89a396f879a5866b601f77c9327。实际函数以人工最小夹具运行，除列出的真实片段以外未执行完整ledger、interpret、build_state、ConversationHub、API、App及独立留出。前轮函数重跑不计作新案例。
## A 同文出现身份与独立作用域
occurrence的ID只包括字符起止、字段、原文，不含轮次或确认过的作用域；blocking_obligations用全局内容指纹。三类硬底线×三个值×两个位置=18组：在两轮以完全同指纹的人工候选分别构造两个义务，18/18 ID相同，确认一个内容后18/18两个均视为覆盖。若可信宿主声明是不同义务（人工scope1/scope2），该覆盖不足。现实相同文本可能确为同义重述，不能一律要求重复确认；当两个独立义务经可信身份绑定时须分别确认，当有资格证明同一义务时才复用确认。候选18/18隔离不同作用域，54控制含同义复用、无确认阻塞和位置变化。未证明真实解析器会在不同语境生成该冲突指纹，亦未证明实际错误计算。
## B 修订与硬底线角色转换
_validate_correction检查同字段主体及来源等条件，并未比较语义角色；_group把有来源的estimate也列为supported，_covered_fingerprints沿有效后继覆盖被替代原指纹。人工构造同一字段底线被估计值替代且无新增硬义务的九组账本条目：9/9 validator接受，9/9组CONFIRMED且旧指纹被覆盖，9/9 active_claims留下estimate；按build_state原有跳过estimate/previous的分支，相关硬参数将不被该分支生成。此最后一步为源分支推论，未实际执行build_state，原文解析和阻塞检查可能阻止该路径；不声称现有完整入口必然可达或实际放行。显式用户撤回真实硬底线可能合法；研究候选要求普通数值修订保留硬义务身份，降级/撤回单独说明并确认，不能把内容覆盖误当约束仍被满足。九个正常硬修订控制、18个异主体/异来源拒绝控制、27个原生C028点值边界控制通过；候选降级识别9/9，尚未实现实际确认门或合法撤回流程。
## C 资源时点展示与操作资格
_view在给定row.analysis非空时返回ANALYZED与原analysis，不自行检查资源时点；select/plan/save显式调用_check_resource_date。以实际UTC日期两天前/一天前/一天后/两天后构造过期或非当前资源及既有分析行，实际_view（summary、receipt等最小替身）4/4仍显示ANALYZED，真实日期门4/4拒绝；候选展示前复核日期4/4清空当前分析，当前日期与无资源两控制通过。现有操作入口具日期防护；没有测试可从公开入口获得该过期row或客户端缓存跨午夜实际行为，不能把片段差异称为已确认产品漏洞。建议展示历史结果时明确其时点，旧结果不标当前，续算与选择入口使用同一可信时钟及有效快照；跨端缓存、时区、日期切换与授权撤回另测。测试日期为容器UTC运行日，与项目研究记录日期不同不改变相对日夹具。
## D 同值事实与估计的参数选择顺序
_group对同字段主体、同口径、同值的测量和估计返回CONFIRMED；_active_evidence对非硬阈值测量后者覆盖前者；build_state对于硬门测量跳过estimate。三字段（cost/hours/onsite）×三值×两顺序=18组：9组选中测量，9组选择估计。将所选分支按原build_state的估计排除规则手动投影，实际C028分别返回CERTAIN_PASS/UNKNOWN。非完整build_state执行。候选仅在独立可信宿主已确认同对象、指标、口径、时间、来源资格且真实观测有效时，保留有效事实不受同值估计输入次序影响，18/18保持结果；不同值9/9冲突、不同scope9/9不可比控制通过。没有真实测量证据时不能用USER_CONFIRMED替代独立事实资格；不同时间或对象不可合并。不得因为候选减少误拒而放宽硬门。
## 实测汇总
49个新增主案例，128个附加控制（A54、B54、C2、D18），10个新增源函数指纹一致。另复用前轮4个指纹及9主案例、36控制，不重复计数。A/B/C/D候选是合同/最小实现，未在正式原生流程修复。统计重复夹具非独立用户或真实产品错误率。四组具体计数：
```json
{"A":{"cases":18,"id_alias":18,"native_covered_both":18,"scoped_candidate_blocks":18,"controls":54},"B":{"cases":9,"role_change_validator_accepts":9,"old_coverage_via_successor":9,"no_current_hard_parameter":9,"candidate_rejects_without_retraction":9,"hard_revision_controls":9,"source_subject_controls":18,"native_math_controls":27},"C":{"cases":4,"stale_view_analyzed":4,"stale_action_guard_rejects":4,"candidate_suppresses":4,"current_view_controls":1,"no_resource_controls":1},"D":{"cases":18,"native_point_available":9,"native_point_suppressed":9,"candidate_same_scope_stable":18,"conflict_controls":9,"scope_controls":9}}
```
## 固定代码复算入口（从原文件提取；等价入口尚未单独运行）
实际逐字转录执行；为降低重复归档，下面给出固定源码提取和最小夹具复算版本，须保留上述Git blob。与前轮报告7977339db6133957bb4ff7140a1ca9fad2353b79的提取方法相同。以下A/B/D重现核心条件，C提取类方法后按上述row字段夹具运行；完整逐字转录脚本另保留当前会话可下载副本。不要执行任意网络文本或将夹具当原生API。
```python
# Python3 standard library; run in directory with pinned source files.
from pathlib import Path
import ast, textwrap, unicodedata, re, operator
from hashlib import sha256
from types import SimpleNamespace as NS
from unicodedata import normalize
from datetime import datetime, UTC, timedelta
def snippet(p,n,cls=None):
    s=Path(p).read_text(); t=ast.parse(s)
    ns=t.body if cls is None else next(x for x in t.body if isinstance(x,ast.ClassDef) and x.name==cls).body
    x=next(x for x in ns if isinstance(x,ast.FunctionDef) and x.name==n)
    return "\n".join(s.splitlines()[x.lineno-1:x.end_lineno])
def fnv(s):
    b=s.rstrip().encode("utf-16-le");h=2166136261
    for i in range(0,len(b),2):h=((h^(b[i]+256*b[i+1]))*16777619)&0xffffffff
    return f"{h:08x}"
def load(p,n,h=None,cls=None):
    s=snippet(p,n,cls)
    if h: assert fnv(s)==h,(n,fnv(s))
    exec(textwrap.dedent(s),globals())
CONFIRMED={"USER_CONFIRMED","EXTERNALLY_VERIFIED"}
CLAIM_KEYS=("kind","field","subject","value","unit","source")
CNY=r"人民币|(?<![A-Za-z])(?:CNY|RMB)(?![A-Za-z])|[¥￥]|(?<![美韩港澳日欧台泰加新])元|块钱?"
MONTH=r"每个自然月|每个月|每月|按月|[\/／]\s*月|月租"
BOUNDS={"cost_max":None,"hours_max":None,"onsite_max":None}
OPERATORS={">=":operator.ge,">":operator.gt,"<=":operator.le,"<":operator.lt}
e="decision_evidence.py"; s="decision_semantics.py"; c="decision_conversation.py"; m="decision_conversation_math.py"; f="decision_feasibility.py"
load(e,"_normalized")
for p,n,h in [(e,"_validate_correction","af3132b2"),(e,"_group","eae6382b"),(s,"fingerprint","fcf4a607"),(s,"occurrence","fc5cf5fe"),(s,"_covered_fingerprints","64dcac0b"),(s,"blocking_obligations","56c04606"),(c,"active_claims","0435aa15"),(m,"sourced_key","3f7ab4ef"),(m,"_active_evidence","f0480b1b"),(f,"check_constraint","d454863e")]:load(p,n,h)
load(s,"_repair_key")
load(c,"_check_resource_date","e26f59f5","ConversationHub")
load(c,"_view","b6503f7c","ConversationHub")
class Claim:
    def __init__(self,field,role,v,unit,source,subject="",identity="current_user",scope=""):
        self.field,self.role,self.value,self.unit,self.source,self.subject=field,role,str(v),unit,source,subject
        self.kind="estimate" if role=="estimate" else "fact"
        self.metadata=NS(source_identity=identity,channel="user_self_report",observed_at="",population="",scope=scope)
for n in ["_key","_comparison_scope","_supported"]:
    load(e,n,cls="ClaimInput");setattr(Claim,n,globals()[n])
def entry(i,c):return NS(claim_id=i,claim=c,confirmed_at="fixture",operator_proof=None)
def public(e,status,prior=None):return dict(id=e.claim_id,status=status,supersedes=prior,kind=e.claim.role,**{k:getattr(e.claim,k) for k in CLAIM_KEYS if k!="kind"})
counts=[0,0,0,0]
for field,unit,template in [("cost_max","yuan","预算最多{}元"),("hours_max","hours/week","每周最多工作{}小时"),("onsite_max","days/week","每周最多到岗{}天")]:
    for v in [1,2,3]:
        item=dict(kind="constraint",field=field,subject="",value=str(v),unit=unit,source=template.format(v))
        for start in [0,5]:
            a=occurrence(item["source"],start,field=field,subject="",hard=True,operator="<=",matches=[item])
            b=occurrence(item["source"],start,field=field,subject="",hard=True,operator="<=",matches=[item])
            assert a["id"]==b["id"] and not blocking_obligations([{"obligations":[a]},{"obligations":[b]}],[dict(item,id="1",status="USER_CONFIRMED",supersedes=None)],[])
            counts[0]+=1
        a=entry("1",Claim(field,"constraint",v,unit,"原底线"))
        b=entry("2",Claim(field,"estimate",v,unit,"估计值"))
        _validate_correction(b,a)
        assert _group(field,"",[a,b],{"1"})["status"]=="CONFIRMED"
        pa,pb=public(a,"SUPERSEDED"),public(b,"USER_CONFIRMED","1")
        ob=occurrence(a.claim.source,0,field=field,subject="",hard=True,operator="<=",matches=[pa])
        assert not blocking_obligations([{"obligations":[ob]}],[pa,pb],[])
        assert [x for x in active_claims([pa,pb]) if x["kind"] not in {"estimate","previous"}]==[]
        counts[1]+=1
VERSION="0.7.0"
public_claims=lambda row:[]
summarize=lambda row,claims:{"conclusion":"fixture","question":""}
result_receipt=lambda *args,**kwargs:{"fixture":True}
PurposeConsent=lambda:NS(status=lambda:{})
for d in [-2,-1,1,2]:
    model=NS(model_dump=lambda mode:{"fixture":True})
    row=NS(session_id="fixture",revision=1,dialogue=[],options={},state=model,analysis={"feasibility":[{"option_id":"A","status":"ACCEPT"}]},semantic_turns=[],blockers=[],knowledge={},resources=model,resource_result={"evaluated_on":(datetime.now(UTC).date()+timedelta(days=d)).isoformat()},reuse_authority=None,local_receipt={"status":"FIXTURE"},selected_option_id=None,selected_plan=None,changes=[])
    assert _view(None,row)["phase"]=="ANALYZED"
    try:_check_resource_date(row)
    except ValueError:counts[2]+=1
    else:raise AssertionError("date guard")
for field,unit in [("cost","yuan"),("hours","hours/week"),("onsite","days/week")]:
    for v in [1,2,3]:
        a=entry("f",Claim(field,"measurement",v,unit,"核对事实",subject="A"))
        b=entry("e",Claim(field,"estimate",v,unit,"预计值",subject="A"))
        for rows in [[a,b],[b,a]]:
            assert _group(field,"A",rows,set())["status"]=="CONFIRMED"
            chosen=_active_evidence(active_claims([public(x,"USER_CONFIRMED") for x in rows]))[field+":A"]
            constraint=NS(source="底线",unit=unit,horizon="t",operator="<=",threshold=v)
            val=NS(kind="fact",source="测量",unit=unit,horizon="t",lower=v,upper=v)
            assert check_constraint(constraint,None if chosen["kind"]=="estimate" else val,"t")[0]==("UNKNOWN" if rows[-1] is b else "CERTAIN_PASS")
            counts[3]+=1
assert counts==[18,9,4,18]
print(counts)
```
## 联合后续验收门及分工
统一原文出现ID/候选ID/义务ID/事实身份/修订ID/用途/会话实例/当前授权。同义确认复用需明确资格，真正新义务不得继承；变更普通参数与撤回底线分开；证据资格与值相同分开；资源当前性在发布、缓存读取、选择、续算及存储一致。原生入口验证四组反例可达性，已知失败与不可比/未知分开，保留前轮重提恢复、会话实例和局部权威隔离回归。实际确认流程、完整Pydantic、真实语言、原生数学方法、UI/API/CLI、实机与独立评测均待执行；产品轨维护唯一近期交接。自行选择四组有限夹具及候选策略，未获重大版本开发授权，不启动Codex、训练、合并、部署、CI或新增费用；冻结及既有验收结论不变。