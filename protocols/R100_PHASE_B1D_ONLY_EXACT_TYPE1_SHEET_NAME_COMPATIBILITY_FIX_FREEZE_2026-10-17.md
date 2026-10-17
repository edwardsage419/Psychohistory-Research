# R100 Phase B1d：B1b来源角色sheet格式单项兼容修正冻结

日期：2026-10-17。仅因首次真实B1b `R100_B1B_AUTHOR_ORIGINAL_TYPE_NAME_NOT_MATCHED` 另立单项事前修订。原第一次fail-closed收据 [B1b初次失败](../research/R100/R100_PHASE_B1B_LIVE_CI_PAIR_RECIPROCITY_SOURCE_RECEIPT.json)永久保留，不能覆盖删除。

随后先独立冻结并执行[B1c仅 workbook.xml/relationships 的真实匿名编码诊断](../research/R100/R100_PHASE_B1C_LIVE_CI_ANON_WORKBOOK_NAME_RECEIPT.json)，真实原官方完整文件MD5/SHA全部再次一致；明确所有10个真实sheet匹配事前候选语法 #2 `(.+)_Type([12])`，在五处理每处理各Type1/Type2两张sheet完整成对。候选#1 `(.+)_Type ([12])` 匹配0份，所以首次严格失败可归因于命名空格差异；候选#3、#8也能匹配，但其规则更宽，选择原预列出且最窄、全10同时满足的**语法#2**，不依赖任何实际人或贡献得分。

## 此次唯一准许的代码变化

将 `research/R100/r100_phase_b1b_original_AB_role_partner_reciprocal_graph.py` 内的 `ROLENAME = re.compile(r"(.{1,60})_Type ([12])")` 唯一替换为 `ROLENAME = re.compile(r"(.{1,60})_Type([12])")`。保持 workbook-to-rels 精确对应、人物自己/对手位置、五处理完整人数、实际partner互指、跨两阶段换伴、person graph连通分量审计、全部12异常组、不公开source ID、拒绝即失败和零行为数据均原样不动。新增至少两个纯synthetic：新格式可解、旧格式在本次新规则下拒绝。

必须复用原GitHub Actions先合成后原官方完整字节审计，并将此次新真实B1b收据写入**新路径** `research/R100/R100_PHASE_B1D_LIVE_CI_PAIR_RECIPROCITY_SOURCE_RECEIPT.json`，避免覆盖原失败的第一次原始机读证据；第一次历史证据不动。

若真正对手配对互证仍失败，记录 `B1B_BLOCKED_BOUNDED` 的正反数量，不再修改原始A/B值或原本文献定义。同样禁止读取C:Z行为，任何行为模型预测=0，PESEN v0.1 FROZEN。
