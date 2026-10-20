# R144 历史制度主义：关键转折、反应性序列和反事实识别的有界研究报告
日期：2026-10-20。目录P1/06-002 Historical Institutionalism。研究资格：**两篇原著概念与方法的一手精读＋项目自设状态机E1穷举；没有原作者数值模型的复现，也没有外部历史E3因果识别**。

## 一手原著身份与真实核验页
1. James Mahoney (2000), “Path Dependence in Historical Sociology,” *Theory and Society* 29(4):507–548, DOI https://doi.org/10.1023/A:1007113830879；[ETH教育归档的原刊JSTOR影印](https://archiv.soms.ethz.ch/teaching/OppFall09/MahoneyPathDependence.pdf)。已逐页可视核对原刊507–509页：一段过去对未来有影响的历史并**不自动**是严格路径依赖；需要有条件性偶然事件、后续机制，以及区分自我强化（self-reinforcing）与反应性（reactive）事件序列。作者并未发布本期六事件有限状态机。
2. Giovanni Capoccia and R. Daniel Kelemen (2007), “The Study of Critical Junctures: Theory, Narrative, and Counterfactuals in Historical Institutionalism,” *World Politics* 59(3):341–369, DOI https://doi.org/10.1017/S0043887100020852；[Capoccia牛津作者本人原文PDF](https://users.ox.ac.uk/~ssfc0073/Writings%20pdf/Capoccia%20and%20Kelemen%20WP%202007.pdf)。已逐页可视核对原刊341–343页：关键转折点的核心是短暂放松结构约束、选择集合可能扩大、行为者抉择具有放大后果，分析必须明确可行反事实及叙事过程追踪。**不**可把每一次终点改革都按事后结果自动命名为关键转折。也没有复验论文中真实政治制度案例。

## 与R143的区别
R143直接复算Arthur(1989)收益递增与技术采用比例差的吸收马尔可夫链：正反馈、随机类型和最终技术锁定。本期完全不使用该收益或随机过程，专门执行人工 **短窗口−动员−改革−巩固−反对−等待** 的反应性因果链，为研究制度形成的时序、反事实方法提供不同于正反馈的可证伪机械示例。

## 计算前冻结的模型和测度
[冻结协议](../../protocols/R144_MAHONEY2000_CAPOCCIA_KELEMEN2007_HISTORICAL_INSTITUTIONALISM_SEQUENCE_COUNTERFACTUAL_PRESCORE_FREEZE_2026-10-20.md)，实际GitHub提交`33f57f4ff24918f0bfeb9cf0221e9a9a4b9ece7a`，早于全部代码与机器结果。
状态(r,c,w,e)∈{0,1}×{0,1}×{0,1,2}×{0,1}，分别表示已改革、联盟动员、开放窗口剩余事件机会、巩固；满足e=1⇒r=1。初始(0,0,0,0)。
- O：若没有巩固，把窗口重设2；有巩固时不重新开启；
- M：入场前w>0时联盟c设1；事件后窗口减少1；
- A：入场前w>0且c1时改革r设1；事件后窗口减少1；
- E：若此前r1，则完成巩固e1；事件后窗口减少1；
- B：若e0，则改革r、联盟c都清0；事件后窗口减少1；
- W：无其他改变，窗口减少1。
这个反应性链条、两事件开放期长度、六个动作的可靠性都是**项目人为设定**，非作者2000或2007的原始数学命题，更不能冒充任何国家历史的实际制度过程。

## 全域穷举与反事实数值
6⁵=**7776**个长度五的人为事件流都由两套独立状态更新程序逐步核算，两个解释器的每一条状态路径都完全相同，共检查每实现38,880个状态转移。最终(r,e)联合状态：
- r0,e0：**7663**条；
- r1,e0：**96**条；
- r1,e1：**17**条；
- r0,e1：0条（严格禁止巩固的改革同时被取消）。
每条历史五处时点均进行 `do(event_t = W)`并单独重跑，**38880次**项目内部成对干预（包括原本W的负对照）。其中最终r变化**373**对，最终e变化**69**对，任何一个变化**388**对，二者同时变化54对。所有按事件/位置分组之和严格相等。没有抽样误差，也没有伪称38880个真实历史样本。

