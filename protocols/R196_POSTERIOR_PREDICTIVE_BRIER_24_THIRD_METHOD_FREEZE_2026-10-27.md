# R196 第三方法：固定均值场近似的未来二元预测风险，计算前冻结

日期：2026-10-27。状态：PRESCORE_FROZEN_INTERNAL_E1。该协议仅扩展已正式验收的R196有限人工变分贝叶斯研究，保留其原有模型、先验、六类权重、m=1/2、COARSE/FINE网格、候选评分和选模结果；R073及PESEN v0.1保持冻结。

## 固定来源与输入

1. research/R196/R196_ALL_12_EXACT_POSTERIOR_SOURCES.json，读取12个来源配置的整数weights、精确真后验及forward-KL边际乘积。
2. research/R196/R196_EXACT_RESULTS.json，读取24个已冻结网格最优候选的selected_mean_field_joint_exact，不重新搜索或重新调参。
3. 对每个来源配置，固定同一潜在状态z并已观察m次Y=1。下一次Y_new条件于z独立，成功概率为w_z/M，M=max(weights)。本研究的未来预测仅对这一同组同潜变量的下一次观测成立；不允许把后验迁移到独立新潜在状态。

## 预定评价及比较

对12个来源配置，分别计算完整真后验oracle、原始均匀先验、真实后验两个边际的乘积分布（forward-KL独立族）、COARSE和FINE的原冻结最优均值场q，共12×5=60个预测。
每个预测的下一次成功概率a=Σ_z q_z w_z/M，真条件成功概率t=Σ_z p_z w_z/M。真未来Brier风险R(a)=t(1-a)^2+(1-t)a^2，oracle风险t(1-t)，超额风险严格等于(a-t)^2。
比较每个网格预测对oracle的超额Brier、对先验的超额Brier，以及FINE与COARSE的未来风险差异。记录FINE KL更小却未来Brier更差的反例数量；如不存在则记录0，禁止改变机制以制造差异。
另检查真后验等于均匀分布的负对照，以及强耦合对称来源（POSITIVE_COUPLED和NEGATIVE_COUPLED）是否因相同likelihood层级而在未来预测上产生等价。输出每一项精确有理数。

## 计算方法与独立审计

R主程序直接计算未来Bernoulli混合概率与解析Brier。B程序独立遍历四个潜在状态与两种未来结果，按真实联合分布计算期望平方误差，不复用R主程序函数。逐条件逐方法对比60项概率、60项风险和60项超额风险。固定故意错误负对照：将同潜变量下一次预测错误替换为重新抽取均匀新潜变量，至少一个非均匀来源必须被检出；同时以错误Brier公式省略负例项作为第二负对照。
程序必须在报告前执行。没有真人数据、没有独立历史资料、没有样本外真人校准。模型内条件未来风险的精确枚举不等于真实外部预测复现。

## 交付与边界

仅新增本协议、research/validation内的R程序/JSON/科学报告、research/evidence_audit内的B独立程序/收据/报告；A轨只在有实际新增数据来源核验时另行提交。保持original239索引及154项待核队列不变，绝不覆盖其他轨。写入前重新核对main HEAD与路径。GitHub Actions仅在已独立确认零费用后才可启动，否则记录NOT_RUN。零新增支出。