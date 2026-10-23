# R269 交叉验证：576完整人工原source与分组泄漏反例，正式有界E1结题索引

日期2026-10-23 Asia/Taipei。原目录11-029 Cross Validation（P0）。[先行冻结协议](../protocols/R269_GROUP_VS_ROW_CROSS_VALIDATION_576_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [研究源文件与原CSV](../research/R269/README.md) · [完整科学报告](../research/R269/R269_SCIENTIFIC_REPORT_2026-10-23.md) · [机器正式验收](../research/R269/R269_FINAL_ACCEPTANCE_STATUS.json) · [最终成功Actions run39902238505](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39902238505)。

三种人工p（1/4,1/2,3/4）×三种固定预测模型=九个冻结人工世界，每world六组潜在独立Bernoulli、两条同组完全复制的12行，64条完整原source。合计576条模型标识的人工来源类型；每种p的原组标签在三模型间重复，不能据此计为576独立实验。逐行LOOR保留同组训练复制行，整组LOGO完整排除全部该组。双方每个source评估12行。GROUP_ID_MEMORIZER在LOOR真实折评分恒0，LOGO恒1/4；GLOBAL_LAPLACE三个p对应LOOR/L OGO（这里均实际记录为LOGO）数学期望31/169与31/144，41/169与41/144，31/169与31/144；CONSTANT_HALF永远1/4。

全部逐原source12个预测和12个Brier平方误差保存为CSV，按原概率精确Fraction积分的18个world×fold方案设计期望与独立的Bernoulli(p)×Binomial(5,p)解析式相同。双Python3.11/3.12各83项真单测成功共166项，独立第三来源CSV逐条折训练重建及SHA256审核success，全部三job completed/success，机器永久原source归档[23b88012](https://github.com/edwardsage419/Psychohistory-Research/commit/23b88012cc4811666aa47d51e16f2df3d79e9760)。当前只证明人工组结构下使用正确验证分割的重要性，不包含任何真人E2或真实历史E3外部复制检验，也不影响冻结R073/PESEN。

下个原目录已确认11-030 Posterior Predictive Checks（P1，拟R270）。项目继续按原目录完成R系列，随后统一归纳、分类，最后熔炼。
