# R224 负对照设计：八个人工机制、4096完整外生来源与错误安慰反例，评分前冻结

日期：2026-10-22。真实原始239模型目录 `09-015 Negative Control Designs`，研究编号 `R224`，优先级P1。科研资格仅为**人工有限数学机制E1**。依所有者顺序继续完成既定R系列之后统一归纳分类，再进行熔炼，不修改R073/PESEN v0.1。

## 文献与方法边界

* Lipsitch, Tchetgen Tchetgen & Cohen (2010), *Negative controls: a tool for detecting confounding and bias in observational studies*, Epidemiology 21:383–388, DOI https://doi.org/10.1097/EDE.0b013e3181d61eeb。论文区分负对照暴露和负对照结果，提醒负对照能指示潜在偏差，强度无法在缺少额外条件时直接推成目标偏差量。
* Shi, Miao & Tchetgen Tchetgen (2020), *A Selective Review of Negative Control Methods in Epidemiology*, Curr Epidemiol Rep 7:190–202, DOI https://doi.org/10.1007/s40471-020-00243-4。论文讨论负对照识别所需条件与双负对照的附加约束。
* Miao, Geng & Tchetgen Tchetgen (2018), *Identifying Causal Effects With Proxy Variables of an Unmeasured Confounder*, Biometrika 105:987–993, DOI https://doi.org/10.1093/biomet/asy038。至少两个合格代理变量和秩条件下的识别结果仅作为外部方法背景，本次**不执行**该论文的一般代理恢复证明、代理秩检测或真实数据复现。

实验目标是构造负对照有信号、无信号、错误选择与控制强度不匹配的数学反例，严守原机制的因果排除限制。任何观察到的偏差预警都不直接代表真实混杂的唯一解释。不存在真实患者、真实决策者或实证因果识别。

## 冻结外生源与八世界

隐含二元U∈{0,1}，P(U)=1/2；四个互相独立等概率整数V_A,V_Z,V_W,V_Y∈{0,1,2,3}。所有变量均由严格确定性阈值构造；每世界完整 2×4⁴ = **512 条原外生来源**，八世界共 **4096条**，每行真概率1/512。实验中随机化仅是人工生成机制，全部统计精确使用Fraction计算，无采样误差。

固定目标暴露 A、负对照暴露候选Z、负对照结果候选W、主要结局Y。对每行U,V源结构产生
A=1{V_A<p_A(U)}；Z=1{V_Z<p_Z(U)}；
W=1{V_W<c_W(A,U)}；Y=1{V_Y<c_Y(A,U,Z)}。
所有阈值是0..4整数，对应概率阈值/4；Y真实人工干预差固定`ATE=E[Y(do(A=1))−Y(do(A=0))]`，保持同一U和V各类型，Z由U及其外生V决定。另记录真`Z→Y`受控因果效应以检测负对照暴露假设是否失效，以及真`A→W`受控效应以检测负对照结果假设是否失效。

各世界固定规则（表中 `(x,y)` 表示 U0,U1 计数阈值/4，`Y0/Y1` 是A=0和A=1在给定U、Z下Y的阈值）：

| 世界 | A阈值 | Z阈值 | W阈值 | Y阈值 |
|---|---|---|---|---|
| RANDOMIZED_WITH_Z_SIGNAL | (2,2) | (1,3) | (1,3) | Y0=Y1=(1,3) |
| HIDDEN_CONFOUNDED_NULL | (1,3) | (1,3) | (1,3) | Y0=Y1=(1,3) |
| HIDDEN_CONFOUNDED_CAUSAL | (1,3) | (1,3) | (1,3) | Y0=(0,2),Y1=(1,3) |
| INSENSITIVE_VALID_CONTROLS | (1,3) | (2,2) | (2,2) | Y0=Y1=(1,3) |
| INVALID_OUTCOME_DIRECT_A | (2,2) | (2,2) | W(A=0)=(1,1),W(A=1)=(3,3) | Y0=Y1=(1,3) |
| INVALID_EXPOSURE_DIRECT_Z | (2,2) | (2,2) | (2,2) | Y(Z=0)=(1,1),Y(Z=1)=(3,3),与A无关 |
| CANCELLED_INVALID_OUTCOME | (1,3) | (2,2) | W(A=0)=(1,3),W(A=1)=(0,2) | Y0=Y1=(1,3) |
| MISMATCHED_VALID_OUTCOME | (1,3) | (1,3) | (1,2) | Y0=Y1=(1,3) |

除显式声明的两种无效负对照外，W仅依U且无A→W直接效应，Z不参与Y方程。对INSENSITIVE_VALID_CONTROLS两个候选对照均合法排除直接效应但不共享主要U偏差；因此可出现真正混杂而负对照统计零。CANCELLED_INVALID_OUTCOME中W的真A→W因果依赖与U混杂正关联相抵消，预期A-W零值，无效的假设不能被表面零值发现。

## 事前统计与验收

1. 从原来源 `P(A,Z,W,Y)` 计算整体观察风险差 `D_AY=E[Y|A=1]−E[Y|A=0]`、负对照结果关联 `D_AW`、负对照暴露关联 `D_ZY`、`D_ZW`，另计算真干预 `ATE`、`A→W` 与 `Z→Y` 的真正do值。所有这些统计都由完整来源求和，严禁用隐藏U或真实潜在值计算观察估计。
2. 仅作**演示性、未经合法识别保证的朴素负对照校正** `D_AY−D_AW`，与真ATE比较。HIDDEN_CONFOUNDED_NULL可恰好0；MISMATCHED_VALID_OUTCOME预期不为0，即使W排除A→W成立，也不能未经偏差比例校准就把对照差直接从主要差减掉。
3. 预定数学断言：RANDOMIZED_WITH_Z_SIGNAL中D_AY=0而D_ZY≠0；HIDDEN_CONFOUNDED_NULL中D_AY=D_AW=1/4且真ATE=0；HIDDEN_CONFOUNDED_CAUSAL中真ATE=1/4、D_AY=1/2；INSENSITIVE_VALID_CONTROLS中真ATE=0、D_AY=1/4而D_AW=D_ZY=0；INVALID_OUTCOME_DIRECT_A中真ATE=0、D_AW=1/2且真A→W=1/2；INVALID_EXPOSURE_DIRECT_Z中真ATE=0、D_ZY=1/2且真Z→Y=1/2；CANCELLED_INVALID_OUTCOME中D_AW=0且真A→W=−1/4；MISMATCHED_VALID_OUTCOME中D_AY=1/4、D_AW=1/8、朴素校正=1/8而真ATE=0。
4. 第二条独立计算路线：直接对固定参数阈值按U的精确条件风险积分，重算D_AY、D_AW、D_ZY和干预ATE，与逐4096原源枚举完全一致。源码两个计算路径的共享只允许固定输入生成表，不允许共享已算的汇总统计。
5. 使用Python标准库的Fraction、csv、hashlib、json、unittest，双Python3.11/3.12测试（每版至少40测试）和第三个完整原来源永久归档GitHub Actions作业。科学报告、正式验收JSON仅在CI真实运行、来源SHA校验和原资料归档核实之后撰写。
6. 八世界原来源、观察统计、真干预oracle与所有负对照假设违反标记需分别记录。保证不将未执行的双代理因果恢复、现实因果推广或文献理论内容混入本实验验收。

状态：`PRESCORE_FROZEN_E1_PENDING_IMPLEMENTATION_AND_CI`，新真人E2=0、历史E3=0。
