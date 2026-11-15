# 数据、时间、插件与证据契约

数学核心只依赖 Python 标准库，`python -S` 可以直接运行，无 FastAPI、React、SQLite 或 GitHub 连接。API/CLI 调用同一 Service，前端只显示后端结果，不复制算法。

## 数据记录 1.0.0

必备字段：schema_version、record_id、record_type、subject_ref、time_context、payload、units、uncertainty、provenance、access_policy、dependencies。对象身份不得缺失/重复；缺失值和未知单位不自动猜测；joint-population-state 显式保留联合依赖，不推定独立。

时间独立记录 simulation_time、round、event_time、observed_at、available_at、cutoff、target_time。必须 event_time ≤ observed_at ≤ available_at ≤ cutoff < target_time。群体反馈在下个 tick 才可访问；群体每 2 tick 更新，其余保持。未定义的零延迟反馈循环拒绝；连续积分器是显式未实现扩展边界。

适配器 binary-population-prevalence@1.0.0 仅接收 individual.states@1.0.0 的 binary 状态，验证身份、数量、单位与时间，转为 group.exposure 的 proportion；不接受未声明 payload 字段，不把 UNKNOWN 自动改为某种概率分布。不兼容理论可维持自己的内部状态，以单独版本适配器接入，而非强制共享内部结构。

## 插件与状态

稳定 ID+精确版本索引，源码 SHA-256 和依赖身份、数学假设、尺度、参数、输入输出、证据与权限单独声明。describe/validate_input/simulate/advance_state/inspect/serialize_state/restore_state 是实际方法；不声明未实现的 predict/estimate。

快照是 canonical JSON + SHA-256，不返回共享可变状态，恢复重新解析并验哈希。分支有新身份和共同父哈希，各自保持 RNG 状态、事件和新快照，不能修改共同过去。日志/快照/运行结果标识科学解释边界，情景差异不等于因果估计。

## 不确定性

可表达 POINT、DISCRETE、DISTRIBUTION、PREDICTION_INTERVAL、CONFIDENCE_INTERVAL、CREDIBLE_INTERVAL、POSTERIOR_SAMPLES、PARTIAL_IDENTIFICATION、MODEL_SET、UNKNOWN、UNIDENTIFIABLE。记录条件、目标、单位、方法、联合依赖、统计解释和来源。首版实际执行 DISCRETE Bernoulli 概率与真实世界有效性的 UNKNOWN；同种复制保留类型，跨种转换拒绝。非离散分布、区间等由后续插件另行提供计算，不声称本版已有通用统计推断器。

机制关系类别：统计关联、候选因果、已识别因果、动态反馈、跨尺度、理论冲突、互补、竞争解释。来源/假设/时间/验证/限制必备；SYNTHETIC 无法直接获得已识别因果地位。多理论并存不自动平均，也不自动选获胜理论。

外部 R/Julia/C++ 插件需要独立版本化数据与运行适配器、来源审查及预算；当前不发现后直接执行，不要求重写原作者代码。

## PR #40 审查补充

离散结果与概率必须是 JSON 数组；UNKNOWN/UNIDENTIFIABLE 不允许夹带量化估计。插件状态恢复在校验模型/版本之外，也校验 individual 的非空二元 states 数组和 group 的 [0,1] exposure；快照恢复还校验身份、父哈希、事件及环境结构。未来其他插件需提供自己的状态校验，通用快照不强制统一内部数学结构。
