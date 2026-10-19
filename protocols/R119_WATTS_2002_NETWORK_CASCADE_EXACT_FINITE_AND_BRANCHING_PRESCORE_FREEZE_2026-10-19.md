# R119｜Watts 2002 邻居分数阈值与网络级联：计算前冻结

日期：2026-10-19（Asia/Taipei）。既定目录P0 04-002 Watts Cascade Model，原文献索引R03。R119是新独立研究，不将R118全局参与阈值等同邻居局部传播。PESEN v0.1及R073全程冻结。

**原文一手出处**：Duncan J. Watts (2002), A simple model of global cascades on random networks, PNAS 99(9):5766–5771, DOI 10.1073/pnas.082090499，原论文全文 https://pmc.ncbi.nlm.nih.gov/articles/PMC122850/ 。本轮在冻结前核阅 Model Specification、Exact Solution on an Arbitrary Random Graph、Results and Discussion。原文以各节点已激活邻居所占比例是否≥自身门槛决定是否转为on，起始少数外生种子，激活后不退出；随机网络规模趋大时研究全球级联窗口与脆弱节点分支条件。原作者采用随机异步次序及大样本随机图；本轮只复算静态无退出闭包与解析分支指标，不复现作者完整随机网络相图。

**冻结的有限图输入**：n=1..10，连续整数标签0..n-1，边是长度2、节点int且不含bool的无向无重复、无自环简单图。n个阈值必须是Fraction且严格(0,1]，故孤立非种子节点不自激活。单一初始外生seed为合法int节点，永远active。未激活节点deg>0时，满足active_neighbor_count/degree≥phi才加入。全部比较用有理数。

**独立算法**：A同步轮次更新已激活集合直到不增长；B按节点标签顺序异步公平扫描直到不增长，不得调用A。两者最终成员集合必须完全相同、人数不下降、且都是闭包；不同更新轨迹不视为失败。原作者的随机异步发生顺序没有被复现为概率分布，只比较单调最终状态。one-neighbor vulnerable判据：deg>0且phi≤1/deg；不脆弱的节点也可能在多个邻居激活后加入。

**事前定值案例**（全部阈值1/2，除特殊反例）：n6 path 0–1–2–3–4–5，seed0→6；n6 star中心0，叶seed1→1、中心seed0→6；path和star均5条边但度数多重集不同。n6 cycle C6，seed0→6；两个互不相连的三角形，seed0→3；后两图每点度数均2、共6条边，但连通性不同，**不能从度数分布唯一确定某个种子的有限图传播规模**。四节点diamond edges 0–1,0–2,1–3,2–3，phi=(1/2,1/2,1/2,3/4)，seed0→4；节点3单邻居不可激活、双邻居可激活。仅种子活跃的无边图不会扩散。

**原文无限网络分支指标**：对度分布p_k，按度条件的one-neighbor vulnerable概率ρ_k，z=Σ k p_k，R=[Σ k(k−1)p_kρ_k]/z。源自Watts原文Eq.(5)，仅在趋于无限且局部类树随机图条件下R>1对应巨型脆弱分支过临界；R=1边界，R<1欠临界。不声称有限图R>1就必然产生大级联。p_k、ρ_k必须精确Fraction列表，p质量和1，z>0；无边z=0明确fail-closed。定值：p3=1、ρ3=1→R2；p3=1、ρ3=0→R0；p2=1、ρ2=1→R1；p1=1→R0；p1=p3=1/2、ρ1=ρ3=1→z2、R3/2。one-neighbor vulnerable(phi,k)用于产生ρ二值案例，例如phi1/3、k3为True；phi1/2、k3为False。

**验收与外延**：Python标准库、至少30项独立测试；所有n=1..4简单无向图（2^{n(n−1)/2}种）、逐节点三种阈值(1/3,1/2,2/3)及全部单一seed穷举，共 3+36+648+20736=**21423个纯数学配置**；A/B一致、闭包、输入fail-closed、已冻结特殊图结果和作者分支指标正确。真实CI success、源码/测试/报告SHA256 machine receipt回读后方标记LEARNING_COMPLETE_BOUNDED_WATTS_NEIGHBOR_THRESHOLD_AND_BRANCHING_ANALYTICS。无真人E2、无前瞻E3，未重现Watts原PNAS 10,000节点ER相图，不做跨R归类与熔炼；R073/PESEN保持冻结。
