# 原239心理史学研究目录：R293 Schwartz基本人类价值模型测量E1闭合与v0.7来源索引

日期：2026-10-23 Asia/Taipei。严格执行用户研究顺序：先完成R系列研究，再统一归纳分类，最后进行模型熔炼。研究当前总目录真实科学结题仍为**NOT_ESTABLISHED**。

## 有界研究成果与文献

原始目录条目01-016 Schwartz Basic Human Values（P1）通过[R293独立研究包](../research/R293/README.md)获得有限人工数学E1证据。原文Schwartz (1992) DOI https://doi.org/10.1016/S0065-2601(08)60281-6，作者本人Schwartz (2012)公开综述 https://doi.org/10.9707/2307-0919.1116；GESTIS/GESIS英文ESS量表手册 https://zis.gesis.org/s/skala/Schwartz-Breyer-Danner-Human-Values-Scale-%28ESS%29?lang=en。后者指出针对不同分析任务正确选择中心化或原始评分的重要性；本轮只研究一个人工例子，**未抓取、拟合或验证真实ESS 21题量表**。

[先行冻结R293实验](../protocols/R293_SCHWARTZ_TEN_VALUE_MEASUREMENT_2112_SOURCE_PRESCORE_FREEZE_2026-10-23.md)，commit [44ede9c4](https://github.com/edwardsage419/Psychohistory-Research/commit/44ede9c449b06fa221c51bdbbc2008c5492aed06)。两个世界合计2112个完整人工来源，独立Bernoulli十槽×响应风格2048行，人工五对互补十槽×响应风格64行，全部精确Fraction验算。

核心结构性风险：潜在独立十维在加入独立共同评分风格后，任意两不同维原始相关为4/5，经个人减全十维平均后为−1/9；人工互补对加入评分风格后从潜在负相关转成原始+3/5，中心化后为−1。以上是**精确概率构造的结果**，不说明真实Schwartz理论十价值的心理冲突强度。内部10×10原始及中心化协方差总共400项由独立程序逐条重算。见[正式R293科学报告](../research/R293/R293_SCIENTIFIC_REPORT_2026-10-23.md)、[完整2112条人工原source](../research/R293/R293_ALL_2112_ORIGINAL_TEN_VALUE_STYLE_SOURCES.csv)、[机器SHA凭证](../research/R293/R293_MACHINE_RECEIPT.json)、[正式验收](../research/R293/R293_FINAL_ACCEPTANCE_STATUS.json)。

[CI run39918965106](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39918965106) 3个job均已completed/success。Python3.11/3.12各153项模型单测及13项独立审计，第三独立审计job重新核对所有2112原source和400矩阵元素，全部原CSV/JSON/SHA永久归档在[commit812d757f](https://github.com/edwardsage419/Psychohistory-Research/commit/812d757f95374495bb732c15d270be4f1de5334f)。新增真人E2、历史E3均为0。

## 历史R013重读和去重边界

旧10月18日知识叠加表的原目录01-016曾记录一个未核实R13文献入口。现[原始R013 ZIP SHA/CRC/7成员逐个全文审计](R293_R013_ORIGINAL_ZIP_MEMBERS_SCHWARTZ_EVIDENCE_AUDIT_2026-10-23.json)，[独立GitHub run39918778414](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39918778414)成功。实际R013原研究主题是预注册指标与受试者单位审计，七个文本成员无Schwartz相关词或价值模型专项源码。因此**不能把R013旧知识标签晋升为01-016完成第二次独立验证**；单份R013未检出也不能证明其它早期所有资料没有相关内容。

## 原目录来源元数据版本对账

| 分类 | v0.6 | v0.7 |
|---|---:|---:|
| 已有候选主R研究来源关联 | 180 | **181** |
| 共享之前模型数学，不新增独立实验 | 3 | **3** |
| 之前范围有限的旧研究关联，无专属主R | 5 | **5** |
| 目前核对材料无逐条模型联系 | 51 | **50** |
| 尚缺确认主R研究关联 | 56 | **55** |
| 原始239个候选模型总数 | 239 | **239** |

[v0.7全239项逐行证据交叉索引](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.7_2026-10-23.json)：相较[v0.6](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.6_2026-10-23.json)只有01-016一条的科研证据元数据改变，其余238项原材料链接保持不变。[下一轮待核55项队列](ORIGINAL_239_PENDING_55_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv)：P1 28项、P2 27项；旧队列仅删除01-016。**181主R关联仍需各自对照E1/E2/E3科研验收，不能写为181真人原论文复现。**

[独立239行、R013原档、2112源SHA审计程序](../research/catalogue_audit/verify_p1_r293_crosswalk_v0_7.py)；[三作业全部成功的v0.7 CI run39919212609](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39919212609)。双Python各14真测试，第三独立source审计重新计算。

## 后续R系列

原目录下一优先缺口为**01-018 Hyperbolic Discounting**，初步理论锚Strotz (1955), *Myopia and Inconsistency in Dynamic Utility Maximization*; Laibson (1997), *Golden Eggs and Hyperbolic Discounting*, *QJE*. 需先查早期研究包、最新原始目录和先前强化学习中的跨期时间折扣应用，确认有界补缺范围。R073和PESEN v0.1继续冻结；不得用合成时间偏好直接推出真实历史预测，个人辅助决策工具仍暂停。
