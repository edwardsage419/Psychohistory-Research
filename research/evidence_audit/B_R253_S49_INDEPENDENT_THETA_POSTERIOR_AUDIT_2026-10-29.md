# B轨：R253 S49隐藏theta前缀预测的内部独立数学复算

日期：2026-10-29。审计目标为事前冻结的 `protocols/R253_S49_PREFIX_THETA_BRIER_PRESCORE_FREEZE_2026-10-29.md`，冻结commit `6c8eb57593aa2940db246409ecccc88602543cfe`。所有输入是人工E1；原R253正式验收不变。

## 两条实际运行的独立路线

R路线用 [Node.js原CSV脚本](../validation/r253_s49_prefix_theta_brier_source_20261029.js) 读取4608条完整原来源，核验源SHA256 `42e19a1d3f8a70ded77b3634d4b48eb8a3326eab0bda2f8b5a5ece3bf0b54d45`，逐世界检查512个九bit源键、等权、原信号阈值、四个公开行动及真实隐藏行动。按前缀分组的theta整数计数直接计算 `sum(n0*n1/(512*(n0+n1)))`，BigInt有理数不使用浮点近似。输出 [精确机器收据](../validation/R253_S49_PREFIX_THETA_BRIER_EXACT_RECEIPT_2026-10-29.json)。

B路线用 [独立Python Fraction程序](b_r253_s49_independent_signal_likelihood_20261029.py)，完全绕过R路线的CSV、阈值源生成器和条件频率函数，从二元theta与四个私人信号的32种理论组合出发，分别按各world q生成精确联合概率 `(1/2)×product(q or 1-q)`，再独立生成公开行动及条件后验。q=1时仅两个正质量组合，其他零支持组合不计入条件概率。Python程序已在本地命令行实际执行。

## 实际比较与负例

九个世界×五个前缀风险 = 45项，九个世界×四项相邻增益 = 36项，共81项跨路线精确Fraction比较，失败0项。Bayes/硬编码/伪报告器及模仿/共同信号两组观察别名的全部风险完全一致。所有世界的无信息风险均为1/4，信息增加后风险单调不升。

负例1：将独立比较器的一项正常风险改成999，Python比较器实际拒绝，`mutation_rejected=true`。负例2：在本地重新生成的原CSV中修改一个公开动作，Node脚本在SHA256入口拒绝。负例3：把真实theta加入预测信息，理论风险恒为0，明确排除在45项合法评分外。

原R253 CSV在本地由冻结原生成器重构，得到382667字节和与远端归档一致的SHA256。已对该字节相同副本执行Node命令行完整源审计。GitHub原始文件通过只读连接器重新核对Git blob `64920e410d5e6550f9a41d8b03f8300320a9a5bf`；原文件本身没有被修改或重新提交。

## 证据资格

`INTERNAL_CROSS_METHOD_EXACT_PASS`。这是同一项目内部、不同语言与不同数学路线的程序性复核，外部独立研究团队复现=0。由于完整总体及真实theta已知，校准是oracle条件概率的数学恒等性质；没有独立样本、置信区间、样本外预测、经验概率校准或人类认知识别。E1=1项有限补充，新增E2=0，新增E3=0。R073及PESEN v0.1冻结。新增GitHub Actions是否运行应以提交后的远端核验为准；本审计未请求收费CI。
