# 自主认知：有作用域的跨轮补全见证及多历史终端身份歧义
2026-11-26。RESEARCH_CANDIDATE / FIXED_NATIVE_FRAGMENTS_EXECUTED / SYNTHETIC_FIXTURE / FULL_NATIVE_NOT_RUN / REACHABILITY_UNKNOWN / INDEPENDENT_NOT_RUN / NO_TRAINING。

## 基线与增量
起点及写前main ddcd754c5de59841372f91a1a96ef59f4eb679d7。核对15近期提交、15开放PR、decision_hub相关目录题名、v3.2及同步规程（blob 7cee2ec8e740ef3b89c0b5d4b2fc7336fac19b85、26c4d946e48f01858fb8e8c2cb06e4f7ba91bf05）、唯一交接前20行（5e74f4f0b37141d631740e844ad8bbbfed232e07）。PR #63仍open/draft，head 734686980b19da9291bdd08b67d4e2519c011acf。读取此前v07略过重提审计95616e3d1c316a7f56f49fc81f07e51e16e6d13d及前轮固定原生修订链审计。前者已研究同文重新提议，前轮已研究角色、比较方向及跨口径修订；本轮只新增原生缺币种/周期重述覆盖对不同发生义务的影响、后继证据作用域、及多个补全见证的终端身份仲裁。非全库查重证明。

## 固定源码及资格边界
固定#63的platform/future_model/src/psychohistory/decision_semantics.py blob 8c6ea6914b5b6e4f01d70331ed5c75c0dc32221b。实际在Python3.13.5容器转录并执行5个原生函数，去尾空白UTF16 FNV1a32与连接器源文本一致：fingerprint fcf4a607、occurrence fc5cf5fe、_covered_fingerprints 64dcac0b、_repair_key 6172c8bc、blocking_obligations 56c04606。FNV仅转录核对，未核对整个原始Git文件字节。CLAIM_KEYS、CONFIRMED、CNY、MONTH按固定源合同提供。
另读取固定decision_language.py c01217b6d6f4c2465ffc0959f3c0219e9638e052中repair构造：hard、无subject和condition、明确operator；仅缺币种且未见非CNY，或联合房租停车费缺周期且未见非月周期；唯一可转换数值。其余歧义不具此repair候选。本轮未运行完整interpret、账本实体、宿主权限、ConversationHub、数学计算、ASGI/CLI/App。实验通过人工原文义务与记录夹具构造输入，不主张真实用户入口可产生全部情形。原生函数用全局内容指纹及重述键判断覆盖，存在合理的同义重述去重用途，不能一律称错误。研究者选择了更严格的显式发生身份关联规则作参照，未授权为产品规范。
研究夹具内不同root表示已经由可信宿主确认的不同义务，而非从相同文本自动猜测。scope为夹具的抽象范围标识，qualified_scope_correction是人工已资格化的修订开关，不是实际鉴权或自动理解。所有结果authority NONE。

## A 补全见证及当前历史版本
两种原文形式：预算最多1000（补充元），房租和停车费合计最多1000元（补充每月）；阈值1000/2000/3000；每组两个缺失义务，原文完全相同但发生于不同轮次。相同根掩码0至3，明确关联掩码0至3，八种证据状态，补全轮在两个义务之后或之间。2×3×4×4×8×2=1536组、3072项义务。实际原生匹配以对象身份诊断每个旧义务是否仍阻塞；不将对象身份当产品发生ID。
新候选以(轮次实例,原文SHA256,Unicode标量起止,字段)绑定发生身份。精确关联须同时绑定原义务、重述发生及证据ID；重述必须晚于原义务、非未知、无条件、具比较符，且与被绑定证据的原文指纹及重述键匹配。历史链要求唯一后继、同根/字段/主体，范围变化须另有可信资格说明，终端仍有效确认。缺失关联保持未解决；合格同根的两个旧义务可以明确关联同一个补全见证，不必强行一对一。此处只实现候选读端口，不实现真实凭证、主体/时间/单位/来源资格验证、历史完整性、grant、并发、持久化或撤回后清除。原文范围变化实际是否等同原义务仍须明确判断；本轮允许的资格标记仅人工夹具。
参照为逐项布尔条件：旧义务先于重述，明确关联及同根，且当前状态为active/verified/superseded_same/superseded_authorized。与候选全部一致，非独立验证。两类源形式及重复参数不等同独立用户样本。八状态细分如下（每行384项义务）：

| 状态 | 原生覆盖 | 严格参照/候选覆盖 | 原生超出严格参照 |
| --- | ---: | ---: | ---: |
| active | 288 | 72 | 216 |
| verified | 288 | 72 | 216 |
| provisional | 0 | 0 | 0 |
| dismissed | 0 | 0 | 0 |
| superseded_same | 288 | 72 | 216 |
| superseded_changed | 288 | 0 | 288 |
| superseded_authorized | 288 | 72 | 216 |
| superseded_conflict | 0 | 0 | 0 |
| 合计 | 1440 | 288 | 1152 |

