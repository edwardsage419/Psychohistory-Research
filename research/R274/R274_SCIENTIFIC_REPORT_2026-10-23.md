# R274 正式科学报告：时间顺序留出与事后未来标签回填的预测信息泄漏

日期2026-10-23 Asia/Taipei。原239候选目录12-004 Temporal Holdout Validation（P0），研究R274。科学性质E1有限人工数学计算，没有真实时间序列的独立预测验证。

## 第一理论来源
Roberts et al. (2017), *Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure*, Ecography 40:913–929, DOI https://doi.org/10.1111/ecog.02881 。Cerqueira, Torgo & Mozetič (2020), *Evaluating time series forecasting models: an empirical study on performance estimation methods*, Machine Learning 109:1997–2028, DOI https://doi.org/10.1007/s10994-020-05910-7 。两研究讨论时间序列验证制度和依赖问题；R274是自行构造的时间顺序信息边界反例，未逐字节复现上述论文数据、案例或预测器。冻结人工六次二元源中两时期各自IID，**没有时序自相关**；研究对象仅包括确定的分布变化与未来信息泄漏风险。

## 先冻结协议与9个人工world
[事前冻结协议](../../protocols/R274_TEMPORAL_HOLDOUT_9_SIXBIT_WORLDS_576_ORIGINAL_SOURCE_PRESCORE_FREEZE_2026-10-23.md)，GitHub独立冻结提交[47b75b49](https://github.com/edwardsage419/Psychohistory-Research/commit/47b75b49afb5c72c5ca2599ab38499e0f2856354)。三个生成机制：
* STABLE_HALF：t1至t4真率a=1/2，t5至t6真率b=1/2。
* RISING_RATE：a=1/4，b=3/4。
* FALLING_RATE：a=3/4，b=1/4。

前四个bit仅作为t4预测截止时已知历史，后两bit是真正未来评估。三个冻结政策：
* PAST_ONLY_LAPLACE：t4生成合法事前q=(K+1)/6，K为旧四bit成功数；未来真实标签不改变预测。
* HINDSIGHT_POOLED：非法地把同一未来两个标签J纳入拟合，事后q=(K+J+1)/8，并对相同两个标签评分；明确标记 future_outcomes_illegally_seen_during_fit=True。其较低损失**不可视为真实样本外预测**。
* PRECOMMITTED_HALF：t4之前固定q=1/2，作为可部署基线。

三机制×三政策＝9world，每world完整2^6=64个有序原source，共**576带模型标签完整人工source**；不同模型共享同一原随机配置，绝不表示576个独立真实历史观察。各源的准确质量a^K(1−a)^(4−K)b^J(1−b)^(2−J)，逐未来行损失存CSV。

## 双路线严格复算
路线A遍历全部9×64有序六bit原source，按实际模型协议固定q，逐未来t5/t6预测损失Brier=(Y−q)^2，再按完整来源质量Fraction积分。
路线B不读取原有序source，独立将K∼Binomial(4,a)、J∼Binomial(2,b)的15类联合计数解析概率乘以下式并求和：
```text
future_two_mean_Brier(K,J,q)=
 [J*(1-q)^2+(2-J)*q^2]/2
```
对合法PAST_ONLY及PRECOMMITTED_HALF，q不依赖J；对于HINDSIGHT，q=(K+J+1)/8确实依赖J，因此**禁止将其按未来独立预测器的风险公式重新包装成可实现泛化性能**。两个路线全部9world逐Fraction一致。第三独立GitHub审计从原CSV检查576个原bit/source质量、q、两个未来逐行Brier、漏看未来标记和SHA256，并验证每个过去四bit改变未来标签时非法q发生变化、合法q恒定。

## 精确结论

|冻结时间机制|合法历史Laplace未来Brier|非法未来泄漏拟合Brier|合法预定半概率基线|
|---|---:|---:|---:|
|STABLE_HALF|5/18|27/128|1/4|
|RISING_RATE|55/144|131/512|1/4|
|FALLING_RATE|55/144|131/512|1/4|

STABLE_HALF时合法历史模型5/18大于基线1/4，未来泄漏后却能报告27/128低于1/4。这并不说明未来泄漏具有真实预测能力，因为用于评分的结果已经参与了同一模型的拟合。分布发生结构性上升或下降时，过去训练所得合法Laplace未来损失55/144更大于预定半概率1/4。非法未来拟合131/512与合法预测评分不能进行公平部署排名。

## 真实执行与原资料永久归档
[完整Python原源码](r274_exact_temporal_holdout.py) · [576个原时间来源与逐未来评分CSV](R274_ALL_576_ORIGINAL_FORWARD_HOLDOUT_SOURCES.csv) · [9world精确结果JSON](R274_EXACT_RESULTS.json) · [来源SHA256凭证](R274_MACHINE_RECEIPT.json)。[GitHub Actions run39903501667](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39903501667) 的Python3.11与3.12各82次真单测全部通过，共164次；第三独立逐原来源时间审计和机器人永久归档成功，三job completed/success。全部CSV/JSON/哈希由机器人提交[仓库commit df5ad9d9](https://github.com/edwardsage419/Psychohistory-Research/commit/df5ad9d907fed3fe1c2c17d8d12eb10ad25c081b)。

原source CSV SHA256 `0a4cc5417df9b99284155f74b187ca191d4ac053c0f2c8d339e12968f8d94657`；结果JSON SHA256 `f7ec6f607161d8d8dc72a28fa47cd95611a70b391b87c2d441eed45ef100013c`。

## 边界与后续
本项仅是人工按时间截取的二元实验，没有现实人类行为时间资料、未处理群体互动、事件发生概率、真实自相关或制度外生变化，也没有真正原R073跨实验预测比较。新增真人E2与真实历史E3均0，R073与PESEN v0.1均冻结。下一原239目录12-005 Equifinality Analysis（拟R275）。继续先研究完成全部原R系列，再统一归纳分类，最后熔炼原创模型。
