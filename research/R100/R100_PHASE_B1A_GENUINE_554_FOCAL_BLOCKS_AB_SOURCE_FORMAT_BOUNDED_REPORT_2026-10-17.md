# R100 B1a正式来源编码报告：已认证原XLSX仅A/B字面值结构，554个候选焦点块，12个未知双编码例外

日期：2026-10-17。**B1a=PASS_BOUNDED_ORIGINAL_AB_FORMAT_ONLY**；B1b人物真实伙伴互证正在按另冻规则审计。**没有读取C至Z列行动/问卷、没有一个真人行为模型得分。PESEN v0.1 FROZEN。**

## 固定来源与预冻结顺序

继续严格复用Zenodo原作者Wang/Hilbe/Zhang 2025 `ThresholdPGG_ExperimentalData.xlsx` 的出版方原MD5 `c40171abb172da8e16b0839db98a2cf2`、完整217396字节、项目SHA256 `825b1cd3226aeca7a19d76d9594f655114b12059648f9ca03b3291c3cf9ab200`。B1a首次读取源A/B字面元数据**此前**已归档[专门隐私和编码审核冻结](../../protocols/R100_PHASE_B1_PINNED_XLSX_AB_ONLY_LITERAL_ROSTER_SCHEMA_DIAGNOSTIC_PRESCORE_FREEZE_2026-10-17.md)。源Python代码限制只解析A/B身份和配对码，不导出source字面值、原表名、人物编号、对手编号，不接触行为真值。20项A2+15项B0+18项B1a纯synthetic先于原行为读取，真实结果由[GitHub Actions机器来源匿名收据](R100_PHASE_B1A_LIVE_CI_AB_SOURCE_FORMAT_RECEIPT.json)永久写回[Git提交dbc7567](https://github.com/edwardsage419/Psychohistory-Research/commit/dbc7567cc4e070e484ab40f9cd69362d682e9724)。

## 原始身份编码的实际非行为审计

十张来源工作表依次有 **55、55、59、59、56、56、52、52、55、55** 个完整四行候选焦点记录，**共554个候选焦点块**。每块A列四个实体XML cell中只有**一个非空数值**，其余三个空；各块B列四个都以Excel共享字符串类型 `s` 给出**四个非空代码**。

B列字面值的无标识等价类分布：

* **542块**恰好含3种不同B码。
* **12块**恰好含2种不同B码。
* 0块其他不同值数量。

12个特殊块按来源匿名成对工作表分布：前四对每表1个，最后一对每表2个。这些是真实来源的编码等价关系事实，不能把异常预先解释为“实验同伴重复匹配”或“源失误”，也不得删除它们来提升预测准确率。四行候选块不能当四名真人或四个独立局；原作者报告五处理554名真人仍须先验证A唯一性、B人物码与互指关联，然后才能说是本研究确认的**554个独立来源人**。发布方对源B列称为每个焦点玩家的两场配对信息，源A列称为Participant ID；这为B1b测试提供有界解释原则而非已证结果。[官方数据说明](https://zenodo.org/records/16918146)。

## 后续已在真实配对检查前冻结的B1b反证

[Phase B1b真正角色与伙伴源互指冻结](../../protocols/R100_PHASE_B1B_AB_FOCAL_ROLE_RECIPROCAL_PARTNER_GRAPH_PRESCORE_FREEZE_2026-10-17.md)要求Type1 B[0]=B[3]，Type2 B[1]=B[2]，然后对剩余对手两个代码按Phase1/Phase2建立跨两源sheet同人的唯一双射和双向伙伴关系，检验任何同伴重复、source A多次复用、对手代码不指向真正焦点人、重复行合计是否满足原作者的两场换伴设计。**所有12特殊等价块都必须保留并参与诊断**。如先验假说失败，只能给出B1b资格阻断的真实反例；不能未经审计回头改模型或读取真人贡献值。

本阶段结论仅为**真实第一手来源A/B码的匿名格式验证 E1**，不代表实际人类贡献E2、心理历史增量、前瞻E3或历史尺度因果。
