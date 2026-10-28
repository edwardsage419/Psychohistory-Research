# MKT097 PaOS 多智能体个人知识图谱、权限与合规证据边界

日期：2026年10月28日。性质：商业产品与市场方法研究，MARKET_E1_OFFICIAL_DOCUMENT_REVIEW。无注册、试用、真实敏感数据或付费服务。

## 与既有MKT记录去重
MKT095和MKT096研究Dcider价值权重、最高价值冲突警示与近似平局。本轮转向PaOS（Pixelitem LLC），研究多智能体协同、跨领域个人知识图谱和安全声称的证据边界；未复用前两轮Dcider发现。

## 真实产品机制及输入
PaOS官方首页 https://www.paos.app/ 声称使用11个专职AI代理：Router、Task Planner、Scheduler、Researcher、Decision Advisor、Goal Coach、Wellness Monitor、Financial Advisor、Synthesizer、Action Proposer、Knowledge Graph Builder。Router选择相关代理，Synthesizer合成建议，Action Proposer提出下一步行动。产品输入涵盖用户价值观、关系、目标、任务、里程碑、日历、Gmail、Whoop健康恢复与睡眠数据。五个视角为Business、Family、Health、Learning、Creative。个人知识图谱被描述为代理回答前参考的动态上下文，提供Obsidian导出。Goal Coach跟踪里程碑、识别阻碍并提出下一步。

官方文档支持产品设计和功能宣称；未见公开的知识图谱schema、边来源与失效规则、代理选择策略、上下文检索授权矩阵、权重更新公式、情景模拟、预测校准、真实用户效果或独立消融实验。关于反馈自我修正，仅能确认目标进度追踪与建议，无法证明代理自动纠正偏差或因果识别。所谓个人数字孪生、长期最优人生路线仍无验证。

## 安全与合规的可核对差别
PaOS首页写“HIPAA-eligible infrastructure”“SOC 2 compliant stack”“End-to-End Encryption”，具体列出Firebase Authentication、Google Cloud、API密钥Fernet加密和数据库存储令牌。Google Cloud官方HIPAA说明 https://cloud.google.com/security/compliance/hipaa/ 明确：云服务受BAA覆盖与实际应用满足HIPAA义务是不同层次，客户负责正确配置、使用受覆盖产品和实现控制；美国HHS没有HIPAA合规认证项目。PaOS使用合规能力基础设施不能自动推出PaOS本身经HIPAA合规审计。Fernet加密API密钥也不能单独证明全部用户数据端到端加密。未获得PaOS自身SOC 2 Type II审计报告、控制范围、BAA适用证据、令牌授权撤销测试、隐私保留期或图谱导出恢复测试。以上为证据缺口，不能据此断定产品不安全或违规。

## 费用、部署与适配
官方早期计划声称前三个月免费、无需信用卡，之后每月USD19；长期零新增费用条件下，不能将试用视为可持续免费基础设施。本轮没有注册。PaOS是云端代理产品，自部署和开源许可没有得到官方证据支持。个人知识图谱、多视角目标跟踪和代理建议可作为未来理论研究比较对象；项目不接入真实Gmail、健康数据或个人关系网络，不提前开发个人决策产品。

## 证据等级和候选检验
官方首页功能、价格及安全用词为MARKET E1文档事实；Google Cloud HIPAA为官方标准解释；产品实际数据流、合规状态、算法与效果均UNKNOWN。后续候选：使用人工合成图谱测试跨视角访问最小化、来源撤销后的记忆失效、代理只读与可执行权限隔离、Obsidian导出可恢复性、用户对价值冲突的最终否决权。所有候选尚未采纳。

来源： https://www.paos.app/ ; https://cloud.google.com/security/compliance/hipaa/ ; https://docs.cloud.google.com/docs/security/compliance/hipaa
