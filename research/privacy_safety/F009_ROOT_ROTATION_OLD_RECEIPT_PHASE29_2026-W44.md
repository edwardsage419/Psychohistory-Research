# F009 第二十九阶段 信任根轮换与旧回执撤销时效

日期 2026-10-31 UTC，2026-W44。目标键 (privacy_safety,F009,phase29,trust-root-rotation-old-receipt-revocation-timing)。承接 phase27 共同故障域与 phase28 共同信任根，本轮研究轮换后旧回执是否仍可用于当前删除或恢复操作。完全人工E1，绝无真实用户数据、私钥、真实签名或收费服务。

## 原始标准与适用边界

NIST SP 800-57 Part 1 Rev.5 提供密钥生命周期与管理一般指导：
https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
RFC 5280 第5.3.2节区分撤销处理日期与可能更早的 invalidityDate：
https://www.rfc-editor.org/rfc/rfc5280.html
RFC 3161 说明时间戳证据、签名时点与证书状态核验，以及时间戳机构密钥泄露风险：
https://www.rfc-editor.org/rfc/rfc3161.html

这些标准没有为本项目规定删除完成的自动授权条件。证书撤销原因、签名产生时刻、可信时间戳、信任根变化与当前请求版本均需分开评价。旧回执可作为历史待审证据，不能自动批准当前不可逆操作。

## 人工枚举与实跑

程序 research/privacy_safety/f009_phase29_rotation_revocation_synthetic_20261031.py 使用Python 3标准库，枚举2个密钥epoch、4种人为状态(active/rotated/compromised/unknown)、2个请求版本、时间戳验证/撤销失效早于签发/签名验证各2值，共128种人工组合。执行206项断言全部PASS。

分类为 REJECT 72、UNKNOWN 42、HISTORICAL_ONLY 12、ELIGIBLE_FOR_HUMAN_REVIEW 2。旧epoch在本人工规则下不会进入当前人工审批资格。明确已在签发前失效的 compromised key 与签名失败均拒绝；轮换后的旧epoch且有可信时间证明时只保留历史审阅；缺时间证明时保留 UNKNOWN。这里的 ELIGIBLE_FOR_HUMAN_REVIEW 仍要求人工独立审查，并非删除已完成或自动执行授权。

所有布尔量由人工设定。没有真正验证证书链、CRL、OCSP、签名算法、可信时间戳、根的组织独立性或删除效果。128种组合均匀枚举不代表现实风险概率。实际RFC 5280/3161适用还取决于证书、签名与具体安全策略。

## 候选控制与风险登记

候选最小状态包括请求版本、回执摘要、签发者公钥标识、epoch、签发与验证时间、撤销理由与失效日期、独立信任根依赖、最短必要保留期限。应避免保存原始个人行为、敏感信息或长期稳定身份。旧epoch或无法验证的撤销信息保留 UNKNOWN/HISTORICAL_ONLY，暂停高影响自动操作，支持人工复核与申诉。下一轮 F009 phase30 检查撤销状态延迟传播和离线设备重放。零新增费用；真人E2=0，历史E3=0。
