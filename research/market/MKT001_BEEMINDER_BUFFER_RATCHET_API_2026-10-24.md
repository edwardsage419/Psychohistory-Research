# MKT001 Beeminder 可计算目标边界与安全缓冲机制深读

研究日期：2026-10-24；轨道：commercial_market；状态：COMPLETE_BOUNDED_DOCUMENT_REVIEW。
observed_head_before_write: 7268374e1af3eaf72cec649abda666b776b0685f
研究性质：对 2026-10-24 商业基线中 Beeminder 条目的具体机制补充；不是新产品发布消息，不构成科研 E2/E3 或人生决策效果验证。

## 本轮真实新增知识

1. 目标轨迹的数据结构。官方 API 的 `road` 是分段轨迹，每个节点由时间、目标值、变化速率三个字段中的两个确定第三个。`roadall` 加入首末节点，`fullroad` 填充缺失字段。这说明该产品使用明确的分段约束轨迹，能够逐段改变目标速率，适合未来研究“长期基准线可解释表示”。
2. 偏离余量的计算对象。`delta` 是当前观测值到红线的距离，`safebuf` 是若不再增加数据还能保持安全的整数天数，`safebump` 是多获得一天安全期所需达到的目标量。`colorkey` 根据安全天数提供风险提示。时间缓冲与数值距离属于不同度量，不能混作单一“人生风险分数”。
3. 收紧与安全边界。`autoratchet` 是自动收紧允许累积的最大缓冲天数的配置；帮助文档说明手动收紧可用，自动收紧属于 Bee Plus 或 Beemium 付费订阅功能，且不清除为休息或意外设置的平坦期。项目不订阅、不调用该 API。
4. 目标修改约束。官方 API 文档对 `roadall` 更新规定，不能在未来一周 akrasia horizon 内使目标变得更容易。这是防止临时改变承诺的设计；对身体状态突变、价值改变或环境危机可能不合适，未来系统必须保留人工撤回与安全例外。
5. 运行成本与外部行为。API 需要认证；本轮只读公开文档，未创建账户、令牌、目标或费用承诺。官网 FAQ 描述越线可能触发真实金钱扣费，不能将其直接作为零成本研究项目的执行机制。

## 输入、状态、目标、反馈与边界

输入：用户手工记录或授权的数据点；公开 API 有 Datapoint、Goal、OAuth 等接口。
状态：当前观测值、日期、分段目标轨迹、距离、剩余安全天数、提醒阈值及承诺状态。
目标：由使用者事先选定的量化行为轨迹。官方公开文档未展示跨领域个人幸福或因果效用函数。
反馈：颜色提示、截止日期、偏离触发、调整缓冲与轨迹；不等于基于真实人生结果的自我校准预测模型。
隐私：API 使用个人令牌或 OAuth；仅证明存在认证机制，数据存储安全、撤销效果、第三方处理与跨域权限仍需独立审查。
费用：部分高级缓冲控制为付费功能；惩罚承诺可能产生费用。研究禁止实际触发。
解释性：轨迹、剩余天数和阈值可由文档解释；完整生产算法源码及统计效果尚未独立审计。
科学验证：本轮 MARKET-E1（厂商 API 和帮助文档的机制描述）；没有外部独立产品测试、随机试验或长期决策效益证据。

## 对心理史学的候选启示

候选 A：把长期基准线表示为可审计的分段函数 b(t)，并将“距离基准线”和“剩余安全时间”分开报告。
候选 B：设置可更改的偏离容忍窗口，同时保留紧急撤回、休息期、测量错误修正及权重重审，禁止强制惩罚。
候选 C：未来以合成情景检验：突发疾病、不可控失业、临时照护义务和长期价值改变时，静态红线与动态风险边界何者产生较少错误警报。
以上均为未采纳的设计假设，不提前建立个人产品或改动 R 系列。

## 资料与实际访问范围

1. Beeminder API Reference，官方技术文档，2026-10-24 访问：https://api.beeminder.com/ 。直接核查 Goal 属性 road、roadall、fullroad、delta、safebuf、safebump、autoratchet、OAuth 和更新约束。
2. Beeminder Help，“Can I get rid of extra safety buffer?”，网页标记 2026-08-17 更新，2026-10-24 访问：https://help.beeminder.com/article/56-can-i-get-rid-of-extra-safety-buffer 。
3. Beeminder Help，“What is safety buffer?”，2026-10-24 访问：https://help.beeminder.com/article/55-what-is-safety-buffer 。
4. Beeminder FAQ，2026-10-24 访问：https://www.beeminder.com/faq 。
5. 本项目先前基线：research/market/COMMERCIAL_PRODUCT_RESEARCH_BASELINE_2026-10-24.md 。

## 执行收据

track: market；subflow: product；run_date: 2026-10-24。
work_performed: 官方 API 数据结构、缓冲、修改权限、价格条件和可迁移机制逐项审读。
evidence_scope: MARKET-E1，厂商文档可核；第三方真实效果 NOT_VERIFIED。
billing_checked: 无购买、无注册、无计费 API、无 CI，新增费用 0。
ci_status: NOT_RUN；blockers: 未取得真实账户的独立产品行为测试及长周期决策效果数据。
next_action: 核查 ProjectionLab 随机情景假设、历史收益抽样和对相关性及时间结构的处理，记录可证实的模拟边界。
