# R247 分支过程：九人工三代二叉家族、2304完整来源、Galton–Watson独立性及共同环境反例，独立计算前冻结

日期2026-10-23（Asia/Taipei）。原始239目录`11-007 Branching Processes`（P1），编号R247。当前项目顺序：先全部原R，再分类，最后熔炼。此R所有结果人工有限E1，新增真人E2/历史E3为0；R073和PESEN v0.1冻结。

## 经典分支定义及材料

Galton–Watson分支过程：单个初始祖先Z0=1，各活跃父节点的后代数为**独立同分布**的K∈{0,1,2}，Z_{n+1}=Σ_{活跃父节点}K；独立个体offspring PGF f(s)=Σ_{k=0}^{2}p_k s^k，若Z0=1则`E[s^{Z_n}]=f^{∘n}(s)`且`E[Z_n]=µ^n`，其中µ=Σkp_k。参见 Berkeley [*Branching Processes: Overview*](https://www.stat.berkeley.edu/users/mathsurv/branchfiles/branch/Overview.html) 和 Cambridge [*Probability, Chapter 14 Branching Processes*](https://www.statslab.cam.ac.uk/~jrn10/Lectures/p.pdf)。**有限n=0..3的精确实验只能证明该人工模型的三代分布、有限灭绝概率与矩，不证明任何真实疫情/政治传播或无限时间生存定理。**

## 全8bit人工源与完整三代二叉树

所有world均有8个独立公平二元外生`U,B0,B1,...,B6`，U潜在共同环境标志，B0对应初始根，B1/B2是两个潜在第一代父节点，B3..B6是四个潜在第二代父节点，采用固定满二叉索引：node0孩子node1、node2，node1孩子node3、node4，node2孩子node5、node6。父节点offspring K=0则无孩子，K=1只激活left，K=2激活left和right；活跃第二代父节点后代数之和即Z3，无需为第三代孩子继续创建来源位。每world完整2^8=256原结构型，九world**2304完整原source类型**，每行1/256。记录原U/B0..6、七个潜在父节点offspring oracle K0..6、完整四代可见大小Y0..Y3、真实隐藏H0..H3及源概率。**U或潜在不活跃父节点K不可输入只看Y的经验识别器**；全部来源为人工树类型，非2304个真实家庭、感染链或思想传播事件。

## 九预冻结机制

1. `IID_FAIR_0_OR_2`：每个潜在父节点独立K=2·B_j（p0=p2=1/2），µ=1，三代观察`E[Z3]=1`，三代存活`P(Z3>0)=39/128`，三代灭绝`89/128`；经典**临界GW有限三代**。
2. `IID_SUBCRITICAL_0_OR_1`：每节点K=B_j（p0=p1=1/2），µ=1/2，`E[Z3]=1/8`、P(Z3>0)=1/8。
3. `IID_SUPERCRITICAL_1_OR_2`：每节点K=1+B_j（p1=p2=1/2），µ=3/2，`E[Z3]=(3/2)^3=27/8`、因每节点至少1个孩子故P(Z3>0)=1。
4. `DETERMINISTIC_ONE`：每节点K=1，Z0..3全1，µ=1但有限灭绝概率0。**不能据µ=1就说所有临界模型必然在有限时间灭绝。**
5. `DETERMINISTIC_TWO`：每节点K=2，Z0..3=(1,2,4,8)，µ=2，P(Z3>0)=1。
6. `GLOBAL_SHARED_ENVIRONMENT`：U=0则所有潜在父节点K=0，U=1则所有K=2，全部parent依赖同一个全路径U。潜在单个节点的K边际仍p0=p2=1/2、µ=1，但P(Z3>0)=1/2，`E[Z3]=4`，**而不是GW独立父节点假设下的1**。所有完整原类型不可因B位未影响结果而丢弃。
7. `GENERATION_SHARED_SHOCK`：根K=2·B0，两个潜在第一代父节点都K=2·B1，四个潜在第二代父节点都K=2·B3。不同代冲击来源相互独立，同代父节点完全相关。每潜在父节点边际µ=1、`E[Z3]=1`，但`P(Z3>0)=1/8`（只有B0=B1=B3=1产生8个第三代）。
8. `SIBLING_ANTICORRELATED_OFFSPRING`：根K=2·B0，潜在第一代左父K1=2·B1、右父K2=2·(1−B1)，第二代父K3..6=2·B3..6且相互独立。每潜在父节点边际p0=p2=1/2，但第一代兄弟offspring完全负相关。`E[Z3]=1`、`P(Z3>0)=3/8`，不同于经典独立GW的39/128。
9. `STATIC_HIDDEN_TREE_SENSOR_ALIAS`：真正物理隐藏家族仅有根(1,0,0,0)，后续无真实后代；报告器按IID_FAIR_0_OR_2使用相同B0..6原来源模拟可见Y0..3。全可见代际大小逐原来源与1一样，但真实H3=0，说明未经独立确认的报告统计不能识别真物理繁殖。只在允许伪观测传感器时有效。

## 真值、独立PGF与非IID的辨识条件

A. 实际原生成路线逐source用七个潜在父节点offspring K、固定二叉父子拓扑从根依次激活，计算Y0..3及真隐藏H0..3。必须每world256完整外生原型且质量和1。
B. 独立第二路线针对**IID四经典world及静止隐藏但观察恰同IID的第九world**，仅从冻结p0,p1,p2直接构造offspring PGF多项式，完成三次函数复合`f^{∘3}`后得到完整`P(Z3=0..8)`，直接与原source观察三代边际逐项Fraction相等。并核对期望µ^3。**不得**将第九world观察PGF成功误指为真隐藏家族遵守GW。
C. GLOBAL_SHARED_ENVIRONMENT、GENERATION_SHARED_SHOCK和SIBLING_ANTICORRELATED的潜在单节点K边际虽然p0=p2=1/2，但违反父节点IID，严禁对其强求经典GW PGF。改以独立显式来源结构计算上述E[Z3]和有限存活率：GLOBAL=4/1/2；GENERATION=1/1/8；SIBLING=1/3/8；与真正IID临界的1/39/128形成有限反例。
D. 锁定FULL_IID与STATIC_HIDDEN_TREE_SENSOR_ALIAS每条相同8bit来源可见全部Y代完全相同，后者隐藏H0..3=(1,0,0,0)。
E. FROZEN IID临界三代灭绝89/128、存活39/128必须与完全原source频数和独立生成函数两路线严格相同。Z3是**三代**结果，不能混淆`P(Z3=0)`与无限未来的最终灭绝概率。对分支系数大于1，有限时间仍能有灭绝，而本具体IID_1_OR_2因最少一个孩子才不会灭绝。
F. Python3.11和3.12各至少45真实测试，第三CI独立source审计全部2304结构原型/8bit唯一/七潜在K/全部四代真实与可见计数、PGF、全部期望/存活差、SHA256，机器人永久main归档成功后才能发布科研报告与正式结题。
G. 任何社会传播或真实人员关系均未观测；本项目的E1正确性不保证历史E3或真人E2可预测性。下一原239目录需核验`11-008 Dynamical Systems Equilibria`，拟R248。
