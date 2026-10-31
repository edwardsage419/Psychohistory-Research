# F009 第四十三阶段 设备身份轮换与删除登记的恢复不可辨识性
日期：2026-11-01 Asia/Singapore，UTC 2026-10-31，ISO 2026-W44。目标键：(privacy_safety,F009,phase43,device_rotation_erasure_tombstone_alias_bridge)。承接phase42删除登记到期与旧备份恢复反例；仅原则性未来安全研究。

## 英文监管来源
英国ICO伪名化指南 https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/anonymisation/pseudonymisation 说明伪名化数据仍可能属于个人数据，关联映射须隔离、最小授权、加密及密钥生命周期管理，指南正处于更新审查。欧洲EDPB 2025-01-17公开征求意见版 https://www.edpb.europa.eu/documents/guideline/guidelines-012025-on-pseudonymisation_en 是征求意见版本，不能视为已最终通过的法规。GDPR原文 https://eur-lex.europa.eu/eli/reg/2016/679 Article 5、17、19涉及数据最小化、删除及接收方通知。phase41/42已核对备份删除与最小化保留原则。没有据此设定统一保留天数或宣称实际法律合规。

## 可复算人工反例
程序 research/privacy_safety/f009_phase43_identity_rotation_erasure_20261101.js，Git blob 52a0f90c475bc53678d22a31c2d13d4027eec27c，V8执行PASS。构造旧标识 deviceA/caseX、新标识 deviceB/caseX、旧标识删除登记。朴素按新标识查旧登记时未命中，错误允许旧备份复活；保存经授权、可核验的轮换映射时，新标识解析到旧标识，删除守卫拒绝恢复。若映射丢失，两个历史（曾删除与从未删除）在可见活动记录、登记及旧备份内容相同，无法从当前快照判断，候选结果UNKNOWN_QUARANTINE。
五个二元维度穷举32种人工状态：无陈旧备份16、删除重放后人工复核3、未知隔离13，自动高影响恢复0。该计数仅是规则覆盖，不能作为实际风险发生率。未测试真实密码学、设备、恢复环境或个人敏感数据。
候选控制：删除登记与数据标识采用分离存储的可验证版本关系，轮换映射仅为合法恢复和删除重放保留最小必要信息，过期或缺失时隔离；不能将伪名化视为匿名化；审计记录不直接存储原始敏感值；人工复核保留申诉与撤销路径。映射的存在会增加可链接性，应设置目的限定、权限、最小期限和销毁计划。
证据：PRIMARY_REGULATORY_GUIDANCE + INTERNAL_NONBLIND_SYNTHETIC_E1。外部独立安全验证NOT_RUN，E2=0，E3=0。未新增费用，个人决策产品开发暂停。下步F009 phase44：研究恢复副本中的删除登记签名失效与映射重建授权的双重未知。
