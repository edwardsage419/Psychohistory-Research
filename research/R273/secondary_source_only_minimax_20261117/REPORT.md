# R273：仅来源群体可见时的跨群体预测风险锐下界

日期：2026-11-17。正式目录 P0/12-003，R 系列 R273。证据性质：原冻结人工 E1 的事后探索性数学扩展。本轮没有修改原模型、冻结协议、1728 行来源、27 世界评分或历史验收等级。

## 一、资料、来源及研究去重

原 R273 已证明三种预测器在独立跨群体 Bernoulli 目标上的 Brier 风险。2026-10-30 R273 S69 另研究两目标测试 bit 的有限配对排名错误。本轮选取此前没有正式审计的来源与目标分布不可区分条件及最坏情形数学下界，避免重复旧评分或 S69 排名分析。

固定来源：
* protocols/R273_CROSS_POPULATION_27_WORLDS_1728_COMPLETE_SOURCES_PRESCORE_FREEZE_2026-10-23.md，Git blob d4a861f07dff96a0055cebaf107e785ee6f0b110，事前冻结提交 91abafba...。
* research/R273/R273_ALL_1728_ORIGINAL_CROSS_POPULATION_SOURCES.csv，Git blob ef22eb3c74f3aafdb24ea26153123329755d18e7，SHA256 b4f417d0b218fd1aaa9082ab7a49e52675df59af9fd80841e74888b31dcd6d52。
* research/R273/R273_EXACT_CROSS_POPULATION_RESULTS.json，Git blob 4db10236ea9c07a8aa17684f421e9a3a89d9a708，SHA256 1f1e35d20ddd486bb7d71c65cea96e9590912268c93f17ad1ec99b7f6ac463b8。
* 理论背景沿用原 R273 已注明的 Yarkoni (2022) DOI 10.1017/S0140525X20001685、竞争解释 Lakens 等 (2022) DOI 10.1017/S0140525X21000340，以及 Bareinboim 与 Pearl (2016) DOI 10.1073/pnas.1510507113。本轮没有重新阅读论文全文，不把本项目的人工定理归给上述作者。

## 二、新的理论问题与严格证明

来源 A 提供四条相互独立的 Bernoulli(a) bit，a∈{1/4,1/2,3/4}。目标测试 Y 独立于来源，Y∼Bernoulli(b)，b∈同一集合。学习器允许访问全部来源 bit，甚至已知来源真率 a，并可使用与 b 独立的随机种子 U。预测概率 q=q(X,U)∈[0,1]，严格不访问任何目标侧标签或其他透露 b 的信息。

给定固定 a，若 b=1/4 或 b=3/4，来源数据 X 的完整分布都是同一个 Bernoulli(a) 四重乘积。因而来源数据和源侧随机预测 q 的联合分布在两个目标环境下完全相同，不可能根据来源样本区分这两个环境。

独立未来目标的期望 Brier = b(1-b) + E[(q-b)^2]。将相对于完全知道 b 的理论 oracle 的超额风险记作 G_b = E[(q-b)^2]。对两个对称目标：

\[
\frac{G_{1/4}+G_{3/4}}{2}
=E[(q-1/2)^2]+\frac{1}{16}\ge\frac{1}{16}.
\]

因此 max(G_1/4,G_3/4)≥1/16。固定预测 q=1/2 对 b=1/4、3/4 的超额风险各为1/16，对 b=1/2 为0，故

\[
\inf_{\text{仅来源数据的 }q}\max_{b\in\{1/4,1/2,3/4\}}G_b=\frac1{16}.
\]

该界限是严格可达的 sharp minimax 超额风险。等号要求 q=1/2 几乎处处成立，否则平均平方差严格为正。证明也适用于仅依赖来源数据和与目标 b 独立的内部随机化算法。增加目标侧信息、引入与 b 有关的先验、改变目标候选集合或评分规则，均可能改变结论。

固定半概率预测器是本轮额外的数学基线，原冻结 R273 模型依旧只有 SOURCE_ORACLE、SOURCE_LAPLACE 和 TARGET_ORACLE。TARGET_ORACLE 需要不允许来源预测器访问的真 b，因此不参与来源侧 minimax 策略集合。

## 三、准确数值对照

下表为真实目标 oracle Brier 风险 b(1-b) 以上的超额风险，并非原归档中的完整 Brier。最坏值仅对 b∈{1/4,3/4} 求最大，加入 b=1/2 也不改变最大。

