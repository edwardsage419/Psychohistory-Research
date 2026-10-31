# B轨 R313 S109 非盲态独立事件树审计

日期：2026-10-31 UTC。目标键：(B,R313,S109_freeze_9e917e7c,independent_event_tree_full_probability_and_mutation_gate)。

已读范围：R313原冻结协议、原R313源码、64个原一步归档、R312 S108前轮交接、S109事前冻结文本及R生成结果。审计为同一研究项目内部非盲态复核；外部独立团队复现 NOT_RUN。

## 原始材料与复核算法

冻结提交 `9e917e7c0ae95604829199efcdd82e89262988e3`。原一步来源blob `b05bd67ee362bfcbb77726ab9262c807c93236cd`。新全结果文件 `research/validation/R313_S109_FULL_256_WORLD_STEP_DISTRIBUTIONS.json`，Git blob `a7850bee0fe1cae3f77f85dd75d42aa99a64f546`，本地SHA256 `5c9cf4a7fff0eef9efc6aef4f37f6e43f12fac64edd2497ba74d920d8e342c7d`。

独立脚本 `research/evidence_audit/b_r313_s109_event_tree_audit.py`。B直接按三种主动节点和各自邻居枚举有向接触，再按有无复制形成分支；每一层按分支概率累计，不导入R程序，也不使用R的矩阵核函数。Python Fraction精确比较全部64个初态、四个时点的256行、16384个含零概率的完整状态单元、840个非零单元、吸收概率、活跃边期望、支持集及汇总。全部一致。

本地执行：Python 3.13.5，普通模式 PASS，`python -O` PASS，两份stdout完全相同。9项有效非空变异全部拒绝：删行、重复世界时点、概率值篡改、终态身份篡改、吸收概率篡改、活跃边期望篡改、支持集摘要篡改、来源blob篡改、固定world1见证篡改。

## 真实失败与限制

R生成程序第一次执行出现时间优先数组的索引错误，触发错误的单调性断言失败。修复后按时间主序 `64*t+w` 重新核验。保留失败信息，不能把首次运行写为通过。

当前B验证器没有引入外部独立团队，测试对模型公式和输出均非盲态。64个世界均为预先指定的合成状态，不能据此计算真人预测置信区间或宣称经验校准。R073冻结模型和评分规则、PESEN v0.1未修改；新增真人E2=0、历史E3=0。原R313正式E1验收状态保持原样，新S109状态PARTIAL。

GitHub Actions未启动，CI NOT_RUN。未使用计费API、收费runner、租赁GPU或购买数据；实际账单及剩余额度未独立核验。下一步在不产生费用的条件下补充仓库原生运行重放，保持原数据与审计程序不可变。
