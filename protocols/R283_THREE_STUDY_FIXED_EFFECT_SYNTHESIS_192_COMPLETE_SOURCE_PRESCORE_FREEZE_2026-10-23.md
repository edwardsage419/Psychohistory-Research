# R283 系统综述与元分析：三个假想研究、192完整来源及异质性与择优偏差；事前冻结

日期2026-10-23 Asia/Taipei。原239候选目录12-013 Systematic Review and Meta Analysis（P1）。核心文献Page et al. (2021), *The PRISMA 2020 statement: an updated guideline for reporting systematic reviews*, BMJ 372:n71, DOI https://doi.org/10.1136/bmj.n71；Higgins et al. (2003), *Measuring inconsistency in meta-analyses*, BMJ 327:557–560, DOI https://doi.org/10.1136/bmj.327.7414.557。
**本项不是实际文献系统综述，也未检索/筛选任何真人论文或从发表研究提取效应。** 模型只用三个虚构的预登记“研究”测试系统综述中预先固定完整纳入与效应汇总算法；PRISMA仅是文献报告透明度的理论参照，不能自称已执行PRISMA系统综述。

## 冻结研究注册与纳入规则
完整假想registry恰三个研究ID S1、S2、S3，每项只有一条处理观察T_i和一条对照观察C_i，全部二元，每项报告风险差d_i=T_i−C_i。三项**必须全纳入**，无结果导向挑选、无真实论文、无检索数据库、无PRISMA流程图。三个人工生成世界：
- HOMOGENEOUS: (P(T),P(C))逐研究均(3/4,1/4)，真效应(1/2,1/2,1/2)；
- BALANCED_HETEROGENEITY: 研究逐项分别(3/4,1/4)、(1/2,1/2)、(1/4,3/4)，真效应(1/2,0,−1/2)；
- ONE_REVERSAL: 研究逐项分别(3/4,1/4)、(3/4,1/4)、(1/4,3/4)，真效应(1/2,1/2,−1/2)。
每world依顺序`T1 C1 T2 C2 T3 C3`六个互相独立二元观察，2^6=64个完整有序原source，其质量∏_{i=1}^3 pTi^Ti(1−pTi)^(1−Ti) pCi^Ci(1−pCi)^(1−Ci)。三world共**192个带机制标签完整原source**，全部具有正概率（不会将192等同真实独立研究）。

## 冻结统计量及可实施性边界
研究风险差d_i=T_i−C_i，理论真实δ_i=pTi−pCi。**假设研究内部方差已由真生成机制直接给出** `v_i=pTi(1−pTi)+pCi(1−pCi)`；权重w_i=1/v_i，固定效应加权估计`D=Σw_i d_i/Σw_i`，目标`δ_w=Σw_i δ_i/Σw_i`，理论估计方差`Var(D)=1/Σw_i`。在每试验只有一条处理一条对照时，v_i根本无法从该试验本身稳定估计；本研究权重为**知道人工DGP的oracle设计权重**，不能包装成从真实文献提取的可部署标准差。
冻结Cochran式加权离差 `Q=Σw_i(d_i−D)^2`。理论独立来源期望 `E[Q]=(3−1)+Σw_i(δ_i−δ_w)^2`，第一项为随机抽样噪声基线（2），第二项为三研究真效应异质性带来的额外Q；不使用Q推导真实显著性阈值，不把Q硬判为I²真实估计。
用于显示选择性报告风险的**不合法post hoc策略** `SELECT_MAX=max(d1,d2,d3)`，不代表预先固定全研究合成结果。比较E[SELECT_MAX]与δ_w以显示只报最有利研究的偏差。

## 事前冻结世界级精确真值
|人工world|固定oracle逆方差权重(w1,w2,w3)|真实δ_w|Var(D)|E[Q]|E[SELECT_MAX]|
|---|---|---:|---:|---:|---:|
|HOMOGENEOUS|(8/3,8/3,8/3)|1/2|1/8|2|469/512|
|BALANCED_HETEROGENEITY|(8/3,2,8/3)|0|3/22|10/3|175/256|
|ONE_REVERSAL|(8/3,8/3,8/3)|1/6|1/8|34/9|419/512|

路线A完整枚举三world各64个原来源，计算各study d_i、固定效应加权D、Cochran Q、post hoc SELECT_MAX、原六bit和原来源质量，准确Fraction加权计算E[D]、Var(D)、E[Q]和E[SELECT_MAX]。
路线B不使用完整六bit原source枚举，直接利用各study独立三值分布：P(d=+1)=pT(1−pC)、P(d=−1)=(1−pT)pC、P(d=0)=pT pC+(1−pT)(1−pC)。解析闭式给出δ_w、方差和E[Q]；另外利用全部3^3=27三值类别组合计算E[SELECT_MAX]，与路线A全source逐Fraction一致。
路线C GitHub Actions第三独立Python审核不导入研究执行程序，逐CSV原source重建6bit全部64配置、各源质量、三study d、oracle权重、D、Q、SELECT_MAX和所有解析真值及SHA256；拒绝漏掉任意S1/S2/S3研究、将SELECT_MAX冒称合成结果或错误赋予真实系统综述的证据等级。

先单独GitHub commit冻结本协议，后实现完整研究数据、结果JSON、可运行Python标准库、报告与机读收据；Python3.11/3.12各≥45真unittest、第三原source审计全成功、完整192 source CSV及结果JSON与SHA机器人永久main归档后才允许**有界人工E1**结题。没有真实文献检索/真实论文样本、新真人E2或历史E3；R073/PESEN v0.1保持冻结。下一原目录12-014 Publication Bias Diagnostics（拟R284）。
