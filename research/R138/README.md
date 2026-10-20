# R138：Mechanism Design（机制设计）

日期2026-10-20。目录 **P2 05-014**。

以Vickrey 1961、Clarke 1971、Groves 1973为一手理论根源，专门研究配置规则和付款规则对**个人如实报告激励**的影响。原始论文关键页已可视阅读，但三组枚举数值都是项目独立构造的有限类型机制，绝非作者原人类实验。

预先冻结之后，确实计算125×3×5=**1875**单物品次价拍卖偏报、729×3×9=**19683**异质两物品单位需求VCG偏报、216×3×6=**3888**二元公共品pivot偏报，合计**25446**次，真报弱占优违反均0。原本第一次61单元测试发现缓存浮点错误，修正为输入检查先于Python缓存后61项全部本地通过。

最重要的制度限制：公共项目成本5，在216个人工估值档案中181个建造、160个建造档案赤字、69个建造档案税收为零。付款随自己的报告变化的非pivot错误机制可诱使虚报，VCG两个单位需求商品付款也不能机械拆成逐物品次价。

研究文件：
- [原一手文献计算前冻结协议](../../protocols/R138_VICKREY1961_CLARKE1971_GROVES1973_DSIC_PIVOT_EXACT_FREEZE_2026-10-20.md)
- [详细科学报告](R138_VICKREY_CLARKE_GROVES_1961_1971_1973_SCIENTIFIC_REPORT_2026-10-20.md)
- [Python完整计算源码、61测试、结果ZIP](R138_Code_61_Tests.zip)
- [独立CI工作流](../../.github/workflows/r138-mechanism-design-61-tests.yml)
- [正式验收状态](R138_FINAL_ACCEPTANCE_STATUS.json)

解压ZIP后同目录运行 `python -m unittest -v test_r138_vickrey_clarke_groves_exact.py` 和 `python r138_vickrey_clarke_groves_exact.py`。全部依赖是Python标准库，整数精确计算。

没有新真人E2或外部历史事件E3。R073与PESEN v0.1冻结；按用户顺序完成全部R，之后统一分类最后熔炼。
