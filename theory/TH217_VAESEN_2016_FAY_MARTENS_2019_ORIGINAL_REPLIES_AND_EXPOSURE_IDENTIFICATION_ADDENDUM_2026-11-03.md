# TH217补记：2016考古解释争论与2019文化学习实验的原作者往返答辩

track: theory
subflow: main
run_date: 2026-11-03 (Asia/Singapore)
observed_head: 0e57611c3766df64b2ee703cf47e75e052888b55
target_key: (theory,Vaesen2016-reply+Martens2019-letter+FayEtAl2019-reply,2016-published-author-PDF+2019-published-originals,archaeological-extrapolation-vs-filtering-and-exposure-identifiability)
status: PRIMARY_REPLIES_FULLTEXT_COMPLETE_BOUNDED; CONSTRUCTIVE_IDENTIFICATION_COMPLETE; EMPIRICAL_REESTIMATION_NOT_RUN
source_access_date: 2026-11-03
CI: NOT_RUN
billing: new_paid_operations=0; account_and_free_quota=NOT_VERIFIED

## 一、原始材料及实际阅读范围

[A] Krist Vaesen, Mark Collard, Richard Cosgrove, Wil Roebroeks (2016), *Reply to Henrich et al.: The Tasmanian effect and other red herrings*, *PNAS* 113(44):E6726至E6727, DOI 10.1073/pnas.1613074113。**直接阅读作者本人大学网站保存的正式原刊排版PDF两页全文**（作者站点PDF内部标为Early Edition pp1至2，后续刊页为E6726至E6727）。https://kvaesen.ieis.tue.nl/PNAS_ReplytoHenrich_online.pdf 。此处是2016年Vaesen等对Henrich等的独立原始回应，补齐TH217原笔记的明确未读项。未逐一读取回应所引用的十篇考古底层论文。

[B] Jason P. Martens (2019), *Scenarios where increased population size can enhance cumulative cultural evolution are likely common*, *PNAS* 116(35):17160, DOI 10.1073/pnas.1910949116。直接阅读PMC正式原刊全文一页。https://pmc.ncbi.nlm.nih.gov/articles/PMC6717298/ 。原文指出实验强制学习者查看指定数量示范者，主动筛选、声望、注意线索等常见文化学习机制被排除，外推至一般文化传播需审慎。

[C] Nicolas Fay, Naomi De Kleine, Bradley Walker, Christine A. Caldwell (2019), *Reply to Martens: Various factors may enable large populations to enhance cumulative cultural evolution, but more evidence is needed*, *PNAS* 116(35):17161至17162, DOI 10.1073/pnas.1911176116。直接阅读斯特灵大学保存的**正式原刊排版PDF两页全文**。https://dspace.stir.ac.uk/bitstream/1893/30143/1/17161.full.pdf 。作者承认声望筛选为合理假说，另提出双人网络筛选、书写等外部认知辅助，明确要求进一步实验检验，避免把该实验解释为普遍的规模负效应。

[D] Fay等(2019), *Increasing population size can inhibit cumulative cultural evolution*, *PNAS* 116(14):6726至6731, DOI 10.1073/pnas.1811413116。此次重新直接阅读正式原刊PDF pp6726至6730的实验设计、Results、Discussion、Methods及图注，确认pp6730的暴露时长；pp6731仅核引文。https://www.pnas.org/content/pnas/116/14/6726.full.pdf 。作者披露数据与R脚本在OSF https://osf.io/486wy ，本轮未读取SI、未下载数据、未运行作者脚本。

## 二、新增竞争解释与更精确的外推边界

