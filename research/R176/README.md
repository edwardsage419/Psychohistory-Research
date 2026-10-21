# R176 长时段主体模拟：96个四主体制度模型的精确验证

**2026-10-21正式科研状态：CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_FINITE_ABM。** 原239候选目录 P2/07-018 Long Run Agent Based History，属于第07分类的最后一个研究条目。

[冻结协议](../../protocols/R176_FOUR_AGENT_INSTITUTION_96_LONGRUN_EXACT_ABM_PRESCORE_FREEZE_2026-10-21.md)先于评分永久提交，研究独立设计的四人工代理遵守规范行为及二元制度滞后反馈，2×2×2×2×2×3=**96个人工世界**；各自13期，聚合十个(k,J)完整联合状态，合计**12480个准确有理数概率单元**。两套完全不同的计算路径（四人身份层32状态直接枚举与聚合层10状态二项分布卷积）在全部样本世界中每状态每期Fraction严格一致。

**关键可识别性结果：** 两个世界当前都恰好有2个代理遵守规范，但制度J分别是0或1，在预设反馈下下一期预期遵守人数分别为161/64=2.515625和417/128=3.2578125，相差95/128。将制度反馈γ与退出d均设为0以后，两种制度状态给出的下一期人数**完整分布**完全一致。这个差异是严格受控的人工机制示例，不能直接解释为现实社会制度因果效果。

[科学报告](R176_SCIENTIFIC_REPORT_2026-10-21.md)、[全部96世界及12480状态精确JSON](R176_EXACT_RESULTS.json)、[机器验收](R176_FINAL_MACHINE_ACCEPTANCE.json)、[源码及20项数学测试](r176_four_agent_institution_micro_macro_exact.py)、[完整ZIP](R176_96_FourAgent_Institution_MicroMacro_Exact_Worlds.zip)均已归档。[GitHub Actions39551579824](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39551579824)双Python各20单测、第三job完整独立执行归档，三job全success；[永久提交b6f82be8](https://github.com/edwardsage419/Psychohistory-Research/commit/b6f82be8a69eac0b6bbd92841e65b14b61c0bab8)。

参考一手来源[Epstein/Axtell1996](https://doi.org/10.7551/mitpress/3374.001.0001)、[Schelling1971](https://doi.org/10.1080/0022250X.1971.9989794)及[Turchin等2013](https://doi.org/10.1073/pnas.1308825110)。没有原文代码精确重跑，也无真实历史年份或人类行为实证；新增E2/E3=0，R073/PESEN v0.1不变。

**下一项：R177 原候选目录 P0 / 08-001 Probability Distribution Families（概率分布族）**。按原239研究目录顺序继续，全部R完成后统一归纳分类，最后模型熔炼。
