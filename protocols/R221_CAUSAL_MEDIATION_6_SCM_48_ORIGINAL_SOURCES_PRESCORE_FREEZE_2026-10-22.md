# R221 因果中介分析：六类四潜在来源 SCM、48条真正随机处理观察与自然直接/间接效应的不可识别性（事前冻结）

2026-10-22。原239目录真实条目 **09-012 Causal Mediation Analysis（P2）**。事前研究状态 `PRESCORE_FROZEN_E1_ARTIFICIAL_SIX_MEDIATION_SCM`。

## 学术来源与边界

Robins and Greenland (1992), *Identifiability and exchangeability for direct and indirect effects*, *Epidemiology* 3(2):143–155, DOI https://doi.org/10.1097/00001648-199203000-00013。Imai, Keele, Tingley (2010), *A general approach to causal mediation analysis*, *Psychological Methods* 15(4):309–334, DOI https://doi.org/10.1037/a0020761。Imai, Keele and Yamamoto (2010), *Identification, Inference, and Sensitivity Analysis for Causal Mediation Effects*, *Statistical Science* 25:51–71。有限离散源模型并非原作者真实数据、工作软件、一般调节/多中介方法或心理机制因果识别的复现。

## 人工真源、自然/受控反事实及真实分配

二元处理T∈{0,1}是唯一真的独立随机化变量，各概率1/2；四类**潜在**个体源U∈{0,1,2,3}各概率1/4，与T独立。每个世界完整4×2=8条原观察来源，6个世界总**48条原SCM×真实随机化观察联合来源**，每条来源在世界内概率1/8。每个U具有一个处理干预响应的自然中介向量`(M(0,U),M(1,U))`及完整的结果响应面`Y(t,m,U)`，人为固定：
- 共同中介反应`M0=(0,0,1,1)`、`M1=(0,1,1,1)`，均有两臂内M=0、M=1的非零来源支持，固定P(M1=1)=3/4、P(M0=1)=1/2、差1/4。
- 不变中介反应`M0=M1=(0,1,0,1)`，两臂M支持都为1/2。

六种真因果SCM：
1. `PURE_INDIRECT`：共同中介反应，`Y(t,m,u)=m`，纯中介效果。
2. `LATENT_COMMON_CAUSE_NO_MEDIATION`：共同中介反应，`Y(t,m,u)=M(t,u)`，即**结构Y由相同U与T决定，完全不依赖人工外部干预M**，但自然观察Y=M。与第一世界的完整观察`P(T,M,Y)`逐八条对应原U/T来源严格一样，真实自然中介效果不同；存在未观测的中介–结果共同原因U。此模型违反顺序可忽略假设，但T完全随机且每T/M观察格都非空。
3. `PURE_DIRECT`：不变中介反应，`Y=t`，只有直接总效应。
4. `ZERO_CAUSAL_EFFECT`：不变中介反应，`Y=0`，无直接/间接效果。
5. `ADDITIVE_BOTH`：共同中介反应，`Y=t+m`（结果不限制二元，取0..2），自然直接与间接均有贡献。
6. `TREATMENT_MEDIATOR_INTERACTION`：共同中介反应，`Y=t×m`，直接和间接效应的分解随设定对照处理t变化。所有外生U类型在同一真SCM中保持同一个人跨潜在干预的身份；八条(T,U)源只是同一四U总体可能被随机分配的观察结果，不能宣称八次独立真人实验。

每条48原资料永久保留世界、U（仅审计）、T、原概率1/8、实测M(T,U)、实测Y(T,M(T,U),U)，M0/M1、四个受控结果`Y(0,0),Y(0,1),Y(1,0),Y(1,1)`及四个嵌套自然结果`Y(0,M0),Y(0,M1),Y(1,M0),Y(1,M1)`，自然/受控反事实**仅审计**，任何只观测统计函数不得读取U、潜在结果或真世界名。

## 固定的两种自然效应分解和识别检验

