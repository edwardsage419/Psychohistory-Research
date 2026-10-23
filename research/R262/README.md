# R262 元胞自动机（原11-022，P1）

九个冻结**一维二元最近邻同步元胞自动机规则，7格周期环**，每world完整128原7bit初态×5时点，九world共**5760完整原source**，严格人工E1科研资格`CLOSED_BOUNDED_E1_SEVEN_CELL_PERIODIC_ELEMENTARY_CA_COMPLETE_INITIAL_STATES`。

[预先冻结协议](../../protocols/R262_ELEMENTARY_CA_9_RULES_SEVEN_RING_5760_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [完整科学报告](R262_SCIENTIFIC_REPORT_2026-10-23.md) · [整数规则位移与独立真值表源码](r262_exact_elementary_ca.py) · [全5760原初态×时点CSV](R262_ALL_5760_ORIGINAL_SEVEN_RING_CA_SOURCE_ATOMS.csv) · [九world像集/固定点/五时点密度JSON](R262_EXACT_RESULTS.json) · [完整SHA256机器收据](R262_FINAL_MACHINE_ACCEPTANCE.json) · [正式有界验收](R262_FINAL_ACCEPTANCE_STATUS.json)。

规则90在七格128均匀原初态上一步只有64种全七bit像，每像两个原前像且整体parity必偶，因此Shannon初态熵7bit→一步状态熵6bit；规则150一步128像，完全一一对应，保存parity，但二者所有五时点的原初态均匀平均1密度同为1/2。规则170右移和240左移在同一原初态上所有时点1总数完全相同，t1时全七维空间状态却在126/128非均匀初态中不同。有限R30/R110的像集和密度不能冒称无限格混沌/普适性或历史演化发现。

[CI run39899036629](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39899036629)三个job成功，Python3.11/3.12各82真实测试共164通过，全部5760原CSV/JSON/SHA bot永久main提交[59f984ad](https://github.com/edwardsage419/Psychohistory-Research/commit/59f984ade41f22cfa2efd16a0584c2a54bd15bd2)。新真人E2/历史E3=0，R073/PESEN v0.1冻结；下一原目录11-023 Genetic Algorithms（R263）。
