# R223 S19 未测混杂敏感性参数误设的252条件精确研究

日期：2026年10月28日。证据等级：有限人工E1。原R223 09-014有限E1正式验收维持不变。

## 冻结来源与方法

计算前协议：`protocols/R223_S19_SENSITIVITY_PARAMETER_MISSPECIFICATION_GRID_PRESCORE_FREEZE_2026-10-28.md`，独立预提交 `8d76c3728ee8e3ae46c20f3ddc29336adc5832f4`。七世界固定输入 `research/R223/R223_EXACT_RESULTS.json` Git blob `3a3f2143357832e25ddf483d7ebd4d66298c5dd1`；原448结构状态CSV Git blob `7a4b6a94332618abe8a8471a656db0353da0ae1f`。网格Gamma_E与Gamma_D分别取1、2、3、5、7、15，共7×6×6=252个精确有理数条件。B=Gamma_E Gamma_D/(Gamma_E+Gamma_D−1)，观测RR下界=RR_obs/B。假设参数的选择是敏感性情景，不能从观察数据估计为真实隐藏混杂。

## 可复算结果

* NULL_CONFOUNDED：观测RR=11/5，真RR=1；36格中下界允许零效应13格；覆盖人工真实混杂参数8格。
* CAUSAL_ALIAS：观测RR=11/5，真RR=11/5；36格中下界允许零效应13格；覆盖人工真实混杂参数36格。
* UNCONFOUNDED_CAUSAL：观测RR=9/5，真RR=9/5；36格中下界允许零效应18格；覆盖人工真实混杂参数18格。
* CONFOUNDED_CAUSAL：观测RR=3，真RR=9/5；36格中下界允许零效应8格；覆盖人工真实混杂参数12格。
* CONFOUNDED_REVERSED：观测RR=1，真RR=3/5；36格中下界允许零效应36格；覆盖人工真实混杂参数12格。
* WEAK_OVERLAP：观测RR=93/19，真RR=9/5；36格中下界允许零效应3格；覆盖人工真实混杂参数3格。
* NO_POSITIVITY：观测RR=6，真RR=9/5；36格中下界允许零效应1格；覆盖人工真实混杂参数0格。

NULL_CONFOUNDED与CAUSAL_ALIAS的全部36格下界及null兼容标记逐项相同，但真实RR分别为1与11/5，构成观测等价而因果不同的完整反例。NULL_CONFOUNDED在Gamma=(3,5)时下界77/75>1，错误的偏小混杂参数会保留看似稳健的正关联；Gamma=(3,7)时下界33/35<1，零效应进入允许范围。原研究的oracle参数为(3,7)。

全部89格具有真实oracle参数覆盖，全部满足下界不超过人工真RR。NO_POSITIVITY世界的oracle参数未定义，覆盖标记为null；其36格仅是假设敏感性情景，无法恢复缺失的U×T观察支持。CONFOUNDED_REVERSED世界观测RR=1、真RR=3/5，null兼容标记不能排除真实保护作用。

## 程序性独立审计与局限

R脚本通过逐格有理数公式生成252行；B脚本采用整数交叉乘积、阈值解析不等式、双轴单调性和观察别名检验，完成1709项核验，失败0项。人为把首格下界改成999后，B程序成功检出差异。归档机器收据保留每世界汇总和独立审计计数。复算方法：使用Node.js运行R脚本并将其JSON结果的rows按固定列导出CSV；B脚本读取原R223结果JSON与归档CSV独立检查。两个脚本均不需要外部依赖。

结果属于固定人工机制的数学审计，缺少真人样本、有限样本置信区间、现实U可测性、现实数据识别与外部团队复现。新增E2=0，E3=0。R073评分规则及PESEN v0.1保持冻结。未运行新增GitHub Actions，CI状态NOT_RUN；未使用计费资源。