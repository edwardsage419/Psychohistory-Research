# A轨：Friedman 与 Oprea 2012 连续时间囚徒困境公开实验候选

日期：2026-10-27。独立研究候选来源审计。研究原文 Friedman & Oprea (2012), A Continuous Dilemma, American Economic Review 102(1), 337–363, DOI 10.1257/aer.102.1.337。正式数据版本 openICPSR V1（2019-10-11），DOI 10.3886/E112495V1，https://www.openicpsr.org/openicpsr/project/112495/version/V1/view 。

## 本轮实际核验的英文一手来源

openICPSR 原始页面确实列出作者、正式版本、实验数据类型和个体决策观察单位。研究设计为60秒连续时间囚徒困境，含八个离散子期的重复匹配对照，以及其他不同网格密度的对照。数据来自 UC Santa Cruz LEEPS 实验室。公开目录 `20091096_data` 共27条文件记录，分三页；第二页实际可见 `BySecond.csv`（929.6 KB）、`Pairs.csv`（3.6 MB）、`Profiles.csv`（7.1 MB）、`Read-Me.pdf`（37.3 KB）及原作者R分析脚本。第一页多项 `._` 前缀是操作系统伴随文件，不能作为独立行为数据。

本轮实际尝试 `BySecond.csv` 的官方公开下载入口，站点跳转至 ICPSR 登录授权流程。依照禁止注册付费账户和禁止访问非公开个人资料的约束，未继续登录、未下载数据，未获取任何真实参与者行记录。因而CSV字段、参与者与配对ID、连续时间刻度、每轮事件次序、场次独立性、原始行数及缺失值均待实际字节核验。公开目录存在不能替代可下载性与合法许可。根目录 `LICENSE.txt` 确实列出但尚未逐字读取，数据再分发许可未确认。

## 研究适配与去重

这是独立于R073 Montero-Porras 2022实验的不同作者与研究设计候选，尚未在原239所有研究中完成全来源去重，故保持 `NEW_INDEPENDENT_EXPERIMENT_PROVISIONAL`。连续时间与八子期控制与R073固定双人100轮 FP/SP 的时间语义不同。R073冻结模型和评分规则不可直接迁移，不能将连续秒级选择硬压缩成100轮或把八子期冒充100轮。可供未来连续时间行为切换、反应速度、时序社会互动研究，但需另行冻结协议。

## 资格结果

`OFFICIAL_REPLICATION_PROJECT_VERIFIED`; `FILE_INVENTORY_VERIFIED`; `RAW_BYTES_BLOCKED_LOGIN`; `FIELD_SCHEMA_UNVERIFIED`; `EVENT_TIME_UNIT_DESIGN_VERIFIED_BUT_ROW_LEVEL_PENDING`; `SESSION_DYAD_IDENTIFIERS_PENDING`; `FILE_LICENSE_PENDING`; `R073_DIRECT_FROZEN_TRANSFER_BLOCKED`; `NEW_E2=0`; `NEW_E3=0`; `ADDED_COST=0`。

来源：openICPSR https://www.openicpsr.org/openicpsr/project/112495/version/V1/view ，美国经济学会论文 https://doi.org/10.1257/aer.102.1.337 。没有使用中文网站、付费数据、私人资料或计费API。
