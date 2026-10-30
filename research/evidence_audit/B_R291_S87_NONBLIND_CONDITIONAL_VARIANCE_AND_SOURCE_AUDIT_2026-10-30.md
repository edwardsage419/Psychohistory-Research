# B轨独立方法审计：R291 S87意向代理测量误差

2026-10-30 UTC。目标键：(B,R291,S87-freeze-4f51f811,conditional-variance-768-source-and-24-risk-audit)。已阅读R291原协议、原研究报告、S87冻结文本和S87持久化全来源/结果，因此属于**同一项目内部非盲态复核**，外部独立复现=NOT_RUN。

## 预定检查与数学独立性
R路线逐(A,N,I,B,J)来源计算预测q并求和Brier损失。B路线只对(A,N,J)三维可见条件分组，以
P(I|A,N), P(J|I), P(B=1|I,A,N)
先计算可见组的总质量m与成功质量s，继而直接使用条件Bernoulli方差
R = Σ_group [s - s²/m]（仅对m>0组）。
四种观测信息FULL_ANJ、AJ、AN、A各自分组。此路线无需枚举B来计算风险，也未导入R实现；两者共享预先冻结的人工DGP常量，故不能称为盲态独立实验。

## 实际远端收据检查
通过GitHub连接器读取完整的持久化
* research/validation/R291_S87_ALL_768_PROXY_SOURCE_CELLS.csv
* research/validation/R291_S87_EXACT_RESULTS.json

B检查器逐行验证8个世界×3误分类率×32来源，共768唯一标签；逐项重算概率、四类预测、四类Brier风险与三种风险差，包含128条零质量来源。24组结果全部精确Fraction一致，无浮点容差。独立本地Python Fraction按条件方差计算24个主要风险差，亦与持久化结果一致。

五个实际执行的负控制全部被拒绝：
1. 重复来源行，拒绝为csv coverage；
2. 删除来源行，拒绝为csv coverage；
3. 修改来源概率，拒绝为source mass mismatch；
4. 修改一个预测字段，拒绝为forecast mismatch；
5. 修改一项结果风险差，拒绝为regret mismatch。

B检查器程序：[b_r291_s87_independent_conditional_variance_20261030.js](b_r291_s87_independent_conditional_variance_20261030.js)。代码生成及测试在V8执行环境完成，归档原生Node CLI尚未执行。

## 科学边界与遗留验证
本轮原DGP完全已知，比较的是总体oracle的精确风险；没有有限真人样本、样本外拟合、时间泄漏风险的现实测量验证或概率校准估计。合成世界中B依赖真实I而非仅观测J，因此误分类导致的规范残余预测价值不能解释为真实规范直接因果效应。R073及PESEN v0.1均未更改。

证据等级E1，A01/A02/A04/A05内部限定检查PASS，A03原生Node和外部环境OPEN，A06 CI与外部复现OPEN。原R291正式有界验收不变，S87科学验收PARTIAL。GitHub Actions因未确认免费额度而未触发，CI=NOT_RUN。无新增收费操作，实际账户账单未核验。
