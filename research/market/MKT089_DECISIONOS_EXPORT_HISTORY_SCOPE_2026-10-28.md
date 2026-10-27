# MKT089：DecisionOS版本历史与导出范围的固定源码审计

日期：2026年10月28日（Asia/Singapore）。证据：MARKET E1，固定源码加离线静态合同检查。新增费用：0。

## 固定来源及研究范围
英文开源仓库 https://github.com/shafaypro/DecisionOS ，固定main提交 `af288e9f1e6c6c097e3eccd30f3b97a85ac22a69`。GitHub仓库标注MIT许可证。核对六份源码：`src/app/api/decisions/export/route.ts` blob `972bac9691d1b5d9a01c171a0e101989985c787c`；`src/lib/decision-export.ts` blob `81df6d1892d29e817d126e5d15d4284de6f10eea`；`src/app/api/account/export/route.ts` blob `4d165921f66d9d7c27b2b4d9f95a9b1ca6714c69`；`src/app/api/decisions/[id]/route.ts` blob `b5809ef4de1028d8f51eb7bd82d1c2fb0fe7b02b`；`src/app/api/decisions/[id]/versions/route.ts` blob `383b11234399d6e3920e540fed0146c86f6cb4be`；`prisma/schema.prisma` blob `f29af9a7ad8fb8f23a388f46850d1133b4205498`。未安装或运行完整应用。

## 新增发现
工作区决策导出接口 `/api/decisions/export?format=json` 的注释将JSON称为适合备份与迁移的版本化信封。源码确实输出 `schemaVersion=1`、当前决策字段、标签、参考链接及完整结果复盘记录。其查询没有读取 `DecisionVersion`、`DecisionEvent`、`DecisionNote`、`DecisionRelation` 或 `ActionItem`，序列化器也没有这些字段。版本化信封只代表导出格式版本，不能替代单条决策的修改历史。使用该工作区JSON文件单独恢复时，无法从文件重建旧版本快照、历史事件、备注讨论或决策关系图。

该应用另有 `/api/account/export` 个人数据导出，查询包含 `decisionVersions`、`events`、`notes` 等关系，但以当前登录用户的贡献为范围。工作区决策导出与个人数据导出具有不同范围。个人数据导出不能被推定为整个工作区的完整历史备份。源码同时有 `/api/decisions/[id]/versions` 历史读取接口，修改决策时创建旧状态快照。上述差异为明确的导出范围问题，不推断服务实际发生数据丢失。

## 产品机制、局限和费用
输入包括问题、方案、理由、替代方案、假设、风险、影响级别、负责人、状态及后续结果复盘。状态由当前决策、修改快照、事件、关系图和复盘记录分层表达。反馈包含定期复盘、结果标记、替代或撤销决策及修订历史；检索与决策健康状态有规则性实现，AI问答属于可选功能。官方README称无AI密钥时可退化为检索。解释性来自引用决策原文、版本历史和关联记录；没有发现独立验证长期决策质量改善的研究。

权限方面，工作区导出遵守当前登录者的可见性过滤，私人决策的公开分享需额外授权；账户导出以本人为中心。真实部署、数据生命周期、跨用户合并及导入恢复路径未执行验证。MIT自部署源码可免费阅读；本轮只用公开源码和标准库。没有安装、注册、付费、调用第三方模型API或启动云端服务。自部署在现实中仍可能有基础设施费用，本项目不采用付费部署。

## 测试、证据边界和候选方法
已对固定GitHub源码执行16项独立静态合同检查，16 PASS，0 FAIL；脚本 `research/market/mkt089_decisionos_export_scope_20261028.js` 仅依赖Node.js标准库，可在取得上述固定源码后重跑。此处的“缺少”只针对指定工作区导出路径，尚未执行完整应用、导入恢复测试、真实用户使用或外部独立研究。证据等级为SOURCE_E1；长期行为改善为UNKNOWN。

未来心理史学候选控制：原始决策、各版本快照、事后反思、引用证据和关系边分别赋予稳定ID；每种导出明确范围和缺失清单；进行离线恢复测试；保留用户人工纠错与拒绝画像。不得将某种导出格式的版本号误认为完整历史证明，不预设唯一人生效用权重。R系列优先顺序不变。

下一MKT090优先检查DecisionOS的单条决策版本恢复与跨工作区权限边界，或转向Basisline的偏好纠错机制；先查是否已有新报告避免重复。
