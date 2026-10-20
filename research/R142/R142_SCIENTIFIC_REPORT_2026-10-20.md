# R142 全球博弈科学报告：原始连续理论与离散私人信号局限

2026-10-20；P2 / 05-018 Global Games；E1项目人工精确贝叶斯博弈，未产生E2或E3。

## 一手论文真实核读

**Carlsson and van Damme (1993)**，*Global Games and Equilibrium Selection*，Econometrica 61(5):989–1018，DOI https://doi.org/10.2307/2951491，原版版面 https://scispace.com/pdf/global-games-and-equilibrium-selection-4o1gmi0b88.pdf 。实际可视核对原印刷989页摘要及2×2全球博弈定义、993页多阶共同知识的缺失与预期行为、994页Eq(2.1)风险占优偏离损失乘积及Eq(2.2)混合无差异概率。作者的特定噪声极限与迭代严格支配结论不自动适用于本次有限离散信号结构。

**Morris and Shin (1998)**，*Unique Equilibrium in a Model of Self-Fulfilling Currency Attacks*，American Economic Review 88(3):587–597，MIT原刊扫描 https://economics.mit.edu/sites/default/files/publications/morris-uniqueequilibriuminamodelofselffulfillingat.pdf 。实际核对印刷588页信息失去共同知识及1998货币投机模型起始定义、590页条件于基本面连续均匀私人信号、591页Eq(1)–(4)攻击比例/国家退出/私人后验预期支付计算。本期**没有复现**1998的政府、货币市场、连续玩家、连续信号及唯一性完整证明。

## 数学精确实验冻结

[远端计算前协议](../../protocols/R142_CARLSSON_VANDAMME1993_MORRIS_SHIN1998_FINITE_PRIVATE_SIGNALS_BAYES_NASH_EXACT_FREEZE_2026-10-20.md)，原始提交`4440f6046cf019d7628c1c8b5f509ea1d13d3adf`先于代码。两名玩家，θ在{-2,-1,0,1,2}均匀，私人信号x=θ+η，条件独立；h=0时η=0，h=1、2时η∈{-h,0,h}且权{1/4,1/2,1/4}。双方选择安全S获得0或冒险A获得θ−κ+2·1{对方A}。κ∈{3/4,1,5/4}，合计9个预定义模型。不将其误写为已发表源论文的原数值模型。

所有可能世界用整数w(θ,x,y)编码，真实概率是w/80。令κ=K/4，则每个私人信号类型x对对方策略q(y)的**严格分数净收益差**为

`Delta(x|q) = sum_{theta,y}[w(theta,x,y)*(4*theta-K+8*q(y))] / [4*sum_{theta,y}w(theta,x,y)]`。

甲、乙各按其可能观察的每个x选择确定性A/S完整表，每人5/7/9个类型、32/128/512种纯策略。每组(h,K)逐个检查所有两人纯策略对的每个正概率类型的单侧盈利偏离：每成本的配对数h0=1024、h1=16384、h2=262144，三成本合计**838656**。独立验证A:按联合类型概率压缩再以位掩码求最优反应；B:不使用压缩条件收益函数、直接枚举完整(θ,x,y)世界并逐类型计算签名和全部纯贝叶斯均衡。每组全均衡列表一致；所有条件后验恰加总为1、两个玩家交换对称、输入严格拒绝float/bool。**混合贝叶斯均衡未枚举**。

## 数学结果

| h | κ=3/4 | κ=1 | κ=5/4 |
|---:|---:|---:|---:|
| 0 | 4 | 8 | 4 |
| 1 | 2 | 2 | 2 |
| 2 | 8 | 10 | 8 |

h1各成本均有2种纯均衡，均按信号大小单调，κ3/4时采取A的信号分别是{1,2,3}或{0,1,2,3}。h2 κ3/4有8个纯均衡，其中非单调纯策略的具体见证：mask490，对可能信号{-4,-3,-2,-1,0,1,2,3,4}选择A时的集合{-3,-1,1,2,3,4}。非单调系项目人工离散支撑/条件信号结构的结果，不能外推现实人类决策。

θ=0、κ=3/4的完全信息2×2协调博弈既有(S,S)又有(A,A)两个纯NE；(A,A)一人偏离损失5/4，大于(S,S)偏离损失3/4，故A风险占优。但**有风险占优≠对任何私人离散信号模型具有唯一全局纯均衡**。h=1与h=2使用不同间距三点误差，不保证形成Blackwell信息序列，不可解释为已识别的“噪声精度变化的因果单调效应”。h0亦非连续微扰理论中同一家族噪声趋零的严格极限。

## 本地测试与科学边界

本期55项unittest首次运行发现3个输入类型拒收测试失败，缘于Python lru_cache按数值哈希把整数1、浮点1.0及True视作等价键，绕过内部校验；修复为**外层在缓存前验证输入**，之后55项测试全通过，结果重新生成。机器研究原件ZIP内含两个.py与`R142_EXACT_RESULTS.json`，GitHub Actions必须校验ZIP及三内部文件SHA256，重新跑55项测试与完整JSON字节完全相等方可验收。

研究不包含2011/1998的国家汇率实证、私人信号实际校准、政策识别、跨地区历史事件概率验证，E2=0、E3=0；R073与PESEN v0.1冻结。坚持研究完全部既定R候选后统一归纳，再熔炼。

## 最终GitHub机器验收

由来源提交 `0f5d2d29586dce0d4225ad66b44b1ee28109e835` 触发的 [GitHub Actions run39393180597](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39393180597) 已完成，conclusion success。job118529382161 Python3.11真实55 tests in 0.326s；job118529382571 Python3.12真实55 tests in 0.337s，总计110次单测0失败。各任务在运行前分别验证ZIP SHA256 `8cfa1ff3b015f984411d821ecc79b9672a1a8dc26e30716d589dd61ddd83e832`、原计算程序 `e4da562dc6a81d56cb655729937d08f0eec6cb27368ec6b4043e4c55a4d338e7`、测试 `069c766a8956757dadd7430ec4ff4f66070b9f4e0b0cbdf6ef888dc8bd64c84d`、JSON `0d376c2ac57ea152c2e38ac4d16013214d07660f311885be45b52af39561a5d4`，各4项OK；之后各跑独立55单元测试及完整838656两人纯策略计算，重算JSON逐字节匹配，日志确实输出`R142 PASS exact 838656 strategy pairs, all 9 private signal games, all sources SHA256`。结题凭据见[R142_PHASE_A_110_REAL_TESTS_838656_FINITE_PURE_BNE_CI_RECEIPT.json](R142_PHASE_A_110_REAL_TESTS_838656_FINITE_PURE_BNE_CI_RECEIPT.json)。这仅是有限人工博弈E1代码远端计算身份与严格复验，不是1993/1998连续理论全文证明的重现，也非真人或事件E2/E3实证。
