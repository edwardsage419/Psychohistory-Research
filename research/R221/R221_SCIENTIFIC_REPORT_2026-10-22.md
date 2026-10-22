# R221 因果中介分析：完全观察等价但自然机制不同的六人工SCM正式研究报告

日期2026-10-22（Asia/Taipei）。原239目录真实编号 **09-012 Causal Mediation Analysis（P2）**。科研状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_SIX_MEDIATION_SCM**。全部为已固定结构方程的人工数理来源E1；新增真人E2=0、真实历史E3=0；并未获得对任何真实心理活动或社会现象存在特定中介机制的因果证据。

## 学术基准、已知边界与源版本

James Robins 与 Sander Greenland (1992), [Identifiability and exchangeability for direct and indirect effects](https://doi.org/10.1097/00001648-199203000-00013), *Epidemiology* 3(2):143–155，指出自然直接/间接效应的识别与混杂问题，不能把条件化中介变量等同于自动识别正确因果路径。Imai, Keele and Tingley (2010), [A general approach to causal mediation analysis](https://doi.org/10.1037/a0020761), *Psychological Methods* 15(4):309–334，构建中介效果的定义、识别、估计与敏感性分析并强调识别条件。Imai, Keele and Yamamoto (2010), *Identification, Inference, and Sensitivity Analysis for Causal Mediation Effects*, *Statistical Science* 25(1):51–71，研究顺序可忽略性下的非参数中介识别。本R221仅基于文献概念独立构造6项人工四潜在来源SCM，而非原作者的真实试验、软件或全部方法复现。

研究在看到任何实际评分之前先提交[原来源、自然效应两种分解、观察估计与验收的冻结协议](../../protocols/R221_CAUSAL_MEDIATION_6_SCM_48_ORIGINAL_SOURCES_PRESCORE_FREEZE_2026-10-22.md)，正式提交[00d8a7e6](https://github.com/edwardsage419/Psychohistory-Research/commit/00d8a7e6e31cca31047640a3b1968a1946a8d9c9)，然后再提交Python程序和CI。没有根据评分结果调整真实机制、中介分布、观测概率、理论对照或识别函数。

## 完整人工原联合来源：六世界×4潜在类型×2真随机处理

真实处理T是独立随机分配的二元变量，P(T=1)=P(T=0)=1/2；潜在U四个类别等概率各1/4，且U与T完全独立。因此每个世界真实可能观测来自4×2=8条原外生×随机处理来源，单条原联合概率1/8；六世界合计**48条完整原始人工来源**，并且每世界原概率严格求和1。这里是八个**互斥可能的人工观察历史**，不是八名随机真人，也不是48项现实独立因果实验。

固定二元潜在中介`M(t,u)`，其共同响应为：
- U=0,1,2,3时，`M(0)=(0,0,1,1)`；
- `M(1)=(0,1,1,1)`；
- P(M=1|T=0)=1/2、P(M=1|T=1)=3/4，两臂内M的0、1都有正概率，符合这里全部非参数观察公式所需的四个T×M格支持。

PURE_DIRECT与ZERO_CAUSAL_EFFECT改用不变中介`M(0)=M(1)=(0,1,0,1)`。全部六真实结果响应面如下：
- **PURE_INDIRECT**：`Y(t,m,u)=m`。
- **LATENT_COMMON_CAUSE_NO_MEDIATION**：`Y(t,m,u)=M(t,u)`，由同一潜在U和处理T确定结果；对M施加独立干预不改变Y，但观察自然M恰好与Y一致，产生潜在中介–结果共同原因。
- **PURE_DIRECT**：`Y=t`。
- **ZERO_CAUSAL_EFFECT**：`Y=0`。
- **ADDITIVE_BOTH**：`Y=t+m`（可取0、1、2，未强行限制二元结果）。
- **TREATMENT_MEDIATOR_INTERACTION**：`Y=t·m`。

每个原观察来源保留实际T、M(T,U)、Y(T,M(T,U),U)，以及仅供**科学审计的隐藏反事实**：M0/M1、四个受控结果`Y(t,m)`与四个自然嵌套结果`Y(t,M(t'))`，共八类反事实，并且始终以同一U建立跨干预反事实身份。任何标为“观察估计”的函数仅接受原数据的`T,M,Y,1/8`，不读取真机制标签、潜在U、反事实或Oracle天然效应。原全来源[CSV](R221_ALL_48_ORIGINAL_MEDIATION_SCM_SOURCES.csv)允许逐原路径审计这些权限边界。

## 定义：一个总效应、两种真正不同的合法自然效应分解

`TE=E[Y(1,M(1))−Y(0,M(0))]`，真结构总效应。定义在固定M0基准的自然直接效应`NDE0=E[Y(1,M0)−Y(0,M0)]`、固定T1的自然间接效应`NIE1=E[Y(1,M1)−Y(1,M0)]`；另定义`NIE0=E[Y(0,M1)−Y(0,M0)]`及`NDE1=E[Y(1,M1)−Y(0,M1)]`。

每个世界均对**四个同一身份U**按真实1/4原来源Fraction计算，逐U先检查可比自然结果，再分别严格验证

`TE = NDE0 + NIE1 = NIE0 + NDE1`。

另对真实随机处理得到的**实际可观察**两臂平均Y计算差，六世界逐Fraction恒等于TE。这里随机T确实保证人工总体总效应的设计识别，但**并不同时保证自然中介效果可从实际观察数据识别**。

## 仅使用观察联合分布的中介公式及额外条件

以完整实际人工观测联合`P(T,M,Y)`独立计算

`gNDE0=Σ_m P(M=m|T0) [E(Y|T1,M=m)−E(Y|T0,M=m)]`

`gNIE1=Σ_m E(Y|T1,M=m)[P(M=m|T1)−P(M=m|T0)]`。

两个gformula函数只读可观察四格的概率、结果条件平均和真正的T随机化源权重，其代数恒有`gNDE0+gNIE1=E(Y|T1)−E(Y|T0)=TE`。但仅当额外的中介–结果因果无混杂、合适的跨世界条件等中介识别假设成立时，二者才能被**解释为真自然NDE与NIE**；不能只因公式可数值计算且拆分和等于TE就称自然机制被识别。

## 六个完整人工世界结果

|已冻真实人工机制|真TE|真NDE0|真NIE1|观察gNDE0|观察gNIE1|观察NIE的偏差|
|---|---:|---:|---:|---:|---:|---:|
|PURE_INDIRECT|1/4|0|1/4|0|1/4|0|
|LATENT_COMMON_CAUSE_NO_MEDIATION|1/4|1/4|0|0|1/4|+1/4|
|PURE_DIRECT|1|1|0|1|0|0|
|ZERO_CAUSAL_EFFECT|0|0|0|0|0|0|
|ADDITIVE_BOTH|5/4|1|1/4|1|1/4|0|
|TREATMENT_MEDIATOR_INTERACTION|3/4|1/2|1/4|1/2|1/4|0|

每个模型另外全部保留`NIE0,NDE1`、真自然Y0/Y1平均、四格中介概率、四格Y条件均值和NDE/NIE观察偏差，完整逐世界Fraction见[六SCM正式JSON](R221_EXACT_RESULTS.json)。六机制没有按代表性社会人口等权得出世界平均“成功率”，各是一个人工条件独立计量。

### 反例A：全部实际观察联合相同，真中介机制完全不同

最强阴性结果是两个机制：PURE_INDIRECT和LATENT_COMMON_CAUSE_NO_MEDIATION。它们对每个U、T的**实际观测**都有相同M及Y=M，因此完整`P(T,M,Y)`的每个概率原子全相等，甚至全部有序8条相应U/T观察行的实际值都相同。两个图T的真实随机化机制完全一致，四个T×M格具有正的实际观察概率，T与真实潜在U确实独立。

但第一模型结果方程`Y=m`真正由M调控，`TE=1/4,NDE0=0,NIE1=1/4`；第二模型结果方程`Y=M(t,u)`不依赖外部干预m，真正`TE=1/4,NDE0=1/4,NIE1=0`。由于所有可观察资料相同，两个模型上的gformula**完全同为NDE0=0,NIE1=1/4**，对第二模型错把全部真实直接机制划为间接中介机制，间接效应偏差+1/4、直接效应偏差−1/4。第二机制即使所有T由研究者**完美随机分配**，潜在U仍将Mediator和Y联系起来；“处理随机化”不是“中介独立随机化”，且不保证顺序可忽略性成立。**只有观测(T,M,Y)的任何估计程序不能区分两者**，并非此次采用某种不够复杂的拟合模型导致的单纯统计误差。

这个不可识别命题针对限定观察量`(T,M,Y)`且U潜在、没有M的额外随机干预；如果研究者能观测足够其他混杂、改变试验设计或额外操纵M，则所拥有的信息可能不同，不能推断此世界在任何研究设计中永远不可识别。

### 反例B：处理–中介交互使“一个固定的效应比例分解”依赖基准

真`Y=t·m`下，`P(M1=1)=3/4,P(M0=1)=1/2`，真TE=3/4。固定中介在**未处理状态M0**时，NDE0=1/2；固定处理在**已处理状态T1**时，NIE1=1/4，得到3/4=1/2+1/4。另一方面固定处理在T0时中介对Y根本没有影响，NIE0=0；在处理后M1状态下NDE1=3/4，得到3/4=0+3/4。两种自然效应拆分均合法且逐U同源数学恒等，而所谓“真实间接效应占总效应的一个唯一比例”在处理–中介效应交互中不成立，须说明确切的反事实基准后才有定义。

### 反例C：总因果效果正确不能保证解释路径正确

所有六世界的实际随机处理观察均值差均等于真正TE，源概率和1，所有四格的中介观测支持均严格非零。但在潜在共同原因的世界中，gformula恰把直接/间接分配反转。故**总效应的随机化识别成功并不检验中介自然效应需要的额外条件**；相同总效应可由不同真实机制组成。对心理史学研究尤须避免以统计相关链或中介统计量机械命名内部心理机制。

## 机器全原样本、CI与永久归档

[原生Python程序与39项固定单元测试](r221_exact_causal_mediation.py)逐来源执行真实T随机化核对、四组TM观察支持、六个自然效应真oracle、两套加总恒等式、完全同分布反例、仅可观察的gformula并对真source分离评分。使用标准库`fractions.Fraction`，无外部API、付费依赖或数值抽样误差。Python 3.11和3.12各39项测试由CI日志完整输出成功，总计**78个通过的测试执行**。[GitHub Actions run39784385018](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39784385018)主工作流实际状态success，第三作业完整重算、核验6世界×8原来源、完整两次自然效应分解和同样观察联合但不同自然效应、原结果SHA，再由机器人永久提交main [70c08466](https://github.com/edwardsage419/Psychohistory-Research/commit/70c0846604fe1d00e0dc933da675f753d7b9fbd5)；两个测试job日志确实各显示`Ran 39 tests`与`OK`。由于某些GitHub作业列表响应可能仍缓存一项“queued”，最终是否全部显示completed/success须以run级conclusion和每job最终独立结果再次核验，不得把缓存当作科学证据。

文件及完整哈希须核对[机器接收JSON](R221_FINAL_MACHINE_ACCEPTANCE.json)：
* [完整六世界精确结果JSON](R221_EXACT_RESULTS.json)；
* [48条真原随机处理、实际观察及自然/受控潜在来源CSV](R221_ALL_48_ORIGINAL_MEDIATION_SCM_SOURCES.csv)；
* [事后有限研究正式验收记录](R221_FINAL_ACCEPTANCE_STATUS.json)；
* [原冻结协议](../../protocols/R221_CAUSAL_MEDIATION_6_SCM_48_ORIGINAL_SOURCES_PRESCORE_FREEZE_2026-10-22.md)。

**R221=CLOSED_BOUNDED_E1_ARTIFICIAL_SIX_MEDIATION_SCM**，有限四U与六人工结构机制外的真实社会机制尚未知，真人E2=0、真实历史E3=0。R073及PESEN v0.1继续冻结。下一真实原239目录**09-013 Causal Inference with Interference（P1）**，研究编号R222；此目录条目历史文献条目标记`R17`并不代表已形成新的完整独立复验结果。仍按先全部原R研究、再统一分类、最后熔炼的用户既定优先顺序。
