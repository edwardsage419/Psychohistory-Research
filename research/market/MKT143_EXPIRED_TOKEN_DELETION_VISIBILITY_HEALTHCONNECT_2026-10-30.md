# MKT143 Health Connect过期令牌与删除可见性范围

日期UTC：2026-10-30。目标键：(market,HealthConnect,MKT143-v1,expired-token-snapshot-deletion-scope)。初始main HEAD：22c7651851cd32b5dab1800df8a6094b5e8b8dde。状态：COMPLETE_BOUNDED_ARTIFICIAL_E1_AND_MARKET_DOC。个人决策产品实施暂缓。

## 英文官方来源及实读范围

1. Android Developers, Synchronize data, https://developer.android.com/health-and-fitness/health-connect/sync-data ，2026-10-30读取。官方指南适用于Health Connect 1.1.0-alpha12及以上。记录ID、版本更新、分页差量、删除通知仅含ID、30天未使用令牌过期、按时间重读去重及恢复策略已检查。官方说明较短重读窗口会有数据差异风险。
2. Android Developers, Read raw data, https://developer.android.com/health-and-fitness/health-connect/read-data ，2026-10-30读取。检查分页、权限及2026年6月步数来源归属变更。后台读取需要额外授权；设备步数来源标签由通用android转为设备与应用范围内合成包名，历史记录仍保留旧标签。
3. 令牌过期后重新读取当前快照无法还原所有历史删除事件及其准确时间，属于接口信息结构推论(INFERENCE)，不是实际设备验证或官方漏洞确认。

## 原生Node人工实验

归档脚本research/market/mkt143_expired_token_snapshot_scope_20261030.js，Node.js v22.16.0运行23项断言及异常输入拒绝，exit=0。全部为虚构记录。初始本地a(-45天)、b(-40天)、c(-3天)、e(-2天)；远端c更新、新增d，b/e已不在快照中。

| 假设 | b状态 | e状态 | 可确认快照缺失数 | 未知数 |
| --- | --- | --- | ---: | ---: |
| 最近30天且范围内完整 | OUTSIDE_SCOPE_UNKNOWN | ABSENT_IN_AUTHORIZED_SNAPSHOT | 1 | 2 |
| 覆盖60天且范围内完整 | ABSENT_IN_AUTHORIZED_SNAPSHOT | ABSENT_IN_AUTHORIZED_SNAPSHOT | 2 | 0 |
| 覆盖60天但权限、分页、来源或一致性缺一 | SNAPSHOT_INCOMPLETE_UNKNOWN | SNAPSHOT_INCOMPLETE_UNKNOWN | 0 | 至少2 |

“完整快照”是调用者提供的人工布尔前提，脚本无法独立验证平台权限、跨页原子性或来源身份。ABSENT_IN_AUTHORIZED_SNAPSHOT仅表示指定范围快照缺失，不能证明历史删除原因、时间、上游从未漏报、备份已擦除。负控制包含重复ID、非法版本、越界记录、错误范围及未授权快照；较旧远端版本单独列为VERSION_CONFLICT。

## 产品登记

类型：Android健康数据互通平台。输入：授权类型与健康健身记录。状态：clientRecordId、clientRecordVersion、Health Connect id、来源、变更token、分页、权限。算法：upsert、差量、删除ID通知、过期后按窗口重读去重。目标：应用数据一致性。反馈与修订：版本化更新和删除。解释性：接口公开，未取得长期人生决策预测模型。隐私：按数据类型授权，删除通知只含ID，来源SPN按设备和应用分隔。费用：只读公开免费资料及本地Node，没有安装、注册、购买或API调用；实际未来集成费用未验证。局限：短窗口无法证明窗口外删除；缺失事件总体没有可信上界。

证据分级：MARKET-DOC为官方文档；INFERENCE为信息结构推论；内部人工E1为脚本测试。真实设备测试NOT_RUN，MARKET-INDEPENDENT-TEST=0，新增真人E2预测=0，历史E3=0。零新增费用操作，账单/免费额度NOT_VERIFIED。

下一MKT144：2026年6月SPN来源迁移引发的历史归因、去重与跨设备汇总负控制。
