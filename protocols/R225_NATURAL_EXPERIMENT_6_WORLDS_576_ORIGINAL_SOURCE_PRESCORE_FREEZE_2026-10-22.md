# R225 自然实验设计：六人工外部配额世界、576完整原来源与表面平衡伪识别反例，计算前冻结

日期：2026-10-22。原始239项目录真实第 **09-016 Natural Experiment Designs（P1）**。研究编号R225。与此前R210随机对照、R213工具变量、R214断点、R215双重差分的实验对象独立，本实验检验**外部处理安排是否真正与潜在结果可交换**，以及前期平衡与零placebo的识别边界。没有外部真实政策，所有原数据均人工E1。

参考文献：
* Dunning (2008), *Improving Causal Inference: Strengths and Limitations of Natural Experiments*, Political Research Quarterly 61:282–293, DOI https://doi.org/10.1177/1065912907306470；以及Dunning (2012) *Natural Experiments in the Social Sciences*, Chapter 8, DOI https://doi.org/10.1017/CBO9781139084444.012，强调先检验“as if random”的真实可信性再计算因果效应。
* Titiunik (2021), *Natural Experiments*, in *Advances in Experimental Political Science*, DOI https://doi.org/10.1017/9781108777919.008，指出“自然实验”称谓有多种使用方式，不能把外部事件表面看来随机视为识别充分条件。
* Hernán and Robins (2006), *Estimating causal effects from epidemiological data*, DOI https://doi.org/10.1136/jech.2004.029496，作为处理组可交换性与观察关联/因果效应区分的背景。项目不复现任何上述论文或书籍的原经验数据或一般理论定理。

## 预冻有限总体、观察和干预

固定四个人工单位 i∈{0,1,2,3}，两个结局时间 pre/post，处理 D_i∈{0,1} 在post出现，四人中恰好两人接受处理。外部配额只允许6个完整处理向量，每种概率1/6。完整四人后期独立Rademacher冲击ε_i∈{−1/4,+1/4}，全部16组概率1/16，故每世界6×16=96个互斥真原来源，六世界合计**576条**，每条概率1/96。各世界每个来源保存原分配索引、4位完整潜在类别U、4位实际Z/D、四个pre、四个后期未经处理潜在结果Y0、四个后期处理潜在结果Y1、四个实际post结果、原冲击4元组及真实概率。

六冻结世界如下。单位固定外生常数0,1,2,3仅充当身份，均不宣称是真人：

1. **AS_IF_RANDOM_VALID**：原六个外部配额Z与后期潜在结果独立；所有pre_i=1；post_i(0)=1+ε_i，post_i(1)=post_i(0)+1。真总体ATE=1。Z=6个配额按均匀概率独立生成。
2. **ENDOGENOUS_FUTURE_SHOCK_ALIAS**：外部未见未来U向量先在六个恰好两人1的向量中等概率生成，Z=U；pre_i=1；post_i(0)=1+U_i+ε_i，post_i(1)=post_i(0)。真总体ATE=0。**实际完整 (Z,pre,post) 的概率分布必须与1完全相同**，同时六个Z值、观察前期平衡、所有后期有处理组/控制组均相同。
3. **AS_IF_RANDOM_NULL**：Z均匀独立，pre_i=1；post_i(0)=post_i(1)=1+ε_i。真ATE=0。
4. **AS_IF_RANDOM_HETEROGENEOUS**：Z均匀独立，pre_i=1；post_i(0)=1+ε_i，post_i(1)=post_i(0)+i。真平均ATE=(0+1+2+3)/4=3/2。异质真效果下处理对照均值差的均匀设计期望仍须独立验算为3/2。
5. **ENDOGENOUS_VISIBLE_SELECTION**：U如世界2，Z=U；pre_i=1+U_i；post_i(0)=1+U_i+ε_i，post_i(1)=post_i(0)。观察pre组差=1，未经调整后期组差=1，真ATE=0；以本世界固定差分机制，组间前后变化差的期望应为0。前期失衡在此可见，区别于世界2同样选择却完全隐藏的未来冲击。
6. **ANTICIPATORY_PRE_RESPONSE**：Z均匀独立；pre_i=1+Z_i/2（冲击已公告、正式政策前提前响应），post_i(0)=1+ε_i，post_i(1)=post_i(0)+1。真后期ATE=1，但前期处理组与控制组差1/2、DID趋势差只有1/2。预期处理组提前响应违背no-anticipation条件。

**潜在因果目标**：固定为随机选一单位、保持外生U与ε和其他人的政策不变，将该单位的post D从0改为1所产生的平均Y1−Y0。对于ENDOGENOUS_FUTURE_SHOCK_ALIAS，U为未观察的自然未来冲击，共享Z的上游原因；do(D)不能改变U，因此真效果仍0，不能把U=Z的观察关系误当机制。

## 观察估计、数学风险和核验

1. **post-treated minus post-control**，每个原分配源恰好两名处理与两名控制，用观察post平均差计算。
2. **pre-period placebo balance**，同一源的pre处理与控制均值差。
3. **fixed two-period DiD**，每单位post−pre变化的两组均值差。
4. 三种统计必须只读取实际Z、pre、post与原事件权重，禁止读取隐藏U、结构反事实潜在结果和真实oracle。另用潜在Y1−Y0仅计算外部真ATE。
5. 完全枚举每世界96源计算E、Bias、Variance、MSE（所有Fraction），与第二独立解析路线核对：对于给定Z，16个独立E_i的零均值让估计期望回到无噪声行；各统计后期独立冲击项方差恰为**1/16**（每人加权系数±1/2，ε方差1/16，合计4×(1/4)×(1/16)=1/16），各世界总方差=固定Z条件均值波动方差+1/16。pre纯确定不含ε。
6. 完整观察`P(Z-vector,pre-vector,post-vector)`进行逐状态精确概率比对，世界1与2必须完全一致，但真ATE分别1与0、两者preplacebo=0、DiD观察期望均1。
7. 仅在世界1/3/4这种真正外生完整随机处理配置下，才能以设计期望把均值估计与真ATE联系；世界2/5不能用观察“每人分配概率1/2、总体配额平衡”代替潜在结果与Z独立条件；世界6用DID时须解释预期提前响应。
8. 双Python3.11/3.12各运行至少40单测，第三GitHub CI job产生576条原来源CSV、六世界Fraction汇总及机器SHA验收并永久提交main。只有CI通过与原文件SHA入库后才允许正式E1结题；失败或接口不一致时保留原失败证据。

本阶段状态 `PRESCORE_FROZEN_E1_PENDING_EXECUTION`。R073和PESEN v0.1冻结，真人E2新增0，真实历史E3新增0。后续继续原目录09-017模型，完成既定R系列后统一归纳分类，最后熔炼。
