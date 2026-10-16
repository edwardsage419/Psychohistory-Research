# R067：R047 资源提取与新二策略博弈数据的适用性关口

日期：2026-10-16。地位：**在 R067 首次读取并统计该真实原始 CSV 之前冻结**。R067 原数学机制含复制子 Euler、动态 Logit 反应和严格最佳反应，固定囚徒困境/协调支付矩阵的数值 E1 已通过；不允许反向把任意实验数据中的非二元行为重标为这些模型已识别的二策略。

## 候选 A：前项 R047 公共池资源实验

作者仓库 `lrdegeest/InequalityCPR` 固定 master commit `1142b0915a0a46e72264358378b3535948f6b2b4`；原始 CSV `data/data.csv` Git blob `73c02176bc9e060af987149594a85f9f7b591230`、长度 239510 字节。作者 `data/label_main_data.do` blob `?（运行时必须从固定提交检出并记录）`，作者 `theory_payoffs.R` blob `8b6f116b0e1f4b750ceb312a46a0b6f505faf09d`。作者 Stata 源码指出必须只保留前 2048 条有效行，再删 `RoundID == 1` 的练习轮，`FF=1` 为惩罚组，`Homo` 区分禀赋条件，唯一组键 `100*Homo + 10*Session + GameID`。收益函数是连续个人提取量 `x` 与组内其它人的总提取量组成的非线性市场份额，而非某个固定对称 2×2 payoff matrix；理论源码给出了平等禀赋社会最优提取 25、纳什提取 40 等参考点。

**R047 判定标准：** 对哈希固定源检查 CSV 结构、有效记录数、受试者/组/时段数、投入/提取的 distinct 值个数、非整数或越界、在同一组内至少 3 种不同提取量的组数、禀赋和惩罚条件。除非能够在作者来源中找到完全明确的**两个实验动作标签**以及与之配套的固定实验支付矩阵映射，否则 `EXACT_BINARY_2X2_PAYOFF_MAPPING=NOT_ESTABLISHED`。即使恰好某轮只有两种提取值，也不得因此推断本实验总体恰有两个策略。禁止据此拟合 R067 已冻结的固定囚徒困境 payoff 动态或宣布因果效果。对 R047 不允许在本阶段执行未经授权的二值化（如 `Invest<=25` 即“合作”）。

## 候选 B：Montero 等 2022 长期重复囚徒困境

作者正式数据集 Dryad DOI `10.5061/dryad.37pvmcvmk`，[出版的来源页](https://datadryad.org/dataset/doi:10.5061/dryad.37pvmcvmk)。论文 DOI `10.1038/s41598-022-11654-2`，原作者声明 188 人、固定配对或逐轮随机配对两种处理；`R=3,T=4,S=0,P=1`。公开目录列 `fix.csv`、`rand.csv`、`README.txt`、说明文档、个人说明文件。本阶段对该来源只执行可重放**远程目录元数据**核查，不能未经来源字段解析和隐私审计就使用任何参与者级行为。若 API 不通，则标 `SOURCE_NETWORK_OR_API_UNRESOLVED`；不可自动当作数据不存在。

这套真人重复 PD 的原始支付矩阵不同于 R067 E1 教学矩阵 `((3,0),(5,1))`；实际拟合若进行必须独立冻结真实矩阵与真实行为状态协议，**绝不以玩具矩阵冒充实测实验收益**。在原始数据真正获得且行动/伙伴/轮次核实之前，`B_E2_BEHAVIOR=OPEN`。

## 故障优先与最小验收

- R047 固定 Git blob 不符、行列无法复现、group 键冲突：直接 `FAIL_CLOSED_SOURCE`。
- 来源完整且行为支持多值连续提取量：`A_E2_SOURCE_VALIDATION=PASS`、`A_BINARY_PD_MAPPING=BLOCKED_MODEL_MISMATCH`；**这是科学成功识别不适用输入，不是模型失效**。
- Dryad 目录如果可验证，保存 DOI/文件名/格式/字节数/是否受限、数据集版本、公开许可和 API 状态；不把元数据核查提升为数据行验证。
- 两个候选均不得将真实个人 ID、行为行、轮次级小细胞或惩罚目标公开到 GitHub；只归档匿名结构计数、固定字节哈希与源 DOI。

`R067_E2_SOURCE_APPLICABILITY_PROTOCOL=FROZEN`
`R067_E2_MODEL_FIT=NOT_AUTHORIZED_THIS_STAGE`
`PESEN_v0.1=FROZEN`
