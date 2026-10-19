# R112：贝叶斯信念更新的有限假说与Beta–Bernoulli共轭学习

日期：2026-10-19。按项目所有者2026-10-18既定顺序，先完成R系列模型学习，再统一分类，最后熔炼。R112对应既定239候选目录中P0条目02-006 Bayesian Belief Updating。**当前学习范围内 LEARNING_COMPLETE_BOUNDED；真实人类行为独立E2=0；PESEN v0.1与R073保持冻结**。此标记严格限离散数学机制和共轭人工样例，不等于人类认知实际遵循此规则，也不等于整个贝叶斯认知模型家族完成实证验证。

## 文献证据
1. Bayes / Price (1763) *An Essay towards solving a Problem in the Doctrine of Chances*, DOI [10.1098/rstl.1763.0053](https://doi.org/10.1098/rstl.1763.0053)，原发表于皇家学会Philosophical Transactions卷53页370至418。它是本机制的历史出处；本研究的有限假说及Beta参数表达为现代形式化。
2. Griffiths, Kemp & Tenenbaum (2008) *Bayesian Models of Cognition*, [作者原始论文手稿](https://charleskemp.com/papers/bayeschapter.pdf)，原稿第5至6页式(1)至(5)明确给出后验及假说归一化形式，并解释认知模型的规范性计算分析；[出版社DOI](https://doi.org/10.1017/CBO9780511816772.006)。

## 本轮计算模型
离散假说后验按合法历史条件似然更新，零支持/零归一化事件严格拒绝；使用对数权重避免极小似然直接乘法下溢。二元先验odds与Bayes因子可以在界限允许时分析。Beta(a,b)与固定θ的Bernoulli独立观测结合形成Beta(a+s,b+f)后验，后验预测成功率a'/(a'+b')，指定有序样本的边际似然为Beta函数比值。

**关键反例**：若第二条消息是第一条的确定性复制，正确第二条条件似然在两个假说下均为1，第一次更新后90%的后验保持90%；错误当作新独立证据，会将其提高至约98.78%。这属于构造数学反例，未使用实际社交网络或真人信息传播数据。

## 真正执行结果

GitHub Actions [run 39233410573](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39233410573)已成功，要求明确打印Ran 25 tests与OK。共25项真正运行、0失败，覆盖归一化、零先验、极小概率、后验odds、顺序独立更新、完全重复证据错误、Beta逐次及批量更新、边际概率、非法输入和数值边界。该结果和三个原文件真实SHA256已由[CI机器收据](R112_PHASE_A_SYNTHETIC_BAYES_CI_ACCEPTANCE_STATUS.json)机器人提交，文件存在且已重新读取确认。

相关材料：
* [原始来源、公式、假设和失败模式正式研究报告](R112_BAYESIAN_BELIEF_UPDATING_SOURCE_MECHANISM_AUDIT_2026-10-19.md)
* [可运行原生Python数学实现](r112_bayesian_belief_updating.py)
* [25项合成单元测试](test_r112_bayesian_belief_updating.py)
* [正式机器验收](R112_FINAL_ACCEPTANCE_STATUS.json)
* [真实CI原文件摘要与测试结果](R112_PHASE_A_SYNTHETIC_BAYES_CI_ACCEPTANCE_STATUS.json)

复算：Python 3.11 标准库，执行
`PYTHONPATH=research/R112 python -m unittest -v research/R112/test_r112_bayesian_belief_updating.py`。
模型属于规范性推断与简单生成模型的数学学习，没有经真人逐人数据评估，既未确证先验的心理来源，也未证明因果、社会模仿或历史级预测有效性。接下来继续尚未独立有界结题的既定P0模型学习，不启动归类或PESEN模型熔炼。
