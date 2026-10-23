# R285 科学报告：离散有限假设族的Holm家族误报和Benjamini–Hochberg错误发现率

日期2026-10-23 Asia/Taipei。原239模型目录**12-015 Multiple Testing Correction（P1）**，本目录最后候选项。原始理论来源：Holm (1979), *A Simple Sequentially Rejective Multiple Test Procedure*, Scandinavian Journal of Statistics 6(2):65–70；Benjamini & Hochberg (1995), *Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing*, JRSS B 57(1):289–300，DOI https://doi.org/10.1111/j.2517-6161.1995.tb02031.x 。

## 事前冻结与人工设计
[独立冻结协议](../../protocols/R285_TWO_HYPOTHESIS_HOLM_BH_2304_COMPLETE_SOURCE_PRESCORE_FREEZE_2026-10-23.md)的GitHub先行commit[923b083c](https://github.com/edwardsage419/Psychohistory-Research/commit/923b083cc61cbafdd339136fe9b5c407cffb88bf)。两个独立检验H1/H2，各四次有序Bernoulli测试bit，合计8bit原source全部2^8=256种，三个真实人工世界BOTH_NULL(p1=p2=1/2)、ONE_SIGNAL(p1=3/4,p2=1/2)、BOTH_SIGNAL(p1=p2=3/4)。三个冻结决策方法RAW_UNADJUSTED、HOLM_FWER、BH_FDR，共3×3=9个world、**2304种带world/policy标签完整原source**，同真p政策间共用原八bit空间，不是2304次独立真人实验。

每个检验根据K=0..4和真实原假设Binomial(4,1/2)计算单侧精确p-value，依次是1,15/16,11/16,5/16,1/16。家族阈值冻结α=1/2，选择这么高的**非真实研究惯用**阈值仅为产生离散小样本中Holm与BH实质不同的拒绝案例，不应作为现实研究推荐。原source完整保存两个K、p-value、policy、拒绝H1/H2、R总拒绝、V错误拒绝、S真实发现、FDP=V/max(R,1)及FWER事件1[V>0]，真实来源质量精确Fraction。

## 理论指标及九world精确风险
FWER=P(V≥1)，FDR=E[V/max(R,1)]，两者不是同一个误报指标。真全部原假设时所有拒绝均假，FDR=FWER。真两假设都非零时没有真原假设可被错拒，故FWER=FDR=0，但仍可比较期望真实发现数。

|真实world|政策|FWER|FDR|E[V]|E[S]|E[R]|
|---|---|---:|---:|---:|---:|---:|
|BOTH_NULL|RAW_UNADJUSTED|135/256|135/256|5/8|0|5/8|
|BOTH_NULL|HOLM_FWER|31/256|31/256|5/32|0|5/32|
|BOTH_NULL|BH_FDR|47/256|47/256|9/32|0|9/32|
|ONE_SIGNAL|RAW_UNADJUSTED|5/16|1615/8192|5/16|189/256|269/256|
|ONE_SIGNAL|HOLM_FWER|145/1024|647/8192|145/1024|351/1024|31/64|
|ONE_SIGNAL|BH_FDR|253/1024|1079/8192|253/1024|459/1024|89/128|
|BOTH_SIGNAL|RAW_UNADJUSTED|0|0|0|189/128|189/128|
|BOTH_SIGNAL|HOLM_FWER|0|0|0|7371/8192|7371/8192|
|BOTH_SIGNAL|BH_FDR|0|0|0|10287/8192|10287/8192|

Holm按升序首次p必须≤α/2才能有任何拒绝，后续阈值α；BH按升序找最大秩r使p_(r)≤rα/2，可拒绝前r项。因此当两检验都给p=5/16，RAW拒两项、HOLM拒零、BH因第二秩p=5/16≤α=1/2而拒两项。这种差异是**特定离散人工源的可复验反例**，不能扩张为所有信号率下BH在错报和功效上必优于Holm的经验规律。

路线A全枚举2304原八bit来源，逐结果按预定规则评分，以精确source概率加权计算九组FWER、FDR、E[V]、E[S]、E[R]。
路线B不调用原source生成，使用两个K各独立Binomial(4,p_i)的5×5=25类别，独立重算三决策策略及九组完整理论分数，逐Fraction一致。
路线C GitHub Actions第三作业不导入模型程序，直接重读CSV全部2304原source，逐源重建两个null精确p值、Holm与BH排序、家族错误和FDP，独立分析25类别并核对原CSV/JSON SHA256。

## 真实CI及科研证据边界
[完整标准库执行器](r285_exact_multiple_testing.py) · [2304个原来源CSV](R285_ALL_2304_ORIGINAL_MULTIPLE_TESTING_SOURCES.csv) · [九world完整多重比较风险JSON](R285_EXACT_RESULTS.json) · [哈希机器凭证](R285_MACHINE_RECEIPT.json)。
[GitHub Actions run39906881178](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39906881178)三个job全部completed/success，Python3.11和3.12各80项真实单测（共160项）通过，第三独立来源审计及完整原CSV/JSON/SHA机器永久main归档成功。[完整原source archive commit41643378](https://github.com/edwardsage419/Psychohistory-Research/commit/41643378604f670fc72234ab608965422c2f4e60)。

原CSV SHA256 `5fd07eb5437fc5e6c46fc8316b9389a83b08676dd41c39d1daee3335ca46aa93`；结果JSON SHA256 `c9997960a0bb5be83ec46d66381b8fa1e00387da41e46e3e50d52943b74d5e45`。

全部只有E1人工数学；新增真人E2=0、真实历史E3=0，R073/PESEN v0.1继续冻结。R285已是原239候选目录最后一项，但**不能因此自动推定此前原R研究全部通过统一科学验收**。下一步应逐原目录审计归档、冻结、科学报告、来源完整性及E1/E2/E3，再依据用户决定判断是否可以统一归纳分类，最后熔炼。
