# R254 随机矩阵与谱方法（原11-014，P2）

九个人工三节点**有限随机对称正/带符号边权矩阵**，18432完整六边bit×三seedbit×四时点来源，正式科研状态`CLOSED_BOUNDED_E1_FINITE_THREE_NODE_RANDOM_SIGNED_SPECTRAL_METHODS`，不是大维随机矩阵定律或真人网络扩散经验。

[先行冻结](../../protocols/R254_SPECTRAL_RANDOM_TRIANGLE_9_WORLDS_18432_COMPLETE_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [正式科学报告含失败CI保存](R254_SCIENTIFIC_REPORT_2026-10-23.md) · [原生整数谱与独立walk源码](r254_exact_signed_spectral.py) · [18432完整原来源](R254_ALL_18432_ORIGINAL_SIGNED_SPECTRAL_SOURCES.csv) · [全部world谱期望JSON](R254_EXACT_RESULTS.json) · [完整SHA256原source机器收据](R254_FINAL_MACHINE_ACCEPTANCE.json) · [正式有界验收](R254_FINAL_ACCEPTANCE_STATUS.json)。

关键：三边无向signed邻接矩阵`det(lambda I-A)=lambda^3−(a²+b²+c²)lambda−2abc`；p=1/2独立开边正权与一负边signed世界每原source rho²相同、E rho²=13/8，但E最大代数实特征值从`5/8+(3/8)√2`降至`1/2+(3/8)√2`，差1/8。有限三点演示不能说明真正大网络临界阈值或真实传播。

[最终CI run39896198396](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39896198396)三job全success，Python3.11/3.12各83真测试共166通过；完整原source/JSON/SHA机器人归档[7c5cb714](https://github.com/edwardsage419/Psychohistory-Research/commit/7c5cb71403cf22308741e26720daed79f021eafb)。首轮审计CSV字符串类型错误致CI失败，保留原失败run39896118162并只修审计、不改数学机制。新人类E2/历史E3=0。下一11-015 Graph Laplacian（R255）。
