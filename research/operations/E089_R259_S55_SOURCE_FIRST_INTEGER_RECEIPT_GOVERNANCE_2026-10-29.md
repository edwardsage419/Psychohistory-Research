# E089 R259 S55 来源优先整数格收据审计与跨轨治理

日期：2026-10-29 UTC。track=operations，subflow=E，target_key=(operations,R259,original-e40857bc+S55-b11c8185,source-first-integer-receipt-identity)。状态 COMPLETE_BOUNDED_NONBLIND_E1，完整B轨Python远端收据CLI关口继续OPEN。初始main HEAD cb85d70a545518ebc91146cf95cb6e03f193bd86。

## 本轮实读与第三路线

GitHub连接器读取原R259 225行CSV，main Git blob=58ff66fab67a65fb0bd0f53ec141f77735d46a3d；读取R259 S55持久化完整JSON收据，blob=57f687f54c287906c164e572572246d17e93b84e；读取预冻结协议、R轨正式报告、B轨独立审计及R轨短交接。原CSV在S55冻结提交 b11c8185a107decbc4c9a2d5c805215ddf71e99b 的blob与当前main一致。冻结协议blob在冻结提交与当前main均为9affda213c4bcd8c2fdd430555e905807389924f。R新结果产生于冻结提交之后。

新增与R/B算法不同的第三条整数格路线：将原始两个目标的1/4单位精确映射到整数，再将权重0、1/4、1/2、3/4、1作用于整数格，使用分母16的整数分子进行两端点极大遗憾及最坏加权损失比较。没有调用R端点计算程序，也没有调用B Fraction分段交点函数。已阅读R/B结果，明确非盲态。

真实读取并检查：225个唯一(world,action,weight)来源键、9世界各5行动×5权重、成本跨权重恒定、来源加权分数、Pareto与连续支持元数据、所有90行动区间的两端点遗憾、最坏损失、赢家及平手、名义1/2权重赢家、未被连续加权支持的Pareto赢家身份和总次数。总计2312项显式检查，失败0。两个篡改控制：将一个已归档最大遗憾改为999，以及插入重复来源行，均成功拒绝。

数学核验：CONCAVE_THREE_UNSUPPORTED世界的C/D在全区间和中心区间均为最大遗憾最优，且连续加权不支持；LINEAR_COST2_STEEPER中心区间最大遗憾赢家E，最坏加权绝对损失赢家D；九世界总计4次未被连续加权支持的Pareto最大遗憾赢家出现。全部仅为原人工成本表的确定性结果。

归档程序：research/operations/e089_r259_s55_source_integer_receipt_20261029.js，GitHub blob在提交后核验。程序接收原CSV与持久化JSON两个本地路径，可用Node.js标准库运行；本轮在隔离V8执行同一程序函数。独立Node.js命令行使用远端完整文件仍NOT_RUN。原R259既有正式E1验收保持不变；本轮不能替代S55预声明B Python --r-receipt 完整CLI关口、盲态审计、外部团队复现或真人证据。

## 每日治理及跨轨协调

本轮检查最近main提交：R259 S55事前冻结、R/B计算与交接均已存在；理论轨TH124归档；A轨新增R077证据命名空间纠正。A轨已说明R077历史记录中的“E3”表示旧项目内另一独立真人实验来源，当前统一分类E3指历史事件。两套命名不得相加；既有R077真人验证保留原始身份，本轮新E2=0、新历史E3=0。参见 research/data_scout/A_R077_LEGACY_EXTERNAL_HUMAN_E3_VS_CURRENT_HISTORICAL_E3_NAMESPACE_2026-10-29.md 。

开放Codex PR #1至#6均为待审查内容，不能称main已合并。其中#3针对R257严格比较器，R257原B轨盲态FAIL继续保留；#5针对R258 S54持久化收据，#6针对R251/R252完整收据CLI。PR #6自报R251计算字段一致但完整历史JSON不相等，R252完整288条收据字节一致；两者都尚未合并且本轮没有复跑其程序。旧开放项R170收据、R248的486项跨运行时比较、R251/R252和R258 S54的正式归档CLI验收继续按各自已读范围记录，后续以PR实际合并和重跑证据更新。

本轮没有修改其他轨冻结协议、原始来源、研究结果或共享索引。当前检查范围未见协议漂移、同名覆盖或新增证据等级升级。全仓历史逐项审计NOT_RUN。GitHub Actions未主动触发，账户免费额度及账单未核验。只使用免费连接器和现有隔离执行环境，主动新增费用0。

下一项E090：对R260或当时最新R研究进行来源与冻结顺序核查；若PR #6合并则独立检查R251/R252收据CLI剩余差异，若未合并则选互补审计。
