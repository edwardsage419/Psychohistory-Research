# R242 差分方程：九有限离散递推世界、180完整初值—代数时点、观测动态与真实状态别名事前冻结

日期2026-10-23 Asia/Taipei。原始239目录 `11-002 Difference Equations`（P0），研究编号R242。R241连续微分方程已正式归档。本R仅有限人工E1，研究离散代际递推、非线性 logistic map、有限递推初值敏感度、传感器导致的完整观察等价与平方观测的符号丢失。R073、PESEN v0.1冻结，真人E2/历史E3新增0。

原始文献背景：May (1976), [*Simple mathematical models with very complicated dynamics*](https://www.nature.com/articles/261459a0), Nature 261:459–467, DOI 10.1038/261459a0；Strogatz (2018, second edition) *Nonlinear Dynamics and Chaos*, CRC Press，离散logistic map与固定点/分岔的教科书方法。本R不把四步有限人工递推结果认定为长期混沌、Lyapunov指数、真实人口振荡或May的原始数值图复现。

所有九世界统一初值`x0∈{1/4,1/2,3/4,1}`，离散时刻`n∈{0,1,2,3,4}`，每世界20个完整原来源型、权重1/20，九世界**180条**。保存原cohort、n、观察y_n及对初始x0的解析敏感度；oracle保存隐藏h_n及其n→n+1真正递推算子，绝不向实际观察回归泄漏。全源Fraction，绝非真实历史系列。

九世界固定：
1. `CONTRACTION_HALF`：隐藏h0=x0，h_{n+1}=h_n/2，观察y=h。
2. `CONTRACTION_SENSOR_ALIAS`：隐藏h0=x0、h_{n+1}=h_n常数，观察y=2^{-n}h；完整可见轨道与1逐source一致，真隐藏不衰减。
3. `CONTRACTION_DOUBLE_COORDINATE_ALIAS`：隐藏h0=2x0、h_{n+1}=h_n/2、观察y=h/2，全部可见轨道与1完全相同，隐藏尺度不同但只是表征重标定。
4. `EXPANSION_DOUBLE`：h0=x0，h_{n+1}=2h_n、y=h。
5. `EXPANSION_SENSOR_ALIAS`：h0=x0，h_{n+1}=h_n、y=2^n h，全部可见轨道与4一样但真隐藏不增长。
6. `SIGN_FLIP_SQUARED_SENSOR`：h0=x0，h_{n+1}=−h_n，y=h_n²；真隐藏每步符号反转，但实际观察y_n=x0²恒定。
7. `STATIONARY_SQUARED_SENSOR`：h0=x0，h_{n+1}=h_n，y=h_n²，与6的全可见轨道及初值敏感度一致但真隐藏没有状态转移。
8. `LOGISTIC_R2`：h0=x0，h_{n+1}=2h_n(1−h_n)，y=h；初值1/2是严格固定点。
9. `LOGISTIC_R4`：h0=x0，h_{n+1}=4h_n(1−h_n)，y=h；初值1/2在n=1到1、n=2到0后继续为0，x0=1/4在n≥1到3/4且固定。本世界可展现不同有限轨道，但不做混沌判定。

验证和评分**在此冻结**：
A. 从原递推逐步模拟h_n，生成全部九×四×五原source，解析chain rule递推`D_{n+1}=f'(h_n) D_n`，其中D0=∂h0/∂x0，linear f'分别1/2、2、−1、1，logistic f'=r(1−2h_n)。观察灵敏度：linear y=h或h/2，时变传感器y=a^n h，squared y=h²，统一在源中记录分数。独立第二路**不读取原来源**，将各自主f表示为有理多项式，进行n次多项式复合，用Horner在初始h0计算h_n及微分导数；对原时变sensor和squared再链式重建可见y与∂y/∂x0；必须与source路径全20状态逐一一致。这避免把同一循环重算误称独立模型。
B. 全部自主隐藏f满足离散半群`f^{m+n}(h0)=f^n(f^m(h0))`，对m,n非负且m+n≤4精确认证；**含随n变化的sensor的可见序列不代表自主隐藏状态**。前瞻一阶可见差`y_{n+1}−y_n`是观察量，不是可直接辨认的隐藏真递推。
C. 三个衰减观察别名CONTRACTION_HALF/CONTRACTION_SENSOR_ALIAS/CONTRACTION_DOUBLE_COORDINATE_ALIAS的完整`P(cohort,n,y)`逐source相同；两个扩张观察别名EXPANSION_DOUBLE/EXPANSION_SENSOR_ALIAS同理；两个平方观察别名SIGN_FLIP_SQUARED_SENSOR/STATIONARY_SQUARED_SENSOR亦同，隐藏符号动力相反。全观察初值敏感度亦一致。唯一观察条件下的不可识别性只针对冻结允许的测量算子，若外部校准传感器不随时变化、可带符号读取隐藏状态，则可排除相应别名。
D. EXACT固定目标：x0=1,n=4衰减可见y=1/16、扩张y=16；x0=1/2在LOGISTIC_R2的所有n为1/2，在LOGISTIC_R4为序列1/2,1,0,0,0；x0=1/4在LOGISTIC_R4为1/4,3/4,3/4,3/4,3/4；观察一阶有限差不能当作连续微分的近似误差保证。
E. logistic有限四步内初值灵敏度可能为0（例如x0=1/2在r=4一步导数0），这仅局部导数、**不是长期吸引子或预测稳健性的普遍主张**。对x0=1/2, r=4，n1的`D1=r(1−2x0)=0`，后续复合初值导数为0；但改变有限正初值扰动仍可能产生二阶非零差异。
F. 所有Fraction计算不能默称有统计随机采样；来源每行1/20用于完全结构范围验证，不是独立真实被试或轨道重复实验。
G. CI要求Python3.11和3.12各≥45真实测试、独立第三job重新生成九世界180条源CSV/完整概率联合及敏感度JSON/SHA256，独立验证三别名族、poly复合与导数一致、logistic固定点、半群和全原source概率，再机器人永久归档main。成功后写正式E1报告与验收；失败run必须留痕，不得标记成功。
H. 下一原目录经核验 `11-003 Stochastic Differential Equations`（P2），计划R243。研究主线仍优先完成全部原R系列再分类及融合。
