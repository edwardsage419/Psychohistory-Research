# R111：McFadden 随机效用和条件 Logit 数学机制学习

2026-10-19。原候选目录P0条目01-005 Random Utility Model；R111是独立研究任务编号，不将两个编号混同。**学习状态 LEARNING_COMPLETE_BOUNDED（仅数学机制、第一手原始文献及纯合成代码）；真人E2=0；PESEN v0.1 FROZEN。**

原学术出处 McFadden (1974) Conditional Logit Analysis of Qualitative Choice Behavior，作者伯克利原件 https://eml.berkeley.edu/reprints/mcfadden/zarembka.pdf 。辅助原作者教材 Train (2009) Discrete Choice Methods with Simulation https://eml.berkeley.edu/books/choice2.html 。

数学进展：冻结独立EV1/Gumbel误差下随机效用达到条件Logit闭式选择概率，正确实现非可用备选概率0、显式噪声尺度、对数似然数值稳定、IID-Gumbel最大效用的随机抽样验证。确认系统效用共同平移的不可辨识性及与噪声尺度同比变化的等价性。复算1974原作者明确指出的汽车与双品牌巴士反例：汽车2/3降至1/2，揭示IID logit的IIA对极相似选项的限制，绝不将限制推广到所有随机效用模型。

独立验证：GitHub Actions [run 39224159791](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39224159791)成功，18项纯合成数学/Monte Carlo测试全通过；[原代码与来源文件完整SHA机读收据](R111_PHASE_A_SYNTHETIC_MATH_CI_ACCEPTANCE_STATUS.json)已经机器人提交并重新读取核实。

* [第一手出处、公式、识别与IIA反例研究报告](R111_MCFADDEN_1974_RANDOM_UTILITY_CONDITIONAL_LOGIT_FORMAL_BOUNDED_LEARNING_REPORT_2026-10-19.md)
* [完整原理源码](r111_mcfadden_random_utility_conditional_logit.py)
* [18项可复运行单元测试](test_r111_mcfadden_random_utility_conditional_logit.py)
* [机器可验收状态](R111_PHASE_A_SYNTHETIC_MATH_CI_ACCEPTANCE_STATUS.json)

验证指令：PYTHONPATH=research/R111 python -m unittest -v research/R111/test_r111_mcfadden_random_utility_conditional_logit.py 。纯标准库、仅人工随机数、固定种子111。该研究没有真实被试效度、竞争模型真人评分、因果机制识别、跨人群外部实验或前瞻预测证据，不能将18项测试称为18次现实模型复现。保持后续独立候选逐项学习，不开展模型熔炼。
