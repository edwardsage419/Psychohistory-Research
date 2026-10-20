# R154 系统动力学存量流量｜100组精确反馈轨迹与数值伪象审计

2026-10-20。原模型目录 **P1/06-012 Stock and Flow System Dynamics**。研究状态 **CLOSED_BOUNDED_E1**。项目自构100组人造双存量A/B的精确有理数轨迹；不涉及原作者模型数据再现，不含真人独立预测或真实历史验证。

原典核对：[Forrester (1961) Industrial Dynamics，MIT Press 书目](https://books.google.com/books/about/Industrial_Dynamics.html?id=KRzHAAAAIAAJ)；[Sterman (2000) Business Dynamics，McGraw Hill出版方目录](https://www.mheducation.com/highered/product/business-dynamics-sterman.html)及[MIT作者书目](https://mitmgmtfaculty.mit.edu/jsterman/business-dynamics/)。未获得/逐页研读原书全文，不能声称重现作者的全部机制模型。

**冻结范围**：A0为0、2、6、10，B0=10−A0；两个转移比例p、q各从0、1/4、1/2、3/4、1中选择，共100个参数组合。记录t=0至12的13时点原始存量及12次双向转移，使用Fraction精确计算，并独立使用闭式解验证全部2600个存量数值完全一致。

**主要结果**：总量N(t)=10在100组封闭系统中逐时点严格保持；即便总量历史完全相同，内部转移比例仍可能不同，只有总量无法识别具体内流和外流。反馈特征根λ=1−p−q；p+q=1时一步达到均衡，p=q=1且初始不均等时出现周期2，而p=q=0时存量不变。数值负对照采用连续速率3/4与Euler步长2，从(10,0)得到人工负存量(−5,15)；旧存量触发的无界延迟流出得到(−10,20)，严格防透支规则将其拒绝。开放系统例(5,5)经入流2、出流1后总量正确为11。

**远程结果**：[GitHub Actions run39435566160](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39435566160)正式成功，Python3.11与3.12各执行119项真实测试并通过，独立归档任务再执行119项并校验四项固定SHA256，合计357次实际单测执行、119种不同测试、0失败。完整结果JSON及ZIP已通过[归档提交4a792b7](https://github.com/edwardsage419/Psychohistory-Research/commit/4a792b717c03702f1709c9f17e843ff1f94f3a53)永久写入main。

**成果材料**：[计算前冻结协议](../../protocols/R154_FORRESTER_STERMAN_STOCK_FLOW_100_TRAJECTORIES_PRESCORE_FREEZE_2026-10-20.md)（提交e0257e0）｜[科学研究报告](R154_SCIENTIFIC_REPORT_2026-10-20.md)｜[完整169095字节JSON](R154_EXACT_RESULTS.json)｜[源程序、测试与结果ZIP](R154_Stock_Flow_100_Histories_119_Tests.zip)｜[正式机器验收记录](R154_FINAL_MACHINE_ACCEPTANCE.json)。

四项SHA256：
* 代码：`2c5e0ade08f6221124c0790d83b1fa94976d9c1c8fa6d85b583a6bfdba139757`
* 测试：`7818731ac70159157261de1f8721cfe06ec0e9772201dedb0ee3b69ffdeef59c`
* 全结果JSON：`5df956c879f1183606292827a5827470a0c2adaa06833d766823949b05a1f7a6`
* 全源码ZIP：`e25f045de436f9aa5fed1bf6be061cd536a3544ba932ceef236330e302e269b5`

独立复算：在 `research/R154` 中运行 `python r154_stock_flow_exact.py > R154_EXACT_RESULTS.json`，再执行 `python -m unittest -q test_r154_stock_flow_exact.py`。无第三方依赖，ZIP用标准库ZIP_LZMA压缩。

新增真人E2=0、真实事件E3=0；R073/PESEN v0.1仍冻结。根据原候选目录，下一研究为 **R155 P1/06-013 Bass Diffusion Model**。维持先全部R系列、后统一分类、最后熔炼的研究顺序。
