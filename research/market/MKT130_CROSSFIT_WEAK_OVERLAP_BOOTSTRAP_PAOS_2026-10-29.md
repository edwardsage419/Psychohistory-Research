# MKT130 交叉拟合、弱重叠与自助法区间的精确人工反例；PaOS产品机制审查

日期：2026-10-29 UTC。目标键：(market,MKT130,none,crossfit-weak-overlap-bootstrap-PaOS)。状态：COMPLETE_BOUNDED_E1。先读取main、MKT129、E098、F008第十四阶段和市场轨交接，避免与既有SNIPW/DR错设实验重复。此轮研究新的同样本干扰和区间覆盖率问题。

## 方法和已运行结果

归档程序：`research/market/mkt130_crossfit_weak_overlap_exact_20261029.py`。Python 3.13.5 标准库 Fraction，2026-10-29 UTC本地原样执行exit 0，程序内所有assert通过，6个无效输入被拒绝。代码Git blob由本轮回读验证。无随机抽样、无真实用户、无OBP包运行。

人工生成：8个彼此独立且具有唯一ID的记录，行动A=1的历史选择概率p=1/20，A=0概率19/20；目标策略永远选择A=1。设Y(1)=1，Y(0)=0，因此目标真实价值1。共九种充分统计量K=0..8，概率为Binomial(8,1/20)，对其做精确有理数全分布积分。已知且正确的行动倾向p用于IPW/DR。

刻意过拟合的同样本奖励模型：如果同一ID的罕见行动A=1及Y=1出现在训练集，则记住该ID的奖励为1；未见过的ID默认奖励0。直接使用训练本行计算DR时，每行贡献A，期望1/20，方差19/3200。以独立ID作为留出折，所有留出ID的奖励模型输出0，交叉拟合DR贡献A/p，期望1，方差19/8。这是针对同样本记忆泄漏的构造反例，交叉拟合修复此处的偏差，同时暴露罕见行动下的高方差。它不构成所有交叉拟合估计器无偏的普遍定理。

普通按行有放回bootstrap：给定K，重采样8次，重采样罕见行动数K*服从Binomial(8,K/8)，以累计分布达到2.5%与97.5%的最小整数作为百分位数端点。对估计量20K*/8生成名义95%区间。若原样本K=0，bootstrap区间严格为[0,0]，无法覆盖真实目标1。P(K=0)=(19/20)^8=16983563041/25600000000≈66.342%。精确枚举全部九种K及其条件bootstrap分布，只有K=1或2时覆盖真值，因此名义95%区间的真实无条件覆盖率423412929/1280000000≈33.079%。本例的百分位定义、已知p、固定n和固定奖励生成机制均在代码中明示。没有模拟抽样误差。

## 解释和适用边界

交叉拟合可以隔离同一训练记录导致的奖励模型记忆污染。若行动覆盖极弱，交叉拟合后的正确IPW/DR仍有很大方差，单次样本可能完全缺少目标行动。仅在观测样本上重采样的百分位bootstrap不能凭空恢复未观察行动的质量。此反例说明需要报告最小行动倾向、有效样本量、K=0频率、区间方法与实际覆盖诊断。未来个人决策研究需独立区分可预测行动价值、不可识别反事实、弃权与现实验证。

来源：Newey & Robins (2017) 交叉拟合方法 https://ifs.org.uk/publications/cross-fitting-and-fast-remainder-rates-semiparametric-estimation ；Su et al. (2020) DR权重收缩 https://proceedings.mlr.press/v119/su20a.html ；Dorn (2025) 弱重叠条件与置信区间 https://arxiv.org/abs/2504.13273 。论文提供方法背景，本文特定数值是本轮独立人工精确计算。未把论文的一般理论归因于此特定人工世界。

## 产品主线：PaOS的知识图谱与多智能体反馈

官方 https://www.paos.app/ 及其2026-01-02博客 https://www.paos.app/blog/from-task-managers-to-agent-operating-systems ：PaOS自述11个专职AI代理，Router选择专家，Synthesizer汇总建议，Action Proposer提出需用户点击批准的行动。知识图谱连接个人价值、目标、关系和历史对话；Google Calendar、Gmail、Whoop提供时间、邮件、睡眠/恢复/负荷等输入；五种人生视角为Business、Family、Health、Learning、Creative。其Goal Coach按里程碑、任务完成、阻塞和目标冲突给出调整建议，参考官方 https://www.paos.app/blog/ai-goal-tracking-accountability 。

状态表达：知识图谱、目标/里程碑、日历事件、任务、跨视角标签。目标：根据用户表述的价值给出多代理建议。反馈：任务完成、日程、Whoop和目标进展。算法：公开页面描述Router/Synthesizer流程，未公开训练目标、图谱模式、价值权重学习、因果模型、置信区间、预测校准和真实评估协议。解释性：有可读建议，尚无证据支持可复算的贡献分解。权限：官方宣称Firebase身份验证、API密钥Fernet加密、Google Cloud HIPAA-eligible、SOC2 compliant stack和Obsidian导出；这些属于厂商声明，未见本轮独立审计报告或可复算撤销、删除、离线密钥验证。基础设施符合某合规框架的资格，不等同于整款产品已独立通过该框架审计。

收费：官网在2026-10-29查询时显示早期参与者前三个月免费、随后19美元/月，宣称无需信用卡；促销和未来价格可能变化。零费用约束下未注册、未绑定邮箱/健康数据、未购买。官方2026-01-10 Wellness文章 https://www.paos.app/blog/work-life-balance-ai-wellness-monitor 报告早期用户35%较少连续高负荷周等数字，缺样本量、分配、基线、可核验统计及独立对照，归类为MARKETING_CLAIM，不能作为行为改善的E2/E3科学证据。

## 证据与后续

MARKET E1人工程序与有理数断言已实跑；产品官方文档支持功能宣称与收费页面显示；独立真实用户效应NOT_VERIFIED；OBP软件NOT_RUN；新增真人E2=0、独立新总体E3=0。个人决策产品开发继续暂缓。候选知识储备：先检验分组交叉拟合、正值支持、区间覆盖与拒答；不固定人生效用权重。

下一项MKT131：以人工群组相关结构检验按行bootstrap与按群组bootstrap的覆盖差异，事前固定样本生成和评价方法，避免重用本轮结果选择阈值。
