# R071 正式限定结题：合作规范反馈、昂贵惩罚与制度监测成本

2026-10-16。依据[心理史学研究统一验收 v1](../../protocols/RESEARCH_ACCEPTANCE_STANDARD_V1_2026-10-16.md)，R071 以**完整的自制 E1 群体机制数学反例及真实来源适用性失败记录**限定结题，状态 **`CLOSED_BOUNDED`**。这只表示有限可验收材料与推断边界已齐备，不是所讨论的三个真实人类机制获得经验验证。真人 E2 仍 BLOCKED/NOT_ESTABLISHED，独立 E3 OPEN。

## 1. 问题与最初冻结对象

本研究从三份经典工作中抽取明示机制问题，而不宣称完全重现作者原来的演化/人类实验：Ostrom (2000) `10.1257/jep.14.3.137`（条件合作者与社会规范）；Fehr & Gächter (2000) `10.1257/aer.90.4.980`（公共物品惩罚实验）；Boyd et al. (2003) `10.1073/pnas.0630443100`（有成本惩罚与持续监控对演化的影响）。

[E1 模型初次计算前冻结协议](../../protocols/R071_NORM_COOPERATION_PUNISHMENT_E1_2026-10-16.md) commit `dcf3a0b2e2137cb8f6430a2437b88cb8738b2f08`：单五人组、固定四种抽象角色 C（无条件合作）/D（无条件不合作）/P（固定惩罚人）/N（条件合作与罚款威慑响应），C+D+P+N=5 精确56个无重复组成。门槛0.5或0.75、外生公开初始规范0或1、三个制度 NONE/VARIABLE_PUNISHMENT/FIXED_MONITORING，总计 **672 个不同初态条件、5376 个确定性组回合**，每组8回合。人数不进化、不做学习参数拟合，罚款按**净损耗**而非转移支付；每回合都要求人均公共收益与罚款/监测等式完全闭合。

## 2. E1 真实执行与关键负结果

[GitHub Actions run 38890695079](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38890695079) 整体 success，**28 项**数学/边界/账务反例测试 PASS、真正在 runner 计算完 **672 条条件×8回合**。第二次 [永久归档 run 38890837355](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38890837355) 再运行测试、核实完整输出 SHA256 `bd8bf1dcc97c5ee9c933e889b68ca50a7403f1d1cf05f67f08195a9cf9b280d8`，将 **68,172 字节**的真实生成合成数值永久存入仓库 [R071_E1_COMPLETE_672_NORM_INSTITUTION_RESULTS.json](R071_E1_COMPLETE_672_NORM_INSTITUTION_RESULTS.json)。完整程序 [r071_norm_cooperation_punishment.py](r071_norm_cooperation_punishment.py)，逐项测试 [test_r071_norm_cooperation_punishment.py](test_r071_norm_cooperation_punishment.py)，解释和完整证据见[E1研究报告](R071_E1_NORM_INSTITUTION_FULL_RESULTS_AND_LIMITS.md)。

符合预注册的两个典型反例：(a) 五人全是条件合作者、无惩罚时，初始公开规范0导致八轮全不合作，初始规范1则始终五人全合作；(b) 一名P和四名N、初始规范0时，无处罚仅P合作，而有成本罚款使N响应威慑全部五人合作，固定监测制度即使没有实际处罚事件，P仍在每轮支付1.2费用。另一反例：一名P+四名坚定D，罚款完全不提高贡献人数。此类数学分化不能直接推广人类规范心理。

若固定各56组等权、每组完整8轮平均，`θ=.5/seed=0` 下，无惩罚第8轮合作比例 **0.560714**，变动处罚和监测处罚均 **0.639286**，但对应群体每轮平均净收益分别 **2.765625、2.187500、0.687500**。其根本含义是：**部分合作行为数量增加，不等于这套固定参数/净损耗制度下群体净收益提高**。这只是模型参数、固定抽象角色与收益记账的条件命题，不是惩罚实际福利的跨社会普遍测量。

## 3. 真正启动但因来源和合约受阻的 E2

