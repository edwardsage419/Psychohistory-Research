# F009 第三十六阶段：跨信任根轮换与离线副本冲突恢复

UTC 2026-10-31T09:18Z，2026-W44。目标键 (privacy_safety,F009,phase36,cross_root_rotation_offline_merge)。继承phase35撤销乱序研究，新增签发信任根变更场景。纯人工候选安全控制，无真实敏感数据、证书、付费服务或产品开发。

原始标准RFC 5280定义CRL版本、签发者、范围、base/delta CRL一致性及证书路径约束；RFC 9162定义追加式日志一致性证明。个人决策授权的规则属于本项目的类比候选，未声称RFC直接规范个人决策系统。
https://www.rfc-editor.org/rfc/rfc5280.html
https://www.rfc-editor.org/rfc/rfc9162.html

虚构四事件：epoch1根A授权GRANT，epoch2根A撤销REVOKE，epoch3根A+B共同认可ROTATE_TO_B，epoch4根B经合法新授权REGRANT。所有签名与根身份仅为字符串，A+B合法迁移是人工前提。设备可信高水位4；候选规则要求完整事件链、唯一epoch、无冲突、可信根迁移。REVIEW仅为人工复核资格，绝非自动授权。

Python 3.13.5原生穷举四事件的16个子集，单设备REVIEW 1、REJECT 7、UNKNOWN 8。三个设备16^3=4096个组合，三设备均REVIEW仅1种。完整四事件的24种交付排列均REVIEW；epoch4单独到达UNKNOWN；已见撤销且缺合法完整后续链则REJECT；高水位丢失、根锚失效、重复epoch均UNKNOWN。全部断言PASS。程序 research/privacy_safety/f009_phase36_cross_root_offline_20261031.py。

候选控制：记录可信根身份、跨根迁移批准证据、事件前驱、撤销高水位、离线副本已见版本与争议状态；未知根、缺链、回退或冲突时暂停高影响自动执行并提供人工申诉。真实签名、法律授权、跨设备传播、删除与备份仍需验证。4096仅是人工组合数量，不能解释为攻击概率。E1人工研究，新增真人E2=0/历史E3=0，零新增费用。下一阶段phase37研究已撤销根签发的迁移凭证与恢复申诉安全。
