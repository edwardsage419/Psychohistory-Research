# MKT144 Health Connect步数来源迁移与跨导出重复归因

日期UTC：2026-10-30。目标键：(market,HealthConnect,MKT144-v1,SPN-source-migration-external-merge-identity)。基线main：b81c231290417ee575986410044ececd36fd5b55。状态：COMPLETE_BOUNDED_ARTIFICIAL_E1_AND_MARKET_DOC。前序MKT143已读，未重复过期令牌实验。

## 英文官方来源与机制

Android Developers, Read raw data, https://developer.android.com/health-and-fitness/health-connect/read-data ，2026-10-30实读。2026年6月起，设备原生步数来源由通用包名 android 转为设备特定、应用作用域的 Synthetic Package Name (SPN)；更新前的历史记录仍标记 android。SPN对同一应用当前设备稳定，对不同应用不可直接比较。官方要求不要硬编码SPN，改用 getCurrentDeviceDataSource；此接口在Android 14且SDK Extension 22或更高版本可用。官方说明不按DataOrigin筛选的aggregate查询自动包括原生步数，单纯来源名称迁移本身不需要更改该聚合逻辑。

输入：Health Connect授权的步数记录、记录ID、日期、步数、DataOrigin。状态：旧android来源、当前应用范围SPN、设备与应用作用域、授权范围、可能的外部导出副本。目标：正确归因和完整性审计。算法：按来源查询或不筛来源聚合、应用内来源识别、外部多源对账。反馈与修订：与MKT143所审计的版本化更新和删除事件衔接。解释性：接口字段与来源迁移规则公开，外部跨应用真实设备身份映射没有文档保证。隐私：应用作用域SPN旨在限制跨应用设备关联。费用：官方公开资料免费，本轮只读和本地Node，无账号、设备权限、付费API或产品订阅。未取得真实用户长期决策改善或独立端到端验证。

## 可执行人工实验

脚本：research/market/mkt144_spn_migration_identity_20261030.js。Node.js v22.16.0实际运行，exit=0，17项检查通过，其中12项正向检查和5项非法输入拒绝。远端归档Git blob应为66a51dc893ec1d06fc007b688ecae5861cd4de28。全部记录、事件身份与镜像来源均为虚构，未读取健康数据。

| 人工处理 | 步数 | 解释 |
| --- | ---: | --- |
| 旧android来源记录 | 1200 | 2026-06-01，记录legacy1 |
| 新SPN来源真实新增记录 | 1400 | 2026-06-02，记录current2 |
| 外部导出额外镜像 | 1200 | 2026-06-01，记录mirror1，人工oracle假定与legacy1同事件 |
| 直接拼接三条记录 | 3800 | 三个记录ID不同，按ID去重无效 |
| 使用人工已知事件oracle去重 | 2600 | 仅在身份映射真实可靠时成立 |
| 虚假增量 | 1200 | 相对于oracle真实2600多计6/13，约46.15% |
| 仅有来源迁移且没有镜像 | 2600 | 不存在额外计数 |

实验显示：来源标签变化和事件重复是两个独立问题。官方SPN迁移本身没有证明产生重复。跨导出重复是额外人工故障注入。不同SPN或相同时间和数值不足以证明两条记录代表同一事件；自动合并会引入误删风险。若可信事件身份不可得，候选系统应标记POSSIBLE_DUPLICATE_UNRESOLVED，并保留原始来源和计数上下界，避免擅自连接跨应用设备身份。

## 证据与下一步

MARKET-DOC：Android官方接口说明。INFERENCE：跨来源合并需要可验证身份与完整性边界。E1：本地人工数据17项检查。MARKET-INDEPENDENT-TEST=0，真实Android设备=NOT_RUN，真人E2预测=0，历史E3=0。未运行GitHub Actions，账单与免费额度NOT_VERIFIED。下一MKT145：同日多来源聚合、重复记录的可识别界和来源身份缺失时的弃权条件，优先查官方聚合去重语义，避免将人工故障误称平台缺陷。
