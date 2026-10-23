# R234 纵向测量等值：九人工两波三项目、2304完整配对外生源、潜在改变与测量漂移等价 — 事前冻结

日期2026-10-23（Asia/Taipei）。真实239原目录 `10-008 Longitudinal Measurement Invariance`（P1），研究R234。优先保持“全部原R学习与有限数学研究 → 统一归纳分类 → 最后熔炼”的owner序列。预冻结本协议须独立先提交，禁止在观察结果后改换源空间与验收目标。本研究只人工E1、未接入真人或历史E2/E3，R073/PESEN v0.1不变。

## 文献锚定

Widaman, Ferrer & Conger (2010), *Factorial Invariance Within Longitudinal Structural Equation Models: Measuring the Same Construct Across Time*, Child Development Perspectives 4:10–18, DOI https://doi.org/10.1111/j.1750-8606.2009.00110.x，PubMed 20369028，是针对同一构念跨时间可比性的直接论文。Putnick & Bornstein (2016), *Measurement Invariance Conventions and Reporting*, Developmental Review 41:71–90, DOI https://doi.org/10.1016/j.dr.2016.06.004，系统回顾配置/载荷/截距/残差等值的现有使用方式。二者均已查询到公开官方摘要与开放版本；本R的人工来源非原作者参与者数据，未重演其现实案例。

## 完整固定概率空间

**同一个**匿名人工个体的两次（time0/time1）三题测量，统一使用八个互相独立、等概率±1原源 `T,H,E01,E02,E03,E11,E12,E13`，前者为跨期不变原特征T，H为time1可能出现的独立真实特质变化冲击，两组三题误差源允许对同一项目的跨时误差复用。每世界2⁸=256条完整来源，各行权重1/256，九世界合计**2304完整配对来源**。这不是2304个真人或2304次真实调查，亦不把time0与time1错误地当作互相独立个体。

固定真实潜因子`F0=T`, `F1=s*T+h*H+delta`。观察time0三项一律 `X0_j=T+E0j`；观察time1各项 `X1_j=nu_j+lambda_j*F1+sigma_j*noise_j`，除特别注明的误差持续机制`noise_1=E01`外，`noise_j=E1j`（j=1..3）。所有固定系数整数或1/2；原完整来源CSV保存八个真外生源、oracle F0/F1、实际六项X、同人3项目差量及真正人工概率，机读结果对观察量一律不读取真潜因子及参数。

## 九个预冻结世界（仅time1参数变化）

1. `STABLE_BASE`：s=1,h=0,delta=0, nu=(0,0,0),lambda=(1,1,1),sigma=(1,1,1)，不复用测量误差。
2. `TRUE_LATENT_SHIFT`：仅delta=1，观测time1三题全部均值+1，真F1−F0均值1。
3. `UNIFORM_INTERCEPT_DRIFT_ALIAS`：仅nu=(1,1,1)，观测time1三题均值也全部+1，但真F1−F0均值0。**2和3对于同一个T/H/6次误差源，实际六项配对X逐源完全相同；完整P(X01,X02,X03,X11,X12,X13)相同，真潜在改变却不同。**
4. `LATENT_INNOVATION`：仅h=1，F1=T+H，真均值改变0、真个体改变的方差1；time1的不同题目之间公共协方差由1升为2。
5. `SINGLE_ITEM_INTERCEPT_DRIFT`：仅nu=(1,0,0)，单一项目可见均值变化、真F不变。
6. `METRIC_ITEM1_DRIFT`：仅lambda=(2,1,1)，time1首项载荷变更，观察跨时间项目cov也改变。
7. `ERROR_VARIANCE_DRIFT`：仅sigma=(2,1,1)，time1第一项特异误差方差由1变4，time1 var第一题5，其它公共Cov不变。
8. `PERSISTENT_FIRST_ITEM_ERROR`：仅第一项目time1沿用E01，不使用E11；跨时首项自协方差增加到2（与time0第一项方差相同），所有其它跨时项目Cov仍1。这是跨时相关残差，**不能**当作真实稳定潜因子自相关上升的充分证据。
9. `LATENT_SCALE_REANCHOR_ALIAS`：s=2,h=0,delta=0, lambda=(1/2,1/2,1/2)，其余默认。time1原latent F1=2T，但实际time1每题仍`(1/2)*2T+E1j=T+E1j`；完整跨时六维可见联合分布与STABLE_BASE逐源相同。未锚定的latent单位差不等于实质metric non-invariance；不同raw λ参数不足以作真实时代差异结论。

## 冻结观测统计、独立校验、边界

A. 每世界由全256原来源计算六维`μ_X`、完整6×6人口协方差、完整配对六项观察联合概率`P(X0,X1)`（整组而不仅边际），及三项跨时观察差均值、**同一受试者**平均总分`S_t=(X_t1+X_t2+X_t3)/3`的跨时差均值与方差。各世界源权重总和1，所有原源各唯一。
B. 第二条与源行枚举严格不同的校验：从固定源顺序T/H/E01..E13的8维线性系数展开六观测项，直接内积得全部36格Cov，常数项给均值。与枚举原源逐格Fraction相同。另用同一解析向量计算潜变量F0/F1的真均值差、真个体改变方差和两期因子Cov，而该真结构信息只限人工oracle，不输入观察估计器。
C. 2与3、1与9必须**逐条原来源**相同的六个可见项目X；全部配对六维观察联合概率严格相等，但2/3的真构念变化均值分别1和0；1/9的原潜在单位不同而观察相同。清楚分隔因果/测量语义非识别和简单单位重参数化。
D. 对`LATENT_INNOVATION`，真实平均个体潜在改变为0，真变化方差1，time1不同项目Cov=2；`ERROR_VARIANCE_DRIFT`第一项目time1观察方差5，其他时间1项目方差2，非对角仍1；`PERSISTENT_FIRST_ITEM_ERROR`首题X01与X11的跨时Cov=2，其他不同项目跨时Cov=1。三种现象必须能够与真正均值改变区别。
E. raw相同指标截距ν、载荷λ、残差σ²的固定参数布尔验收只反映预设人工坐标；不属于在真人纵向SEM上拟合得到的统计显著性。第三方需要外部稳定锚题或研究设计才能确认潜在结构跨时代可比性，不能用本人工oracle代替独立观测。
F. 使用Python3.11与3.12各≥40次真正单元测试、GitHub Actions第三独立门槛重算所有2304原配对来源并核验两组配对全分布别名与36协方差、SHA、机器收据，将CSV/JSON/收据永久归档main；之后单独提交报告与正式有界结题。失败保留、CI元数据不一致需注记，不能只凭排队态宣称 success。
G. 无真实人级纵向样本、样本CFA拟合、动态人格变化证据、时间相依误差的一般识别定理；仅E1人工。R073/PESEN v0.1冻结。原目录下一条是`10-009 Differential Item Functioning`（拟R235），完成本项后再次实查。
