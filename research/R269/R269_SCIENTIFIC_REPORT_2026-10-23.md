# R269 正式科学报告：重复群组数据逐行留出泄漏与完整群组留出验证

日期：2026-10-23 Asia/Taipei。原239目录：11-029 Cross Validation（P0）。研究编号R269，证据级别：有界人工数学E1，新增真正人类E2=0、真实历史E3=0。

## 来源与具体研究目标

理论背景：Roberts, D.R. et al. (2017), "Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure", *Ecography* 40:913–929, DOI https://doi.org/10.1111/ecog.02881；Arlot & Celisse (2010), "A survey of cross-validation procedures for model selection", *Statistics Surveys* 4:40–79, DOI https://doi.org/10.1214/09-SS054；scikit-learn LeaveOneGroupOut定义 https://scikit-learn.org/stable/modules/cross_validation.html 。这里实现自建有限群组数学反例，未声称重新使用这些论文的原数据或代码。

问题：若每组两条完全一致的观测，按**单条行**留出可能泄漏组身份，按**完整组**留出时组身份模型失去记忆对象。两种交叉验证对“预测已知群组的下一条观测”和“预测未见群组”分别评估不同目标，不能用前者替代后者。

## 预评分冻结设计

[先行冻结协议](../../protocols/R269_GROUP_VS_ROW_CROSS_VALIDATION_576_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md)，独立冻结GitHub提交[1ba86be0](https://github.com/edwardsage419/Psychohistory-Research/commit/1ba86be0a35b77c0d5e5f6a72bb102ba08c48795)。三个生成概率p∈{1/4,1/2,3/4}，各source有六个独立Bernoulli(p)隐变量Z0到Z5，每组两条相同标签，共12个观测行，实际独立生成单位仅六组。每个p有64个完整原latent序列，以概率p^K(1-p)^(6-K)计权。

固定三种模型：GROUP_ID_MEMORIZER记住训练已知群组id标签，未知群组默认1/2；GLOBAL_LAPLACE对训练全行用预测(成功行数+1)/(训练行数+2)；CONSTANT_HALF始终预测1/2。3p×3模型=9world，逐world64条source，共576种带模型标签的人工来源配置；同p源序列在三个模型间重复使用，所以绝不代表576个独立抽样样本。

LOOR：12个逐行留一折，每折训练11行，包括验证行同组的复制行。LOGO：6个完整group留一折，每折训练10行，验证该组的两个行。12行在两个方案中均各验证一次；以平均Brier=(y−p预测)^2衡量，损失逐source逐row完整归档。LOGO的训练和验证组交集严格为空。

## 两条独立路线与冻结数学真值

路线A针对九world全部576 source实际生成每个训练折，再拟合冻结模型输出每个验证行的预测值和平方误差；来源权重全部Fraction精确归一并积分算设计期望。路线B无来源枚举或折训练：固定目标组真标签B∼Bernoulli(p)，余5组成功数S∼Binomial(5,p)且与B独立，通过数学训练规模写出预测值：
```text
GLOBAL_LAPLACE:
q_LOOR = (2S+B+1)/13
q_LOGO = (2S+1)/12

E[LOOR Brier] = [1+160*p*(1-p)]/169
E[LOGO Brier] = [1+160*p*(1-p)]/144

GROUP_ID_MEMORIZER: LOOR 0; LOGO 1/4
CONSTANT_HALF: LOOR 1/4; LOGO 1/4
```
路线C为独立CI解析CSV逐条检验：576条源有效质量、二元向量互异、12列group与target正确、每种验证折train/test确实分离、同组复制仅在逐行LOO中保留、12条预测和12条loss逐个一致、SHA256正确。所有九world两协议**18项完整设计平均分数**与封闭数学解析路线严格有理一致。

## 冻结九世界最终结果

| p_true | 预测器 | LOOR 平均Brier | LOGO 平均Brier |
|---|---|---:|---:|
|1/4|GROUP_ID_MEMORIZER|0|1/4|
|1/4|GLOBAL_LAPLACE|31/169|31/144|
|1/4|CONSTANT_HALF|1/4|1/4|
|1/2|GROUP_ID_MEMORIZER|0|1/4|
|1/2|GLOBAL_LAPLACE|41/169|41/144|
|1/2|CONSTANT_HALF|1/4|1/4|
|3/4|GROUP_ID_MEMORIZER|0|1/4|
|3/4|GLOBAL_LAPLACE|31/169|31/144|
|3/4|CONSTANT_HALF|1/4|1/4|

若用**设计期望**的LOOR选模型，三种p均毫无争议选择GROUP_ID_MEMORIZER，因为同组复制在训练中，它的损失为0；如果目标是未知组，实际完整组LOGO对该模型为1/4。对p=1/4和3/4，GLOBAL_LAPLACE的LOGO误差31/144，低于记忆器和固定半概率模型的1/4；对p=1/2，GLOBAL_LAPLACE反而为41/144，高于两个恒1/4模型，存在预期相同的两候选。

GLOBAL_LAPLACE的两个方案训练量11 vs10，也影响参数估计；当前有限源无法单独将其误差差异因果分配给泄漏或样本量。因此“分组验证更贴近未见组任务”是在**预定外推对象**与数据依赖关系下得出的，而非“所有组CV分数必须大于所有行CV”的普适定律。

## 真实执行与代码归档

[原生标准库完整代码](r269_exact_group_cross_validation.py) · [576原来源CSV及每行逐折预测损失](R269_ALL_576_ORIGINAL_CLUSTERED_CV_SOURCE_TYPES.csv) · [九world和18项独立解析评分](R269_EXACT_RESULTS.json) · [SHA256机读凭证](R269_MACHINE_RECEIPT.json) · [GitHub Actions run39902238505](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39902238505)。Python3.11与3.12各83项真单测通过，共166项；第三独立来源审计成功，共三作业completed/success。完整原CSV、结果JSON与SHA256永久归档[commit23b88012](https://github.com/edwardsage419/Psychohistory-Research/commit/23b88012cc4811666aa47d51e16f2df3d79e9760)。

来源CSV SHA256 `6bc98c0c07c2a6d48184e6a8643dbd515dfa470ba626a10928d90614ce75155d`；结果JSON SHA256 `d7dda54fdd07148713cd8acbaaafb06bc1282a005b48b09f570211e1a7d4193e`。

## 证据边界及下一研究

目前只证明九人工world精确模型与验证机制的结构性风险；没有实际真人跨场次留出试验，也没有与R073固定模型进行新数据比较，不能从本次数学演示声称历史趋势得到预测。新增E2=0、新历史E3=0、R073及PESEN v0.1继续冻结。原R学习保持优先，下一目录11-030 Posterior Predictive Checks（拟R270），全部原R完成后再统一归纳分类，最后熔炼。
