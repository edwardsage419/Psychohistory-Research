# v0.7 中文情景评分、评价口径修订与 C029 原生数学片段连接审计
2026-11-25。RESEARCH_CANDIDATE / EXACT_FULL_SCENARIO_MODULE_EXECUTED / NATIVE_FRAGMENTS_EXECUTED / SYNTHETIC_DEVELOPMENT / FULL_APP_NOT_RUN / INDEPENDENT_NOT_RUN。起始main e6027255ada9eee5cfee3351c260ce9e9486191d，固定Draft #62 head e61bbad10932edabc9a87483e5407fdae6c751cc，尚未合并。核查近期15提交、14开放PR、v3.2及同步规程前22行、唯一产品交接前22行blob 5e74f4f0b37141d631740e844ad8bbbfed232e07。查重reference/semantic span/native state/language/candidate obligations/scenario score/scenario basis/scenario comparability/scenario correction/regret/scenario/C029/scale，已有原生C029数值验证及后悔界研究（217e8df6352dcefbb2685daad4c3e8adacdca759、32aab8f9c28631a51aaa69cf7c74f835d8a9a36d等）；本轮只增加完整v0.7情景评分文字入口、口径修订、同值重复与可行集合覆盖连接，不重计既有数学研究。非全库去重证明。
## 固定源码和执行身份
platform/future_model/src/psychohistory/decision_scenarios.py，blob 0a18c9c203ec9d4c8e712b4ad1c82c8336da4399。通过连接器完整读取、容器逐字复现3300 UTF-8字节，实际本地计算Git blob SHA1完全一致。运行全部scenario_candidates及confirmed_scenarios，无替换函数体。decision_regret.py blob e56689a54897d95eaa126540c23fca51cc0eede7，实际转录执行_validate 42–76 e8303e28、_validate_points 79–80 db379f40、_utilities 93–100 d19ea768、_leaders 111–113 9a3d415d、_point_regret 116–121 79af4f91（FNV1a UTF16去尾空白匹配）。decision_evidence.py blob b45932af6346fb0df072ffb6cb13ef0cd6991b7a，实际复用前轮固定_validate_correction 137–148 af3132b2及_group 220–239 eae6382b，FNV匹配；归一化及Claim/metadata/entry为最小夹具，未执行完整Pydantic模型或coherent_history。另读decision_state.py 0840855431fbc88fe212785584277aa01be74d93相关字段、decision_language.py 4e6733499f74db505e2cedaff84cf8c5eae207d1前50行、decision_semantics.py c7158c996f82c208b4d142b2863ddc3e27efa267前50行、decision_v05.py bc27cc42e4a8224c86c3113d044a328ae5eeba3e前50行。前轮已核查原生_project调用confirmed_scenarios。容器直接raw.githubusercontent.com DNS失败，下载代理无法取得完整开放语言模块；没有执行完整interpret、ConversationHub、API、CLI、App、C029完整Method调度及真实Pydantic账本。Python3.13.5，标准库执行；不同于正式支持环境。比较参照同一研究者、同一合成输入，非独立验收。
## A 正常中文情景评分至数学复算
两个方案、两个情景、三个精确数值(-1.25,0,2.5)，81种矩阵，两个输入标签顺序。162/162实际中文句式经完整scenario_candidates提取；人工给定选项及确认状态，经confirmed_scenarios和原生后悔值片段计算。独立直接公式参照使用Fraction(Decimal(v))，最大后悔值和全部并列最优集合162/162一致。该输入是受限显式评分句式，非开放语言语义准确率。
## B 情景与可行选项完整性
3个选项，两个情景各可出现4种大小至少2的选项子集；7种非空ACCEPT集合，3种评价口径确认状态。336组。原生confirmed_scenarios可以保留不完整评分集合，原生_validate_points正确针对已通过硬约束的方案要求每情景有完整评分及共同口径。40组通过、296组拒绝，与人工逻辑预期全部一致；216组存在缺失的可行方案评分（其中部分也无确认口径，非独立错误计数）。硬约束本身的求解未执行，ACCEPT由可信夹具提供。不能要求被硬门排除的所有方案仍有评分，也不能默认某个缺失但可行的方案得零分。另6个不合格句式控制拒绝。
## C 评价口径修订跨轮绑定
现有confirmed_scenarios只查唯一有效口径声明，再给全部有效历史评分添加当前horizon；单个评分没有独立的口径修订ID检查。81种矩阵，旧口径“未来一年收入满意度”已被替换，新口径“未来三年工作生活平衡”被确认，旧评分仍确认。人工夹具明确两口径不等价且未给转换/重新核对。81/81原生投影及数学校验接受并按旧分计算；候选81/81阻断；81个明确授权重绑正控、81个新口径待确认负控通过。另实际连接前轮固定账本修订验证函数，4种旧口径×4种新口径=16组实际中文basis解析；16/16同主体字段及自述来源的_validate_correction允许，16/16 _group确认新口径，16/16原生评分投影改标新口径，48项异主体、异来源、异通道修订拒绝控制通过。说明跨模块缺少口径身份绑定的风险；合法新声明可能本来就明确适用于全部现有评分，不能一律阻止。只有可信宿主核实等价、有效转换或用户重新确认相关评分才允许重绑。这里的确认、superseded、独立口径及权威关系仍是人工夹具，未运行原生完整确认与更正路径，不能断言真实入口必然误放行或已有用户事故。
## D 同值重复陈述
81种矩阵，重复第一个情景评分但交换两个选项的陈述顺序；真实解析产生不同source，原生confirmed_scenarios遇同一情景选项第二条评分立即返回None。81/81不能开展后悔值分析。候选在可信宿主明确认定同一情景、同一方案、同一评价量尺、相同时间、相同数值及来源资格的前提下合并同值单元、保留全部来源ID；81/81仍与直接数学参照一致。不同值冲突、不同口径、来源资格缺失各81项拒绝控制。禁止仅凭文字相同、值相同或相同情景标签自动认定同义。原生账本真实去重及确认入口未运行，不能以该压力测试代表产品误拒率。
## 实测
```json
{"normal":{"cases":162,"exact":162},"coverage":{"cases":336,"accepted":40,"correct_blocked":296,"missing_feasible_cell":216},"basis_revision":{"cases":81,"native_accepts_unqualified_rebind":81,"candidate_blocks":81,"explicit_rebind_controls":81,"unresolved_basis_controls":81},"duplicate":{"cases":81,"native_unavailable":81,"candidate_exact":81,"conflict_controls":81,"unknown_scope_controls":81,"unauthorized_controls":81},"parser_controls":6,"basis_ledger":{"basis_pairs":16,"native_validator_accepts":16,"new_group_confirmed":16,"native_projection_relabeled":16,"negative_controls":48}}
```
676个主案例（162+336+81+81+16）及459项附加控制（162+243+6+48）。相同矩阵跨实验复用，非676个独立人次。研究代码完整本地重放两次、输出逐字节一致。会话可下载ZIP SHA256 596e278bd5594430e48b8634f7b5fb619f60a69f924115dd7c1cc192e52ff460，8文件。实际执行probe.py SHA256 b1387a5f5e29650979af46f8293f492faba16d5ea36a544dd9b962517710aa93；basis_ledger.py 8f34cf5ec9129ffee9804a50661f63429d2484b919d1c30de019802115d0014a；results.json fe06852f6e2ba5ab2acad650f08429755dab4ceb73bfc1159ed16c5419679c90；basis_ledger_results.json e235dd20fdd1c2d18f7836ac2496c8c9b8c04a046a407efabc1c9166bfb39c5a。固定源及片段本地SHA256：decision_scenarios.py 2de4570836cc5149b6106d348316d182a15775bf54ac72f101d34de2ce3a41a8；regret_fragments.py 858a531326cf5ab5db22868567f3b7016ddd602a9674b9756d39a2bbb98b3364；evidence_fragments.py 14d1635b30ae22b1576b8be4d0423af9b656bd19444a5806651b7c623ff956b4。
## 固定原生源码复算入口
下列紧凑复算入口与实际本地试验使用同一数据构造及核心判定，采用源码AST提取替代本地逐字转录；为避免重复归档原始模块，依赖固定候选的三个完整文件。该紧凑入口未单独运行；实际执行脚本及输出保存在上述ZIP。取三个文件同目录，从下列代码块另存python执行。不要执行任意网络内容。
```python
from __future__ import annotations
from pathlib import Path
from hashlib import sha1
from fractions import Fraction
from decimal import Decimal
from types import SimpleNamespace as NS, ModuleType
from itertools import product, combinations
from unicodedata import normalize
import ast, json, copy, importlib.util
def load_fragments(path,names,blob,globals_):
    b=Path(path).read_bytes()
    assert sha1(f"blob {len(b)}\\0".encode()+b).hexdigest()==blob
    src=b.decode("utf-8"); t=ast.parse(src)
    for name in names:
        f=next(x for x in t.body if isinstance(x,ast.FunctionDef) and x.name==name)
        exec(compile(ast.Module(body=[f],type_ignores=[]),path,"exec",flags=__import__("__future__").annotations.compiler_flag),globals_)
    return NS(**{n:globals_[n] for n in names})
b=Path("decision_scenarios.py").read_bytes()
assert sha1(f"blob {len(b)}\\0".encode()+b).hexdigest()=="0a18c9c203ec9d4c8e712b4ad1c82c8336da4399"
import decision_scenarios as S
R=load_fragments("decision_regret.py",["_validate","_validate_points","_utilities","_leaders","_point_regret"],"e56689a54897d95eaa126540c23fca51cc0eede7",{"Fraction":Fraction})
def normalized(v):return normalize("NFC",v or "").strip()
E=load_fragments("decision_evidence.py",["_validate_correction","_group"],"b45932af6346fb0df072ffb6cb13ef0cd6991b7a",{"_normalized":normalized})
A=["方案甲","方案乙"]
def opts(labels):return [dict(id=x,label=x,status="CONFIRMED") for x in labels]
def parse(t,labels,status="USER_CONFIRMED"):return [dict(c,status=status) for c in S.scenario_candidates(t,labels)]
def basis(t,labels,status="USER_CONFIRMED"):return parse(f"都比较{t}，分差可比较，分数越高越好",labels,status)
def row(n,labels,v):return f"情景{n}："+ "，".join(f"{a}得{x}分" for a,x in zip(labels,v,strict=True))
def evaluate(out,labels,accept=None):
    ss,b=out if out is not None else ([],None)
    ss=[NS(**{**s,"utilities":{k:NS(**{**v,"lower":Decimal(v["lower"]),"upper":Decimal(v["upper"]),"horizon":v.get("horizon")}) for k,v in s["utilities"].items()}}) for s in ss]
    c=NS(state=NS(scenarios=ss,scenario_basis=b,deadline="当前比较"),feasible=[NS(id=a,label=a) for a in (labels if accept is None else accept)])
    if R._validate_points(c):return None
    p={k:tuple(lo for lo,hi in v) for k,v in R._utilities(c).items()}
    w={k:max(v) for k,v in R._point_regret(p).items()}
    return w,set(R._leaders(w))
def attach(claims,bid,prefix):return [dict(x,basis_id=bid,claim_id=f"{prefix}{i}") for i,x in enumerate(claims)]
def candidate(claims,labels,bid,qualified):
    bases=[x for x in claims if x["field"]==S.BASIS_FIELD and x["status"]!="SUPERSEDED"]
    if len(bases)!=1 or bases[0]["status"]!="USER_CONFIRMED" or bases[0].get("basis_id")!=bid:return None
    cells={};ret=[bases[0]]
    for x in claims:
        if not x["field"].startswith(S.PREFIX) or x["status"]=="SUPERSEDED":continue
        if x["status"] not in ("USER_CONFIRMED","EXTERNALLY_VERIFIED") or x.get("basis_id")!=bid or x.get("claim_id") not in qualified:return None
        k=(x["field"],x["subject"]);v=Decimal(x["value"])
        if k in cells and cells[k]!=v:return None
        if k not in cells:ret.append(x);cells[k]=v
    return S.confirmed_scenarios(ret,opts(labels))
o=dict(normal=0,coverage=0,accepted=0,blocked=0,basis=0,duplicate=0,controls=0,basis_ledger=0)
for v in product(["-1.25","0","2.5"],repeat=4):
    m=[v[:2],v[2:]]
    w={a:max(max(Fraction(Decimal(x)) for x in s)-Fraction(Decimal(s[i])) for s in m) for i,a in enumerate(A)}
    oracle=w,{a for a in A if w[a]==min(w.values())}
    for rev in [False,True]:
        labels=A[::-1] if rev else A
        t="。".join(row(n,labels,s[::-1] if rev else s) for n,s in zip(["顺利","困难"],m))
        c=parse(t,A)+basis("未来一年收益",A)
        assert evaluate(S.confirmed_scenarios(c,opts(A)),A)==oracle;o["normal"]+=1
    raw=parse("。".join(row(n,A,s) for n,s in zip(["顺利","困难"],m)),A)
    old=attach(raw+basis("未来一年收入满意度",A),"old","c")
    old[-1]["status"]="SUPERSEDED"; c=old+attach(basis("未来三年工作生活平衡",A),"new","b")
    assert evaluate(S.confirmed_scenarios(c,opts(A)),A) is not None
    assert candidate(c,A,"new",{x["claim_id"] for x in c}) is None;o["basis"]+=1
    rebind=[dict(x,basis_id="new") if x["field"].startswith(S.PREFIX) else x for x in c]
    assert evaluate(candidate(rebind,A,"new",{x["claim_id"] for x in rebind}),A)==oracle;o["controls"]+=1
    pending=[dict(x,status="PROVISIONAL") if x["field"]==S.BASIS_FIELD and x["status"]!="SUPERSEDED" else x for x in c]
    assert evaluate(S.confirmed_scenarios(pending,opts(A)),A) is None;o["controls"]+=1
    c=attach(raw+basis("未来一年收益",A),"same","c")+attach(parse(row("顺利",A[::-1],m[0][::-1]),A),"same","d")
    ids={x["claim_id"] for x in c}
    assert S.confirmed_scenarios(c,opts(A)) is None
    assert evaluate(candidate(c,A,"same",ids),A)==oracle;o["duplicate"]+=1
    bad=copy.deepcopy(c);bad[-1]["value"]=str(Decimal(bad[-1]["value"])+1)
    assert candidate(bad,A,"same",ids) is None;o["controls"]+=1
    bad=copy.deepcopy(c);bad[-1]["basis_id"]="unknown"
    assert candidate(bad,A,"same",ids) is None;o["controls"]+=1
    assert candidate(c,A,"same",ids-{c[-1]["claim_id"]}) is None;o["controls"]+=1
C=A+["方案丙"];sets=[list(x) for n in [2,3] for x in combinations(C,n)]
for x,y in product(sets,repeat=2):
    for mask in range(1,8):
        a=[v for i,v in enumerate(C) if mask&(1<<i)]
        for bs in ["USER_CONFIRMED","PROVISIONAL","ABSENT"]:
            c=parse(row("甲",x,range(len(x)))+"。"+row("乙",y,range(len(y))),C)
            if bs!="ABSENT":c+=basis("未来一年收益",C,bs)
            ok=bs=="USER_CONFIRMED" and set(a)<=set(x)&set(y)
            assert (evaluate(S.confirmed_scenarios(c,opts(C)),C,a) is not None)==ok
            o["coverage"]+=1;o["accepted"]+=int(ok);o["blocked"]+=int(not ok)
for t in ["情景顺利：方案甲得2分","情景顺利：方案甲得2分，方案甲得1分","情景顺利：方案甲得2分，未知方案得1分","情景顺利：方案甲得2分，方案乙约1分","都比较收入，分数越高越好","情景顺利：方案甲得2.1234567分，方案乙得1分"]:
    assert parse(t,A)==[];o["controls"]+=1
class Claim:
    def __init__(self,x,identity="current_user",channel="user_self_report"):
        self.__dict__.update(x);self.role=x["kind"];self.kind="fact"
        self.metadata=NS(source_identity=identity,channel=channel,observed_at="",population="",scope="")
    def _key(self):return normalized(self.field),normalized(self.subject)
    def _comparison_scope(self):return tuple(normalized(v) for v in (self.unit,self.metadata.observed_at,self.metadata.population,self.metadata.scope))
    def _supported(self):return self.kind!="unknown" and bool(self.source.strip()) and self.role!="previous" and (self.role!="conditional" or self.field=="move_if_onsite_max")
def entry(i,x,**kw):return NS(claim_id=i,claim=Claim(x,**kw),confirmed_at="fixture",operator_proof=None)
for old,new in product(["未来一年收入满意度","未来半年学习收益","未来一年工作稳定性","未来两年通勤负担"],["未来三年工作生活平衡","未来五年职业成长","未来一个月现金安全","未来四年学习成果"]):
    a,b=basis(old,A)[0],basis(new,A)[0];p,q=entry("p",a),entry("q",b)
    E._validate_correction(q,p);assert E._group(S.BASIS_FIELD,"",[p,q],{"p"})["status"]=="CONFIRMED"
    c=parse(row("顺利",A,[1,2]),A)+[dict(a,status="SUPERSEDED"),b]
    assert S.confirmed_scenarios(c,opts(A))[0][0]["utilities"][A[0]]["horizon"]==new
    for n in [entry("q",b,identity="other"),entry("q",dict(b,subject="other")),entry("q",b,channel="separate_source")]:
        try:E._validate_correction(n,p)
        except ValueError:o["controls"]+=1
        else:raise AssertionError("invalid correction")
    o["basis_ledger"]+=1
assert o==dict(normal=162,coverage=336,accepted=40,blocked=296,basis=81,duplicate=81,controls=459,basis_ledger=16),o
print(json.dumps(o))
```
## 接入与验收要求
统一语义接口将评分单元绑定到情景规范身份、候选行动、指标定义、量尺版本、共同时间范围、事实/估计/假设类别、来源、确认及修订代次。评分口径修订触发受影响单元失效；保留历史版本，允许真正同义重述复用与经授权转换，不自动套用旧分数。完整原生测试从真实文本、真实候选、真实ledger校验、_project、C028门、C029校验与执行到结果收据及界面；另测试缺失口径、同名不同义、同值不同口径、明确重绑、证据撤回、相同词面不同实体、重复/过期/并发请求、既有高级结构化情景兼容和独立留出。保持目前C029独立可行集合检查及精确算术。候选不得把自定义评分推定为现实概率或统一人生效用。项目轨职责不变，产品轨维护唯一交接。没有启动重大版本开发、训练、CI、PR合并、部署、费用或冻结变更。自行选定有限输入、口径对、方案集合及夹具资格，实际开放语言、真实用户、实体App及独立验收仍待完成。
