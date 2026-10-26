# MKT043 Exist 描述性滚动基准与 Beeminder 承诺轨迹的漂移对照

研究日期：2026-10-26（Asia/Singapore）
轨道：commercial_market
执行状态：COMPLETE_BOUNDED_OFFICIAL_SOURCE_AND_SYNTHETIC_COMPARISON
preflight_main_head: 2e19d0f01c93dd0922be15281287e09b7dd9de51
dedup: MKT001, MKT029, MKT030, MKT031, MKT040, MKT041, MKT042, E011, F002
资料语言：英文公开官方资料；无中文来源
证据：MARKET_E1_OFFICIAL_DOCUMENT + E1_SYNTHETIC_ARITHMETIC；费用与功能营销属于厂商自述，独立用户改善效果 UNKNOWN
费用：无注册、无付费、无试用、无认证 API、无 CI、无云计算；本轮主动新增费用 0；账户整体账单和 GitHub 免费额度未独立核验

## 1. 新增比较及文档边界

Exist 的 Averages 官方资料明确：所谓 average 实际按最近60天中位数计算，每周生成，分别保留 overall 和七个星期分组的历史快照，客户端将其用于当日相对通常行为的进度展示。它是随观察数据变化的描述性参照，不能推定为用户认可的长期目标。官方 API 返回历史平均值并受 read scopes 限制。未访问真实用户或生产服务。

Beeminder 官方 API 的 road、roadall、fullroad 表示分段目标轨迹，delta 表示到红线的数值距离，safebuf 表示剩余安全天数。帮助文档明确，目标更容易、退出或休息通常要提前7天安排，ratchet 可以主动缩减缓冲。手动 ratchet 可用，自动 ratchet 为 Bee Plus/Beemium 订阅功能。新近官方帮助页面明确普通用户的0美元试用承诺通常仅限前7天或首次脱轨，之后可能进入5美元承诺；Beemium 才可将特定目标的承诺上限保持为0美元。故 Beeminder 实际目标操作不符合本项目绝对零新增费用的无风险要求，本轮只审读公开网页。

本轮新增重点是把两种不同的参考机制置于同一组可复算的人工行为轨迹，检验“通常行为恢复到100%”是否与“固定承诺目标完成”相互矛盾。对 Beeminder 的计算只使用理想化分段线性约束示例，不声称复现服务端 safebuf 或费用逻辑。

## 2. 人工数列与独立数学检查

Python 3 标准库 statistics.median，人工预历史60天每天10单位，之后连续31天每天4单位。另设一个完全独立、在低值阶段开始的固定行为承诺目标8单位/天，初始累计缓冲为0。分别计算滚动60天中位数、当日值与中位数的比值、当日值与固定目标的比值，以及新承诺期内累计偏离。实际执行24项断言，24通过，0失败。

| 连续低值天数 | 最近60天中位数 | 当日4/描述性基准 | 当日4/固定目标8 | 新承诺期累计差值 |
| :---: | :---: | :---: | :---: | ---: |
| 1 | 10 | 40.0% | 50.0% | -4 |
| 15 | 10 | 40.0% | 50.0% | -60 |
| 29 | 10 | 40.0% | 50.0% | -116 |
| 30 | 7 | 57.14% | 50.0% | -120 |
| 31 | 4 | 100.0% | 50.0% | -124 |

第30天的60个样本恰为30个10与30个4，标准中位数为7；第31天变为29个10与31个4，中位数跳到4。相同的当日4单位，在描述性参照中从40%升到100%，相对未改变的8单位目标仍只有50%。这构成“描述性基准漂移掩盖固定目标缺口”的严格人工反例。

重要限制：Exist 官方每周更新中位数，表格模拟的是每天重新计算的潜在60天滚动值；实际产品显示跳变可能延迟至下次周更新。没有证明 Exist 会用该比值公式绘制进度条，也没有证明用户会受误导。Beeminder 真实轨迹可能带历史超额、安全缓冲、休息、速率修订与特殊目标类型；表中累计差值只适用于明确设定的独立新承诺期。

