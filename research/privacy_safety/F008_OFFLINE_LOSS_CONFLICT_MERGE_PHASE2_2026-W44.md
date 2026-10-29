# F008 第二阶段：遗失设备、离线期限与冲突合并中的撤销传播

日期：2026年10月29日，第44周。轨道：privacy_safety。状态：PHASE2_BOUNDED_E1_IN_PROGRESS_UNADOPTED。承接F008第一阶段。

## 英文来源
1. [官方开源文档] Automerge https://automerge.org/docs/hello/ 。离线副本可本地修改并在重连后合并并发变更；同步一致性本身不提供撤销或物理清除保证。
2. [正式标准] NIST SP 800-63B-4 Authenticator Event Management https://pages.nist.gov/800-63-4/sp800-63b/events/ 。关于遗失或受损认证器失效与通知的指导，适用范围有明确边界。
3. [正式标准] NIST SP 800-63B-4 Session Management https://pages.nist.gov/800-63-4/sp800-63b/session/ 。区分会话总时限和不活动超时。
4. [官方安全指导] NIST SP 800-63B-4 Syncable Authenticators https://pages.nist.gov/800-63-4/sp800-63b/syncable/ 。讨论同步密钥跨设备扩散和撤销风险。

## 合成状态机
Node标准库脚本research/privacy_safety/f008_offline_loss_conflict_20261029.js已本地执行16项断言，失败0。服务器初始授权版本7，设备A在线、B离线。候选离线只读租期至人工时点10，时点9允许旧缓存只读但禁止高影响动作，时点11应用层拒绝读取。A撤销后服务端版本升至8，B仍持有物理缓存。B旧版本编辑可留存在CRDT式合并对象，候选服务端版本门拒绝其重新进入有效派生数据。设备B被标记遗失时，缺少确认，GLOBAL_ERASED保持UNVERIFIED。B重连、同步版本8并清理缓存后，历史备份仍未核验，状态BACKUPS_UNVERIFIED。

租期、版本门、只读限制和撤销优先均为本轮自拟候选政策，不能归因于Automerge实际产品。应用层拒绝读取无法远程清除旧物理副本，离线设备仍可能在其他软件中访问旧数据。

## 风险与候选控制
R1长期离线副本无法即时物理删除；R2并发合并可能恢复旧派生内容；R3租期与离线可用性冲突；R4遗失设备密钥失效不能证明内容清除；R5设备确认、备份与物理清除证据须分别记录。候选控制均UNADOPTED：来源授权版本单调递增、服务端拒绝旧写、租期及可用性成本透明、重大动作人工确认、遗失设备单列UNKNOWN、历史副本未核验时禁止声明GLOBAL_ERASED。

证据等级为官方文档加人工E1。没有真实设备、浏览器、密钥或云服务测试，没有真实敏感数据及新增费用。F008继续IN_PROGRESS。下一阶段研究实际Automerge冲突语义与可验证清除边界，若安装受限则仅审查开源文档和源码。