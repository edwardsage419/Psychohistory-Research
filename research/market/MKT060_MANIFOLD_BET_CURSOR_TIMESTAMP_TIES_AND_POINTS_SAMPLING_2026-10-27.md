# MKT060 Manifold历史交易分页同时间戳遗漏与图表点选择机制

日期：2026-10-27（Asia/Singapore）。轨道：market。状态：COMPLETE_BOUNDED_FIXED_SOURCE_SYNTHETIC_E1。主动新增费用0。前序MKT058与MKT059研究结算撤回审计，本轮独立研究公开历史读取和图表抽样，避免重复。

## 1. 来源、版本与证据边界

官方英文API说明 https://docs.manifold.markets/api （2026-10-27查阅）说明 GET /v0/bets 无需认证，按创建时间倒序，before和after使用交易ID作为游标，beforeTime和afterTime使用时间戳。文档称默认及最大limit为1000。官方同时说明API仍处alpha阶段，公开读取与商业AI训练数据许可须区分；商业训练需要另行授权。只阅读公开资料，未访问收费API、注册或交易。

固定源码 https://github.com/manifoldmarkets/manifold/tree/fc99df0f05b564d98276ea7159f0c5f71090a904 ，本轮直接读取并记录Git blob：
1. backend/api/src/get-bets.ts，858d2067214003e5e26d1fcc8fd6d49b36e2bdd4。
2. backend/shared/src/supabase/bets.ts，ab107278ddbb072166c62be6b25ed31181639bd9。
3. common/src/api/schema.ts，按固定提交读取；包含bets和bet-points公开GET schema。
4. common/src/supabase/bets.ts，包含NON_POINTS_BETS_LIMIT=10000。
5. docs/docs/api.md，按固定提交读取。

证据等级：OFFICIAL_DOCUMENTATION、FIXED_SOURCE_INSPECTION、SYNTHETIC_BRANCH_TEST，汇总MARKET E1。没有执行真实PostgreSQL查询、线上负载测试或验证生产缓存，不能推断已发生具体用户数据遗漏事件。

## 2. 新增真实机制

MKT060-F1：ID游标在实现中退化为单一时间边界。get-bets.ts把before交易ID先查成createdTime，传入getBetsWithFilter的beforeTime；shared/supabase/bets.ts使用contract_bets.created_time < beforeTime，排序只指定created_time，没有第二个bet_id稳定排序键。源码注释承认同一createdTime有多笔交易时分页技术上不正确。若一页最后一条和未返回记录拥有相同创建时间，下一页的严格小于谓词会跳过其余同时间记录。after方向也使用严格大于时间戳，存在对应边界问题。时间戳并列是否常见及真实漏失规模未测。

MKT060-F2：points模式不是完整时间序列。shared/supabase/bets.ts在points=true时选取created_time、prob_before、prob_after、answer_id等列，并按bet_id排序后应用limit。源码注释称以随机交易ID跨历史取样。这个实现选择固定ID字典序靠前的记录，不能保证时间均匀覆盖、最近记录覆盖或保留概率峰值；调用者后续按createdTime排序也无法恢复被limit排除的事件。与完整交易列表的按时间排序是不同语义。

MKT060-F3：图表点的时效需要单独核对。get-bets.ts对符合条件的points查询使用20秒内存缓存，最多500条缓存键。common/src/api/schema.ts为独立bet-points路由声明public,max-age=86400,stale-while-revalidate=3600的HTTP缓存策略。真实边缘缓存是否遵循该策略、请求路径如何使用以及生产部署行为尚未验证。用于严格历史回放时应标注缓存生成时刻。

MKT060-F4：API文档与固定源码的limit口径不一致。英文文档将GET /v0/bets默认和最大值写为1000；固定源码的NON_POINTS_BETS_LIMIT为10000，schema的上界为50000，非points超过10000会被处理器拒绝。该差异意味着不能仅依靠文档推断实际分页大小。尚未请求线上接口核对当前部署。

## 3. 人工可重放反例与测试

用与源码等价的纯JavaScript数组过滤、排序和limit构造六条人工交易。两条交易具有相同创建时间100，ID分别为a1和z9，其他交易时间90、80、70、60。按时间降序及ID升序稳定排列，limit=1第一页返回a1；将其ID解析为时间100后，第二页采用created_time<100返回时间90的y9，z9被遗漏。一次性读取六条时z9存在。真实SQL在并列时间的顺序可能不同，但任何页尾并列边界均有相同漏失条件。

另用四条人工图表点：ID a的时间10，ID b的时间90，ID c的时间20，ID z的时间100。按ID取前两条返回时间10、90；按时间取最近两条应为100、90。图表抽样遗漏最新时间100。此为确定性的构造反例，未测真实ID分布。

本轮12项人工断言全部通过，0失败。覆盖首尾游标、并列时间、严格边界、一次性完整读取、points的ID排序、limit截断、最新记录遗漏和两种查询语义差异。人工测试没有运行作者的TypeScript、PostgreSQL或线上API。

## 4. 面向心理史学的候选方法

输入：预测事件ID、创建时间、可见时间、事务版本、预测前后概率、目标身份、来源和权限。状态：不可变原始事件流、可重建历史快照、图表下采样副本分开。算法：使用(时间,稳定唯一ID)复合游标及确定性次序；分页记录总数与游标范围，对同时间戳建立负对照；评分读取完整有资格的事件，不能从有限points图表恢复正式历史。反馈：记录纠错、重算和样本遗漏警报。解释：展示事件ID、截止规则、数据版本和抽样口径。隐私：公开交易记录不自动等于可自由训练或无限期保留的个人画像，权限和许可证另核。费用：只用公开免费英文资料和人工数组。

候选控制MKT060-C1：每个分页游标绑定唯一排序键，保存采集截止与全量核对收据。
候选控制MKT060-C2：图表采样、正式评分、审计导出采用不同数据契约，禁止把points结果标为完整历史。
候选控制MKT060-C3：缓存生成时间、数据有效时间、读取时间分别保留；过期或未知时展示UNKNOWN。
候选控制MKT060-C4：用同时间戳、并发写入、limit边界、撤回及重结算事件进行未来免费本地集成测试。

以上仅是候选知识储备，不改变冻结协议、R系列顺序或个人效用权重。用户长期决策改善、真实故障率和第三方独立验证均为NOT_VERIFIED。

## 5. 子轨协调和下一轮

2026-10-27 E028已完成日检，E本轮针对新增R193单独执行有界复算并拟登记E029；2026-W44 F002已完成授权撤销及数据生命周期专题，不重复建立F003。市场新风险可供F后续研究数据完整性、历史可见性和纠错证据。

下一轮MKT061优先对比另一开源系统的历史事件复合游标、下采样和完整导出，或进一步检查Manifold真实SQL测试覆盖。坚持零新增费用，不启用Actions和计费服务。
