# R136 第三方法科学报告：四状态马尔可夫链有向树精确复算

日期：2026-10-25。范围：原始 05-012 Direct Reciprocity，既有 R136 Press–Dyson 2012 模型。**本轮正式新 CI 验收未完成，预注册负对照发现设计缺陷。**

## 事前冻结与原始来源
在本轮计算前，第三方法协议已提交：`research/validation/R136_THIRD_METHOD_MARKOV_TREE_PROTOCOL_FREEZE_2026-10-25.md`，commit `5ced86008f01097e08710accd9c3cdc1840030fa`。来源为 Press & Dyson (2012), PNAS, DOI 10.1073/pnas.1206569109；项目已归档的原始数学结果 `research/R136/R136_MATHEMATICAL_RESULTS.json`，Git blob `a1495bc01a71064e190116e2ec71580aa3e8e1f1`，本地执行时经原始字节 Git blob SHA1 校验通过。该来源先前已完成 43 项单测、两个 Python 环境的历史 CI；本轮没有重跑原 ZIP。

## 独立第三方法
新 Python 标准库程序 `research/validation/r136_markov_tree_independent.py` 采用马尔可夫链有向生成树定理：每个四状态根有16棵有向入树，四根合计64棵。对每个根求全部树权重之和，按总权重归一化得到稳态分布。完全独立于既有的 Gaussian 稳态解与 Press–Dyson 行列式程序。

精确 Fraction 结果：
* χ×φ 冻结网格中合法策略14组；每组81种 q；合计1134组敲诈策略收益约束 `sX−1−χ(sY−1)=0`，全部通过。
* Equalizer 81组，Y 收益严格 `5/3`，全部通过。
* 1215组均通过 `vP=v` 和 `Σv=1` 精确检查。
* 两个既有确定性对手 q=(1,1,0,0)、(1,1,1,0) 的全部有向入树权重总和为0，未输出虚假的唯一稳态。
* 归一化错误负对照通过。
* 本地 CSV 1215行，115527字节，SHA256 `c1e5c7680314e8734d6388662aef322b1e03befd7111dd5e5596b2c9c40ee856`；完整 CSV 在本地生成，可用仓库脚本的 `--output` 选项重建。**本轮未将115527字节 CSV 上传至 GitHub**，不能声称远端保存了完整 CSV。

## 冻结负对照的真实失败
原协议要求“故意不交换 Y 的 q2/q3，必须使敲诈收益等式失败”。执行后发现这一要求**数学上不具有鉴别力**：Press–Dyson ZD 条件对任意对手 q 都成立。错误交换 q2/q3 等价于换了一个对手策略，仍满足该线性收益等式。故冻结负对照实际结果为 `FAILED_NONDISCRIMINATING`，严禁计为通过。

具体见证 χ=3、φ=1/20、q=(1/4,1/2,3/4,1/4)：
* 正确 q 排序：X收益 `721/328`，Y收益 `459/328`，ZD 残差0。
* 错误 q 排序：X收益 `3413/1448`，Y收益 `2103/1448`，ZD 残差仍为0。
* 两种稳态与收益不同。事后新增“直接检查转移矩阵差异”诊断可以识别排序错误，已单独标注 `POSTHOC`，不得作为原冻结负对照通过。

## B 子流程独立复算
B 的独立复算协议在执行前另行冻结，commit `ec9e10e9646efab81594ca5d2f4c75ffc8cc8cb2`。独立 Python `research/validation/r136_b_gauss_jordan_replay.py` 不导入树算法，采用精确 Gauss–Jordan 消元，对1215行完整CSV逐行复算稳态、两方收益和约束。实际结果：1134/1134敲诈行一致，81/81 Equalizer行一致，两个奇异条件正确拒绝，逐行差异0。对上面 q 排序反例亦给出完全相同的四个精确收益分数。

## 科学等级与后续
本轮结果属于**有界本地 E1 双算法一致**，原冻结负对照失败使本轮完整协议验收继续开放。状态 `BOUNDED_LOCAL_E1_REPLAY_CONFIRMED_WITH_PRE_REGISTERED_CONTROL_DESIGN_DEFECT`。内部算法独立复核不等于外部团队独立复现。

尚未执行新的 GitHub Actions，未核验新 CI；未新增真人 E2、历史 E3、样本外预测、概率校准、因果估计。没有改动 R073、PESEN v0.1 或 original239。待核队列保持原统计口径。后续应在新冻结协议下修复负对照，再决定是否完成正式验收，旧失败记录必须永久保留。

复现命令：

```bash
python research/validation/r136_markov_tree_independent.py --source research/R136/R136_MATHEMATICAL_RESULTS.json --output R136_MARKOV_TREE_1215_EXACT_ROWS.csv
python research/validation/r136_b_gauss_jordan_replay.py R136_MARKOV_TREE_1215_EXACT_ROWS.csv
```

本轮计算使用本地 Python 3.13.5 标准库。未使用收费 API、GPU、收费数据库或新的付费计算。
