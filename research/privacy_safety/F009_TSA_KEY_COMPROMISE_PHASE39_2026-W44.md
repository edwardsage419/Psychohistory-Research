# F009 第三十九阶段 TSA私钥泄露与历史时间戳回执
日期：2026-10-31 UTC，2026-W44。目标键：(privacy_safety,F009,phase39,TSA_compromise_and_independent_witness_evidence)。承接phase38签名者妥协时间窗口，新增时间见证机构本身的密钥泄露研究。无用户敏感数据、真实密钥、真实设备或个人决策产品开发。

## 原始标准
RFC 3161 第4节 https://www.rfc-editor.org/rfc/rfc3161.html 区分正常停止TSA服务与TSA私钥泄露。正常停用且未泄露时，符合撤销原因约束的旧令牌可能保留历史有效性；TSA私钥已泄露时，该私钥签发的令牌不再可信。RFC提及审计轨迹和两个不同TSA的令牌可帮助辨别历史真假，须独立验证。RFC 5280 https://www.rfc-editor.org/rfc/rfc5280.html 规定证书路径与CRL撤销语义。标准用于PKI，本轮个人决策授权规则只是候选类比，不宣称标准直接要求以下人工策略。

## 实际人工枚举
Python标准库程序 research/privacy_safety/f009_phase39_tsa_compromise_20261031.py 枚举八个二元字段：签名者有效、主TSA泄露、第二TSA有效、第二信任根独立、审计轨迹可用、撤销状态新鲜、人工恢复批准、令牌时间是否早于声称泄露。256种状态，普通模式与python -O均实际执行PASS；关键检查采用显式ValueError。

结果：REJECT 128，UNKNOWN 118，REVIEW_PRIMARY 8，REVIEW_SECOND_WITNESS_ONLY 2。REVIEW仅指进入人工审核，全部状态禁止AUTO_EXECUTE。主TSA已泄露时，令牌表面时间早于泄露时刻不能自动恢复信任；仅当独立第二TSA、独立信任根、审计轨迹、最新撤销信息和人工批准齐备，才可用第二见证证据进入人工审核。原受损TSA令牌仍不被信任。此枚举不是攻击发生概率，第二TSA的真实独立性尚未证明。

候选控制：最小化保留签发与见证时间、证书链/撤销原因、可信根标识、授权版本和审计摘要；历史证据与当前执行权限分离，提供人工复核、纠错、申诉与可撤销授权。真实签名、密钥泄露日期、TSA证书、撤销列表和离线设备NOT_RUN。应继续评估过度拒绝和跨文化公平。证据：PRIMARY_STANDARD_DOCUMENTED、INTERNAL_SYNTHETIC_E1；E2=0，E3=0。未注册收费服务、未触发CI，账单/额度未核验。下一阶段研究可信时间见证的证据续期与历史签名信任更新。