1. **2016年争论的实际目标。** Vaesen等在E6726指出，他们批评的是把特定人口规模模型直接用于解释**考古记录中的猎采者物质文化变化**。他们明确承认人口规模可能在某些文化演化情形中有作用。其要求逐一核对考古案例与模型的示范者选择、传递保真度、选择压力等前提，并指出跨领域的语言复杂性、专利例证不能直接裁定猎采者器物记录。这是对TH217中“人口规模理论普遍有效或普遍无效”二分叙述的限定。双方对考古保存偏差、复杂性测量、有效文化人口规模仍有争论，不能单凭答辩裁定历史因果。
2. **2019年双方共同确认的边界。** Martens认为声望等模型选择偏差可降低逐一处理全部示范者的记忆负担；Fay等答辩承认这种机制合理，同时提出网络双人互动和外部记忆工具等替代过滤机制。原实验把过滤机会固定为受限，无法从其结果决定哪种过滤机制在现实中占主导。声望也可能指向高地位但低技能者，因此“声望筛选必然提高文化性能”仍是待证假说。
3. **原实验处理包的关键测量细节。** Fay等正式原刊p6730 Methods说明1、2、4示范者条件中每件纸飞机的观看时间固定1.5分钟，总观看时间分别为1.5、3、6分钟；各条件制作时间均5分钟。每代可见示范者数量N、实际接触件数F、总观看时长T在这些条件下满足F=N、T=1.5F。参与者随机分配条件可以识别该实验条件包的因果对比，但在缺乏正交操作时，不能独立估计固定F或T下仅改变N的效应。固定单件观看时长解决了“每件观看时间随规模缩短”的旧设计问题，尚未隔离总信息负荷、总观看时间及模型池规模。
4. **原实验的其他测量边界。** p6728报告飞机相似性有第二评分者子集，评分者间相关约0.59，不能将飞机相似性视为无误复制保真度。p6729指出飞机折叠复杂度与工作记忆负担均可能解释保真度下降。p6730 Methods中个人学习同一人跨8代反复制作，社会学习每人仅参与1代，比较时保留练习机会不等价。

## 三、构造性不可识别反例与可证伪实验条件

设N为候选示范者池规模，F为实际接触的示范者数量，Y为可取正负的标准化文化性能变化。构造两个纯人工世界：

世界A：Y_A(N,F)=N/(N+1)−F/5。
世界B：Y_B(N,F)=F/(F+1)−N/5。

当F=N，N∈{1,2,4}时，两世界的全部可观测结果相同，依次为3/10、4/15、0。固定F=2，将N从1增至4，世界A的变化为+3/10，世界B为−3/5，方向相反。因此，即使实验条件间存在稳定的随机分配差异，也不能只用F=N的对角观测区分“更大候选池的收益”和“更多信息暴露的负担”各自的因果贡献。

Python标准库Fraction执行7项精确断言，7/7 PASS：三个对角点相等、两种固定F下相反的方向、1.5分钟乘2与乘4的时长算术。人工函数仅证明指定设计下的逻辑不可识别性，**不是**作者模型、实际数据拟合、真实人类行为或历史预测。

后续候选实验需要正交操作N（可选候选池）、F（实际接触件数）、过滤许可和总观看时间，分别记录选中示范者的真实性能、记忆负荷、作品复制相似性、后代实际表现及网络接触结构。可证伪假说：在F与总观看时间固定时，若仅增大N仍提高长期表现，说明候选池的额外价值可能存在；若过滤许可改变效果方向，需报告N×过滤条件的交互与链级不确定性。当前只是方法储备，未开展实验。

## 四、证据范围、覆盖与登记

新增的是两场争论的**三份独立原始答辩全文**及原实验pp6730方法细节，继续沿用TH217。覆盖考古推论的模型适用性、文化学习筛选机制、双人网络和外部认知工具。未执行原始543名参与者数据复算、考古记录再分析、正式勘误查询穷尽、独立因果实验或R轨预测。来源文字的作者立场与本轮构造性反例分开存档。

C011: COMPLETE，2026-11-03，原有日记回忆测量研究已读核；本轮无新C编号。
D003: COMPLETE，2026-W45，实际2026-11-02，人口转型与代际财富流向专题已读核；本轮无新D编号。
R: 最近main含R127原始表审计；R073与PESEN v0.1冻结，E1/E2/E3与MARKET证据等级不因本理论补记改变。12个开放Codex PR未经合并，不计入main成果。
CI: NOT_RUN；新增收费操作0；GitHub额度和账户账单NOT_VERIFIED。

next: 在后续轮次转向其他弱覆盖学科；TH217后续只保留2004正式勘误、Fay2019 SI与OSF源版本的定向核查。不得以连续微专题新增TH编号；全部R系列完成后才统一分类和有条件模型熔炼。
