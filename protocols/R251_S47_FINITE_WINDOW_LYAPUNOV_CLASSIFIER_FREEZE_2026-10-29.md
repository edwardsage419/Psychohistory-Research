# R251 S47 有限观察窗口稳定性分类审计，事前冻结
日期：2026-10-29。研究路径：R主线。证据级别：E1人工数学。当前main基线：3fd35607eeb48be9efa338214c71956cbb372010。

## 冻结来源与目标
固定读取 research/R251/R251_ALL_405_ORIGINAL_LYAPUNOV_SOURCE_ATOMS.csv，原始blob b8ca35f1e7779f38bcbd60051973819aa3b29061；九种人工离散映射、九初值、五时点，共405条source。R251原始冻结15568be1625414aa72a179c93f315535de704d73及原正式验收保持不变。不得修改来源、模型函数、分类真值、R073评分或PESEN v0.1。

在每世界八个非零初值，共72个确定性轨道上，预先定义两个只依赖t=0..4观察的判别器：
1. STRICT4：t=0,1,2,3四次V(x_{t+1})-V(x_t)都严格小于零。
2. NET4：|x_4|严格小于|x_0|。
每个世界另统计全部45行单步ΔV的正、零、负数量；对每条轨道保存四次ΔV符号和NET4分类。固定局部子集：|x0|<=1/12且x0!=0，每世界4条。所有比较采用精确有理数，不允许浮点容差。仅原始t<=4可用，禁止用未来状态作为早期预测输入。

## 真值与事前负例
原R251解析分类真值固定为：全局或局部渐近吸引的世界 HALF_CONTRACTION、NEGATIVE_HALF_CONTRACTION、ZERO_MAP、CUBIC_LOCAL_INWARD、LOGISTIC_R3_CENTERED；Lyapunov稳定但不渐近吸引 IDENTITY_NEUTRAL、SIGN_FLIP_NEUTRAL；不稳定 DOUBLE_EXPANSION、CUBIC_OUTWARD。此处不把单个轨道是否收缩当作无限时间稳定性的数学证明。

预先指定负例：ZERO_MAP到达固定点后ΔV=0，因此STRICT4应拒绝；LOGISTIC_R3_CENTERED的正初值单步V可增加，虽在|x0|<=1/12范围内两步收缩；IDENTITY_NEUTRAL与SIGN_FLIP_NEUTRAL的NET4不收缩，但系统稳定；LOGISTIC_R3_CENTERED在大初值上可能呈不同有限轨道行为。比较结果只作为有限窗口分类器的审计，不能重写R251解析证书。

## 验收与独立方法
R轨逐行读取原始405条source，校验9×9×5完整键、质量、状态、候选V、下一状态、单步ΔV、导数与初值敏感度；按初值聚合72条轨道，计算冻结的两个分类器。
B轨以独立Python Fraction映射公式直接重算九世界×八非零初值×五时点，不调用R轨分组逻辑，比较逐世界汇总及关键反例；增加单字段篡改拒绝测试。两轨均须明确其为内部程序性复核，外部独立复现=0。
新增数据A轨仅开展公开来源门槛审计，优先服务R主线。E1、E2、E3隔离。无新增费用，未经费用核验不触发GitHub Actions。