互斥分解（先归入未经资格确认的作用域改变）：288范围变化、576不同根、288同根但没有明确关联。最后288并不证明自动重述修复不合理，只说明在本轮严格合同下缺资格。实际产品完整阻塞判断还受其他入口及数学门影响，不是错误放行率。原生与候选在本参照下都无漏覆盖，候选零超覆盖。17项专项控制：同文发生身份、合法关联、缺关联、原文变更、错误值、错误根、缺证据、重复ID、同轮、条件见证、合法后继、缺后继、分叉、跨根、未确认范围变化、夹具确认范围变化、原生同轮不补全。普通及-O结果字节相同，显式检查在优化模式继续执行。

## B 多重见证与终端身份
两种字段×三个阈值×两位关联掩码×两位根掩码×两个见证各五状态(active/dismissed/conflict/changed/authorized)=2400组。两个见证可各有后继，先用A端口确认单个见证资格，然后按实际有效终端ID去重。没有终端UNRESOLVED；一个SINGLE_TERMINAL；多个AMBIGUOUS_TERMINALS，保留所有身份，不选第一个，也不按相同数值强行合并。此端口只表达身份歧义，不评估多个来源的真实可靠性、合法同义聚合或科学决策效果。构造中部分多条同根记录可能不满足原生完整账本的去重/冲突规则，故不能声称原生账本可达。
实际结果UNRESOLVED 1944、SINGLE_TERMINAL 432、AMBIGUOUS_TERMINALS 24。其中24项若只取首个合格见证会造成虚假唯一性，6项虽然数值相同，终端记录ID仍不同。全部2400组与独立直接掩码参照一致，全部逆序结果一致；额外两控制：同一终端由两次独立重述见证仍为单终端，重复见证幂等。普通及-O结果字节相同。参照和候选均由同一研究者实现，不是独立验收。

## 实际运行产物
Python3.13.5标准库；两完整脚本各在普通及优化模式执行且对应结果逐字节一致。共3936组主要场景，19专项控制。完整源码、普通/优化结果及README随当轮聊天ZIP交付；未将该ZIP的字节写入GitHub。本报告提供复算算法及计数，不冒称下方摘录为已独立执行的完整程序。
SHA256：
study.py 65f42d438a01258fc8facdb344ff9d3f9948e80ace73a60ee64921944efda120
multi.py c071f78d1f5e5b111c6e2fabdb1531e0e628b1e3082535f8afd03f61180de6fb
results.json ed5c12a285ae5699d316fc0b7a639f05c4eba7e351360973e4aafc35ce1bd45c
multi_results.json 455b087eca66e6979742666694e4a210d5f8812a717cc92343f751ec8a55257d

## 核心算法摘录
原生函数应从固定源码按上列名称提取；实际运行使用逐字转录并校验指纹。下方为候选研究的核心逻辑说明，完整原始执行文件另见ZIP。
```python
def terminal(start, entries):
    by = {c['id']: c for c in entries}
    if len(by) != len(entries) or start not in by:
        return None
    cur = by[start]
    visited = set()
    while True:
        if cur['id'] in visited:
            return None
        visited.add(cur['id'])
        nxt = [c for c in entries if c.get('supersedes') == cur['id']]
        if cur['status'] in CONFIRMED:
            return cur if not nxt else None
        if cur['status'] != 'SUPERSEDED' or len(nxt) != 1:
            return None
        n = nxt[0]
        if (n['root'] != cur['root'] or n['field'] != cur['field']
            or n['subject'] != cur['subject']
            or (n['scope'] != cur['scope']
                and not n.get('qualified_scope_correction'))):
            return None
        cur = n

def resolve(old, witnesses, entries, links):
    valid = set()
    for w in witnesses:
        if scoped_repair(old, w, entries, links):
            end = terminal(w[3], entries)
            if end is None:
                raise RuntimeError('terminal lost')
            valid.add(end['id'])
    return ('UNRESOLVED' if not valid else
            'SINGLE_TERMINAL' if len(valid) == 1 else
            'AMBIGUOUS_TERMINALS', tuple(sorted(valid)))
```
scoped_repair的完整步骤：校验两个原文锚、轮次顺序、明确关联三元组、见证状态/条件/比较符、证据ID/根及指纹、相同repair key，然后核对terminal。所有步骤只返回是否有当前合格身份，不提供数学或写入权限。当前算法逐层扫描后继，最坏O(n²)，未优化为邻接索引，未测真实设备资源或执行入口。不得在生产环境使用未鉴权的布尔资格字段；后续需要与可信会话实例、revision、grant、源身份、确认凭证和稳定对象作用域绑定。

## 后续责任
优先验证真实语言入口生成同文不同义务时的作用域、修订及补全可达性；建立无需反复追问的明确关联确认与同根重述复用，不能用人工root冒充自主语义理解。独立轨持有未见测试，区分同义重复与不同预算用途、单位和时间纠错、跨轮条件及来源、重复终端及真实冲突，核查真实原生门、错误放行/拒绝及追问负担。当前无真实用户、训练、原生完整执行、独立验收、竞品、Mac/iPhone、生产代码改动、PR合并、部署、主动CI或新增费用，冻结、证据等级及唯一交接不变。
