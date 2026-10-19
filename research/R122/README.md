# R122：简单传播、复杂传播与宽桥的有限数学研究

日期：2026-10-19（Asia/Taipei）。原239候选目录P0 04-005 Simple versus Complex Contagion（原来源索引R04）。

**科研状态：CLOSED_BOUNDED_PRIMARY_CENTOLA_MACY_2007_BRIDGE_AND_DISTINCT_NEIGHBOR_MATH。**
**模型学习状态：LEARNING_COMPLETE_BOUNDED_CENTOLA_MACY_COMPLEX_CONTAGION_AND_BRIDGE_ANALYTICS。**

## 第一手文献和范围

Centola, D. & Macy, M. (2007). *Complex Contagions and the Weakness of Long Ties*. American Journal of Sociology 113(3):702–734. DOI https://doi.org/10.1086/521848；[出版方原论文](https://www.journals.uchicago.edu/doi/10.1086/521848)，[Penn托管原刊全文](https://ndg.asc.upenn.edu/wp-content/uploads/2016/04/Centola-Macy-2007-AJS.pdf)。直接核阅原刊702–706、710–714、728页；本研究还进行原文关键页面可视复核。

作者强调一名邻居提供信息即可传播的机制（simple）与需要多名**不同邻居**共同确认的传播机制（complex）的区别；对简单传播，长连接可缩短距离；对复杂传播，跨社群桥的**有效宽度和来源结构**决定能否引发新的采纳。原作者给出**特定规则环形图**的解析式：Wmax=z(z+2)/8（偶数度z），Wc=a(a+1)/2（绝对人数门槛a）。例如z4时Wmax3、a2时Wc3；这些式子不能直接当任意图中只数跨边数量的充分条件。

**限制**：这里主要是对原作者数学/计算理论的限定学习，没有重现2007原论文全尺度随机重连或二维晶格模拟，没有取得原作者实验级社交网络或真人参与者的个人逐行数据。

## 独立自构的网络反例

本阶段自建两个三人三角形社区A={0,1,2}、B={3,4,5}，初始三名A节点均已加入，行动不可退出，以不同活跃邻居人数作为参与门槛。

| 新构造跨群体边 | 简单a=1终态 | 复杂a=2终态 |
|---|---:|---:|
| 唯一连接(2,3) | 6 | 3 |
| 三条分散(0,3),(1,4),(2,5) | 6 | 3 |
| 三条有序强化(1,3),(2,3),(2,4) | 6 | 6 |

在有效三条边布局下，复杂传播同步人数轨迹为3→4→5→6：B3首先接触两个**不同**A人，然后B4有A2+B3，最终B5有B3+B4。分散布局中每个B人初期只见一个A人，因此无法启动复杂传播。**两个图均3条跨边不意味着都能成功**。这是本项目数学自构例，不是原论文Fig1中原实验数值，也不声称重新估计真实群体社会强化强度。

如A社区只激活一名种子，即便内部为三角形、复杂门槛a2仍无法进一步蔓延；两名种子才能引发第三名。这也说明**种子配置**不能与边数量分开看。本模型固定人数门槛，纯粹增加边不会增加该门槛；原作者重连模型则可同时删除本地边，不能混淆两个操作。

## 真实可复算机器验收与失败审计

两套独立Python 3.11标准库求解器：
1. 同步逐轮更新所有满足至少a个不同活跃邻居的未激活节点。
2. 完全独立穷举所有含外生种子的阈值闭合集合，取交集得到最小可达闭包，不调用第一套算法。

从n=1至4遍历**所有有标签无向简单图**，每节点门槛取合法的{1,2}与[1,n]交集，所有初始种子集合。n=1/2/3/4分别2、32、512、16384组，总共**16930组**纯数学网络—门槛—种子方案，在每一个配置均独立核对**完整终态激活集合**并核查不遗落可激活节点。

**失败记录完整保留**：首次[GitHub Actions 39258433825](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39258433825) 的51项测试中50项通过、1项失败：程序错误生成n=1、门槛2，违反预冻结合法范围。追加[修正审计 R122-CORR-001](../../protocols/R122_CENTOLA_MACY_2007_COMPLEX_CONTAGION_DISTINCT_REINFORCEMENT_BRIDGE_WIDTH_FREEZE_2026-10-19.md)，保持原数值门槛合法域，只修正n=1可枚举值并相应将数学配置总数从16932修正16930。这一事后修复有明确证据，不可隐瞒为原先的预定成功。

最终[GitHub Actions 39258676907](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39258676907) **success：51项实际测试全部通过，0失败；16930组穷举通过**。机器自动提交程序、测试、研究报告三份文件SHA256及解析式/反例结果，[正式CI收据](R122_PHASE_A_COMPLEX_CONTAGION_51_TEST_16930_GRAPH_CI_ACCEPTANCE.json)已被独立回读。通过指向的仅是有界第一手文献和数学计算，新增真人预测E2=0。

## 研究资料

- [源原文与计算前冻结合同及审计偏差](../../protocols/R122_CENTOLA_MACY_2007_COMPLEX_CONTAGION_DISTINCT_REINFORCEMENT_BRIDGE_WIDTH_FREEZE_2026-10-19.md)
- [第一手来源、临界桥宽公式与独立图案例科研报告](R122_CENTOLA_MACY_2007_COMPLEX_CONTAGION_BRIDGE_SCIENTIFIC_REPORT_2026-10-19.md)
- [人数阈值及独立闭合算法执行程序](r122_centola_macy_2007_distinct_neighbor_complex_contagion.py)
- [51项正式测试](test_r122_centola_macy_2007_distinct_neighbor_complex_contagion.py)
- [成功CI机器收据与源码SHA256](R122_PHASE_A_COMPLEX_CONTAGION_51_TEST_16930_GRAPH_CI_ACCEPTANCE.json)
- [科学结题状态、失败和成功证据索引](R122_FINAL_ACCEPTANCE_STATUS.json)

复算（Python3.11标准库）：PYTHONPATH=research/R122 python -m unittest -v research/R122/test_r122_centola_macy_2007_distinct_neighbor_complex_contagion.py 。

本研究没有真实社会结构、每个人的多个独立可见来源、真实规范压力/个体认知、随机人类参与或模型跨网络预测数据，因此**数学E1不等于真人E2因果证据**，更不是长期历史事件的概率预测结题。R073与PESEN v0.1冻结；所有既定R模型先学完，再统一分类，最后熔炼。
