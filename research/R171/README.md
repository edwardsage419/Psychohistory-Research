# R171 文化系统发育：400个真实语言树端点及79,800对路径距离精确复算

日期：2026年10月21日。原模型目录 **P2 / 07-013 Cultural Phylogenetics**。正式科研等级 **CLOSED_BOUNDED_E1_SOURCE_DESCRIPTIVE_REAL_TREE**。本阶段已实际读取并永久归档**发表过的真实语言系统发育树**，不再只是人工文化模型；但仍不属于独立的历史预测或原作者贝叶斯系统发育重建。

## 一手来源、固定版本、许可证

原研究：Gray、Drummond、Greenhill（2009），[Language phylogenies reveal expansion pulses and pauses in Pacific settlement](https://doi.org/10.1126/science.1166858)，《Science》323(5913):479–483。使用语言词汇资料和贝叶斯系统发育模型研究太平洋地区定居过程。

[Phlorest 原生整理的南岛语系树仓库](https://github.com/phlorest/gray_et_al2009)采用 **CC-BY-4.0**。固定原始 Git commit `a2e535f07c05d214fe7d36fe03747f4cfd5f9ca5`，通过 GitHub Actions 使用固定 commit 的原始 URL 取得四份完整资料，并分别校验原 Git SHA1 和原始文件字节数。源文件已永久保存在 [source/](source/)：`summary.trees`（10954字节）、`languages.csv`（23461字节）、`trees.csv`（65932字节）、`Generic-metadata.json`（15415字节）。原始文章与整理版本均需引用；具体整理版发布 DOI 尚未固定，以精确 commit 防止来源漂移。详见[科学报告](R171_SCIENTIFIC_REPORT_2026-10-21.md)。

## 完整原始树复算

[计算前冻结协议](../../protocols/R171_REAL_PHYLOREST_AUSTRONESIAN_TREE_FULL_DISTANCES_PRESCORE_FREEZE_2026-10-21.md)已在提交ecdfbd7完成。两套独立 NEXUS/Newick 解析器恢复的真实树拓扑和所有分支长度严格相等。

| 来源结构 | 实际复算结果 |
|---|---:|
| 原始树端点/语言表记录 | **400/400** |
| 端点ID与语言表完全对应 | **400（100%）** |
| 树全部节点 | 756 |
| 分支 | 755 |
| 内部节点 | 356 |
| 多于两个子节点的分叉 | 26 |
| 零长度分支 | 52 |
| 距根部至端点长度最小/中位/最大 | 1.733214 / 4.633214 / 4.633215千年 |

NEXUS源标注`[&R]`已定根，而CLDF对应`Tree_Is_Rooted`字段留空，未擅自补填。原本包含多叉及零分支，不强行把它转换成二叉树。不同的端点长度意味着不能默认所有标签所代表的观察处于同一历史年代。树中还包含用于分析的语言外群，不宜简单认定全部为当代南岛语日常使用者。

## 全部79,800个原始语言对距离

对400个树端点，恰有`400×399÷2=79,800`个不重复配对。**一套最低共同祖先法与另一套无向树路径遍历法，全部结果用Decimal精确相等。** [全量2292699字节CSV](R171_ALL_PAIR_PATRISTIC_DISTANCES.csv)保存每个真实语言ID配对及树分支路径长度（千年）；SHA256：`66ab2bb5645fcf86dfc91287c0886d2987470e2d65e457ce570106c02edf21ee`。平均树路径长度约7.400635，最大9.266429，最小为0；不同名称之间树距离为0可由零长树边导致，不等于两种语言具有相同语言结构。

九组事前选定的复算例子包括：
* SquliqAtayal—CiuliAtayal：**2.644574**
* Bali—Sasak：**3.795798**
* MalayBahasaIndonesia—Melayu：**0.344650**
* Kanakanabu—Saaroa：**0.010696**
* OldChinese—Buyang：**6.345432**

单位均为原始树枝的累加千年值，**不是两种语言最后共同祖先的独立测年值，更不能因此断言原作者2009年关于台湾起源和移民时间线的历史假设已被独立验证**。全部9组及其他所有语言对都保存在原数据结果中。

## GitHub测试验收及完整档案

[首次双环境CI39542653422](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39542653422)与[最终哈希固定/归档CI39542768099](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39542768099)均成功。Python3.11和3.12两轮各运行103项真实测试，独立永久归档任务再次运行103项，合计**515次单测执行、103种方法、0失败**。归档任务还重复下载并核对原始四份源文件、重新生成全部79,800对距离、复算全部数据/测试的固定SHA256。[完整资料永久提交c181afd](https://github.com/edwardsage419/Psychohistory-Research/commit/c181afddf9863da320ed0ef7ec348234ca9a7b2d)。末轮日志有一次测试脚本CSV文件句柄未显式关闭的非致命ResourceWarning，**不影响数据哈希、概率/距离复算或测试通过结论**，作为低优先级测试代码清理项保留。

成果：[原始资料source/](source/)｜[程序](r171_real_phylogeny_exact.py)｜[103项测试](test_r171_real_phylogeny_exact.py)｜[完整结构与来源JSON](R171_EXACT_RESULTS.json)｜[全语言对原始树距离CSV](R171_ALL_PAIR_PATRISTIC_DISTANCES.csv)｜[全部原始文件和程序ZIP](R171_Real_Austronesian_Full_Tree_103_Tests.zip)｜[正式科学报告](R171_SCIENTIFIC_REPORT_2026-10-21.md)｜[机器验收收据](R171_FINAL_MACHINE_ACCEPTANCE.json)。

校验哈希SHA256：
* 程序 `04c204fb99e3ecd6a2a920fb1938a760c53c199111255bcfc44c3746f30a0183`
* 测试 `4b6b36c5bb561a6be198399e93f735d0380ff411e61366a8095525595445eadb`
* JSON `65c18ba18eb50d4a977fbfdd02b29ba6b81e72f0b4578374f3cbb61899052f11`
* CSV `66ab2bb5645fcf86dfc91287c0886d2987470e2d65e457ce570106c02edf21ee`
* ZIP `f96399cd16915d7a6e90cefcb995692bd0c91beaa6b7cfb7b0250db0cd8a4765`

独立复算：从GitHub clone完整仓库后进入 `research/R171`，执行 `python r171_real_phylogeny_exact.py > R171_EXACT_RESULTS.json`、`python -m unittest -q test_r171_real_phylogeny_exact.py`；仅依赖Python标准库。需要复取原始资料时可先运行 `python r171_real_phylogeny_exact.py --fetch-sources`，只会请求固定原始commit并严格校验哈希。

**证据等级：本轮新增真实原始历史语言资料的来源一致性验证和描述性树数学复算，为E1_SOURCE_DESCRIPTIVE，不是独立历史预测E3。** 新增真人留出预测E2=0，外部历史预测E3=0。R073和PESEN v0.1继续冻结。下一候选为原目录 **R172 P1/07-014 Historical Event History Models（历史事件史模型）**。继续先完成既定R系列，之后统一分类，最后熔炼。
