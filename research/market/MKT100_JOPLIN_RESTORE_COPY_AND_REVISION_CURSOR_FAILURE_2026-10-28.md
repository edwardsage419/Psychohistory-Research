# MKT100 Joplin历史恢复副本与修订游标失败机制
日期：2026-10-28。证据MARKET E1。对照MKT098至MKT099 meld全目录恢复研究，选择新的开源产品，避免重复。

## 上游固定身份
laurent22/joplin dev HEAD b613d0064d018c2f68d983c907ab88e2712da116。
packages/lib/services/RevisionService.ts blob e2aea82a1f1513a1a6a8c7e1e804fe812711cb9f；
packages/app-desktop/commands/restoreNoteRevision.ts blob c80870643a12db51555f3aca330e5141d5a12da0；
packages/lib/services/RevisionService.test.ts blob 91658f2a33759476298d398baadd5a4b94fc3783。
官方英文文档 https://joplinapp.org/help/apps/note_history/ 和 https://joplinapp.org/help/dev/spec/history/ 。

## 机制新发现
1. restoreNoteById重建指定历史修订后调用importRevisionNote。该函数去掉原note.id和创建/修改时间，定位Restored Notes目录后用Note.save写入新实体。当前笔记不在该调用路径被覆盖。官方文档也明确恢复为副本。与meld的全目录快照覆盖/删除机制形成可验证对照。其他入口和插件未全面审查。
2. collectRevisions在单条修订生成异常时记录错误并继续处理，之后把revisionService.lastProcessedChangeId更新为当前change.id。源码注释明确说明失败的变更越过游标后不再处理；随后ItemChangeUtils.deleteProcessedChanges可清理已处理记录。由此存在条件性修订历史缺口风险。尚未触发真实差分错误，不能声称实际用户笔记丢失。
3. 官方文档规定一般每10分钟收集历史修订，默认保留90天；跨设备同步时，较短保留期的设备删除旧修订并同步，使全局实际保留期限趋向最短配置。源码测试覆盖修订重建、清理、冲突及删除笔记时的历史记录；本轮未运行上游Jest或完整应用。

## 产品机制与证据矩阵
真实输入：本地Markdown笔记、标题正文元数据、变更事件、同步设备。
状态：当前笔记、差分修订链、lastProcessedChangeId、恢复副本、跨设备TTL。
算法：差分重建、周期收集、历史清理、复制恢复；无证据显示人生效用优化或长期因果预测。
目标：可靠笔记保存、版本追溯及恢复。
反馈：用户选择修订并获得恢复副本；错误写日志，失败游标自动重试未见于本路径。
隐私：官方称offline first；外部同步可选，E2EE需要手动启用并在设备间同步密钥，不能假定默认开启。
解释性：可查看修订及恢复结果；跳过游标是否向普通用户显式展示UNKNOWN。
费用与许可：客户端免费开源，额外Joplin Cloud是付费选项；根LICENSE固定版本为AGPL-3.0-or-later，子目录可能另有许可。本轮仅公开审阅，未注册或消费。
局限：未运行完整应用、多设备同步或真实错误注入，故障率与长期用户效果UNKNOWN。

候选控制：默认恢复副本；全局覆盖前预览并确认；历史生成失败保留重试队列与明确告警；多设备TTL更改展示全局实际保留期限。均未采用、未开发。
来源 https://github.com/laurent22/joplin/blob/b613d0064d018c2f68d983c907ab88e2712da116/packages/lib/services/RevisionService.ts
下一轮MKT101核验Joplin跨设备修订清理传播，或转向TriliumNext的备份恢复。