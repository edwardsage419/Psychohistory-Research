# 心理史学原239项研究续进：R293/R294 有界科学结题及v0.8完整原目录证据审计

日期：2026-10-23 Asia/Taipei。性质：依据冻结协议完成两项有界数学机制研究，与全部239模型科学结题严格区分。用户确认的研究顺序仍是：优先完成全部原R系列研究，随后统一归纳分类，最后熔炼和独立模型。

## 本轮两项新增独立研究

| 项目 | 原目录条目 | 事前冻结 | 完整原人工来源 | Python3.11/3.12主测试 | 三job科学CI |
|---|---|---|---:|---:|---|
| R293 十价值测量与评分风格/中心化 | 01-016 P1 | [44ede9c4](https://github.com/edwardsage419/Psychohistory-Research/commit/44ede9c449b06fa221c51bdbbc2008c5492aed06) | 2112 | 153+153=306 | [run39918965106](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39918965106) 成功 |
| R294 双曲/指数/准双曲跨期偏好反转 | 01-018 P1 | [9c78d082](https://github.com/edwardsage419/Psychohistory-Research/commit/9c78d082902cedffb8ad64159915d8d6f5e12299) | 144 | 583+583=1166 | [run39919476504](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39919476504) 成功 |

R293 [正式科学报告](../research/R293/R293_SCIENTIFIC_REPORT_2026-10-23.md)、[正式JSON验收](../research/R293/R293_FINAL_ACCEPTANCE_STATUS.json)：人工独立的十潜在值分数经共同评分偏移产生原始rho=4/5，减个人十槽均值后rho=−1/9；人工设定的互补对从原始+3/5变成中心化−1。按冻结人工源级分数精确计算全部400协方差元素；这无法证实真实Schwartz1992十类动机环结构、跨国测量等价或真实ESS21量表的相关性。原作者来源：Schwartz (1992) DOI https://doi.org/10.1016/S0065-2601(08)60281-6；(2012) DOI https://doi.org/10.9707/2307-0919.1116；GESIS英文ESS测量 https://zis.gesis.org/s/skala/Schwartz-Breyer-Danner-Human-Values-Scale-%28ESS%29?lang=en。

R294 [正式科学报告](../research/R294/R294_SCIENTIFIC_REPORT_2026-10-23.md)、[正式JSON验收](../research/R294/R294_FINAL_ACCEPTANCE_STATUS.json)：固定72个人工折扣/奖励配置和各2个时点的144选择；双曲30配置中8反转，指数18中0，准双曲24中7。Strotz1955 DOI https://doi.org/10.2307/2295722 和 Laibson1997 DOI https://doi.org/10.1162/003355397555253 为理论一手锚。这些是人为选择的参数格点计数，不能读成真实人类行为频率或储蓄福利预测。

两项均有各自独立的可运行程序、CSV、JSON、SHA256、独立不导入模型的第三来源审计；本轮合计**2256个完全不同标签的人工研究source**，不是2256名真人；双环境模型unit tests实际1472次通过。另R293第三独立审计的13项逆向测试与R294的12项均双环境运行且第三审计独立重放，两次科学CI总计6个成功作业。新增真人E2=0、独立真实历史E3=0。

## 历史R013重复研究风险核验

10月18日旧索引01-016有未经核实的R13相关文献标签。本轮实际重读[R013七成员原ZIP审计JSON](R293_R013_ORIGINAL_ZIP_MEMBERS_SCHWARTZ_EVIDENCE_AUDIT_2026-10-23.json)的原始SHA256和CRC，GitHub [run39918778414](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39918778414)成功，R013主题是预注册指标/受试者单位审计，七原成员未发现Schwartz专属数理机制证据。它不应冒充额外独立Schwartz研究；此有限ZIP核验不能代替其它所有历史档案审计。

## 原239目录主研究证据交叉索引

| 目录状态 | v0.6（R292后） | v0.7（R293后） | **v0.8（R294后）** |
|---|---:|---:|---:|
| 找到候选主研究R关联 | 180 | 181 | **182** |
| 共享已有R数学机制、禁止重复计数 | 3 | 3 | **3** |
| 只有历史范围有限资料关联 | 5 | 5 | **5** |
| 当前核对材料未发现逐条关联 | 51 | 50 | **49** |
| 尚需确立候选主R对应的原模型 | 56 | 55 | **54** |
| 原始候选唯一模型总数 | 239 | 239 | **239** |

[完整v0.8原239模型来源交叉索引](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.8_2026-10-23.json)：相较v0.7仅01-018一行新增R294可溯源人工E1。R293对v0.6只增加01-016一行。所有原始239条的名称、顺序和优先级均保持不变。[当前剩余54项证据队列](ORIGINAL_239_PENDING_54_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv)含P1 **27**、P2 **27**，不因未找到对应链接就判定其从未学习或理论错误。

目录元数据专项第三独立复验：[R293 v0.7 CI39919212609](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39919212609)三job success，Python3.11/3.12各14项真测试；[R294 v0.8 CI39919681224](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39919681224)三job success，Python3.11/3.12各15项真测试，第三核验包括144原来源CSV/结果SHA256。**档案与目录完整不能替代现实实证效度，原239整体研究结题仍NOT_ESTABLISHED。**

## 下一步研究主线

下一原目录P1待审编号是**01-019 Habit Formation**，必须先查早期R001至R064学习材料、习惯模型的真实原作者文献、强化学习重复行为与习惯自动化的测量区别，才能决定R295需要何种独立学习/检验。保持既定R系列→归纳分类→熔炼顺序。R073与PESEN v0.1继续冻结，个人辅助决策系统继续暂缓。
