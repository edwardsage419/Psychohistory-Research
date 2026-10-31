# TH185 ICPSR37070公开元数据、复算代码来源与数据使用许可边界

研究日与英文来源检索日：2026-11-01（Asia/Singapore）。目标键：(theory,Paluck2016+ICPSR37070v2+ICPSR_LLM_POLICY,method-theory-v1,release_crosswalk_design_licensing)。状态：THEORY_NOTE_BOUNDED; RAW_DATA_ACCESS_BLOCKED_BY_POLICY; REPLICATION_CODE_ACCESS_UNVERIFIED。非盲态：已阅读本仓库TH182至TH184、C009、D002与索引，已知2018正式更正和49校缺失。理论轨只读来源与公共书目，不执行R轨真实数据复算。

## 1. 原始来源、阅读范围与证据等级

1. [A，公开研究元数据，已读Methodology、Study Design、Sample、Version History、Notes] Paluck EL, Shepherd HR, Aronow P (2020). *Changing Climates of Conflict: A Social Network Experiment in 56 Schools, New Jersey, 2012-2013*, ICPSR37070 V2，2020-09-14，DOI:10.3886/ICPSR37070.v2。https://www.icpsr.umich.edu/web/ICPSR/studies/37070/ 。研究说明56校四校一块、28校处理，先选15%学生的seed-eligible池（按性别和年级分层，最多64人），再从池中随机邀请约一半；49校有行政记录。发布页称24471 cases与482 variables，V2增补17个此前未公开字段。仅引用公开研究级元数据，未读取ICPSR分发的原始数据、代码本或下载包。
2. [A，ICPSR官方政策全文，已读] ICPSR (2025-01-20网页，2024-12-11批准). *Can I Use Large Language Models and Other AI with ICPSR Data?* https://www.icpsr.umich.edu/sites/ICPSR/news/can-i-use-large-language-models-and-other-ai-such-as-chatgpt-google-gemini-etc-with-icpsr-data 。政策明确区分公开研究级元数据与研究数据：前者可引用并署名，后者不得在未获适当许可的条件下提供给可能保留数据的LLM。研究级元数据采用CC BY-NC 3.0 US。
3. [A，ICPSR官方再分发政策全文，已读] ICPSR (网页核验2026-11-01). *Redistribution Policy*. https://www.icpsr.umich.edu/sites/icpsr/about/policies/redistribution 。要求数据再分发事前获书面许可，并明确LLM数据输入的限制。https://www.icpsr.umich.edu/sites/icpsr/about/policies/terms-of-use 同时规定不得尝试识别研究对象。
4. [A，作者机构公开论文记录，已读Related Data] Yale ISPS (2016). Paluck, Shepherd, Aronow原始PNAS论文条目，DOI:10.1073/pnas.1514483113。https://isps.yale.edu/resource/changing-climates-of-conflict-a-social-network-experiment-in-56-schools 。明确指向作者复算代码Dataverse DOI:10.7910/DVN/29199，并指出另有Princeton存档数据需要申请且受IRB同意约束。代码存档入口尝试访问遭遇Javascript/机器人验证，文件清单、许可及与2018更正的版本对应尚未核验。
5. [A，正式原刊与更正，已读原刊Methods/Data Availability和2018更正，沿用TH184阅读记录] Paluck et al. (2016), PNAS 113:566-571, DOI:10.1073/pnas.1514483113；Paluck et al. (2018), PNAS 115:E3598, DOI:10.1073/pnas.1804429115。原刊30%与2018更正25%、总体不显著的冲突保留，未声称复算。
6. [B，方法原刊作者机构摘要，已读] Aronow PM, Samii C (2017). *Estimating average causal effects under general interference*, Annals of Applied Statistics 11:1912-1947, DOI:10.1214/16-AOAS1005。https://isps.yale.edu/resource/estimating-average-causal-effects-under-general-interference-with-application-to-a-social 。随机化分配机制、暴露映射与估计目标必须同时声明。未在本轮重读整篇论文。

## 2. 新增条件命题与竞争解释

