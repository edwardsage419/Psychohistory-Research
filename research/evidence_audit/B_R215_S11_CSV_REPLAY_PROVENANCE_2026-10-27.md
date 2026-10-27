# R215 S11 独立计算及CSV归档二次重放收据

日期：2026-10-27。前置归档提交 `35fc54511cb4a14f847536fe69de682e8d8261f5`。

从正式GitHub仓库固定文件中核对：R程序Git blob `af2a6c27ddee1ffbeeebdf4d3cba795b1cf6c110`，B程序Git blob `d294956cafa411bbbaa37ef16c6a66bf5c6d9b6c`，36条件CSV Git blob `8b1633bb1e8e10db9196fbc236531d9d9214769e`，均与本地实际执行和生成的字节身份一致。

新增跨路径独立审计入口 `python research/evidence_audit/b_r215_s11_crosscheck.py`，只使用Python标准库。实际本地执行通过：R/B精确有理数字段比较540项，R/归档CSV精确字段比较396项，错误CSV风险值注入检出1项，R内部断言1625项，B解析断言288项，失败0项。该审计入口用于事后比对两条独立算法输出，不参与任何模型拟合、规则选择或R轨主计算。

当前远端CI仍未运行。内部程序性复核不等于外部独立复现；R215正式原验收不变，E1人工限定，E2=0，E3=0，R073/PESEN v0.1冻结。
