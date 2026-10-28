# MKT098 meld 本地Markdown知识库的Git恢复与未追踪笔记风险

日期：2026年10月28日。研究性质：MARKET E1 固定源码静态审阅，未安装应用、未调用任何模型API或收费服务。与MKT097的PaOS云端代理架构审阅独立。

## 固定来源与机制
上游仓库 https://github.com/kizz-tech/meld ，固定提交 91a44d78d97ba454b38ff8dfd8520ab895f8d447。源码证据：
* src-tauri/src/adapters/git/mod.rs，blob a94db64317650a53c82132d29b6416efa4ef90b5。
* src-tauri/src/adapters/mcp/mod.rs，blob 69c147fd6b32fc07e38728ac7a012294b865118a。
* src-tauri/src/adapters/vault/mod.rs，blob d2a444c8394446f8fae197766d09b1ba6c6d2007。
* SECURITY.md，blob 9743724000bea2b7ca515323c696f8c34fe9b2c1。
该产品以用户本地Markdown/Obsidian/Logseq目录为输入，MCP工具kb_search、kb_read、kb_create、kb_update、kb_list供代理访问，使用本地索引及可选外部或本地模型。Markdown正文是主状态，.meld/.git裸仓库保存应用自己的版本快照；应用会给现有用户Git仓库增加.meld/忽略项。用户可通过历史记录和Git回滚查看修改。许可证AGPL-3.0，开源代码可免费审阅；外部模型、搜索API或本地算力的费用不由开源许可免除，本项目未启用。

## 本轮新增源码级风险一：恢复会删除快照外的Markdown
git/mod.rs第108至139行的apply_tree_snapshot_to_vault先枚举恢复树中的.md路径，再通过vault::list_md_files遍历当前目录。凡当前存在但恢复树未包含的.md文件，会调用std::fs::remove_file删除。git/mod.rs第314至339行的revert_commit先计算回滚树，随后调用该全目录快照应用函数。
vault/mod.rs第190至211行的list_md_files遍历目录内全部可见Markdown，不区分是否被.meld Git追踪。人工逻辑反例：应用先追踪a.md；用户随后用Obsidian手动新增尚未纳入.meld提交的b.md；再对a.md执行历史回滚，回滚树没有b.md，则快照应用分支会尝试删除b.md。该结论由固定源码控制流直接支持；真实安装环境的文件系统结果尚未运行验证。若b.md已纳入目标恢复树，以上删除条件不成立。涉及数据丢失风险，后续若需确认应在隔离临时目录做非敏感测试。

## 本轮新增源码级风险二：Git提交失败可能不影响写入成功反馈
mcp/mod.rs第1044至1075行的kb_update在写入前后分别调用auto_commit_files，但使用let _ = 忽略两次Result错误；第853至878行的kb_create在写入后同样忽略Git提交结果。写入成功后，接口主要依据文件内容回读判定成功。故磁盘笔记更新成功但版本记录失败时，接口可能仍返回成功，用户不能从成功提示推出Git备份存在。该结论限于源码逻辑，尚无故障注入或真实用户数据证据。

## 与未来决策模型的关系
这类本地优先系统可提供持久状态、来源引用、用户修改及版本回滚的参考。候选控制：仅修改明确追踪的文件，恢复前列出拟删除文件并要求用户确认；对未追踪笔记拒绝静默删除；Git写入错误作为单独可见的失败状态；回滚后逐文件验证。不得直接将这些候选控制视为已实现或已验证。

## 隐私、解释性、反馈与限制
官方SECURITY.md声称数据本地保存且无云同步或遥测；用户若配置OpenAI、Anthropic、Google等外部模型，实际输入可能发送至所选提供商，具体传输范围需另查源码及网络测试。代理引用本地笔记和Git历史支持一定可追溯性；决策效用函数、跨人生目标优化、因果识别、长期预测校准及实际用户决策改善均未证实。费用为开源许可免费审阅，外部推理或托管成本未知。未注册、未运行、未接入个人敏感数据。

## 证据分级
固定Git源码的控制流与测试存在性：MARKET E1 SOURCE REVIEW。未追踪笔记反例：静态控制流推导，运行影响待验证。Git提交错误传播：静态控制流推导，故障注入待验证。README及SECURITY的隐私声明：开发者声明，未独立验证。真实用户影响、漏洞可利用性和决策效果：UNKNOWN。

下一步MKT099：优先核查meld回滚行为是否已有上游测试覆盖，以及同类本地知识图谱的权限撤销和可恢复性，避免对未验证影响作事实升级。