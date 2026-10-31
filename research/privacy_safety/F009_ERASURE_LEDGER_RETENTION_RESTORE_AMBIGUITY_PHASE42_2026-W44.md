# F009 第四十二阶段 删除登记保留期限与旧备份恢复的不可区分风险
日期：2026-10-31 UTC，2026-W44。目标键：(privacy_safety,F009,phase42,expired_erasure_ledger_stale_backup_ambiguity)。

## 原始来源
GDPR官方法条 https://eur-lex.europa.eu/eli/reg/2016/679 ，Article 5(1)(c)(e) 数据最小化及保存限制、Article 17删除权与限定例外、Article 19接收方通知。EDPB英文指导 https://www.edpb.europa.eu/sme/be-compliant/respect-individuals-rights_en 强调登记和处理权利请求、通知接收方。EDPB 2026-02-18协调执法报告 https://www.edpb.europa.eu/system/files/2026-02/edpb_cef-report_2025_right-to-erasure_en.pdf 记录备份及删除流程的实际难点。英国ICO英文指导 https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/ 说明有效删除请求可能涉及备份，具体措施依保存计划和技术能力而定。ICO 2025-11-04日志保留指导 https://ico.org.uk/for-organisations/law-enforcement/guide-to-le-processing/accountability-and-governance/logging/how-long-can-we-keep-logs-for/ 指出需按目的及法定义务决定必要保留期；该页面针对英国执法处理，不能机械套用于未来私人决策产品。

## 候选冲突与安全原则
删除登记可帮助阻止旧备份恢复已删除对象，但登记本身可能包含可链接身份标识，长期保存会产生隐私与安全风险。未来应按对象类型、恢复窗口、离线副本最大寿命、合法依据和具体管辖区决定最短可解释保留期。禁止设定未经证据支持的统一天数。保存期限届满时，仍可能有不可确认的离线旧副本；候选安全控制是隔离恢复、限制处理、人工审查和完整副本重验，不能把“登记过期”解释为“历史删除失效”。登记可最小化字段、权限及链接性，但简单哈希和固定标识也可能仍可链接个人。确有法定保存例外时单独记录依据与复核期限。

## 人工状态实验
实际使用 Node.js v22.16.0 执行 research/privacy_safety/f009_phase42_minimal_erasure_ledger.js，Git blob 48ac076893897ea092a09fd3c0ea5d9ebff9eb63。六个二元维度：是否恢复、备份陈旧、删除登记存在、复制副本范围已知、登记是否过期、是否有法律保留例外，共64个人工状态。结果 NO_RESTORE 32，RESTRICTED_REVIEW 16，RETENTION_REVIEW 4，UNKNOWN_QUARANTINE 4，UNKNOWN_REPLICA 3，REPLAY_ERASURE_REVIEW 2，REVIEW_ONLY 3；自动高影响恢复0。Node --check及原生命令均通过。

构造两个不同历史：一份没有删除义务，另一份存在已完成的删除义务；登记到期后当前活动数据、登记及陈旧备份的可见内容相同。朴素恢复会使第二种历史的虚构 caseX 复活，当前快照无法辨认两种历史。候选守卫对陈旧备份且无登记的恢复保留 UNKNOWN_QUARANTINE；仍有有效登记时可先重放删除再进入人工复核。该反例为人为构造的可识别性问题，不能当作实际泄露率或法律合规证明。

证据等级：PRIMARY_LEGAL_TEXT + PRIMARY_REGULATORY_GUIDANCE + INTERNAL_SYNTHETIC_E1。真实个人数据、真实备份、设备及密码学均未使用；法律合规测试 NOT_RUN，固定保存期限 NOT_DETERMINED，实际账单 UNKNOWN。未来个人决策产品仍暂停。下步 F009 phase43：研究最小化删除登记在设备轮换与不可连接身份下的重放条件。
