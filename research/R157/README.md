# R157 结构人口理论｜72组完全Fraction的三因素压力与滞后反例

2026-10-21。原目录 **P2/06-015 Structural Demographic Theory**；正式结题等级 **CLOSED_BOUNDED_E1**。直接研读[Turchin (2013)原始40页论文](https://escholarship.org/content/qt6qp8x28p/qt6qp8x28p_noSplash_c3d0ac79e973d3c6029f872002050fcd.pdf)中的三因素压力乘积 Ψ=MMP×EMP×SFD；核对[Goldstone1991](https://jackgoldstone.schar.gmu.edu/books/)与[Turchin2003](https://peterturchin.com/books/historical-dynamics/)原出版资料，但这两本书没有全文复算。额外审阅[Georgescu2023发表于PLOS ONE的独立质疑](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0287912)，该论文认为结构人口理论针对当代美国的三项具体实证预测没有得到其审查资料的支持。各原作者实证结果均未在本阶段重新计算。

**人工模型：** 项目自建人口压力M、精英压力E、财政压力F的三环节有界滞后递推；三者全部是0到1之间的纯人工Fraction数值，**并非**作者实际人口、薪资、精英、国家负债变量的精确测量模型。保留作者的指标乘积形式Ψ=M×E×F；另定义比较性平均数Q=(M+E+F)/3。H三个档位，人口、精英、财政滞后参数分别两档，财政缓冲三档，共72种预先冻结的完整人工世界，每个世界13时点。

**独立精确验算：** 标准Fraction直接逐时点并行递推与另一套独立仿射矩阵幂展开对全部72×13×3=2808个状态数值完全严格相等；每时点Ψ及Q计算同样严格相等。源论文乘积指标并不是政治暴力概率，更不能把本项目零乘积解释为某社会绝对安全。

**预设负对照：** 人口压力先上升，精英压力到下一期上升，财政压力第3时点才首次正值。人工实例H=1、a=b=c=1/4、缓冲r=0的t1=(1/4,0,0)、t2=(7/16,1/16,0)、t3=(37/64,5/32,1/64)。另有两组不同的H与调整参数，在t1具有同一个向量(1/4,0,0)，到t2人口分量变为7/16与3/8，单时点信息不足以识别各个参数。对于向量(1,1,0)和(1/2,1/2,1/2)，乘积排序与加总平均排序方向相反，说明评价依赖聚合规则。财政缓冲为1时乘积恒为0，但另外两个压力分量可以上升。

**GitHub CI与归档：** [首轮run39521661742](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39521661742)和[最终固定哈希run39521779601](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39521779601)均success。Python3.11及3.12每轮各102项真正单元测试，归档任务另跑102项，总共510次实际执行、仅102种不同测试、0失败。四项SHA256校验成功，完整JSON与原生源码测试ZIP已由[归档提交b1a19d4](https://github.com/edwardsage419/Psychohistory-Research/commit/b1a19d47c9dc0f5d9ed608e15adca8dc2cba2825)永久写入main。

**全部材料：** [计算前冻结协议](../../protocols/R157_TURCHIN2013_GOLDSTONE1991_THREE_PRESSURE_72_WORLDS_PRESCORE_FREEZE_2026-10-21.md)（提交94f7552）｜[学术报告与竞争模型](R157_SCIENTIFIC_REPORT_2026-10-21.md)｜[源码](r157_structural_pressure_exact.py)｜[102项测试](test_r157_structural_pressure_exact.py)｜[完整223711字节JSON](R157_EXACT_RESULTS.json)｜[永久ZIP](R157_Structural_Pressure_72_Worlds_102_Tests.zip)｜[机器验收](R157_FINAL_MACHINE_ACCEPTANCE.json)。

四项SHA256：
* 程序 `78795ada49b623a188c6fb3042817d35803120145cd2cc97f7d1e361e00888e3`
* 测试 `6b47799fd0cf92998d0468c05886785c03db537fbec56e4cdfe624936c85fd85`
* JSON `a62c20840815cd6bfcfd30c13e41b79d5745c6bd508e7ee3bfdf234eb4230e78`
* ZIP `b40bd070cea916c3f5479049fdfda87763bf3592d1bb716a54d357b9928f856d`

复算指令：进入 `research/R157`，执行 `python r157_structural_pressure_exact.py > R157_EXACT_RESULTS.json` 及 `python -m unittest -q test_r157_structural_pressure_exact.py`。全部使用Python标准库。

**新增真人E2=0、外部历史预测E3=0**。R073/PESEN v0.1继续冻结。下一原目录 **R158 P2/06-016 Conflict Event Process Models**。继续先全部既定R系列，再统一归纳分类，最后开始熔炼。
