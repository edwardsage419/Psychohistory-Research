# F009 第二十七阶段 多见证共同故障域与伪独立性

日期：2026-10-31 UTC，2026-W44。目标键：(privacy_safety,F009,phase27,correlated-witness-common-mode-failure)。证据为NIST公开标准的一般密钥与数据保护原则，加内部人工E1候选策略实验。

## 标准范围
NIST SP 800-57 Part 1 Rev.5：https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
NIST SP 800-88 Rev.2：https://csrc.nist.gov/pubs/sp/800/88/r2/final
OWASP Cryptographic Storage Cheat Sheet：https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
上述标准讨论密钥管理、介质清理与存储保护；没有为本项目规定两见证门槛、设备版本规则或任何自动决策批准。以下均为待检验候选。

## 人工实验
三个见证ID，前两个共享同一提供方及故障域A，第三个属于B。各见证状态为fresh/stale/unknown，再乘撤销标记与当前版本标记各两值，共108种人工状态。Python 3.13.5标准库执行枚举及断言通过。只要求至少两个fresh的宽松策略接受28种；同时要求两个不同提供方故障域、当前版本、无撤销的候选策略接受5种；宽松策略额外接受23种。典型反例为A域的两个见证均fresh而B域unknown，宽松策略错误将两份关联信息当作独立确认。

数量来自人为枚举，不能代表真实攻击概率。严格策略仍然假设提供方身份、密钥、签名、撤销与独立性可信；没有进行实际密码学或跨机构测试。两个故障域也可能共享上游身份源或管理者，故域标签本身仍需证据。

## 候选控制
未来删除版本和恢复证明需记录最小化的见证来源、签名密钥身份、故障域、请求版本、撤销状态及保留期限。缺少可验证独立性时输出UNKNOWN并暂停高影响自动操作。不能凭两份一致回执宣称真实删除完成。不得保存用户原始敏感行为到见证服务。仅作研究知识储备，不开发个人决策系统，不设置人生效用权重。新增真人E2=0，历史E3=0。下一专题：独立故障域判断所需的最小可审计证据。
