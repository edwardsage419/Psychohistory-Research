# 自主认知原生修订链：硬约束角色、比较作用域及方向投影一致性
2026-11-26。RESEARCH_CANDIDATE / FIXED_NATIVE_FRAGMENTS_EXECUTED / SYNTHETIC_TYPED_RECORDS / FULL_NATIVE_NOT_RUN / REACHABILITY_UNKNOWN / INDEPENDENT_NOT_RUN / NO_TRAINING。

## 基线与去重
起点及写前REST main 4e23b75f793a5df1b98b2289466d2191001efdf5；检查20近期提交、15开放PR、decision_hub相关目录题名、v3.2与同步规程（blob 7cee2ec8e740ef3b89c0b5d4b2fc7336fac19b85、26c4d946e48f01858fb8e8c2cb06e4f7ba91bf05）、唯一交接前20行（5e74f4f0b37141d631740e844ad8bbbfed232e07）。PR #63直接核对open/draft，固定head 734686980b19da9291bdd08b67d4e2519c011acf，未合并。读取既有跨轮指代修订身份 da54c5b88ed0f19f5c5d272230a1959b811f5b5e、v0.7片段批量审计 5442d4bbeb465bbd11d5901e150a5887263e61ca（重点B、D）、v0.8条件方向修订529750962f2686179703de19e37d5e037fd75d0d及整合账本规划907f12081ddce7bb752ae498bcf21f4b4b218a60相关段落。前轮检索分组及条件政策组合不重复。新增实际v0.8 coherent_history完整函数的两步修订链穷举、比较口径更正与并列来源差异、比较符/字段冲突的实际投影片段。非全库无重复证明。

## 固定资产及转录范围
以下均为上述PR固定head下platform/future_model/src/psychohistory/文件。
- decision_evidence.py e50cb06065e3b1571aef9104bb6109ab1b522bba：实际执行8个函数，FNV1a32去尾空白逐字符指纹分别为 _normalized d7b179a3、ClaimInput._key 99da35bf、_group_key 4a98a7d9、_comparison_scope 81dc1538、_supported 78c94514、_validate_correction aa927ea2、EvidenceLedger.coherent_history 68711852、_group eae6382b。转录前与固定连接器文本核对；FNV仅转录诊断，非密码学证明，未重算整个原始Git文件字节。
- decision_semantics.py 8c6ea6914b5b6e4f01d70331ed5c75c0dc32221b：实际执行NEGATION/COMPARATORS/_OPERATOR常量块 cc94ee38及comparison 5e9884b4。
- decision_conversation_math.py 73557b6650b1a77727c968b114ddfd17c1f591bd：实际执行_operator 0e118de0，仅供应原文件对应hours_max/hours_min两项BOUNDS。静态读取其余build_state等源，未调用。
- decision_conversation.py 3d961454e971b9d505606e9b0156dcb280fd6587：静态读取public_claims、active_claims、blocking_constraints、confirm、_project、_compute；未实际执行，尤其不能推断所有这些门均放行。
- decision_language.py c01217b6d6f4c2465ffc0959f3c0219e9638e052：静态读取_numeric_claims及_qualify。已有显式比较符对应_BOUND_DIRECTION字段选择、UNKNOWN比较拒绝的前置保护，本轮未重跑完整语言入口。

实际Python 3.13.5标准库容器执行probe.py及projection.py各普通与-O一次。Pydantic实体、claim_id、时间、proof匹配均人工夹具；probe阶段比较符为可信符号token夹具，projection阶段替换为真实固定comparison。不是完整EvidenceLedger、原生C028、事务、持久化、授权或ASGI/CLI/App验收。点值判断用标准库operator与人工参照，非原生数学门执行。所有记录原创虚构，未用真实用户或训练。研究者自选分布、角色、符号、时间、口径、阈值及基线。

## A 连续硬约束修订
两类初始严格工时边界（上限<，下限>）。每次编辑4角色×4表达（同方向严格、同方向含等号、反方向严格、裸数值）×2证据kind，连续两编辑。对每条链同时运行首步及完整coherent_history，与按源逻辑另写的逐步参照核对；参照同一研究者设计，非独立规范验证。

| 指标 | 严格上限 | 严格下限 |
| --- | ---: | ---: |
| 链数 | 1024 | 1024 |
| 通过 | 104 | 104 |
| 首步拒绝 | 704 | 704 |
| 首步通过而次步拒绝 | 216 | 216 |
| 已通过链中末项变为estimate角色或非fact | 0 | 0 |
| 首步非revision角色且裸数值仍通过完整链 | 22 | 22 |
| 通过链末项显式严格方向与初始字段方向不一致 | 25 | 25 |

相对于历史v0.7审计，v0.8实际函数追踪硬约束后继，禁止estimate降级。裸数值经constraint或strict_constraint角色通过可能是显式新底线确认的合理设计，不能单独视作错误；需要区分角色来源和用户确认。方向不一致只是人工记录反例。8专项控制：合法链1、已被替代祖先再次修订、异来源身份、异channel、未确认修订、时间倒序、内容身份不匹配、连续链末项estimate共7负向，均通过。