每个世界真总效应TE=E[Y(1,M1)−Y(0,M0)]；
- 以M0为基准的自然直接效应`NDE0=E[Y(1,M0)−Y(0,M0)]`；
- 以T1为基准的自然间接效应`NIE1=E[Y(1,M1)−Y(1,M0)]`；
- 以T0为基准的自然间接效应`NIE0=E[Y(0,M1)−Y(0,M0)]`；
- 以M1为基准的自然直接效应`NDE1=E[Y(1,M1)−Y(0,M1)]`。
逐四U真来源Fraction求出五者、两独立加总恒等式`TE=NDE0+NIE1=NIE0+NDE1`，并另从实际T随机化观察组条件均值差估计`E[Y|T1]−E[Y|T0]`，逐世界必须与真TE精确相等。该TE可由随机化识别，不等于自然直接/间接效应也能由随机化自动识别。

只从观察**P(T,M,Y)**（T随机，U隐藏），固定非参数mediation formula：
`gNDE0 = Σ_m P(M=m|T=0)[E(Y|T=1,M=m)−E(Y|T=0,M=m)]`
`gNIE1 = Σ_m E(Y|T=1,M=m)[P(M=m|T=1)−P(M=m|T=0)]`。
只读八条原观察来源的`T,M,Y,1/8`，不读世界结构/潜在真值，全部四条件(T,M)保证正概率，分母非零。逐世界输出`gNDE0,gNIE1`及其相对真`NDE0,NIE1`的偏差。**当且仅当额外识别条件足够**时这个formula才可代表自然机制分解；此处TRUE `PURE_INDIRECT`和`LATENT_COMMON_CAUSE_NO_MEDIATION`在观察层完全同分布，gformula必相同，而真NDE/NIE分别(0,1/4)与(1/4,0)，构成严谨不可识别案例；只有随机化T、观察正值性仍不够。

反例六`TREATMENT_MEDIATOR_INTERACTION`预期TE=3/4，`NDE0=1/2,NIE1=1/4`但另一分解`NIE0=0,NDE1=3/4`，说明“唯一一组直接/间接占比”不一定存在。其余世界预先固定：PURE_INDIRECT:(TE=1/4,NDE0=0,NIE1=1/4)；LATENT:(TE=1/4,NDE0=1/4,NIE1=0)；PURE_DIRECT:(TE=1,NDE0=1,NIE1=0)；ZERO:(0,0,0)；ADDITIVE_BOTH:(TE=5/4,NDE0=1,NIE1=1/4)。按资料计算逐项检验而不改变预期规则。

真Y(t,m,u)的**受控干预**不是自然嵌套`Y(t,M(t'))`，不能把“控制M固定”与跨世界自然效应混同。研究假设单一稳定SCM并由研究者人为规定跨世界潜在响应的联合关系，不能把该联合关系自称现实可直接观察。

## 数据来源和验收限制

当前只做完整人工SCM机制审计E1；T的确随机，但Mediator的响应由潜在U共同决定，故随机处理不足以保证中介–结果条件交换性。在任何现实数据中还需顺序可忽略性、无处理后中介–结果共同原因等额外不可检验条件或其他识别设计。任何人工差异不能当作真人心理中介证据E2或真实历史E3。

纯Python标准库+Fraction完整源重演至少30单元测试，GitHub Actions Python3.11和3.12各执行全部测试，第三独立重算六世界×八真原观察=48来源、观察gformula两路/真嵌套反事实两分解/完全相同(T,M,Y)联合分布，JSON、原48来源CSV、机器SHA，真实永久提交main并核验三job成功后才能正式标记 `CLOSED_BOUNDED_E1_ARTIFICIAL_SIX_MEDIATION_SCM`。原239目录下一项 **09-013 Causal Inference with Interference**，若继续编号R222；原目录此前该项已有R17文献定位但未完成新的独立验证。按原239逐项完成后统一分类最后熔炼。