## 3. 两种机制的输入、状态、算法、目标、反馈、权限及费用

Exist：输入是用户手工或第三方授权的日级属性；状态为时间窗、属性、overall与星期分组中位数及生成日期；算法已知60天中位数与周更新，缺失处理和异常日算法仍未完全公开；反馈是相对通常行为的图形与趋势；无证据表明自动调整用户规范目标。API读取受权限范围限制，撤权后外部缓存的衍生快照清理未知。公开个人订阅价格属于厂商报价，见MKT042，未购买。

Beeminder：输入为手工或授权集成的数据点；状态包括累计观测、分段红线、偏离距离、剩余安全时间、截止时间及承诺金额；目标轨迹由用户设定并受七天修改约束；反馈包括颜色、提醒、缓冲收紧、脱轨和可能收费。解释性优点是约束轨迹和截止时间可读。无独立长期效用提升或人群公平性验证。认证和隐私边界详见MKT001/MKT029/MKT031。免费加入与“零费用风险”不是同一条件，绝不注册或激活目标。

## 4. 对心理史学未来候选方法的限定启示

候选 C1：并列保存描述性行为参照 b_obs(t)、经用户明确确认且版本化的目标 b_goal(t)、单独可解释的安全边界 b_safe(t)。三者允许不同方向、不同单位及时间窗口，不能预设单一人生效用权重。

候选 C2：任何“达到100%”显示必须标注分母的来源、窗口、样本量、版本和生成时间。参照自动漂移不能默默修改目标，目标修订须保留用户同意、理由、适用起点及前后版本。

候选 C3：当突发疾病、照护责任、就业变化或价值重审使旧承诺不再适用时，应保留人工立即停止自动决策与纠错权；七天锁定和经济惩罚不能作为默认安全控制。

候选 C4：未来可在不使用真实敏感数据的前提下，比较固定目标、滚动中位数和用户批准的目标修订，在独立合成情景中衡量误报、漏报、恢复延迟和解释一致性；之后才考虑真实研究验证。

以上均是知识储备，不修改R系列、R073、PESEN或任何冻结协议，也不提前构建个人决策产品。

## 5. E/F 状态与下一项

E：2026-10-26正式E004已完成。本轮新近R173事后Brier/影响诊断及原始E1关联证据做增量只读核验，另见E012。既有R170全状态复核缺口、R136原冻结负对照和original239证据审计仍开放。

F：2026-W44 F002已完成，本轮不重复立项。新增候选风险为描述性参照漂移伪装目标完成、7天承诺退出与突发脆弱状态冲突、经济惩罚与零费用不兼容。F003候选仍为错误偏好归因、派生记忆证据语义与人工申诉。

下一轮 MKT044：比较 ProjectionLab 的情景假设版本、随机模拟与目标阈值的分离，优先检索官方免费文档与可复算的概率边界案例；先去重MKT002/MKT027/MKT028。

## 6. 公开英文一手来源

1. Exist object types, Averages: https://developer.exist.io/reference/object_types/
2. Exist Averages API: https://developer.exist.io/reference/averages/
3. Beeminder API Reference: https://api.beeminder.com/
4. Beeminder safety buffer: https://help.beeminder.com/article/55-what-is-safety-buffer
5. Beeminder manual and auto ratchet: https://help.beeminder.com/article/56-can-i-get-rid-of-extra-safety-buffer
6. Beeminder change goal: https://help.beeminder.com/article/54-how-do-i-change-my-goal
7. Beeminder akrasia horizon: https://help.beeminder.com/article/45-what-is-the-akrasia-horizon
8. Beeminder pledge free exceptions: https://help.beeminder.com/article/23-can-i-have-goals-without-pledges
9. Beeminder cost: https://help.beeminder.com/article/19-how-much-does-beeminder-cost
10. Project MKT042: research/market/MKT042_EXIST_SIXTY_DAY_MEDIAN_WEEKDAY_BASELINE_OUTLIER_MISSINGNESS_2026-10-26.md