## B 修订与跨口径记录的区别
128组：4项比较口径差异位图（unit/observed_at/population/scope）×2新角色（measurement/revision）×2字段×2主体；同一来源身份及自报channel，新旧值不同。两条路径分别执行coherent_history和_group，一是明确指定替代，二是两条并列证据。128/128指定替代被接受且新组CONFIRMED；120个含口径变化的替代同样接受。并列证据在120个口径变化组为INCOMPARABLE，其余8组不同值为CONFLICT。
比较口径可以因明确更正而合法改变，故不能规定凡口径改变一律禁止。当前片段不能辨别是修正同一事实的原错误口径，还是用户报告另一时期、范围或对象的独立事实。候选要求：在原文和可信宿主没有明确确认改变维度及旧值是否被替代前，保留旧版本与新证据独立，局部输出UNKNOWN或INCOMPARABLE；对真正明确的单位/时间纠错允许生成新版本。不同主体或来源保持已有保护，不将任意新报价当旧事实替换。此候选属于接口规范，未实现生产修复或实测候选门。

## C 方向冲突的原文到数学接口定点诊断
2个工时字段×3角色×6表达（4显式比较、复合比较UNKNOWN、裸数值无比较），初始为同字段的严格底线。实际执行固定comparison、coherent_history、_operator。人工构造字段/原文不一致记录，不从原生解释器生成。每个显式反方向通过案例在11、12、13三个值上独立比较原文关系和投影关系。
36组中28通过；8组显式反方向被接受并全部投影回字段默认方向，累计20项点值判断差异；12组同方向显式比较匹配；8组含无比较或复合比较的记录通过（不能把合法裸数值和复合比较混同）。4项额外原文比较控制（不是高于、不能低于、不得超过、裸数值）通过。

| 字段 | 新角色 | 原文关系 | 投影关系 | 点值差异数 |
| --- | --- | --- | --- | ---: |
| hours_max | constraint | > | <= | 3 |
| hours_max | constraint | >= | <= | 2 |
| hours_max | strict_constraint | > | < | 2 |
| hours_max | strict_constraint | >= | < | 3 |
| hours_min | constraint | < | >= | 3 |
| hours_min | constraint | <= | >= | 2 |
| hours_min | strict_constraint | < | > | 2 |
| hours_min | strict_constraint | <= | > | 3 |

关键限制：真实_numeric_claims根据comparison结果选择字段方向，且UNKNOWN拒绝生成数字候选；真实confirm使用已展示的claim，_project另检查未决原文义务及底线。因此本轮只复现有类型记录的跨模块接口边界，未证明用户可触发，未认定当前v0.8有实际错误放行。后续独立验收要覆盖所有合法原生输入、恢复/迁移路径及候选宿主构造，核查方向、角色、字段、单位及原文锚一致后才进入数学计算；显式矛盾时拒绝或澄清，未知保持UNKNOWN；真正改变上限/下限的意图用明确取消旧底线和新建底线表达，不直接把两方向混成同字段修订。不得未经独立验收宣称漏洞修复。

## 运行收据与复算
本次容器实测probe首次0.157675619秒，仅为片段夹具时间，不是完整产品、真机或性能承诺。普通/O模式非耗时结果相同，projection结果逐字节一致。8+4专项控制均通过。两个执行脚本及结果见当轮聊天ZIP；本报告不假称完整本地文件已另存GitHub。SHA256：
- probe.py 7646cbb71a32a82148950aca7b895a3f0ce09bccbf84abe5dbfcdb778c5e0099
- projection.py 7be8c5e2af93248d7f7818182afa475bc98fc83dda9dbc08abf6c94f51de9694
- results.json e0fe344708a674f142960f5f19eed717402ba0d6fb2122491f21f54e67e0a11a
- projection_results.json 0770f2b8cb3120b653c3d94e4d650c124b7a3f03be74506bbac791cf5614d047

供后续独立验收的核心复算方法（说明性摘录，未作为独立脚本运行）：固定源以AST提取上述8函数及比较函数、常量和_operator；按实际角色与比较符构造每个Claim，metadata同源，给定确定位置身份及同一ISO时间。先检查每个片段FNV，再分别调用coherent_history和_group、comparison及_operator。两步链的计数参照：
```python
from itertools import product
for direction in ("<", ">"):
    other = ">" if direction == "<" else "<"
    items = list(product(
        ["revision", "constraint", "strict_constraint", "estimate"],
        [direction, direction + "=", other, "bare"],
        ["fact", "estimate"],
    ))
    # initial: strict_constraint / fact / direction
    # for a,b in product(items, repeat=2):
    #     construct immutable chain and run fixed native coherent_history
    #     compare each prefix against independent direct guard
    assert len(items) ** 2 == 1024
```
本轮不改生产代码、PR、交接、冻结或证据等级，无训练、部署、主动CI、额外费用。下一责任：独立验收轨按固定候选真实入口确认可达性、检查有类型的原生映射与修订跨口径路径；模型与产品轨形成统一原文义务/字段/角色/作用域确认合同；待所有者另行授权纳入完整版本工程，非独立小Codex任务。
