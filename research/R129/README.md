# R129：胆小鬼博弈（Chicken Game）与鹰鸽冲突的有界模型学习

日期：2026-10-20（Asia/Taipei），既定目录候选 P2 / 05-005 Chicken Game。

**正式研究状态**：CLOSED_BOUNDED_FIRSTHAND_SMITH_PRICE_1973_FIVE_STRATEGY_TABLE_AND_EXACT_ANTICOORDINATION。
**限定学习状态**：LEARNING_COMPLETE_BOUNDED_CHICKEN_ORIGINAL_1973_TABLE1_AND_EXACT_ANTICOORDINATION。

与R128猎鹿两个**对角**纯Nash不同，严格的简化Chicken模型有两个**非对角**纯Nash（一个坚持一个退让），共同升级造成损失。不同人是否及时协调角色是关键；该结论是对事前设定支付结构的数学推导，不是现实国家之间冲突的预测。

## 真正阅读的一手文献与原作者结果

**Maynard Smith & Price (1973), The Logic of Animal Conflict**, Nature 246:15–18，DOI [10.1038/246015a0](https://doi.org/10.1038/246015a0)，[研究机构托管原期刊全文影印](https://public.ek-cer.hu/~szabo/EGT20/library/maynard_n73.pdf)。原刊第15页基本动机、第16页五种策略设计和Table1全部25个已发表模拟均值、第17页“limited war”和进化稳定的讨论均真实阅读并可视核查。

必须明确：**1973作者实际模拟的是Mouse、Hawk、Bully、Retaliator、Prober-Retaliator五种策略**，分别安排15种配对，每种2,000次随机计算机战斗；原Table1是保留1位小数的原作者**模拟均值**，不是我们自行产生的动物记录，也**不是现在流行的V,C二策略鹰鸽方程**。R129只使用文章印刷的25个一位小数进行原表程序化审计，**没有重跑当年全部30,000次随机计算机模拟**、没有原作者RNG、个体仿真轨迹及野外观察数据。

忠实恢复原Table1行与列的五策略矩阵后，逐列最佳反应如下：面对Mouse，Hawk/Bully同得80；面对Hawk，Mouse收益19.5最高；面对Bully，Hawk收益74.6最高；面对Retaliator，Mouse和Retaliator均为29；面对Prober-Retaliator，Retaliator收益23.1最高。因此按已印**舍入值**，只有Retaliator自遇Retaliator是**弱**对称纯Nash必要比较的候选。原作者文字称Retaliator为ESS；但由于Mouse/Retaliator相关四格印刷收益全同为29.0，**R129不能从这一位小数的表格独立证明严格二阶ESS判据**，并非声称作者原结果错误。作者的生物适应论、计算机模拟及本项目数学表格审计具有不同的科研证据级别。

**Russell (1959), Common Sense and Nuclear Warfare** 的双车Chicken政治类比仅能从电子书所引部分核查书目，本轮没有完整逐页核查原始1959印本，也没有分析任何真实政治人物、核冲突记录或政策危机频率。参见[电子书背景页](https://www.perlego.com/book/1615329/common-sense-and-nuclear-warfare-pdf)。后续简化Hawk-Dove模型的公开学术语境，可参见[Games and Economic Behavior 2025](https://doi.org/10.1016/j.geb.2025.03.003)或[Scientific Reports 2019](https://www.nature.com/articles/s41598-019-43770-x)，但不得把它误记成原1973作者Table1真正模拟的同一个模型。

## 自构的精确两人冲突支付模型（不冒充原1973 Table1）

设两个行动：H坚持/升级，D退让；共同争夺资源价值V>0，双方同时坚持伤害总成本C>V，行人支付HH=(V−C)/2，HD=V，DH=0，DD=V/2。选V=2、C=6则行矩阵为：

| 自己 / 对方 | H坚持 | D退让 |
|---|---:|---:|
| H坚持 | −2 | 2 |
| D退让 | 0 | 1 |

使用直接逐对手行动收益与**另一套**枚举双方偏离的Nash检查，两个严格纯均衡为(H,D)、(D,H)，双方H/H各−2不是Nash。对手H的主观概率为q，本人坚持相对退让的期望收益差是(V−Cq)/2，所以对称**独立混合无差**比例 q*=V/C。在V=2,C=6时，q*=1/3，双方独立升级概率1/9，各人期望2/3、两人总期望4/3；这些都是合成制度参数下的数学答案。

更进一步，保持两人各自的H**边际概率完全相同=1/3**，仅改变四个联合行动结果HH/HD/DH/DD的相关性，会改变真实**模型内**冲突概率：

| 项目设定的联合信念 | 双方H/H概率 | 两人期望总收益 |
|---|---:|---:|
| 独立混合 | 1/9 | 4/3 |
| 相互错开的角色安排 | 0 | 2 |
| 完全同向同步 | 1/3 | 0 |

三组各人坚持倾向都为1/3，**仅靠两人边际不能确定危险相遇概率与福利**。证明用一套逐四个结果对双方实际支付分别加权的程序及**独立**解析福利等式 E(total)=V−C×P(HH)，在三组及其它实际测试中完全Fraction一致。特别强调这三组是**数学上合法的联合分布，不表示都为有激励相容保证的相关均衡**；研究中若实际有承诺/相互信号，可执行性需要额外模型。

另一个独立自构机制：从纯均衡预定(H,D)出发，每个人独立以概率ε执行翻转误差。真正同时坚持的概率ε(1−ε)，ε=1/2时最大1/4，而ε=0或1时为0。对13个严格Fraction误差率0、1/12、...、1，解析与直接四个错误事件独立枚举一致。

成本敏感性：V固定2、成本C从6升至12时，**仅假定双方按新的对称独立混合Nash实际重新优化**，各自H倾向由1/3降至1/6、HH由1/9降至1/36。如果外部机制已固定H概率1/3，则成本变化**不必减少HH概率**而可能扩大伤害损失。因此不能从游戏数学直接推导现实政治冲突变少，更不是对核战略行为的科学预测。

## 真CI与三份SHA256独立归档

[GitHub Actions run39352534382](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39352534382) **completed success：68项真实unit tests全部通过、0失败**；另对项目自设51组V,C合法游戏、每组13个对手H边际信念做663个精确收益差检查，另外逐游戏求真实无差q*=V/C；在n=2角色错误率的13点网格使用公式与独立布尔事件核对；对1973原刊25格逐列求最优应对并记录作者ESS结论与舍入精度限制。**全部源表、模型与结果均与人级E2预测明确分开**。

CI通过后GitHub Actions机器人真正写回源码、测试、科研报告三个文件的SHA256和实际数学结果。[自动化真实机器收据](R129_PHASE_A_ORIGINAL_1973_68_TEST_51_GAMES_663_BELIEFS_CI_ACCEPTANCE.json)已通过主仓库重新读取。

归档文件：
- [计算前冻结协议](../../protocols/R129_CHICKEN_SMITH_PRICE_1973_SOURCE_TABLE1_AND_EXACT_CONFLICT_FREEZE_2026-10-20.md)
- [完整原1973五策略Table1及数学模型的研究报告](R129_CHICKEN_1973_ORIGINAL_FIVE_STRATEGY_TABLE_AND_CORRELATED_CONFLICT_SCIENTIFIC_REPORT_2026-10-20.md)
- [可独立复现的Python标准库Fraction程序](r129_chicken_original_table_and_exact_conflict.py)
- [68项一手文献与精确数学测试](test_r129_chicken_original_table_and_exact_conflict.py)
- [GitHub Actions真实数学审计与三份SHA256](R129_PHASE_A_ORIGINAL_1973_68_TEST_51_GAMES_663_BELIEFS_CI_ACCEPTANCE.json)
- [正式科学验收与证据范围](R129_FINAL_ACCEPTANCE_STATUS.json)

本地复算：PYTHONPATH=research/R129 python -m unittest -v research/R129/test_r129_chicken_original_table_and_exact_conflict.py。

**科研边界**：一手原作者1973**模拟汇总表**实读、合成反协调均衡与相关性数学反例完成；1973原随机模拟轨迹没有被重新执行，Russell整书不是一手全本复核，真人/动物原行为数据0行，新增独立人级E2=0，现实冲突历史E3=0。R073与PESEN v0.1仍冻结，继续逐项完成所有R系列才统一分类并最终熔炼。
