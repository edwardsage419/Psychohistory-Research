# R267 拉丁超立方抽样（11-027，P1）

科研状态：**CLOSED_BOUNDED_E1_EXACT_DISCRETE_THREE_LEVEL_LATIN_HYPERCUBE**。九个人工二维三层网格world，原source共**6885种**，每world IID729与独立随机双排列LHS36种，双方都是3次f评价。穷举来源与独立卷积/相对排列两路线的全部18完整估计PMF一致，双向ANOVA残差提供第三方差公式。

[先行冻结协议](../../protocols/R267_LATIN_HYPERCUBE_9_FINITE_GRID_WORLDS_6885_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [计算源程序](r267_exact_discrete_latin_hypercube.py) · [全部6885原source CSV](R267_ALL_6885_ORIGINAL_GRID_SAMPLE_SOURCES.csv) · [九world与18完整PMF结果](R267_EXACT_RESULTS.json) · [SHA256计算凭证](R267_MACHINE_RECEIPT.json) · [正式科学报告](R267_SCIENTIFIC_REPORT_2026-10-23.md) · [机读正式有界验收](R267_FINAL_ACCEPTANCE_STATUS.json)。

三类纯加性函数LHS方差严格0；三种非加性函数（中心化交互、相等事件、模3和）LHS方差是IID的3/2。小样本n=3、离散网格、无连续区间内抖动，与原论文的连续/大样本渐近设置严格区分。

[全三job成功CI run39901198271](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39901198271)，Python3.11与3.12各136个真单测共272通过，第三原source审计通过。全部CSV、JSON、SHA由机器人永久归档到main：[82087648](https://github.com/edwardsage419/Psychohistory-Research/commit/82087648e4be587e156ee32846d4cc83c8cef9fd)。

新增真实人类E2=0、真实历史E3=0，R073及PESEN v0.1均冻结。下一候选原目录11-028 AIC and BIC（拟R268）。原R系列完成前不开始熔炼。
