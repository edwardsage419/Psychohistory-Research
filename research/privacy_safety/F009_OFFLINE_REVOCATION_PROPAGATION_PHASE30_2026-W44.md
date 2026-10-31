# F009 第三十阶段 离线设备撤销延迟与旧回执重放

UTC日期2026-10-31，2026-W44。目标键 (privacy_safety,F009,phase30,offline-revocation-propagation-and-cached-receipt-replay)。承接phase29旧信任根回执。仅候选安全控制，零真实个人数据和密钥。

## 原始资料

NIST [SP 800-63B-4](https://csrc.nist.gov/pubs/sp/800/63/b/4/final)于2025年7月正式发布，2026-10-06发布实施资源说明，讨论身份认证器管理和会话边界。OWASP [Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)说明服务端会话失效、绝对超时和风险事件后的重新认证。两者均没有为本项目规定离线数据删除完成的自动批准条件。本文将其作为一般安全原则，未作法律合规认证。

## 人工E1实验

Python 3标准库程序 research/privacy_safety/f009_phase30_offline_revocation_20261031.py 枚举6个布尔变量：离线、旧回执缓存、人工假定签名有效、撤销通知已送达、请求版本当前、见证状态当前，共64状态。实际执行199项断言全部PASS。

宽松人工策略只看缓存回执和签名有效，接受16状态。严格候选策略要求设备在线、撤销通知已送达、请求和见证均当前，且缓存回执和签名条件满足；分类为REJECT 32、UNKNOWN 31、ELIGIBLE_FOR_HUMAN_REVIEW 1。宽松策略额外接受15状态。数字仅是均匀枚举人工状态的数量，没有现实概率意义。唯一“具备人工复核资格”状态也不代表删除已完成或自动授权。

## 风险与候选控制

离线设备可能仍持有撤销前的缓存回执。仅凭过去签名通过无法证明当前撤销状态。候选控制为回执绑定请求版本和有效期、最短必要撤销元数据、重新联网时核对当前撤销版本和独立见证、失联期间高影响操作进入UNKNOWN、恢复时人工复核和申诉渠道。应限制敏感原始行为数据进入安全日志。真实签名、CRL/OCSP、设备、网络延迟和实际删除均未验证，人工策略只是未来设计备选。新增真人E2=0、历史E3=0。下一轮研究离线时钟漂移与短期授权过期，仍不得开发个人决策产品。
