# 心理史学：原239目录三个P0待核条目的成员级历史取证、R286补缺及目录映射v0.2

日期2026-10-23 Asia/Taipei。科研性质：历史原始研究包**真实字节/成员检验**，加上一项新独立TD(0)人工数学研究；不是所有239项的科学结题。

## 一、74份原始ZIP确实再次独立读字节

[扫描前固定取证规则](../protocols/ORIGINAL_239_P0_EARLY_74_ZIP_MEMBER_AUDIT_INPUT_AND_KEYWORD_FREEZE_2026-10-23.md)，独立先行提交[fc4bd241](https://github.com/edwardsage419/Psychohistory-Research/commit/fc4bd2414fc0b1cdf83a8ff71bdf488c713f6ac6)。随后实际读取先前Library恢复的**74份ZIP原始二进制**，逐个与清单SHA256、Git blob SHA1、压缩文件长度、member数、解压总字节数以及Python `zipfile.testzip()` CRC逐一对照，全PASS。共重新枚举**840份ZIP文件成员**，其中**799份**符合扩展名、大小及解码限制而全文检索，另**39份**为非目标文本格式/二进制成员、**2份**为超出本轮1MiB单文本成员检索限额，不能声称所有内容全文都查过。

[全部74原ZIP逐成员检索报告及有限文本线索](ORIGINAL_239_P0_EARLY_74_ZIP_CONTENT_SCAN_RESULTS.json) · [ZIP/扫描JSON SHA256机读凭证](ORIGINAL_239_P0_EARLY_ZIP_SCAN_SHA256_RECEIPT.json) · [实际扫描执行程序](../research/catalogue_audit/scan_early_zip_P0_2026_10_23.py)。采用**事前强线索/相关词典**，最多存一条原旧文字极短上下文：实际命中可扫描文本成员总79份（同一成员可能匹配多个模型），其中01-008有12份成员含任一检索词、8份含强线索；02-002是16/9，04-001是71/14。主要重复源为旧目录本身及历史知识包快照，**匹配数不是独立论文数或已复算模型数**。

[GitHub Actions run39908965330](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39908965330)三作业已全部completed/success，第三审计不导入执行器源码，真实重新解压全部74 ZIP并核对源SHA、CRC、成员全数及输出SHA；机器人永久归档[commit3ad1fb44](https://github.com/edwardsage419/Psychohistory-Research/commit/3ad1fb4493d2ca1c6362829d1e879ed955fce111)。新增真人E2/历史E3=0。

## 二、三个P0的证据范围与去重归属

**01-008 Softmax Choice Rule：复用R111的核心归一化数学E1，不新增一次独立研究样本。** 早期R061原ZIP报告已明确使用softmax把模型状态Q转换为下一次私人选择概率；这属于特定社会学习模型应用，而非软件原始模型普适实证。独立后期[R111直接一手数学报告](../research/R111/R111_MCFADDEN_1974_RANDOM_UTILITY_CONDITIONAL_LOGIT_FORMAL_BOUNDED_LEARNING_REPORT_2026-10-19.md)和[可执行概率规则](../research/R111/r111_mcfadden_random_utility_conditional_logit.py)实际计算`P_j=exp(V_j/τ)/Σ_k exp(V_k/τ)`（在可选集合上，采取稳定pivot归一化），并已做18项人工数学单测；[机读验收](../research/R111/R111_PHASE_A_SYNTHETIC_MATH_CI_ACCEPTANCE_STATUS.json)直接锚定原目录01-005 Random Utility Model。新02-002独立补缺的到来不改变这一事实：**01-008现在有共享的核心Softmax函数机制证据，但未建立所有心理场景的真人Softmax拟合、偏差/参数因果解释或独立的01-008专属原作者复现**。因此标记`SHARED_CORE_FORMULA_E1_NO_SEPARATE_PRIMARY_R`，不能把R111再计一次独立实验。

**02-002 Temporal Difference Learning：已新增独立R286补缺，限定人工数学E1正式验收。** 旧知识包明确含`心理史学_24个核心模型初步研读卡_v0.2.md`，出现02-002教学表达式；早期[R063](../research/R063/R063_EVIDENCE_AUDIT.md)是Najar2020的metaVS与固定VS2源程序审计，不应替代Sutton1988标准TD(0)机制。为避免这种混同，新[R286正式科学报告](../research/R286/R286_SCIENTIFIC_REPORT_2026-10-23.md)按Sutton1988 TD预测形式，冻结一个A→B→terminal独立Bernoulli回合模型，实做前五训练+独立第六未来奖励的TD(0)→MC→先B后A对照，9世界**576完整有序原source**。前瞻评分独立于训练，三策略五轮轨迹、Source概率、未来Brier与独立奖励系数积分九项全部Fraction相同。以p=1/2为例标准TD0未来Brier155/512、MC683/2048、错序2445/8192（错序虽低却不是在线TD(0)，也非第六轮数据泄漏）。
[R286预评分冻结](../protocols/R286_TD0_TWO_STATE_5_EPISODE_3_POLICY_576_ORDERED_SOURCE_PRESCORE_FREEZE_2026-10-23.md)在[d055e148](https://github.com/edwardsage419/Psychohistory-Research/commit/d055e14831565571ca9e953d311b55e7eed9ef42)先于运行；[最终CI run39909168454](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39909168454)三个job success，Python3.11/3.12各93项真实单测合计186项通过，第三576完整原source独立重新积分及永久CSV/JSON/SHA归档[cdf9c6ee](https://github.com/edwardsage419/Psychohistory-Research/commit/cdf9c6ee74630e5ed1fddd26dc25e069b485281c)。标准TD模型学习E1明确，但无真人机制认证、实时未来预测或真实历史外推。

**04-001 Granovetter Threshold Model：共享R118同一1978原作者论文的阈值机制E1。** [R118机读正式验收](../research/R118/R118_FINAL_ACCEPTANCE_STATUS.json)在原主目录03-019之外已经**显式声明**`first_party_related_prior_catalogue_id=04-001`，且[R118正式研究报告](../research/R118/R118_GRANOVETTER_1978_THRESHOLD_CROWD_EXACT_DISTRIBUTION_AND_SAME_MEAN_SCIENTIFIC_REPORT_2026-10-19.md)核阅Granovetter1978原刊多个具体页面、复算100人0..99阈值与单人阈值改动造成100→1的结果，44真测试，n=1..5共8476完全数学配置双算法一致。它是真正同一原机制的可检验学习成果，不应仅看[R069多种网络传播机制](../research/R069/R069_FINAL_ACCEPTANCE_STATUS.json)的关联项而漏掉。但R118的全群体阈值不是Watts局部邻居随机网络阈值，仍无真人动员阈值测量与现实反事实事件预报，因此只可`SHARED_ORIGINAL_GRANOVETTER_1978_E1_NO_SEPARATE_PRIMARY_R`，**不是独立第二组真实试验或复算两次真人预测**。

## 三、239条目录映射v0.2及机器验收

新增[全239行独立保留的v0.2交叉索引](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.2_2026-10-23.json)建立在旧[v0.1](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.1_2026-10-23.json)之上，只对上述三条原P0改变已核查证据等级；其他236条依原v0.1保留待验状态，原239模型目录自身一字未改。

|映射级别|原目录条目数|解释|
|---|---:|---|
|有后期主研究R对应的目录条目|**174**|原173+新TD补缺R286；其余173科学结题范围尚未逐项复核|
|额外两项与主R共享同一数学或原作者机制|**2**|01-008→R111，04-001→R118；不创造两项独立研究数|
|仅有历史范围有限的旧关联，没有主R|**5**|需要逐项检验旧研究是否覆盖目标原定义|
|当前这两层材料尚未检出条目关联|**58**|绝不直接判为“从未研究”|
|总计|**239**|新增人类E2=0、真实历史E3=0|

目前没有尚未判明的原P0目录条目，但不等于所有P0已通过真实外部效度评估。**后续待核主R对应条目共63项（P1=36，P2=27）**，完整队列见[待核63原模型CSV](ORIGINAL_239_PENDING_63_PRIMARY_RESEARCH_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv)。

[全239行新旧链接差异机器复核程序](../research/catalogue_audit/verify_p0_reconciliation_v0_2.py)与[最终GitHub Actions run39909421488](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39909421488)三job全部completed/success，Python3.11/3.12各249个实际测试（共**498次通过**），第三CI独立检测全部239行及源R111/R118/R286归属、v0.1到v0.2的差异、Zip取证和所有原文件SHA。[机读重核结果](ORIGINAL_239_P0_RECONCILIATION_MACHINE_RESULTS.json)、[机器哈希凭证](ORIGINAL_239_P0_RECONCILIATION_SHA256_RECEIPT.json)经机器人归档[GitHub提交a3492890](https://github.com/edwardsage419/Psychohistory-Research/commit/a34928903025e55d97ffec220dc04c6ec4e73dd7)。

下一阶段沿原239顺序继续核查P1和P2的主研究缺口，首批从**01-001 Expected Utility Theory、01-002 Prospect Theory、01-004 Bounded Rationality**等开始，以优先消除真缺口与避免重复研究。对173旧主R项仍需阅读每项实际CI/验收范围，不能把174个关联直接断言为全部已科学验证。**先完成原R系列→再统一归纳分类→最后原创熔炼**；R073、PESEN v0.1冻结，个人决策工具继续暂缓。
