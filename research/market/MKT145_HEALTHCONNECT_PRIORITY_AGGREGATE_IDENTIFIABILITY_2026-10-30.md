# MKT145 Health Connect多来源聚合优先级与历史可识别性

日期UTC：2026-10-30。目标键：(market,HealthConnect,MKT145-v1,activity-priority-and-asof-aggregate-identifiability)。本轮起始main：6a149b5db01f91d9702c5fefefcb9cdb348825a4。状态：COMPLETE_BOUNDED_ARTIFICIAL_E1_AND_OFFICIAL_DOC。已读MKT144及MKT143，研究问题改为用户可变的Activity优先级和聚合语义，避免重复SPN身份迁移。

## 官方英文资料与机制

Android Developers, Read aggregated data, https://developer.android.com/health-and-fitness/health-connect/aggregate-data ，页面最后更新2026-10-22 UTC，本轮2026-10-30读取。官方API允许按时间区间和数据类型进行aggregate，按dataOriginFilter筛选单个来源，并可按时长或日历周期分桶。用户自行设置Activity和Sleep来源的优先顺序；Aggregate API对这两类重复数据按用户优先级去重。其他类型的聚合数据来自所有写入该类型数据的应用，不能默认沿用Activity/Sleep去重语义。官方文档还说明默认读取历史范围与首次授权前30天有关，扩大范围需要额外历史读取权限；卸载再安装后权限重新授予。

真实数据输入：应用写入的时间戳、区间、数据类型、DataOrigin、数值、用户授权和优先顺序。状态表达：时间范围、来源优先级、来源身份、权限、数据类型、查询时点。算法：平台官方聚合与来源筛选；本轮人工程序只实现极简逐分钟优先级选择规则，绝非Health Connect平台实现。目标：避免同一重叠活动被重复计算、保留跨时点可解释性。反馈与修订：用户改变优先顺序或来源记录后，同一时间段聚合可变化，应记录as-of查询时点及规则版本。解释性：展示所用来源、优先顺序、时间窗口、完整性状态。隐私：健康数据读取需要用户授权，不能在不同应用之间擅自关联设备标识。费用：只读免费公开文档与本地V8测试；未注册收费服务、购买产品或调用计费API。官方材料未提供长期个人决策改善的独立预测证据。

## 人工可执行实验

程序：research/market/mkt145_priority_aggregate_identifiability_20261030.js，远端Git blob 49a0cd2deb354371f4cb4767e123f57d4ba63bd7。函数通过V8实际执行16项检查，其中11项正向和5项异常输入拒绝。所有数据虚构，不读取真实健康数据。

设20分钟，两来源A、B在前10分钟各每分钟100和80步；后10分钟只有A每分钟50步。人工规则假设两来源重叠区间只保留优先来源，非重叠区间保留现有来源。

| 人工计算 | 步数 |
| --- | ---: |
| 直接相加全部来源 | 2300 |
| 假设A优先 | 1500 |
| 假设B优先 | 1300 |
| 优先级未知但限定A/B两种规则 | 1300至1500 |
| A与B优先结果差 | 200 |

该1300至1500界依赖已知的人工重叠结构、仅有A/B两种优先规则、来源值完整可信；它不是平台返回值的保证，也不是统计置信区间。若跨来源记录并非同一活动，或历史权限不完整，不能把这个界当作真实步数界。平台真实重叠拆分、分桶、权限和设备行为均未执行。

## 研究用途与证据

MARKET-DOC：2026-10-22更新的Android官方聚合说明。ARTIFICIAL-E1：16项本轮V8测试。INFERENCE：同一历史日期的聚合值可能因用户优先级变化而改变，未来研究需保留来源与规则的历史快照。MARKET-INDEPENDENT-TEST=0；真实Android设备=NOT_RUN；真人E2样本外预测=0；历史E3=0。营销承诺未被当作科研证据。

与MKT144区别：MKT144研究SPN来源标识迁移及人工跨导出镜像重复；本轮确认平台本身存在针对Activity/Sleep的优先级去重机制，并量化一个规则变更的人工敏感性。零新增费用，未触发GitHub Actions；账单及免费额度NOT_VERIFIED。

下一MKT146：核查官方是否提供可复原的历史优先级版本和聚合来源贡献，构造缺失历史规则时的审计弃权条件，避免把当前优先级误套到过去。
