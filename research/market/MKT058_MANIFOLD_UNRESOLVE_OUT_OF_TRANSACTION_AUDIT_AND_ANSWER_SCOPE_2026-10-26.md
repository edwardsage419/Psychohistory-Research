# MKT058 Manifold结算撤回的审计事务边界与答案身份隔离

日期：2026-10-26（Asia/Singapore）。研究轨：market。状态：COMPLETE_BOUNDED_FIXED_SOURCE_SYNTHETIC_E1。开始及写入前main HEAD：febd07d2e1e49bb9be020a9c089c3631c5256229。前序MKT056、MKT057研究Metaculus结算与榜单；本轮换用Manifold的独立多选结算撤回和审计事件路径，避免重复。只读公开英文资料、固定源码和合成状态机。主动新增费用0。

## 1. 固定来源与证据界限

英文官方API文档 https://docs.manifold.markets/api ，读取2026-10-26，注明GET /v0/market/[marketId]返回当前市场和答案，/bets与/comments分开读取；内部POST /unresolve要求认证，非稳定公开API；独立多选答案用answerId逐项结算。官方FAQ https://docs.manifold.markets/faq 确认免费参与、初始虚拟mana、可购买额外mana、争议可能重新结算。官方API条款提醒商业AI训练数据需另行许可，不能据此假定历史数据可无限制训练。

固定作者仓库 https://github.com/manifoldmarkets/manifold ，main commit fc99df0f05b564d98276ea7159f0c5f71090a904。直接读取并固定Git blob：
1. backend/api/src/unresolve.ts，92cde60a419b879a206769cfcb2535d0748b2d89；
2. backend/api/src/unresolve.test.ts，1b90681bf08fada1dce6e97c61af6e3c425a1194；
3. backend/api/src/resolve-market.ts，69ad119313374f8fe1040f3633653050717632ba；
4. backend/shared/src/record-contract-edit.ts，5c48f39bd17fd53df69e0f477a246f76e5161d21；
5. backend/api/src/get-market.ts，0bc1a469cda8bd8c6d94409561eadc243526ddcc；
6. common/src/contract.ts，ba004b0cc6c6973e416120f1fde226a51ef307ee。

以上为FIXED_SOURCE_E1。没有连接生产数据库、执行服务端代码、认证API、交易或获取真实用户资料。官方规则是OFFICIAL_DOCUMENTATION，源码行为是SOURCE_INSPECTION，下面测试是SYNTHETIC_BRANCH_MODEL，真实线上失败发生率、第三方复现和长期决策收益均为NOT_VERIFIED。

## 2. 本轮新增机制

**MKT058-F1，审计记录与业务事务可能分离。** unresolveMain使用createSupabaseDirectClient().tx执行撤回；undoResolution内部先更新合同、再调用recordContractEdit。recordContractEdit另行调用createSupabaseDirectClient()建立连接并向contract_edits插入包含旧合同状态及updated_keys的记录，没有显式接收当前事务句柄。unresolve.ts的源码注释明确提及：此前撤回尝试在记录自身edit后失败，因recordContractEdit在事务外写入，留下后续edit；恢复subsidyPool时必须跳过这些记录。由此可确认存在非原子审计写入路径和源码作者识别的历史异常场景。不能仅凭源码判断当下所有部署都可复现、失败概率、最终资金余额或完整审计事件链。

**MKT058-F2，撤回范围依题型变化。** 二元和linked多选采用整题撤回，传入answerId被拒；independent多选必须传answerId，读取答案时按(id, contract_id)双字段约束并FOR UPDATE行锁，后续UPDATE也绑定合同。已归档的unresolve.test.ts包含跨合同答案拒绝、同合同答案成功、未知答案拒绝三类单元测试。代码存在具体隔离保护，不应将其误写为跨合同答案越权已成立。

**MKT058-F3，结算撤回涉及补偿账务和权限。** 代码按合同及可选答案身份查找结算支付事务，插入逆向补偿事务，恢复指标和答案概率。创作者一般仅在最近10分钟内自行撤回，管理员/版主有不同权限；已删除市场和PERP等路径另有禁止条件。部分历史结算事务受兼容性时间门槛限制。独立答案撤回不等于整题撤回，也不等于个人数据删除。

**MKT058-F4，当前API与历史事件可见性不同。** get-market.ts从当前contracts和answers行构造FullMarket；内部存在contract_edits和audit_events等记录。官方公开GET文档未承诺向普通用户提供可核验的完整结算、撤回、逆向支付和审计事务链。不能把当前状态快照当作可独立重建全部历史的证据；也不能由公开GET字段缺失推断内部历史已丢失。

## 3. 15项人工分支与事务示意检查

使用Python标准库自写极简状态机，对源码中显式的分支约束构造13个正反例：binary整题允许、binary传answerId拒绝、linked整题允许、linked传answerId拒绝、independent同合同已结算答案允许、independent缺answerId拒绝、跨合同答案拒绝、未结算答案拒绝、创作者超10分钟拒绝、版主超时仍可、非创作者且非版主拒绝、已删除市场拒绝、PERP拒绝。再构造2个纯示意事务情景：审计外部提交而业务事务回滚会留下审计记录；假设同事务写入则一起回滚。共15项断言通过，0失败。

这些是手工抽象逻辑检查，没有运行作者TypeScript、SQL事务或其Jest测试；示意事务的结果属于数据库一般语义下的条件性推导。未验证记录写入和后续失败在真实运行中的时序、事务隔离或故障频率。

## 4. 对心理史学未来方法的候选启示

真实数据输入类别为市场问题、题型、答案ID、结算结果、结算时间、身份与权限、支付交易、审计变更；状态表达包含整题和逐答案resolution、resolutionTime、isResolved、交易及旧快照；算法侧涉及按题型分支、时间权限门槛、事务补偿和指标恢复。反馈是市场概率、用户余额、指标和当前市场状态。可解释性可由固定源码分支核对，跨时间的正式历史重建仍缺公开完整证据。隐私上，交易和审计可能包含用户身份与行为记录，访问和删除生命周期须另审。费用模式为免费虚拟币参与并可自选付费，研究未注册或购买。

候选控制：
1. MKT058-C1：未来版本化预测账本中的业务状态变更、审计事件和补偿动作应具备同一事务身份或可证明的可靠outbox关联；失败事件单列，不冒充已提交状态。
2. MKT058-C2：每条答案事件绑定parent_id、answer_id、actor_role、version_id、transaction_id和commit_status，确保同名选项不会替代稳定身份。
3. MKT058-C3：撤回结算、纠正评分、回滚资金、删除隐私数据和撤销授权分别保留不同事件类型和核验口径。
4. MKT058-C4：将历史可回放性拆为当前状态、原始事件、补偿事件、正式评分版本和公开导出权限，分别登记UNKNOWN或VERIFIED。
5. MKT058-C5：F轨后续研究审计日志最小化、纠错申诉、补偿证据和隐私删除的张力，避免在不可删日志中重复保存敏感原文。

以上仅为候选知识储备。R系列完成前不实施个人决策产品，不改变R073/PESEN等冻结协议，不设置单一人生效用权重。

## 5. 子轨与下一步

E轨本日已有E004全轨实质检查；本轮另对R191新第三方法完成1494项独立BigInt有理数核对，单独归档E027。F轨本周F002已完成授权撤销与派生数据生命周期专题，不重复创建F003。

下一轮MKT059优先检查Manifold的contract_edits审计事件是否具备公开历史导出、实际事务边界的集成测试，以及更正事件的版本身份；若没有新增可验证信息，则转向其他免费开源情景版本管理系统。不得使用交易API或计费服务。