## 相同事件集合、不同顺序的机制
对{O,M,A,E,B}五种不同事件的120种排列，事件总数统计量全部相同，但最终有**116条未改革、4条已改革**，完整状态共有7种：
`OMAEB`（先开启→动员→采纳→巩固→反对）最终r1/e1；`BEAMO`最终r0/e0，虽然两者事件多重集合完全相同。顺序作用在本模型内通过“窗口和先决条件”构造而产生，不构成社会现实中的历史偶然事件已被独立证明。

## 不可由静态观察完全识别的证据
`OMAWW`与`OMAEW`在第五步都保持r1；但是前者e0、后者e1。两者同时再施加B，前者改革被撤销，后者不被撤销。因此“当前看上去存在同一个制度”并不代表隐藏的联盟、保护或恢复机制相同，若只观察单个终点r会发生表象合并。然而本例的`entrenched`是研究者在构造程序中**直接预设和可观察的潜变量**：真正历史研究中是否能独立测到、反事实能否识别仍没有证据，不能以模型可观测性替代真实历史材料。

## 单测、机器证据及科研边界
Python标准库确定性代码 [R144_Mahoney_Capoccia_Kelemen_171_Tests.zip](R144_Mahoney_Capoccia_Kelemen_171_Tests.zip) 完整提供2份Python/全部7776轨迹与120排列结果JSON，含171项unittest（其中120项逐一检查无重复的事件多重集合的不同排序）。一次最初测试失败来自测试错误地传入字符串而非序列元组：代码接口如期拒收字符串；只修正测试入参、不改源状态转移，之后171项本地测试全通过。ZIP SHA256 `34d8d5cbf20aac09dcb0f3438d635eab6fef013bc75381e83b7d8be85811d0a9`；Git ZIP blob `442bfbd29a55d22a848a4bada6c83e6784cd1806`。须在GitHub Actions Python3.11/3.12完成每任务四项SHA256、171真实测试与原JSON逐字节完整复算后再正式CLOSED_BOUNDED。

**未复现论文作者量化模型、未做过程追踪史料采集、没有观测性识别/随机历史试验；新增真人E2=0、历史E3=0。** R073/PESEN v0.1继续冻结。坚持全部既定R先学习完成、再归纳分类、最后熔炼。

## 远端GitHub机器凭据（运行之后追加）

[GitHub Actions run39397216634](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39397216634) 在原始源码commit `21ee3ac9d2d4eba705304573ebe072ae5ed645d4` 真正执行，status completed、conclusion success。Python3.11 job118542806511完成171 tests in 3.016s；Python3.12 job118542806818完成171 tests in 3.464s，合计342次、0失败。两个任务分别先完成Git ZIP SHA256 `34d8d5cbf20aac09dcb0f3438d635eab6fef013bc75381e83b7d8be85811d0a9`、主源码 SHA256 `5abf5a76ead93d073703e0cf7bba3d1a45692250654f68a2a4045e81be5bd573`、测试源码 SHA256 `782ae3958c1b60ad047c73e306cf0d1e1b3c96280f99ab5c2b6756a97748aaeb`、机器原结果 SHA256 `9de14efba003219420451ea3191bc67d1c8e9fb4dc8121186c228754ca2b734e` 各4项检查通过；再执行全部171单测，并重复生产全部7,776条五步序列、38,880个配对do干预和120全排列结果，比对原JSON字节完全一致。真实job日志各打印 `PASS R144 source-bounded 171 tests 7776 histories 38880 paired event substitutions`。详细审计[R144_PHASE_A_342_REAL_TESTS_7776_HISTORIES_38880_COUNTERFACTUAL_CI_RECEIPT.json](R144_PHASE_A_342_REAL_TESTS_7776_HISTORIES_38880_COUNTERFACTUAL_CI_RECEIPT.json)。机器复算成功**只认证合成理论E1**，不涉及原作者真实历史案例E3。