TH185-01 [公开事实] 论文24191名学生与ICPSR发布页24471 cases相差280。case是否一人一行、增量来自补录或处理均未确认，禁止将280直接判定为重复学生。
TH185-02 [公开事实及待核] 发布摘要称482变量，网页检索片段显示变量列表共499条，差17；V2确实新增17字段。482+17=499仅为一致性线索，无法确定搜索索引计数、变量实际版本或重复项；变量列表动态页本轮访问返回错误，状态UNVERIFIED。
TH185-03 [公开事实] V2增加的17个字段为第二波调查条目，发布说明还提到标准化缺失值、重编码及保密处理。新增字段的实际时间、变量编码与分析用途仍须核验；不能自动用于2016年原刊的基线调整。
TH185-04 [设计事实] 56校在四校分块内随机分配；仅有28/56总数无法恢复每块处理数量。若每块2/4，支持集6^14只是条件性值。
TH185-05 [设计事实] 校级随机、校内种子池筛选与邀请、网络暴露构成多级机制。不能以独立Bernoulli学生处理概率代替固定规模抽样及分层规则。
TH185-06 [人工反例] 4名合格学生固定选2名，某学生认识其中2名，至少一人被选概率5/6；错误的两个独立1/2抽签得到3/4。校级1/2随机后，无条件暴露概率5/12（假设校级与种子抽样独立）。
TH185-07 [方法] 原始学校标识、四校分块ID、分块内处理数量、校级随机标签、合格池、种子邀请标签、社会参照者、网络邻接、行政记录是否可得、结果时间窗及2016/2018分析规格应构成最小映射清单。这些是**候选字段角色**，不是声称已在公开数据中找到的实际变量名。
TH185-08 [方法] 研究级公开可访问性不等于研究数据可向LLM输入或可重新发布。依ICPSR官方政策，现有自动化不下载、不上传、不再分发其数据与代码本；必要时另行取得书面许可或选择许可明确的独立公开来源。
TH185-09 [方法] Yale明确指向Dataverse代码DOI；链接存在不代表本轮已成功下载或核对代码版本。2016原始代码与2018更正代码的差异仍UNKNOWN。
TH185-10 [人工部分识别] 23/28处理校、26/28对照校行政结果可用。假设校级结果被限制在[0,1]且各校等权，缺失学校的任意值使处理减对照均值差的可行区间宽7/28=25个百分点。真实行政纪律事件可重复计数，不能直接使用此界。
TH185-11 [人工反例] 观察处理均值2/5、对照均值1/2时，完整56校差界为[-29/140,3/70]，跨越零。两均值均为人工设定，未读取真实学校结果。
TH185-12 [竞争解释] 学校随机化提高校级干预意向效应识别，但行政数据缺失、记录行为改变、网络干扰和样本进入仍可导致不同估计目标。个人网络传播与学校总体结果应分别估计。
TH185-13 [方法] 数据加工前后应保存每个字段的角色、单位、版本、缺失代码、波次、处理前后属性和派生方式；只凭变量名相同不能证明测量等值。
TH185-14 [方法] 同一学校中种子处理的边际概率与任意同伴暴露概率不同，且正概率由真实抽样支持集决定；把可观测同伴的所有暴露状态视为可达会导致非法逆概率权重。
TH185-15 [伦理] 数据涉及未成年人及关系网络。任何未来实证复算须遵守原始同意、去识别、研究用途、存储及再分发限制，不能尝试重识别或个体画像。
TH185-16 [证据边界] 本轮数学检查仅是标准库合成设计审计。无法回答真实分块标签、2018显著性变化来源、校级失访原因或历史外推效果。

## 3. 数学审计及验证清单

归档脚本 `th185_public_metadata_design_audit.py` 完全独立于ICPSR文件，使用Fraction与itertools。20项unittest在Python普通和优化模式均通过。包括24191与24471的280差、482+17的候选算术、14块条件组合、7校缺失、固定规模抽样的5/6暴露率、两阶段5/12暴露率，以及人工二元校级结果差的区间宽1/4。算术相等不证明任何元数据来源差异的原因。

未来验证顺序：第一，取得ICPSR对LLM处理和文档使用的书面许可，或在完全独立、合规环境人工审阅且不向本系统传输受限内容；第二，恢复代码档案的文件清单、版本、许可证、依赖和2018更正对应；第三，由R/实证轨在许可允许的独立环境进行真实分块ID与分析样本映射；第四，预先固定学校级ITT与网络暴露两个估计目标，再分析失访敏感性与更正后方差。未经这些步骤不得报告真实数据复算成功。

## 4. 四层联系与当前协作

个体层：学生规范感知、调查响应及种子邀请。群体层：同伴连接、种子暴露与学校内干扰。制度层：学校行政报告、四校随机分块、研究许可及数据加工。历史层：2012至2013实验、2016论文、2018更正、2019至2020数据发布版本。跨层机制仍是候选解释，不构成历史预测。

C今日2026-11-01已有C009，保持只读；D本周2026-W44已有D002，保持只读。R轨最新观察为R320 S116交接，独立研究主线保持优先。开放Codex PR #1至#12均视为待审，尤其#1的R257 S53缺口与#3候选修复未并入main。E1/E2/E3无新增科学验收。未触发CI、付费服务、敏感数据读取或个人决策产品开发。

下一TH186：公开许可明确的独立学校网络干扰方法材料，重点比较固定规模种子分配、分块校级随机和网络暴露正概率；保留ICPSR数据访问许可阻塞。
