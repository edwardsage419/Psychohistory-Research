# Hardin 1968 公共资源与多目标极值断言：原著限定审查
track: theory
run_date: 2026-11-17 (Asia/Singapore)
observed_main_head: 7539dd3302ee5a2765b9c6afda3f5cf960394135
target_key: (theory,Hardin-1968,DOI:10.1126/science.162.3859.1243,simultaneous-maxima-and-commons-governance-boundary)
status: PARTIAL; PRIMARY_AUTHOR_TRANSCRIPTION; CONSTRUCTIVE_LOGICAL_COUNTEREXAMPLE; NO_HISTORICAL_CAUSAL_VALIDATION

## 原著身份及实际阅读
Garrett Hardin (1968), “The Tragedy of the Commons,” Science 162(3859):1243–1248, DOI https://doi.org/10.1126/science.162.3859.1243 。直接阅读Garrett Hardin Society署名全文转录 https://www.garretthardinsociety.org/articles/art_tragedy_of_the_commons.html ，具体为 “What Shall We Maximize?”, “Tragedy of Freedom in a Commons”, “Pollution”, “How To Legislate Temperance?”, “Mutual Coercion Mutually Agreed Upon” 段落；另核对Science出版者元数据及摘要。转录非出版社排版页影像，页内精确行号与原刊逐页核对尚未完成。文章其他人口政策与心理断言仅初步浏览，未做逐项证据审查。

## 可核原著命题及必要限定
1. 作者在“What Shall We Maximize?”断言两个或更多变量不可能同时最大化。这一无条件数学表述过强。取定义域x∈[0,1]，f(x)=x，g(x)=x²，则二者均在x=1达到各自全局最大值。若f(x)=x且g(x)=1−x，则二者无法在同一x同时最大化。是否可同时最大化由目标函数与可行集决定；目标冲突、帕累托权衡和社会权重的规范性选择必须分别处理。两个例子为本轮构造性逻辑反例，不是原作者公式、真实人口数据或真人验证。若作者意指一般不存在保证所有目标共同极大的定理，应收窄措辞，不能将其解释为任意双目标都绝不可能同时最大。
2. “Tragedy of Freedom in a Commons”采用无约束开放牧场、个人获取新增牲畜的私有收益与放牧损害分摊的思想实验。其结论有开放进入、私人边际收益、损害外部化、缺乏有效约束等条件；原文牧场例子不是随机化田野试验，也不证明所有共同产权治理必然失败。
3. “Pollution”将资源提取型公地与排放污染型公地分开，指出私人产权对某些资源提取的约束未必解决跨界排污。此点禁止把作者立场简化为“私有化可解决一切公地问题”。
4. “Mutual Coercion Mutually Agreed Upon”明确讨论税收、停车收费、共同同意的强制规则，包含治理机制的条件性设计。其人口政策主张属于规范性政治判断，不能由牧场模型或双目标数学论证直接推出。
5. 竞争机制：Ostrom (2009), Science 325:419–422, DOI https://doi.org/10.1126/science.1172133 ，在资源系统、使用者、治理规则和监测条件的交互框架下提出有条件自组织；已见仓库 theory/OSTROM_2009_SES_SELF_ORGANIZATION_NONMONOTONIC_BOUNDARIES_2026-11-16.md。两者对开放进入与有效治理边界的设定不同，单一资源耗竭历史结果无法排他识别个人动机或治理失败原因。

## 测量、识别与研究状态
候选可观测量：资源再生率、实际进入和退出规则、监测可见性、违规成本、边际私人收益、共享损害、使用者人数、群体组织与规则执行记录。要检验Hardin型机制，必须先验证开放进入和外部化条件，控制生态资源变化及选择进入；观察资源枯竭本身不足以确定机制。C个人多目标测量可借鉴目标共同最优的可行集检查，但仓库已有C004动态多目标主题，本轮不制造C编号，也不赋予任何个人目标权重。D005第47周迁移专题已存在，本轮不制造D编号。

证据等级：原著署名转录的直接文本阅读、出版社书目信息、构造性数学反例；无原刊影像逐页校勘、原作者实证复算、历史因果识别或R科学验收。TH新编号0，R关闭条件0。R073/PESEN v0.1冻结，R E1/E2/E3/MARKET不升级。Tests: NOT_RUN（逻辑反例可手工核查）；CI: NOT_RUN；费用账单NOT_VERIFIED，未调用付费资源。

下一步：核对Science原刊排版中“maximize for two (or more) variables”准确上下文与von Neumann/Morgenstern引用；检索Ostrom 2009支持材料及相关原始田野数据，审查制度规则的操作化；C当日合格成果另行核实。


## 2026-11-17 原著独立补读：Conscience Is Self-Eliminating（署名转录）
来源同上，实际读取 Garrett Hardin Society 英文转录 “Conscience Is Self-Eliminating” 全节及 “Pathogenic Effects of Conscience” 前三段，另读取 “Mutual Coercion Mutually Agreed Upon” 关于社会安排的段落。原刊逐页校勘仍未完成。任务键：(theory,Hardin-1968,author-transcription-2005,conscience-selection-versus-horizontal-transmission)。

原文提出：若节制繁殖的倾向可遗传且较少生育，则仅依赖良心劝说的群体，节制倾向可能在代际选择中下降。原文特别承认传递可通过生殖细胞或文化途径（exosomatic）。这一论证依赖传递与繁殖差异持续存在，不能直接当作历史人口规律或任何特定群体的事实。

独立构造性反例：令 p_t 为第 t 代具有节制规范的比例，具有规范与不具有规范者的预期子代数分别为 f_C 与 f_N，且 f_C<f_N。若完全垂直继承且无突变，则 p_(t+1)=p_t f_C/[p_t f_C+(1-p_t)f_N]，当0<p_t<1时比例下降。若下一代经普遍制度教育、水平学习以概率1采用该规范，则 p_(t+1)=1，尽管 f_C<f_N。更一般地，先经垂直选择得 q_t，再以独立概率 h 将未采用者转化，则 p_(t+1)=q_t+h(1-q_t)。当 h>0 且 q_t<1 时，文化传播可以抵消部分选择；是否持续下降取决于 h、两组生育率及代际机制。此为数学构造，非原作者原式、非人口历史验证。

竞争解释：生育差异的文化/经济共同原因、代际价值转变、制度教育、迁移、选择性参与及测量误差，均可产生类似的规范比例轨迹。候选可观测量：分组生育率、代际规范测量、父母子女配对、同伴传播、教育政策与人口迁移。若无跨代配对及传播机制测量，单看群体规范下降无法识别遗传选择。尤其不能由此支持强制性人口政策；原文规范主张需要独立的伦理与人权评估。

证据级别：作者署名转录直接文本、独立代数反例；没有原刊影像核对、纵向人口实证、因果识别或R验收。新TH编号0；C当日与D本周验收仍待核实；CI NOT_RUN，未触发收费资源。下一步优先查文化传递经典原著中垂直、水平与斜向传播的定量条件，避免继续停留在Hardin单文献。
