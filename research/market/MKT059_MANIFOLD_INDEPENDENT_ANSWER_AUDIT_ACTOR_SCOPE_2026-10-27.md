# MKT059 Manifold独立多选答案的结算审计身份与授权范围

日期：2026-10-27（Asia/Singapore）。轨道：market。状态：COMPLETE_BOUNDED_FIXED_SOURCE_SYNTHETIC_E1。上次研究：MKT058事务外审计写入。本次专注独立答案结算的审计身份范围，避免重复。研究前main HEAD：3c4f3156bcc3eafa262f4fd8984d6bd0ca80b30a。主动新增费用：0。

## 1. 原始英文资料与固定版本

官方API说明 https://docs.manifold.markets/api （2026-10-27读取）确认独立多选题 shouldAnswersSumToOne=false 按answerId逐答案结算，内部POST /unresolve需要认证且接口不稳定；公开GET市场仅提供当前市场与答案，交易和评论需另外读取。官方FAQ https://docs.manifold.markets/faq 说明创建者通常结算，版主在特殊情况下可纠正结算。API文档标明公开GET无认证，部分写入收取mana，商业AI训练数据有许可限制。本轮没有调用任何写入API、交易、注册或购买。

固定公开源码仓库 https://github.com/manifoldmarkets/manifold/tree/fc99df0f05b564d98276ea7159f0c5f71090a904 ，提交 fc99df0f05b564d98276ea7159f0c5f71090a904。直接读取Git blob：
1. backend/api/src/unresolve.ts：92cde60a419b879a206769cfcb2535d0748b2d89。
2. backend/shared/src/resolve-market-helpers.ts：a52f248084086a28783fbc53a5581ec151159dfc。
3. backend/shared/src/analytics.ts：7e060c7beaa7892c9465bc30a28c9b132500a495。
4. backend/shared/src/audit-events.ts：fb8863f85e3f71dbc2c7ec28d04de0688bc7d4eb。
5. backend/shared/src/helpers/try-or-log-error.ts：244bdfddd3709a5cceece789d7feeacabb8b63db。
6. backend/api/src/unresolve.test.ts：1b90681bf08fada1dce6e97c61af6e3c425a1194。

证据类别：OFFICIAL_DOCUMENTATION支持接口语义；FIXED_SOURCE_INSPECTION支持代码控制流；SYNTHETIC_PREDICATE支持人工断言。真实数据库事务、线上授权结果、用户损失、漏洞利用及第三方独立验证均为NOT_VERIFIED。

## 2. 新增机制及有界风险

**MKT059-F1：审计事件的答案身份未与授权检查同粒度绑定。** unresolve.ts对独立答案先使用 answers.id+contract_id读取该答案的resolution_time并锁行，属于答案级正确身份隔离；但创作者撤回时判断“上一次是否由版主结算”，SQL从audit_events按contract_id、name='resolve market'查询最新一条，未按answerId筛选。resolve-market-helpers.ts在独立答案结算后调用trackPublicEvent(resolver.id,'resolve market',{resolution,contractId})，未把answerId传入事件数据。analytics.ts和audit-events.ts将事件按contract_id、user_id及data写入。故该检查目前按整题最新结算者，而实际结算与撤回按独立答案。

**MKT059-F2：该粒度不一致在人工事件序列中产生双向资格偏差。** 在同一独立多选题中，不同答案可能由不同角色结算；最新整题事件若属于版主，创作者撤回另一答案的操作也会被该检查拒绝；反之，最新整题事件若属于创作者，该检查不会单凭目标答案先前由版主结算而拒绝。以上均是固定源码分支的条件性推断，真实部署还受时间、余额、其他权限、队列及状态限制，不能视为已证实的线上越权事件。该现象与MKT058已确认的跨合同答案ID保护是不同维度，后者仍有效。

**MKT059-F3：审计事件写入属于事务提交之后的尽力而为记录。** resolve-market-helpers.ts在pg.tx返回后调用trackPublicEvent；audit-events.ts独立建立连接，tryOrLogError遇写入错误返回null。若审计事件未记录，unresolve.ts的lastResolution可为空，代码中的“最近版主结算”限制无法从该事件得出。实际故障频率及是否存在其他补偿保护尚未验证。事件缺失不能自动等同于权限突破。

**MKT059-F4：测试覆盖范围有限。** unresolve.test.ts的三个现有测试聚焦跨合同答案拒绝、同合同答案成功和未知答案拒绝，mock了recordContractEdit及数据库事务。它们没有直接覆盖同一市场不同答案由不同角色先后结算、审计事件写入失败或真实PostgreSQL提交边界。不能将这三个测试的通过外推为上述新问题已被生产测试覆盖。

## 3. 独立人工分支检查

使用JavaScript构造与unresolve.ts角色判断等价的纯函数，固定创作者、版主、最新整题audit事件、目标答案、10分钟门槛及是否已结算。10项断言全部符合固定源码分支，0失败。包含：创作者与最近事件同一角色、最近事件为其他角色、目标答案身份变化但整题最新事件不变、版主角色、创作者超时、非创建者无权限、审计事件缺失、同题不同答案结算者不同。没有运行作者TypeScript/Jest、没有调用服务端或数据库，未进行任何真实账号权限测试。

结论限于“源码条件谓词可以跨答案混淆最近结算者”，不能声称线上事故已经发生。风险等级为CANDIDATE_AUTHORIZATION_SCOPE_HIGH_FOR_FUTURE_TEST，证据等级MARKET E1。

## 4. 未来心理史学的候选方法接口

数据输入：题目ID、稳定答案ID、结算事件ID、actor_id及role、事件时间、事务提交状态、评分版本、权限撤销状态。状态表示：每答案的结算版本及整题聚合状态分离。算法：授权谓词绑定与变更操作相同的最小对象身份，审计事件与业务状态采用可核验的提交关系。反馈：结算、撤销、申诉、纠错及历史评分各有独立事件类型。解释性：展示“哪一条事件及哪个对象身份支持此次操作”。隐私：尽量使用不含敏感原文的稳定标识和有限保留策略。费用：仅审阅公开免费材料。可验证性：需要人工合成多角色多答案时序、审计事件丢失和数据库回滚集成测试；本轮尚无此证据。

候选控制MKT059-C1：每个授权决定引用answer_id、actor_id、resolution_event_id和提交版本，不用整题最新actor代替答案级来源。
候选控制MKT059-C2：审计缺失应标记UNKNOWN，禁止当作“未曾由版主操作”的肯定证据。
候选控制MKT059-C3：结算、撤回、人工申诉、纠错和删除个人数据分别建模，不能以一个undo状态代替。
候选控制MKT059-C4：审计写入应具备与业务提交同事务的记录，或可重放的可靠outbox和对账收据；未来需要正反例验证。
候选控制MKT059-C5：审计日志最小化保留对象ID与证明，不重复保存私人偏好、交易说明或敏感文本。

上述均为候选知识储备。R系列主线和冻结协议不变，不开发个人决策产品，不设定唯一人生效用权重。

## 5. 子轨协调及下一轮

E轨本次对R188原始8640行和4320项整组删除进行了新的独立精确检查，拟单独登记E028；F轨2026-W44的F002已经完成，本轮不重复建立F003。新发现与F未来的授权证据、纠错和申诉专题相邻。

下一轮MKT060优先查证Manifold的逐答案事件身份测试与修订记录，或转向开源预测系统的版本化审计链和完整导出。仍只使用公开非中文来源、免费读取和人工数据。
