# MKT136 迟到标签、修订时间窗校准及 ActivityWatch 0.14 数据机制

日期：2026-10-30 Asia/Singapore。目标键：(market,MKT136,none,delayed-revision-window-calibration-ActivityWatch-v0.14)。状态：COMPLETE_BOUNDED_ARTIFICIAL_E1。先完成 R 系列，后统一分类，再模型熔炼。未使用真实个人数据。

## 1. 人工实验与实际执行

八条人工预测 A 至 H，生成时点 0,0,1,1,2,2,3,3；前四条预测概率 1/5，后四条为 4/5。最终人工标签分别为 0,0,1,0,1,1,0,1。固定成熟窗口为预测后 3 个时间单位。首次可见标签时点为 1,5,6,2,3,7,8,4。C 初始标签 0 于时点 9 改为 1；F 初始标签 0 于时点 10 改为 1。预测及数据设计为本轮人工选择，非真实行为样本。

每个评估时点只把 prediction_at + 3 <= cutoff 的记录纳入目标总体。仅首次标签已可见的记录参与可见 Brier；标签缺失的记录保留在目标总体中，以二元结果 0/1 各自可能的平方误差计算严格有限可行界。最终真值列仅用于人工 oracle 核验。无分布假设，区间是确定性部分识别界，并非95%置信区间。

| cutoff | 成熟记录 | 可见标签 | 可见Brier | 全成熟总体Brier可行界 | 最终真值oracle |
| --- | ---: | ---: | ---: | --- | ---: |
| 4 | 4 | 2 | 1/25 | [1/25,17/50] | 19/100 |
| 6 | 8 | 6 | 1/25 | [1/25,19/100] | 19/100 |
| 8 | 8 | 8 | 19/100 | [19/100,19/100] | 19/100 |
| 10 | 8 | 8 | 19/100 | [19/100,19/100] | 19/100 |

重要反例：cutoff=8 和 10 的总体 Brier 都是19%，但两个预设预测概率组的等权经验校准误差 ECE 分别为25%与5%。在8时点，低概率组实际阳性率0、高概率组1/2；在10时点，修订后分别为1/4与3/4。C和F的两次修订对总体Brier的影响相互抵消，导致总体评分掩盖了分组校准变化。两组每组四条，ECE采用固定二箱绝对校准差加权，无事后选箱。

归档标准JS程序 research/market/mkt136_delayed_revision_window_calibration_20261030.js，Git blob df7916214d974e937fec71beb0e77d63816776a2，远端文件回读后在V8原样执行，8项正断言及7项非法输入拒绝均PASS。原生Node.js命令行及GitHub Actions NOT_RUN。该程序没有估计真实迟到分布、标签误差率或预测改善效果；人工E1，新增真人预测E2=0、历史E3=0、外部独立团队=0。

方法背景：Gao & Yang (2022) 多窗口迟到反馈建模 https://arxiv.org/abs/2205.12406 ；Chen et al. (2022) 迟到标签更正 https://arxiv.org/abs/2202.06472 。论文仅提供方法背景，本轮数字由人工实验计算。

## 2. ActivityWatch 公开英文官方资料深读

上游：ActivityWatch/activitywatch，正式发行 v0.14.0 于2026-10-06 UTC 发布，v0.14.1 于2026-10-10 UTC 发布。官方发行说明、数据模型、同步指南和官网实际查阅。无注册、安装、采集个人活动或付费。

* 数据输入：窗口标题、应用活动、浏览器标签页、离开设备状态及可选编辑器活动；watcher 按设备和来源写入 bucket。每条事件包含 timestamp、duration、data。所有事件时间戳以UTC存储，原始时区偏移丢弃，跨本地日期解释须另行保留时区。
* 状态与算法：心跳事件可按相同 data 和 pulsetime 合并为持续时段；报告界面按分类和时间聚合，属于活动描述统计。没有公开证据表明该产品提供因果人生策略、反事实效用优化或经验证的长期预测。
* 目标及反馈：用于个人活动回顾、分类和时间分配反馈，允许用户自定义类别与导出。同步数据被导入带有 synced-from 标记的桶，设备各自写自己的数据，其他设备只读。
* 同步修订：官方 v0.14 指南明确同步默认关闭，需要用户选用现有文件传输工具；最近7天的来源设备编辑可以同步，**删除不会同步**。这构成跨设备删除语义的明确产品限制。不能把某设备删除视为所有复制品已擦除。其他设备持有完整副本，磁盘占用增加；设置不参与同步。
* 隐私权限：官方宣称默认本地存储、不设 ActivityWatch 服务器或账户；同步目录若交给 Dropbox/Google Drive 等第三方工具则会由第三方传输/保存。v0.14.0说明提供敏感窗口标题预入库过滤和可选服务端API key。需要分别核查本地暴露、同步文件访问控制、备份删除、设备丢失等威胁。
* 解释性与费用：事件来源、时间、持续长度可检查；官网声明 MPL-2.0 免费开源，无功能门槛，AW Pro 为可选资助。无长期人生决策效果的独立研究证据。本轮仅官方技术文档支持，未运行实际软件或独立安全审计。

官方来源：
https://github.com/ActivityWatch/activitywatch/releases/tag/v0.14.0
https://github.com/ActivityWatch/activitywatch/releases/tag/v0.14.1
https://docs.activitywatch.net/en/latest/buckets-and-events.html
https://docs.activitywatch.net/en/latest/syncing.html
https://activitywatch.net/blog/syncing-your-activitywatch-devices/
https://activitywatch.net/

## 3. 候选控制与证据边界

未来候选字段：prediction_at、maturity_horizon、label_first_seen_at、label_revision_at、label_version、cutoff、missing_label_count、per_bin_calibration、device_origin、sync_version、deletion_tombstone_status。历史as-of与最终裁定评价应分开；缺失标签必须显示可行界与弃权；汇总Brier相同也要审查分组校准。若未来涉及多设备，撤销授权、删除本地数据、删除同步副本和清除备份分别登记。以上均为候选知识储备，无产品开发。

费用：无新增服务、收费API、CI、订阅或敏感数据接入；GitHub实际账单与免费额度未核验。下一项 MKT137：标签修订的方向性选择及多组公平性校准，在严格预设评价截止后测试。
