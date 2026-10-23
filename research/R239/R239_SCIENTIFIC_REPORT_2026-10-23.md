# R239 定性比较分析：九人工crisp-set QCA世界、144完整原来源、有限多样性与充分条件非因果识别

日期2026-10-23（Asia/Taipei）。原239目录 `10-013 Qualitative Comparative Analysis`（P2），科学状态 `CLOSED_BOUNDED_E1_CRISP_QCA_FINITE_TRUTH_TABLE_IDENTIFICATION`。全部E1有限人工布尔构造；不包含真实国家、制度、历史事件、跨区域社会观测，真实人类E2/真实历史E3新增0。R073与PESEN v0.1始终冻结。

## 原著、研究边界与先冻结审计

Ragin (1987), [*The Comparative Method: Moving Beyond Qualitative and Quantitative Strategies*](https://www.jstor.org/stable/10.1525/j.ctt1pnx57)，原书由 University of California Press 出版，提出布尔配置比较法并强调不同组合路径。Schneider & Wagemann (2012), [*Set-Theoretic Methods for the Social Sciences*, 第六章](https://doi.org/10.1017/CBO9781139004244.009) 以无观测配置说明真值表的逻辑余项与有限多样性，且需要区分有社会证据和未经经验检验的配置。Baumgartner & Thiem (2020), [*Often Trusted but Never (Properly) Tested: Evaluating Qualitative Comparative Analysis*](https://doi.org/10.1177/0049124117701487) 对QCA的真实因果发现评价提出重要方法争议与设计要求。本R没有复算这些作者的任何真人或历史案例，也不采用未验证的因果解释。

[模型源产生前冻结协议](../../protocols/R239_QCA_9_WORLDS_144_FULL_CONFIGURATION_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md)永久提交 [af9ead71](https://github.com/edwardsage419/Psychohistory-Research/commit/af9ead7125b7a46a7dffc79b1f080ff6a69bc94d)，然后才提交Python原生算法、CI工作流及完整来源。九机制、真值表阳性一致性阈值、逻辑余项处理及因果干预结论均先冻结，评分后未修改。

## 九世界完整外生来源、观测与自编QCA算法

每个人工世界四独立二元外生源`X,B,C,U`，完整16种类型，全部1/16质量、九世界**144条完整原来源**。实际配置条件 A、B、C 中，通常`A=X`，两别名世界特意令`A=U`；Oracle结果由冻结布尔结构函数f(A,B,C,U)取得。实际QCA观察只包含在案`S=1`的A/B/C/Y，不读取隐藏U与Oracle干预结果；有限多样性两世界设置S=0当A=0且C=1，未入选的完整原来源仍保存，观察Y明确记录−1“缺失”，绝不把它冒充Y=0。

独立配置统计以八行真值表记录每配置的正/负被选择原来源行数、正例一致性比率，空行标`remainder`且一致性**null**，同一配置同时有Y=0/1的矛盾行标`contradictory`。阈值=1才允许阳性配置；二元充分性一致性`Pr(Y=1|X=1,S=1)`，必要性一致性`Pr(X=1|Y=1,S=1)`，分母无支持时返回null不填零。三条件所有27种don’t-care子立方完整枚举，精确最小DNF集合覆盖DP以“最少项数→最少字面量→词典序”的固定顺序决定表达式；保守模式不允许覆盖逻辑余项、简约模式允许但不把余项当经验事实，均不可覆盖实际阴性或矛盾配置。全部用整数/Fraction，无浮点阈值。

**算法与证据界限：** 源行经完整原概率算观察结果，独立解析路径从冻结结构函数在全部B/C/U八个状态重算do(A=1)减do(A=0)总体因果oracle，逐九世界相符。额外把DNF逐一应用在八个布尔配置上，正行必被覆盖、负/矛盾行必不被覆盖（余项根据模式分隔）。但最小DNF是一种对已观察真值表的配置摘要，并非现实世界充分因果律验证。

## 九个人工世界的最小观察配置与真正因果效果

记`A`等指存在、`¬A`指不存在、`∨`析取、`∧`合取，以下“最小配置”只是**被冻结人工源中已观察记录的精确布尔描述**。

| 人工世界 | 被选原源 | 逻辑余项 | 矛盾行 | 保守最小观察阳性DNF | 人工真do(A)平均效应 |
|---|---:|---:|---:|---|---:|
| AND_AB | 16 | 0 | 0 | A∧B | 1/2 |
| OR_AB | 16 | 0 | 0 | A∨B | 1/2 |
| EQUIFINAL_AB_OR_NOTA_C | 16 | 0 | 0 | (¬A∧C)∨(A∧B) | 0 |
| CONTRADICTORY_A_XOR_U | 16 | 0 | 8 | 无100%一致阳性配置 | 0 |
| LIMITED_A_AND_B | 12 | 2 | 0 | A∧B | 1/2 |
| LIMITED_UNSEEN_BRANCH | 12 | 2 | 0 | A∧B | 0 |
| ALIAS_A_CAUSAL | 16 | 0 | 0 | A | 1 |
| ALIAS_U_CONFOUNDED | 16 | 0 | 0 | A | 0 |
| NEGATED_A_AND_C | 16 | 0 | 0 | ¬A∧C | −1/2 |

**未观察配置与真值表潜在歧义：** LIMITED_A_AND_B与LIMITED_UNSEEN_BRANCH的源生成机制分别为`Y=A∧B`及`Y=(A∧B)∨(¬A∧C)`。对于**真正选择入表的12个来源**，两个世界的配置A/B/C、记录Y、选择标记及原概率完全同分布，八行中两行A=0,C=1均为完全无结果的逻辑余项，保守/简约最小可见DNF都为A∧B。**但在两个未观察配置上**，后者实际Y=1而前者Y=0；后者按人工do(A)平均真实效应0、前者1/2。这个有限反例准确说明在缺少观察支持时，依据已见配置推出的“实际社会成功路径”不能不经其他来源就合理覆盖逻辑剩余行。没有假装从后者隐藏Oracle真值推得QCA观察可识别。

**同样的充分/必要证据对应完全不同因果效果：** ALIAS_A_CAUSAL在真实机制中A=U但结果Y=A，ALIAS_U_CONFOUNDED中同样A=U、结果Y=U。两世界对全部16个原X/B/C/U来源逐源产生**完全相同的实际A/B/C/Y**，全部八配置与完整可观察联合概率逐格严格一致；两者在观察中A都是Y的100%充分及100%必要集合条件，最简DNF同为A。但是冻结人工oracle`do(A)`真的在前者改变Y（平均效果1），在后者不能改变Y（效果0）。关键反例的边界是A=U的结构造成给定U后A根本没有对照变动支持；并非证明拥有额外随机干预证据或真实重叠时QCA永远不能辨认因果路径。

**矛盾行不会自动变成不存在正例：** CONTRADICTORY_A_XOR_U里结果Y=A XOR U，隐藏U条件下每个已见ABC配置正例与负例各一，八个配置的一致性都为1/2，严格100%阈值没有任何“可靠阳性配置”，最简DNF空。然而全部源中仍有Y=1的真实发生率1/2，不可解释为结果从不发生。改变阈值或纳入额外可靠条件U会形成不同可检验研究，本文没将此模型隐条件加入实际观察QCA。

**组合多路径与反向非对称：** EQUIFINAL_AB_OR_NOTA_C的阳性是两条条件路径的析取，且A因正负配置出现可能使平均do(A)效应0，即使个别ABC配置中干预Y不同。NEGATED_A_AND_C的结果只在¬A且C时发生，观察最简配置为¬A∧C，干预A平均效应−1/2。这明确把集合描述、必要/充分、平均因果效果等**不同逻辑目标**分开。

## CI、全源永久档案与正式资格

[纯标准库Python源码](r239_exact_crisp_qca.py) · [全部144原配置结构来源CSV](R239_ALL_144_ORIGINAL_CONFIGURATION_CAUSAL_SOURCES.csv) · [九世界全部真值表/最小DNF/真实干预结果JSON](R239_EXACT_RESULTS.json) · [原来源SHA机读凭证](R239_FINAL_MACHINE_ACCEPTANCE.json)。

[GitHub Actions run39887152751](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39887152751)总体completed/success，三个job均completed/success，Python3.11/3.12日志各`Ran 85 tests`、`OK`，合计**170次真实单测执行通过**。第三作业独立核验全九世界144完整原X/B/C/U来源概率1/16、原总质量1、完整八配置真值表、有限两行逻辑余项、8个矛盾行、两个完全观察别名、一致性与必要性及干预oracle差别、输出文件SHA，实际日志输出`R239_ALL_144_QCA_COMPLETE_SOURCES_AND_LOGICAL_REMAINDER_CAUSAL_ALIASES_VERIFIED`；机器人永久保存完整源数据与结果到main，提交[bdf60072](https://github.com/edwardsage419/Psychohistory-Research/commit/bdf60072f0f77a3cb953125c81f5c3395e0b45c1)。

全部原CSV SHA256 `c8263f4b21afe819976d6b7978604592248f7717439e5f5b035e42ef035195bd`，结果JSON SHA256 `33fba6344a0ce4bb90d5df050f97538e45793f5009d38de1ad5db4fcda6f66f5`。

本研究严格限于有限crispset QCA，未真实调查社会配置、没有时间外预测、制度干预、自然实验或历史适用性。新增真人E2=0/真实历史E3=0。R073/PESEN v0.1冻结。下一原目录 `10-014 Inter Coder Reliability Models`（R240），之后跨入 `11-001 Ordinary Differential Equations`；遵守全部原R结束后分类再熔炼。
