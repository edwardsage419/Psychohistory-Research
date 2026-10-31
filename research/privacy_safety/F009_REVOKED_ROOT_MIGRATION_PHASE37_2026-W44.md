# F009 第三十七阶段：已撤销信任根签发迁移凭证与恢复申诉

UTC 2026-10-31T10:20Z，2026-W44。目标键 (privacy_safety,F009,phase37,revoked_root_migration_credential_gate)。继承phase36跨根离线合并，专门增加旧根已撤销、迁移签发时间未知、独立恢复批准及旧授权缓存场景。全部虚构状态，绝不读取私人数据或执行产品授权。

一手公开标准RFC 6024要求信任锚管理考虑来源认证、重放检测、密钥妥协恢复；RFC 5280描述证书撤销、invalidityDate、可信锚及证书路径；RFC 9162提供日志一致性机制。将这些原则类比为个人决策授权候选，标准本身并不规定此类个人产品策略。
https://www.rfc-editor.org/rfc/rfc6024.html
https://www.rfc-editor.org/rfc/rfc5280.html
https://www.rfc-editor.org/rfc/rfc9162.html

程序 research/privacy_safety/f009_phase37_revoked_root_migration_20261031.py 枚举3种旧根状态ACTIVE/REVOKED/UNKNOWN、3种迁移签发相对撤销时间BEFORE/AFTER/UNVERIFIED、可信时间、独立恢复批准、新根凭证、完整前驱链、撤销高水位、旧授权缓存六个二值条件，共3×3×2^6=576个人工世界。严格候选规则返回REJECT 128、UNKNOWN 446、REVIEW 2；宽松规则只检查新根凭证及完整链，接受144种，其中142种未达到严格人工复核资格。普通Python 3.13.5及优化模式均执行PASS，使用显式ValueError检查。

REVIEW仅代表人工复核资格，绝不代表自动授权。对于已撤销根签发的历史迁移凭证，时间在撤销前也必须有可信时间及独立恢复批准；若私钥被提前攻破，撤销前签名仍可能不可信，需要更强的历史妥协时间证据。已知撤销后签发或仍使用旧授权缓存时，人工规则拒绝；未知根/缺链/时间不可核验时UNKNOWN。候选策略可能过度保守，未进行可用性与公平性评估。

实际密码学、真实签名、可信时间硬件、法律权限、跨设备离线恢复及申诉流程均NOT_RUN。576为穷举组合数，非现实发生率；全部INTERNAL_SYNTHETIC_E1，新真人E2=0、历史E3=0。零新增费用。下一phase38研究妥协发生时间早于公开撤销时间时的回溯影响和申诉证据。
