# R286 S82 科学报告：奖励序列相关性改变 TD(0)、MC 与更新顺序的留出风险

日期：2026-10-30 UTC。新增研究范围：冻结于 main commit `c625031ce3e62ee772eb3567b906199e21a3f6f0` 的 R286 S82 Markov 奖励依赖。原 R286 2026-10-23 有界 E1 正式验收保持原状。本轮结论为 INTERNAL_NONBLIND_EXPLORATORY_E1，新增 S82 科学验收 PARTIAL。

## 来源与设计
原始理论：Sutton (1988), Learning to Predict by the Methods of Temporal Differences, DOI https://doi.org/10.1007/BF00115009；原 R286 固定来源为 `research/R286/r286_exact_td0_learning.py`、原冻结 `protocols/R286_TD0_TWO_STATE_5_EPISODE_3_POLICY_576_ORDERED_SOURCE_PRESCORE_FREEZE_2026-10-23.md`。原学习率1/2、两个非终止状态、五训练奖励、第六完全留出奖励、三算法更新顺序不变。S82 将奖励从 iid Bernoulli(1/2) 改为平稳二态 Markov，P(Yt=Yt-1)=s∈{1/4,1/2,3/4}，rho=2s-1。每 s×算法 64 个完整六位来源，总576条带算法标签人工来源，均保存原始位序、来源质量、VA5、未来奖励和平方损失。没有任何真人观察。

## 全部精确未来 Brier 风险
|相邻奖励保持概率 s|相关 rho|标准在线TD0|完整回报MC|先B后A的另一算法|固定1/2预测基线|
|---|---|---:|---:|---:|---:|
|1/4|负1/2|33/128 = 0.2578125|205/512 = 0.400390625|2557/8192 ≈ 0.312134|1/4|
|1/2|0|155/512 ≈ 0.302734|683/2048 ≈ 0.333496|2445/8192 ≈ 0.298462|1/4|
|3/4|1/2|75/256 = 0.29296875|227/1024 ≈ 0.221680|1957/8192 ≈ 0.238892|1/4|

相同的算法、训练长度、单期奖励边缘概率和评分规则下，风险排序发生三次变化：负相关时三算法中 TD0 最优；独立奖励时先 B 后 A 最优；正相关时 MC 最优。常数 1/2 基线在 s=1/4 和 s=1/2 的九策略对照中优于三个学习规则；s=3/4 时 MC 与先 B 后 A 优于常数基线。该结果说明时序相关性影响有限样本预测风险，不能据此断定哪种算法更符合真实人类学习。

## 数学复算
R 路线：对每 s×算法的 64 个有序 Y1..Y6 来源逐期运行学习更新，仅使用 Y1..Y5，计算 (Y6−VA5)^2，按平稳 Markov 来源概率加权。B 路线：独立使用原 R286 的系数向量 c 与 Cov(Yi,Yj)=rho^|i-j|/4，计算
`R=1/4+(1−sum(c))²/4+(sum_ij c_i*c_j*rho^|i-j|)/4−(sum_i c_i*rho^(6−i))/2`。
9组精确 Fraction 相等；s=1/2 的三组风险与原 R286 的冻结风险逐项一致。全部来源总质量每组为1；第六位从未进入训练。主 Python 源码本地原生命令行 `--test`、`--emit` 均 exit 0，生成576行 CSV 与9组 JSON。本轮脚本在 Python 3.11 以上标准库运行；实际执行环境 Python 版本见 B 报告。

## 验收边界
A01 问题与范围 PASS；A02 原始 R286 冻结与来源 PASS，S82 全人工；A03 本地 Python 原生命令行 PASS，远端重新下载并逐字节重放尚待核验；A04 负例由 B 独立检查器测试，详见 B 报告；A05 E1 限定 PASS；A06 新增 S82 正式验收 PARTIAL。未进行真正外部团队复现；真人 E2 预测0，历史 E3 预测0。R073 模型及评分规则和 PESEN v0.1 冻结。GitHub Actions 未触发，免费额度及实际账单未独立核验。

新增材料：`research/validation/r286_s82_markov_reward_exact_20261030.py`、`research/validation/R286_S82_ALL_576_MARKOV_REWARD_SOURCES.csv`、`research/validation/R286_S82_EXACT_RESULTS.json`。下阶段先核对远端完整文件身份，再检查 R287 原有冻结研究与未覆盖的互补问题。