| 来源 a | 来源可使用的预测器 | b=1/4 超额 | b=3/4 超额 | 最坏超额 |
| --- | --- | ---: | ---: | ---: |
| 1/4 | SOURCE_ORACLE | 0 | 1/4 | 1/4 |
| 1/4 | SOURCE_LAPLACE | 1/36 | 7/36 | 7/36 |
| 1/4 | 事后 CONSTANT_HALF | 1/16 | 1/16 | 1/16 |
| 1/2 | SOURCE_ORACLE | 1/16 | 1/16 | 1/16 |
| 1/2 | SOURCE_LAPLACE | 13/144 | 13/144 | 13/144 |
| 1/2 | 事后 CONSTANT_HALF | 1/16 | 1/16 | 1/16 |
| 3/4 | SOURCE_ORACLE | 1/4 | 0 | 1/4 |
| 3/4 | SOURCE_LAPLACE | 7/36 | 1/36 | 7/36 |
| 3/4 | 事后 CONSTANT_HALF | 1/16 | 1/16 | 1/16 |

SOURCE_ORACLE 即使完美知道来源真率，在来源率为 1/4、目标率为 3/4 的情形下仍有 1/4 超额风险。Laplace 将极端来源概率向 1/2 收缩，最坏值下降至 7/36，但仍高于 sharp 1/16 界限；当来源率为1/2，其额外参数估计方差导致 13/144 超额。这不构成现实普遍采用常数半预测的建议，该方法只在已明示的目标集合与最坏情形评分准则中达到最优。

## 四、实际数学重算与原生 CI

研究源码：research/R273/secondary_source_only_minimax_20261117/verify.js。只用 Node 内置库及 BigInt 有理数，不导入原模型生成器。

实际完整检查：
1. 1728 行原世界和有序六bit来源、四条训练/两条目标成功数、联合生成概率、原三预测器输出、训练与目标每行 Brier、均分和系统偏差，逐行精确一致；
2. 27 冻结世界各64条来源的质量总和均为1，目标 Brier 与原归档 JSON 及独立矩公式完全相等；
3. 来源四bit 类型在目标 b=1/4、1/2、3/4 下的边际概率一致，共 144 项；
4. 对 3 个来源 a、两个目标极端和 3 个来源可用候选 q 的超额风险与平方恒等式逐项验证；
5. 错误来源概率、替换整个来源 CSV 的哈希篡改，均触发明确拒绝。

本轮用隔离 V8 JavaScript 直接读取已归档完整 CSV 与 JSON，完成第一条精确解析；独立使用本地 Python Fraction 的 Binomial(4,a) 五组计数积分检查三个来源概率下的全部模型边界数值。另在 GitHub Actions 标准 ubuntu-24.04 的 Node 22 和 Python 3.11 实际执行所提交的代码，并在 CI 中使用独立 Python Fraction 再核验18个边界风险单元格。

**实际成功 CI**：[44035277277](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/44035277277)，job 133876573726，head aab3efc221f1087a0585035643e2af1eec1d4b08，completed/success。日志信号：

* R273_MINIMAX_1728_SOURCE_27_FROZEN_WORLDS_PASS
* R273_SOURCE_ONLY_TWO_TARGET_1OF16_SHARP_BOUND_PASS
* R273_SOURCE_SHA256_MUTATION_REJECTED

此前 [44035175824](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/44035175824) 为真实 FAILURE。原因是故意修改的数值 728/4096 可以约分，先触发分数规范化拒绝，而测试强制预期进入概率质量错误。后改为规范但概率错误的 731/4096，确认准确走到质量校验拒绝路径。没有隐藏失败历史，也没有将失败当作科学数据矛盾。

## 五、证据等级及未闭合事项

**COMPLETE_BOUNDED_INTERNAL**：人工源 1728、原 27 world 复算、完整来源边际不可区分和 sharp minimax 证明、额外数学基线、独立 Python 算术与真实 Node/Python CI、负向控制。

**NOT_RUN**：外部科研团队独立复现、真人跨群体留出 E2、跨时期历史预测 E3、R073 冻结策略第二真人数据验证、因果迁移或个人产品开发。

**UNCHANGED**：原 R273 CLOSED_BOUNDED_E1_ARTIFICIAL_CROSS_POPULATION_TRANSFER，原目录 12-003 P0 待核状态，R073/PESEN v0.1 冻结及全部科研验收门槛。新增 E2=0、E3=0，正式待核队列减少0。GitHub 公有仓库标准只读 CI 未调用收费服务或 API，实际账单未读取。

下一项高价值 R 主线任务仍是寻找可合法使用的独立真人跨环境行为数据并检验其是否满足冻结协议；另需继续 R272 既有正式生产门槛独立裁定。这两项都未因本人工数学结论自动闭合。
