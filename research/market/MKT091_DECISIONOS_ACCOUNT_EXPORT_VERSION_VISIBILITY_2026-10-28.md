# MKT091：DecisionOS个人导出与历史版本可见性边界审查

日期：2026年10月28日（Asia/Singapore）。性质：商业产品机制研究。证据等级：MARKET E1（固定源码及人工条件反例）。主动新增费用：0。

## 本轮真实增量与固定来源

英文官方开源仓库：https://github.com/shafaypro/DecisionOS 。截至本轮核验，上游main仍为 `af288e9f1e6c6c097e3eccd30f3b97a85ac22a69`，提交日期2026年10月7日。已读取以下固定Git blob：

* `src/app/api/account/export/route.ts`：`4d165921f66d9d7c27b2b4d9f95a9b1ca6714c69`
* `src/app/api/decisions/[id]/versions/route.ts`：`383b11234399d6e3920e540fed0146c86f6cb4be`
* `src/app/api/decisions/[id]/route.ts`：`b5809ef4de1028d8f51eb7bd82d1c2fb0fe7b02b`
* `src/lib/tenant.ts`：`d5a4ea40dd8d94d1cbbaf92a5f1cc1318a57af1e`
* `prisma/schema.prisma`：`f29af9a7ad8fb8f23a388f46850d1133b4205498`

新增发现：当前决策的历史版本API通过 `visibleDecision` 核查当前工作区与可见性；个人数据导出接口直接包含用户参与修改过的 `decisionVersions`，没有对这些版本所关联决策的当前可见性进行逐项重新过滤。每次编辑的版本 `snapshotJson` 保存修改前的完整决策记录，关联于编辑者 `changedById`。

人工条件场景：作者最初将一条决策设为工作区可见，另一成员在可见期间参与修改，之后作者将其改为私人。按照当前 `visibleDecision` 谓词，该成员不能通过版本API查看当前私人决策；其个人导出仍可能包含此前由本人编辑所产生的旧版本快照。这个场景揭示“当前读取授权”与“个人贡献历史导出”两种数据范围的差异。历史快照在此前可见期间已经被编辑者接触，不能据此推断泄露了其从未获准读取的新内容。完整应用的实际响应、删除与撤销效果、法律合规性和真实用户影响均未测试，不能宣称已经发生隐私事故。

独立静态合同与人工情景脚本 `research/market/mkt091_decisionos_export_visibility_contract_20261028.js` 共20项检查通过、失败0项；固定远端脚本内容已在本轮重新执行。检查仅覆盖列明的五个源文件与一个合成场景。

## 输入、状态、反馈、权限、解释性与费用

输入为结构化决策问题、备选方案、理由、假设、风险、负责人、可见性及后续复盘。当前状态由 `Decision` 表达；历史由 `DecisionVersion.snapshotJson` 与修改事件记录；个人导出按用户贡献关联历史，工作区导出按当前决策可见性组织。修改与复盘形成反馈闭环，历史页面和源记录支持有限解释性。MKT089已研究工作区导出遗漏历史，MKT090已研究最新编辑After字段显示问题；本轮仅新增个人历史导出与当前权限范围的关系，避免重复计算前两项。

官方README标注MIT开源、自部署、无付费订阅方案，官方仓库：https://github.com/shafaypro/DecisionOS 。本轮未部署、注册、安装、调用AI服务或购买资源。实际自部署和可选在线AI可能产生费用，本项目不采用。尚无本轮独立实证证据证明该产品改善长期个人决策质量。

## 候选方法及研究边界

未来个人决策系统应分别声明当前数据可见性、历史快照保留、个人数据可携带权与撤销授权后的处理范围；历史导出应标注其来源和授权依据，允许人工检查并在适用条件下限制再次使用。此为未采纳的方法候选，尚未建立产品规则，不接入真实敏感数据。研究保留R系列先行、之后归纳、最后熔炼的顺序。

下一轮MKT092可审查DecisionOS历史快照与账户删除的数据生命周期，或转向Dcider、Basisline的人工偏好纠错，先检查最新market登记。