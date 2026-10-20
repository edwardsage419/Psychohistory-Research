# R142 事前冻结协议 — Carlsson–van Damme 1993 / Morris–Shin 1998 全球博弈的离散信号边界

日期：2026-10-20。原候选目录 P2 05-018 Global Games。**本文件在R142模型程序和测试编写前提交**，一手原文检查不等于重新复现作者完整连续分布唯一性证明。

一手实际可视读：
1. Carlsson, Hans & Eric van Damme (1993), “Global Games and Equilibrium Selection,” *Econometrica* 61(5):989–1018, DOI 10.2307/2951491。原刊版面 https://scispace.com/pdf/global-games-and-equilibrium-selection-4o1gmi0b88.pdf ，亲核原印刷989/993页：不完全信息的私有噪声，iterated dominance，2×2 risk dominance，knowledge与common knowledge区分。该稿的进一步广义结论需要连续信号、小噪声及限制，不能声称任意有限离散噪声都唯一。
2. Morris, Stephen & Hyun Song Shin (1998), “Unique Equilibrium in a Model of Self-Fulfilling Currency Attacks,” *American Economic Review* 88(3):587–597。MIT作者托管原刊全文 https://economics.mit.edu/sites/default/files/publications/morris-uniqueequilibriuminamodelofselffulfillingat.pdf，实际核阅原印刷588、590：政府/连续投机者/攻击或不攻击、单位交易费、私有条件信号在[θ−ε,θ+ε]均匀分布且独立，政府观测θ及攻击比例；在完整前提下得到唯一阈值均衡。离散模型以下不是其原国家货币银行危机模型的精确复演。

本项目新建、明确标注E1 **离散2人条件关联信号的贝叶斯协调博弈**。θ∈{-2,-1,0,1,2}、各等可能（先验1/5）；两名玩家以条件于θ独立的信号x_i=θ+ε_i行动。噪声h∈{0,1,2}；当h>0，ε∈{-h,0,+h}概率{1/4,1/2,1/4}；h=0全部概率集中ε=0。玩家在所见x_i为条件类型时在安全S(收益0)与攻击/冒险A之间选，A收益θ−κ+2·1{对手也A}；κ∈{3/4,1,5/4}，绝不引申到Morris–Shin作者的连续政府撤钉模型。策略是按其实际出现的全部x值指定确定性0/1行动的完整类型应对表；两位玩家都独立选自己的应对表。不包含mixing或双层对手学习。私人各见x而不见θ或对手信号/动作。

冻结9组合(h,κ)，对所有实际可能信号对应的全部 2^m 策略逐一计算**纯Bayesian Nash equilibria**，均衡定义为每个正概率类型在对方固定策略下都不存在盈利单侧变更，允许有相等效用时的多个最佳反应；不把“唯一纯Bayesian Nash”写成“所有混合贝叶斯均衡都唯一”。联合概率由整数权 w(θ,x,y)=noise_numerator(x-θ)noise_numerator(y-θ)，分母为80，联合条件收益差精确score(x,other policy)=sum_theta,y w*(4θ-4κ+8*other_attack(y))，得真实条件净差score/(4 sum_world_w_for_x)。所有有理数严格用整数/Fraction，无随机模拟亦无浮点凑零。策略遍历2^m，对每组所有政策二元组2^(2m)；在正权类型对任何存在盈利的安全/进攻偏离即判非均衡。

研究比较：h=0,κ3/4下θ=-1与0各有两个严格纯协调均衡（A,A与S,S），其它θ有唯一严格动作，理论预计完全信息有4套全信号纯Bayesian政策均衡；要复验其他κ和噪声，**冻结不预测**正噪声一定消灭多重。风险优势：已知θ=0、κ3/4时A对(A)的单位增益5/4、安全偏离A损失3/4，A为风险占优但A/S均属Nash；这仅是单状态2×2结果，不证明整个离散全球博弈自动风险占优选择。比较h=1,2时纯BNE数量和具体攻策略阈值是否由信号单调，可出现边界/多个均衡并准确报告。

独立验收路线：预先枚举联合世界权并算精确条件后验 (θ,opp x|own x)，与归并整数score逐策略对比；按类型符号推导各玩家逐信号最佳反应集合，与逐个类型实际收益的全策略比较结果一致；核验交换两位玩家保持分布及角色对称，先验、条件边缘与归一；非法h/κ、float/bool拒绝；显式显示对应完全信息2×2多个纯NE与BNE区别；若离散模拟存在正噪声多个均衡，明确不得归为原论文定理反例，因为模型限制不同。

任何研究结果只用于有限人工理论范围、E2真人0，E3历史事件预测0，R073与PESEN v0.1继续冻结。源码/单元测试/机读JSON必须SHA256归档；远端GitHub Actions Python3.11/3.12真实运行且独立完整重算才可CLOSED_BOUNDED。原R学习完毕后再统一归纳、分类、熔炼。
