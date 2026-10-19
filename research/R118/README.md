# R118：Granovetter 集体参与阈值的有限数学复验

日期：2026-10-19（Asia/Taipei）。原候选目录 **P0 03-019 Threshold Participation**；关联但不重复记作实证的 **P0 04-001 Granovetter Threshold Model / 旧资料源 R02**。

**科研状态**：CLOSED_BOUNDED_GRANOVETTER_1978_ORIGINAL_THRESHOLD_CROWD_THEORY_AND_EXACT_MATH。

**模型学习状态**：LEARNING_COMPLETE_BOUNDED_ORIGINAL_GRANOVETTER_FINITE_THRESHOLD_AND_SYNTHETIC_COUNTEREXAMPLES。

新增真人逐人预测E2=0，R073与PESEN v0.1保持冻结，整体仍处于先R系列学习、后统一分类、最后模型熔炼的阶段。

## 第一手论文

Granovetter M. (1978), Threshold Models of Collective Behavior, American Journal of Sociology 83(6):1420–1443，DOI https://doi.org/10.1086/226707 ；[Stanford托管原刊完整PDF](https://snap.stanford.edu/class/cs224w-readings/granovetter78threshold.pdf)。直接核阅作者印刷1422、1424、1425、1426页：按别人已行动人数或比例定义每个人的门槛；原百人阈值级联案例；阈值累积分布下一期变化公式；最简单版本无成员退出。

## 真正可复算结果

**原作者的百人演算**：门槛为0,1,2,...,99时，从一个自愿入场的门槛0者逐人触发到100人；只把阈值1改成2，最终仅1人。该题是原论文的理论反例，不是100个真正发生骚乱的人类观察。

**本项目新数学构造**：进一步把原门槛99改为98，抵消前面的+1。两组100人的门槛和皆为4950，均值精确为49.5；第一组最终100人，第二组最终1人。该两人修改、均值完全相等案例是研究者额外创造的逻辑反例，不属于原论文的实证证明。

**算法**：一套同步逐期入场（不退出）和一套独立排序法，从无先行参与者的初始状态分别求可达最小集体参与闭包。模型只观察**全群体**已参与人数，不是邻居网络阈值传播；人群真实阈值与历史变化尚未测量。

GitHub Actions [运行 39248405444](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39248405444) success：**44项纯数学/合成单元测试全部通过，0失败**。另外对 n=1…5 所有合法有序整数阈值向量进行了2+9+64+625+7776=**8476个数学配置的完整枚举**，两个独立求解器结果一致、参与轨迹单调且最终满足阈值固定点。这不是8476次真人实验。

## 资料与复验

- [原论文与模型边界冻结协议](../../protocols/R118_GRANOVETTER_1978_THRESHOLD_PARTICIPATION_FINITE_CROWD_PRECALC_FREEZE_2026-10-19.md)
- [详细一手机制及平均值反例研究报告](R118_GRANOVETTER_1978_THRESHOLD_CROWD_EXACT_DISTRIBUTION_AND_SAME_MEAN_SCIENTIFIC_REPORT_2026-10-19.md)
- [可执行标准库Python原理实现](r118_granovetter_1978_finite_threshold_participation.py)
- [44项独立数学/合成测试](test_r118_granovetter_1978_finite_threshold_participation.py)
- [真实CI、原始源文件SHA及全枚举机器收据](R118_PHASE_A_1978_THRESHOLD_44_TEST_EXHAUSTIVE_CI_ACCEPTANCE.json)
- [正式科研验收](R118_FINAL_ACCEPTANCE_STATUS.json)

标准库复算：PYTHONPATH=research/R118 python -m unittest -v research/R118/test_r118_granovetter_1978_finite_threshold_participation.py 。

证据边界：数学源文与算法核验E1成立，真实原人行为数据E2=0、现实事件前瞻预测E3不存在；没有个体收益、政治倾向、规范预期或社会网络身份的独立测量。后续仍继续既定其他R模型学习，不提前模型融合。