为了避免在虚构真人经验上推进，已先冻结[Dryad 真数据来源/字段门](../../protocols/R071_E2_DRYAD_PGG_NOISE_SOURCE_APPLICABILITY_2026-10-16.md)，尝试访问 Dryad DOI `10.5061/dryad.n02v6wx03`、真实数据发布页所列 `noisy-PGG.csv`。官方公开元数据记载 384 名参与者/96个四人组完成，其中分析320人/80组，这**不是本项目从原始数据复核得到的计数**。[GitHub Actions run 38891213930](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38891213930) 源安全11项测试 PASS，但文件 HTTP 请求失败，实际真数据作业 FAIL；`SOURCE_UNRESOLVED`，没有建立任何真实原始 CSV SHA256、行数或列名，不能冒充 E2 PASS。另此前 R047 真实公共资源抽取多水平数据虽来源已验证，人数/行为/制度模型与 R071 五人二元贡献同样 **BLOCKED_MODEL_MISMATCH**。[来源候选及失败证据](R071_E2_SOURCE_CANDIDATES_AND_BLOCKERS.md)、[机读匿名失败收据](R071_E2_DRYAD_SOURCE_ATTEMPT_RESULTS.json)。

不改变此前作者发表的公共物品随机惩罚效果，亦不能用发表论文的群体数、性别/国家描述制造项目自己的真实统计。对接受惩罚的人是否因规范或收益混乱改变行为仍没有因果测量；R071 不创造 E3。

## 4. 六门限定研究档案验收

| 项 | 结论 | 理由和永久保留的限制 |
|---|---|---|
| A01 范围与预定义 | PASS | E1完整实验条件在首次结果前冻结；E2 真数据探索有独立先验协议，不因失败后缩小窗口 |
| A02 来源及合法使用 | PASS（限定研究包） | 三份出版社一手 DOI、旧 R047 源证明与新 Dryad 元数据可追溯；Dryad 原件未拿到、真人数据绝不宣称核验 |
| A03 代码与实际运行 | PASS | 28+11 项纯测试，各状态不同；672×8 真正 E1 运行+固定 SHA 永久 JSON；E2 工作流明确 failure |
| A04 负结果 | PASS | 惩罚下合作与福利可方向相反、固定监测成本、D不响应；E2 原件 HTTP 失败、四人/五人合约不等价全部归档 |
| A05 科学推断 | PASS | E1 数学固定类型不能推出人类行为、机构制度有效性、跨时期文化演化；E2 未成、E3 OPEN |
| A06 归档和交接 | PASS | 本文、机读最终状态、SHA 固定结果、原代码与反例、真人源失败和[开放研究门](R071_POST_CLOSURE_OPEN_GATES.md)，GitHub main 可核验 |

六项 PASS 是有界交付包的验收结论，**不是**说本研究原广义问题“制度如何真实导致规范产生”的 E2/E3 已被证明。R071 的完整广义目标没有前置覆盖真人 E2；**现在限定结题是 `RETROSPECTIVE_SCOPE_DECISION`**，不伪称在 R071 启动前便已决定 E1 完成后立即关闭。

## 5. 移交

正式状态 `R071=CLOSED_BOUNDED`；
`R071_E1_SYNTHETIC_NORM_PUNISHMENT=PASS`；
`R071_E2_DRYAD_REAL_SOURCE=SOURCE_UNRESOLVED`；
`R071_E2_HUMAN_NORM_AND_ENFORCEMENT=BLOCKED_MODEL_CONTRACT`；
`R071_E3_EXTERNAL=OPEN`；
`R071_LONG_TERM_CULTURAL_AND_INSTITUTIONAL_CAUSALITY=NOT_ESTABLISHED`；
`PESEN_v0.1=FROZEN`。

下个不同科学家族可新建 **R072：重复博弈中的信誉、社会记忆与制度信号可信度**，以独立可证伪数学假设连接个体信息更新、群体行为和制度约束。真人源获取/现有 R071 规则精确适配留在 [独立开放门](R071_POST_CLOSURE_OPEN_GATES.md)，不能反向修改已经固定的 E1 历史轨迹。
