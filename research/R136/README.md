# R136 直接互惠：Press–Dyson 2012 零行列式策略

日期：2026-10-20。原始239模型目录 **P1 / 05-012 Direct Reciprocity**。

研究边界：与R130已完成的1981年TFT和1993年WSLS/Pavlov确定性轨迹分开。本研究读取Press与Dyson的2012年原刊方程，独立计算随机记忆一阶策略的四状态马尔可夫链、稳态收益、零行列式收益约束、收益固定策略及执行失误反例。**本阶段没有新真人E2及真实历史事件E3。**

## 主要严格数学结果

- 在预注册的 14 种可行敲诈参数 × 81 种随机对手策略 = **1,134组**中，独立Fraction稳态线性方程与原文Fig2B行列式方法逐一严格一致，并且全部满足 `s_X−1=χ(s_Y−1)`。
- Equalizer策略 `(9/10,3/4,1/8,1/20)` 对全部81种随机对手给出 `s_Y=5/3`。
- 16种确定性对手中有2种使上述具体敲诈策略的稳态分布不唯一；这些条件下不输出凭空选定的唯一长期平均收益。
- 对χ=3,φ=1/20 的原设计，额外加入项目设定的5%独立执行翻转后，原线性收益约束残差从0变为 `−25/64`。此测试不声称所有噪声下ZD策略均不可能重新设计。
- 共43项本地标准库unittest通过，真实[GitHub Actions 39380956698](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39380956698)已在Python 3.11/3.12各43项、共86次真实执行成功且0失败。每环境独立验ZIP及两Python文件SHA256、重新运行完整1134个ZD案例。

## 一手来源与复算

Press & Dyson (2012), *Iterated Prisoner's Dilemma contains strategies that dominate any evolutionary opponent*, PNAS 109(26):10409–10413。DOI https://doi.org/10.1073/pnas.1206569109 。实际查阅原刊印刷10410–10411页有关Fig2、Eq3–9、11–16，经典囚徒困境收益R=3、S=0、T=5、P=1。2013年Hilbe等有限进化群体文章仅作上下文，没有本期实证或源仿真复现。

原始Python使用Fraction、标准库unittest，**没有额外软件依赖**。下载ZIP、解压、运行：
```bash
python -m unittest -v test_r136_press_dyson_2012_zd_exact.py
python r136_press_dyson_2012_zd_exact.py
```

正式材料：
- [事前冻结协议](../../protocols/R136_PRESS_DYSON_2012_MEMORY_ONE_ZD_EXACT_STATIONARY_PRESCORE_FREEZE_2026-10-20.md)
- [科学研究报告](R136_PRESS_DYSON_2012_DIRECT_RECIPROCITY_EXACT_SCIENTIFIC_REPORT_2026-10-20.md)
- [两份原生Python文件ZIP](R136_ZD_Code_43_Tests.zip)
- [机读数学结果](R136_MATHEMATICAL_RESULTS.json)
- [验收状态](R136_FINAL_ACCEPTANCE_STATUS.json)
- [GitHub Actions工作流](../../.github/workflows/r136-press-dyson-zd-43-tests.yml)

R073与PESEN v0.1继续冻结。遵循全部R系列模型学完后再统一分类与归纳，最后熔炼。

**机器接收凭据**：[R136_PHASE_A_43_TESTS_1134_ZD_GITHUB_CI_ACCEPTANCE.json](R136_PHASE_A_43_TESTS_1134_ZD_GITHUB_CI_ACCEPTANCE.json)。完成有界学习；仍是数学模型复算，没有新真人样本、E2或E3预测。下一R137预计原目录05-013网络互惠。
