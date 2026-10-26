# B轨 R201新队列构成变化独立算法审计

日期：2026-10-27。状态：PASS_INTERNAL_ALTERNATE_ANALYTIC_RECOMPUTATION。

## 冻结、输入与算法独立性
R主程序重新枚举四人事件次序、训练风险集、部分似然与候选选择，逐项展开未来事件的Brier损失。B程序 research/evidence_audit/b_r201_cohort_shift_independent_20261027.js 独立读取原R201正式CSV中的120条已冻结训练前缀及其来源概率和选中HR，不调用R新增计算函数。B直接使用解析恒等式 B=1-2Σp_iq_i+Σq_i²，重新构造三种新队列协变量配置的预测分布。

## 实际审计
在120条原训练前缀与三种测试构成组合上完成360条评分记录的1440项字段精确比较，全部一致。27个聚合世界的216项风险及概率字段精确比较，全部一致。27项来源质量归一化检查通过。

负对照一：篡改原CSV中的一项已选HR，B审计实际报错。负对照二：篡改新增R收据中的一项oracle差距，B审计实际报错。两项均检出。

机器收据 research/evidence_audit/B_R201_COHORT_SHIFT_1656_EXACT_AUDIT_RECEIPT_2026-10-27.json 保存字段计数、来源Git blob、负对照结果与边界。原CSV blob 18248e299595818e4d06b394e4d2d42aead6c2bd，R新增收据 blob aa2ec16703fc32f70ed4724a2a823fb02d42055c，B脚本 blob e2bd46a06ac2b006a4c351e432364a250e0ed807。

## 科学证据判定
本轮验证程序性独立算法一致性。R和B均在同一研究主体控制下，属于内部复算。原训练与新队列的独立性只在人工生成机制下成立。新队列没有真人观测，不能报告现实概率校准、置信区间、外部数据复现或一般性样本外有效性。E1人工=PASS_BOUNDED_INTERNAL，E2预测=0，E3预测=0，外部独立复现=0。

原R201验收不变；R073与PESEN v0.1继续冻结。没有主动启动GitHub Actions，CI成功未建立。
