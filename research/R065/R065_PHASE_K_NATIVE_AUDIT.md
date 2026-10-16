# R065 Phase K：原作者七目标函数原生执行及 Model 3 锚点

日期：2026-10-16。已冻结的研究协议：[Phase K](../../protocols/R065_PHASE_K_NATIVE_7_OBJECTIVES_GATE_2026-10-16.md)，事前提交 32abf4909c35d67c07d043d1d524a5b9db73f7ef。该阶段属于既有 Phase J 之后的原生执行可行性审计。

## 来源与核验

原作者：arielevy8/obs-learning-fishing，固定提交 fd5f435b5368b69916e7acc6a9991aa5f46b3ddb。

* model_fitting/objectives.py Git blob：5e98133fa274ef2a112b24f6fdcd802d4f9d3eec。
* model_fitting/fit_utils.py Git blob：6046f083a1181b10a7d991c8c9fd2e53c1f2b487。
* 处理数据 Git blob：01bf211468abe093618dfa5e5c39e883230c9c03。
* 原始 24 人 Git blob：继承 Phase J 匿名 SHA1 顺序清单，每人 136 条正式实验试次，1,327 次自主选择，所有文件逐个校验。
* 运行环境：Python 3.11，numpy 1.26.4，pandas 2.2.3，scipy 1.14.1。

真实 GitHub Actions [run 38842410238](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38842410238) 已完成，结论 success。synthetic job 116785274333 和 native seven source job 116785274612 两项成功。后一作业真正导入并调用哈希验证后的**未经修改的作者七个 Python 目标函数**，以作者原生 Pandas 输入对 24 人计算。匿名聚合成绩来自该作业输出日志，原作者个体原始试次不重新分发。

## 原生运行聚合成绩

以下每个模型均使用其各自的**无约束参数零向量**及原作者参数转换。零向量只是测试输入，模型参数不同，此成绩**不可用作模型排名或优劣推断**。

| 模型 | 固定零向量的总 NLL |
|---|---:|
| 1 | 2425.247683459 |
| 2 | 4967.384025748 |
| 3 | 4540.105500373 |
| 4 | 2027.753399608 |
| 5 | 2027.753399608 |
| 6 | 1395.152084531 |
| 7 | 1395.152084531 |

Model 4/5 的两个权重在此固定输入处同时为 0.5，Model 6/7 亦如此，因此相应模型对的零向量总 NLL 相同。这不表示最优拟合或泛化成绩相同。

另外以 Phase J 已知 β 值运行原生 Model 3，完成跨实现锚点：

| 比较 | 原生作者代码 NLL/选择 | Phase J 归档值 |
|---|---:|---:|
| 已拟合 β=0.4991210117528604 | 0.6765811147513733 | 0.6765811147513738 |
| 固定 β=5 | 1.352738455600013 | 1.3527384556000137 |

两次原生源数据复算相对 Phase J 归档的误差均远小于事前 1e-8 门限。此结果验证了 Phase J 作者时间轴的 Model 3 固定参数 NLL 可由作者**native Python**程序还原。

## 证据等级与开放关口

Phase K 的 **NATIVE_EXECUTION=PASS**、**MODEL3_PARITY=PASS**。原作者全部七模型目标函数的原生入口已在固定作者真实数据上运行，两个 CI job 均有成功记录。

原作者其余六个模型均尚未进行优化拟合；Model 3 此处也复用旧 β，没有新增训练。作者层级 EM、参数后验、iBIC、两套时钟的同预算七模型拟合、完整 226 人拟合、受试者独立留出预测与外部人群检验全部保持 OPEN。

下一关口应单独固定七模型共同优化预算、初始化和收敛处理、作者规范与候选边界时钟、按参与者划分训练测试集；作者历史层级拟合复现与独立预测应区分报告。

附：[聚合结果与成功 CI 元数据](R065_PHASE_K_NATIVE_RESULTS.json)，[可运行源码](r065_phase_k_native_objectives.py)，[十项离线测试](test_r065_phase_k_native_objectives.py)。

**R065_FULL_SEVEN_MODEL_EQUAL_FIT = OPEN**

**R065_INDEPENDENT_PREDICTION = OPEN**

**PESEN_v0.1 = FROZEN**
