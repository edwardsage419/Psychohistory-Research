# B轨：R265 S61独立协方差计算与持久化收据完整覆盖审计

UTC日期：2026-10-29。目标键：(B,R265,S61,independent-covariance-and-persisted-receipt-gate)。本轮属于同一项目内部非盲态E1审计；研究者已读原R265九函数和历史结论。S61 B算法源码先于本轮R结果提交，先执行再查看R输出，但未实现外部团队独立复现。

## 已读范围和冻结顺序

原R265完整九函数及原结果JSON、S61冻结协议；原R265结果Git blob `c23f899ba78a95651bc843c16871da348644001b`。冻结协议commit `13f61626eba9d33fe0174d43b482b7f8fe4ec5e0`，B源码预先归档commit `5085b47375abc08f0ba296eaa90e58567378ad32`，R源码commit `09650f5903c8e6258ca74daf227e97c1474ae8f4`，持久化收据commit `dd392cd6f81c9d4df1c87bd65f5362dc5500f7fc`。时间顺序符合本次新增结果先冻结B路线的要求。

## 两条独立算法与真实执行

R源码 `research/validation/r265_s61_dependent_input_conditional_projection_20261029.js`：从全部16四位配置按精确概率质量聚合条件均值，再算投影方差。B源码 `research/evidence_audit/b_r265_s61_covariance_oracle_20261029.js`：先用二元变量协方差恒等式求单变量Fi，再用独立三位补集分组概率求Ri。两者没有调用彼此的计算函数，均用BigInt有理数表示，底层算术和九个输出函数定义仍属同一项目内部。

远端归档源码被重新读取并在隔离V8环境直接执行，九世界×两分布18行完整覆盖；每行比对world、design、mean、variance、residual、四个Fi、四个Ri，共234字段，差异0。其中198项是数值字段。R程序重新生成的18行与持久化JSON逐对象相等。原R265独立输入P0的九世界×四输入×两个指标共72项与历史JSON完全一致。P1中有三个世界的一阶Fi总和大于1，同时存在Fi>Ri，符合预先冻结的相关输入反例。

严格收据检查器 `research/evidence_audit/b_r265_s61_strict_receipt_gate_20261029.js` 对远端完整JSON核验唯一世界设计键、18行覆盖、234字段、E1元数据、冻结commit及E2/E3=0，结果PASS。五个负例均被拒绝：复制重复行、把数值改999、把E1改成E2、删除一行、以布尔False替代有理数字符串。

## 失败、修复与剩余验收

最初归档的检查器CLI使用Node require加载B脚本，但B脚本只提供顶层compute函数，没有module.exports；这会造成原生命令行入口失败。随后以Git blob保护方式修改新增检查器，改为Node vm在独立上下文执行B源码；B预先归档源码没有变动。初版检查器commit `8f244a5b7e1456e65ffa4ee0e4563fa710c3c023`，修正commit `3418dc8b58c5ed0bea9d5d487eb60c582e5c407e`。修正后的归档检查器在V8直接调用verify成功，尚未执行真实Node CLI，不能将其记为CLI exit0。

本轮尚未执行原R265 144行CSV的重新全字节复算；72项P0基线来自原R265正式JSON而非原始CSV重读。输入相关性是人为指定的P1设计，不构成真实参数联合分布验证。没有真实留出集、经验校准、cluster bootstrap、外部独立研究团队复现。新增E2=0、E3=0。

验收：`INTERNAL_EXACT_E1_CROSS_ROUTE_PASS`，`PERSISTED_RECEIPT_GATE_V8_PASS`，`NATIVE_NODE_CLI_NOT_RUN`，`EXTERNAL_REPLICATION_NOT_RUN`。R073与PESEN v0.1冻结，原R265正式验收状态不变。未启动GitHub Actions及收费计算。
