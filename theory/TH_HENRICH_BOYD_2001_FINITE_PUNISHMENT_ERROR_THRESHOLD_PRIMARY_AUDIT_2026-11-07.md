# Henrich与Boyd 2001：有限惩罚链稳定条件的原著核对

track: theory
run_date: 2026-11-07 (Asia/Singapore)
target_key: (theory,Henrich-Boyd-2001,10.1006/jtbi.2000.2202,finite-punishment-stability-error-threshold)
observed_head: b02fc80f6394511e65902281bf1f4a09646f95e2
status: PRIMARY_SPECIFIED_PAGES_READ; NO_MODEL_REPLICATION

## 来源与实际阅读
Joseph Henrich and Robert Boyd (2001), “Why People Punish Defectors: Weak Conformist Transmission can Stabilize Costly Enforcement of Norms in Cooperative Dilemmas,” Journal of Theoretical Biology 208(1):79–89, DOI https://doi.org/10.1006/jtbi.2000.2202 。作者公开的原刊PDF：https://henrich.fas.harvard.edu/sites/g/files/omnuum5811/files/henrich/files/henrich_boyd_2001.pdf 。实际核读印刷页84–86的惩罚阶数、公式(7)–(15)、局部稳定条件，以及86–88页群体选择和基因入侵条件的论述；附录完整Jacobian与全部参考文献未逐项核验。PDF文本提取有字符替换问题，符号精度仍需以原始排印图像复核。

## 关键原著限制及更正
原作者给出末阶惩罚所需从众倾向的阈值随惩罚阶数下降的结论，其显式前提包括行为错误率 e < 1/N，其中N是群体人数。原著公式(10)、(12)及Stability Condition 1依赖此约束；若Ne≥1，不能从文中直接推出“任意小正从众强度必存在某有限惩罚阶数使合作稳定”。在第一种稳定条件下，合作成本C亦需满足相应惩罚约束；第二种稳定条件另有对从众强度的下界。不能只引用摘要的“arbitrarily small”而省略这些条件。

原文在解释第二阶时明确写出惩罚收益差比前阶缩小，而从众传播强度在阶数之间保持不变（印刷页84–85，式(8)–(10)附近）。这属于模型指定的传递规则；原文没有在此引入“高阶惩罚观察概率随阶数降低而使从众参数同步下降”的机制。因此，前轮提出 s_k=4^{-k}、d_k=2^{-k} 的构造性反例检验的是扩展模型的可能失效，不能宣称反驳原作者在固定从众规则下的定理。

原著还明确指出，非合作且不惩罚也是均衡；局部稳定性并不决定社会最终落在哪个均衡。迁移可能破坏群体差异。作者基因入侵分析以文化演化更快、收益与遗传适应度成比例、突变改变错误率为条件；并给出文化合作稳定但反社会变体可能入侵的参数区域（印刷页87–88，式(16)–(18)）。这些均是理论模型结论，未构成历史或真人行为预测验证。

## 竞争解释与识别限制
高阶惩罚的行为发生率、观察机会、社会学习强度与惩罚成本可能共同变化。仅观察到合作率和惩罚率，无法区分固定从众强度、依赖可观察机会的学习机制、制度执行或声誉效应。可证伪的扩展模型比较需要先指定每阶实际可观察行为数量及学习规则，再比较阈值与均衡稳定域；尚未执行。

与现有Henrich 2004及Possajennikov评论记录的关系：本条核实2001原始数学模型的前提与公式位置，不新增同题TH编号，不追认此前构造性反例为原模型反证。

## 执行边界
C当日既有C013完成于2026-11-07；D本周既有D003完成于2026-11-02。未使用个人资料。数学程序测试NOT_RUN；完整Jacobian复算NOT_RUN；真人与历史实证NOT_RUN；CI NOT_RUN。未调用新增收费服务；账单及免费额度NOT_VERIFIED。R073、PESEN v0.1冻结与既有证据分级不变。下一步复核PDF原始排印公式与附录，随后轮换历史制度或文化人类学其他原著。
