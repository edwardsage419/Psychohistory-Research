# R142 全球博弈：私人信号与有限纯贝叶斯均衡

2026-10-20，原239模型目录P2 05-018 Global Games。

一手文献核验：Carlsson and van Damme (1993) Econometrica 61:989–1018 DOI 10.2307/2951491，原刊989、993、994页；Morris and Shin (1998) AER 88:587–597，原刊588、590、591页。前者的风险优势/迭代优势消除，后者的连续投机者+连续信号+政府弃钉模型，**均不等于本期两人有限离散信号的数学例**。

本期从项目自建θ∈{-2,-1,0,1,2}、两位玩家独立有噪声私人信号、风险行动收益θ−κ+2·1{对方也风险行动}构造有限Bayesian协调游戏。h∈{0,1,2}，κ∈{3/4,1,5/4}，完整枚举9种人工情境及**838656对**纯条件策略，双路径独立重建正概率信号类型的全部纯Bayesian Nash。纯均衡数：
- h0: 4、8、4；
- h1: 2、2、2；
- h2: 8、10、8。
存在私人信息的离散人工例仍可多重均衡；不能将作者连续微扰模型唯一性定理泛化成“任何私人噪声就必然唯一”。h1与h2不是已经论证的Blackwell嵌套信息实验，不得当作均衡数随噪声恶化的单调规律。只计纯BNE，不含混合策略BNE。首次55项本地测试捕获3项输入验证先后与lru_cache键别名的缺陷，修正后全部55项通过。

研究证据：纯E1人工模型。新真人行为E2=0；现实历史事件E3=0。R073、PESEN v0.1冻结，先完成全部R再统一分类，最后熔炼。

文件：
- [计算前冻结协议](../../protocols/R142_CARLSSON_VANDAMME1993_MORRIS_SHIN1998_FINITE_PRIVATE_SIGNALS_BAYES_NASH_EXACT_FREEZE_2026-10-20.md)
- [数学与一手文献报告](R142_SCIENTIFIC_REPORT_2026-10-20.md)
- [Python程序、55项测试、完整原生JSON的ZIP](R142_Finite_Global_Games_55_Tests.zip)
- [机器结果摘要](R142_MACHINE_RESULTS_SUMMARY.json)
- [验收状态](R142_FINAL_ACCEPTANCE_STATUS.json)
- [GitHub Actions](../../.github/workflows/r142-finite-global-games-55-tests.yml)

解压ZIP并执行：`python -m unittest -q test_r142_finite_private_signals.py`、`python r142_finite_private_signals.py > replay.json`。依赖仅Python标准库。
