# F009第八阶段：不同服务通行密钥撤销与本地凭据副本

日期UTC：2026-10-30，2026-W44。目标键：(privacy_safety,F009,phase8,RP-credential-manager-revocation-scope)。状态：COMPLETE_BOUNDED_ARTIFICIAL_E1。延续第七阶段计数器风险研究，本阶段专注服务端注销与凭据管理器副本的独立生命周期。

## 英文一手资料

W3C WebAuthn Level 3 Recommendation, 2026-08-25, https://www.w3.org/TR/webauthn-3/ 。公钥凭据与RP ID绑定，RP必须验证origin，规范不提供通用跨RP撤销。Google for Developers, Passkeys user journeys, https://developers.google.com/identity/passkeys/ux/user-journeys ，2026-10-30实读。服务方移除服务器保存的公钥可以使该服务不再接受该凭据，私钥不会因此从用户设备或凭据管理器自动删除。Google for Developers, Passkeys, https://developers.google.com/identity/passkeys ，2026-10-30实读。跨设备同步由凭据管理器完成，通行密钥按站点/服务隔离；生物识别材料不传给网站。Google for Developers, supported environments, https://developers.google.com/identity/passkeys/supported-environments ，2026-10-30实读，凭据可在管理器内同步到其他设备。

## 人工风险控制实验

脚本 research/privacy_safety/f009_rp_credential_lifecycle_phase8_20261030.js；Node.js v22.16.0原生执行，exit=0，15项检查通过，其中10项状态断言、5项非法输入拒绝。归档Git blob应为5cef32397238b2b737f3b2c30b06472a035d6542。

人工服务rpA和rpB各自登记不同凭据。撤销rpA旧凭据后，rpA验证拒绝，模拟凭据管理器仍保留旧私钥副本，rpB原凭据仍可用。随后模拟本地删除旧副本及rpA新epoch凭据绑定。旧epoch被拒绝，人工signatureVerified=false时拒绝。脚本的signatureVerified仅为虚构布尔前提，未进行真实签名验证、设备管理器删除或服务端认证测试。

## 候选控制与风险登记

F009-08A：将RP端注销误认为所有同步副本已物理删除。候选控制：独立显示SERVER_REVOKED与MANAGER_COPY_UNKNOWN，保留用户自行管理设备副本的指导。
F009-08B：误认为一个RP撤销可跨站点阻断所有凭据。候选控制：按RP ID、账号和credential ID分别登记，不进行跨服务隐式撤销声称。
F009-08C：新凭据绑定后旧epoch操作重新生效。候选控制：服务器端验证绑定epoch和撤销记录，人工高风险操作需二次确认。
F009-08D：保存跨站点凭据关联元数据形成新的跟踪面。候选控制：最小化服务内凭据ID，避免建立跨RP全局关联索引。
F009-08E：误将人工布尔值判定为真实密码学证明。候选控制：所有正式安全验证要求实际challenge、origin、RP ID、签名和计数器校验，审计中明确标注NOT_TESTED。

证据：W3C标准及Google官方产品技术文档；本地人工E1状态机。实际密钥、真实用户、真实设备、跨RP安全实验均未接入。外部独立复验0，新增真人E2预测0，历史E3=0。无付费API、注册、CI或新增费用；账单及免费额度NOT_VERIFIED。下一F009 phase9：账户恢复备用方式与凭据撤销后的授权边界，检查恢复流程绕过风险及人工申诉渠道。
