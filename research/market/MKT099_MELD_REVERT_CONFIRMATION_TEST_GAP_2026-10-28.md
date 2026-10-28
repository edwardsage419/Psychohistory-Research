# MKT099 meld 历史回滚的用户确认、测试覆盖及提交顺序
日期：2026-10-28。证据：MARKET E1 固定源码静态审阅。承接MKT098，聚焦尚未独立记录的UI与测试边界。

## 固定上游来源
kizz-tech/meld 固定提交 91a44d78d97ba454b38ff8dfd8520ab895f8d447，与本轮检查的上游main一致。
1. src/components/history/HistoryPanel.tsx，Git blob 7a07cf7bcdcbf379d3eb061fb4c95f91a42462b0，36至43行与84至90行。
2. src-tauri/src/runtime/tauri_api/commands/history.rs，get_history和revert_commit。
3. src-tauri/src/adapters/git/mod.rs，Git blob a94db64317650a53c82132d29b6416efa4ef90b5，108至139、314至340及344至489行。
4. src-tauri/src/adapters/mcp/tests.rs，Git blob 555384eca8b421f206a38bb7d3925633b9312ac7。
5. 官方网站 https://meld.kizz.me/ ，GitHub README https://github.com/kizz-tech/meld 。

## 新增机制发现
UI的Revert按钮直接调用handleRevert，handleRevert直接await revertCommit(commitId)。该组件没有确认对话框、拟删除文件预览、未追踪文件保护开关或回滚范围确认。Tauri命令直接将commit_id传给git::revert_commit。此结论限于所检查的UI和命令路径，未进行运行时测试，也未全面证明应用其他入口不存在保护。
git/mod.rs的回滚函数先构造目标Git树，执行apply_tree_snapshot_to_vault，之后才执行repo.commit更新HEAD。若快照应用过程中部分文件写入或删除后发生I/O错误，或文件应用成功而Git提交失败，磁盘状态与版本历史可能短暂或持续不一致。静态源码没有可见的全目录事务回滚。实际故障触发条件与可恢复性仍未知。
git/mod.rs包含一个revert_commit_restores_previous_markdown_snapshot测试，覆盖同一个已追踪note.md的v2回退到v1。另有auto_commit_files_stages_only_target_markdown_files测试，证明提交可只包含选定文件。在该模块的七个测试及mcp/tests.rs已审阅测试中，没有找到“恢复时保留未追踪Markdown”的专门反例，也没有找到“提交失败后文件回滚”的故障注入测试。测试缺口不能直接推断生产环境发生过数据丢失。
MKT098此前已经确认快照应用会删除目标树外的Markdown，MKT099新增的是UI确认缺口、测试覆盖边界与文件先改动再提交的失败顺序，避免重复计作新漏洞。

## 产品机制矩阵
输入：用户指定的本地Markdown目录、历史Git提交、可选模型上下文。
状态：Markdown正文、本地SQLite索引、.meld/.git历史；恢复的目标树和当前目录可能不一致。
算法：Git revert计算树、全目录快照应用、Git新提交；语义检索与代理写入属于其他模块。
目标：可追溯的知识管理与历史恢复，尚无正式人生效用函数或长期预测评价。
反馈：写入读回检查、历史记录、回滚错误提示；未见当前路径的拟删除文件预览。
隐私：官方宣称本地保存；外部模型BYOK可能外发所选输入，具体权限与数据流仍待运行验证。
解释性：可显示历史提交和变更文件；不等于回滚影响范围完整预览。
费用：本地开源AGPL-3.0许可可免费审阅，官方本地Ollama模式标注免费；BYOK可能产生提供商计费，未来托管AI标价每月12美元且仍标为coming soon。本项目没有使用任何模型、下载应用或产生费用。
局限：未安装Rust应用、未运行上游测试、未故障注入；长期用户效果和实际数据丢失率未知。

## 候选安全控制
恢复前展示拟修改与拟删除路径，未追踪文件默认保留，用户显式确认影响范围；先在临时目录构造并验证目标状态，再原子替换或保留可恢复检查点；Git提交失败需准确报告且提供回滚。均属未采用候选，不提前实现个人决策产品。

证据等级：固定源码及上游测试存在性为E1 SOURCE；故障路径属于静态条件推导；实际删除与用户影响UNKNOWN。
下一步MKT100比较其他开源本地知识图谱的恢复保护及可验证备份，优先检查具备明确测试的项目。
