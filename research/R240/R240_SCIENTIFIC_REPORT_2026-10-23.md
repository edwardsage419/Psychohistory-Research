# R240 内容分析编码一致性：九人工二值标注世界、2304完整原来源与κ/α和真实准确性不可等同

日期2026-10-23（Asia/Taipei）。实际239原目录 **10-014 Inter Coder Reliability Models（P1）**。科研资格 `CLOSED_BOUNDED_E1_FINITE_ARTIFICIAL_INTER_CODER_RELIABILITY_AND_ACCURACY`。全部仅人工有限标注机制；没有历史原文本、真实人工编码人员、受训标注员、真值标注或正式编码实验，新增真人E2/历史E3均0。

## 一手来源、冻结次序与模型边界

Cohen (1960), [*A Coefficient of Agreement for Nominal Scales*](https://doi.org/10.1177/001316446002000104), *Educational and Psychological Measurement* 20:37–46，给出从原始一致率中校正按两名编码者各自边际计算的偶然一致率κ。Krippendorff (2004), [*Reliability in Content Analysis: Some Common Misconceptions and Recommendations*](https://doi.org/10.1111/j.1468-2958.2004.tb00738.x), *Human Communication Research* 30:411–433，说明编码一致系数的结构、适用条件及误读风险；Artstein & Poesio (2008), [*Inter-Coder Agreement for Computational Linguistics*](https://aclanthology.org/J08-4004/), *Computational Linguistics* 34:555–596，讨论语言注释的编码一致和κ、α区别。本研究仅精确计算两个二元编码者的人工population κ，以及另一个**配对完整、无放回有限符号集合**的nominal α，不声称实现Krippendorff α全部缺失数据规则、多名编码者或真实人类可靠性推断。无原论文真实样本及方法效果复算。

先于程序源码及CI提交[九人工机制、完整原来源及期望反例的独立冻结协议](../../protocols/R240_INTER_CODER_RELIABILITY_9_WORLDS_2304_FULL_ANNOTATION_ATOMS_PRESCORE_FREEZE_2026-10-23.md)，冻结commit [23ffd774](https://github.com/edwardsage419/Psychohistory-Research/commit/23ffd77477c9eba53867692e27303ecc666a55e9)。后续第一次CI失败仅因归档验收脚本中的JSON字符串与整数比较，**完全没有更动原人工模型、概率源、数值统计或源码**；失败运行保留，下文单列。

## 2304完整人工文章—标注类型及两条算法

每世界人工8个独立二元外生`T,U,E1…E6`完全枚举2⁸=256种原来源型，每条1/256，各世界质量和1，九世界共**2304条原来源**。T是数学定义的“隐藏正确二值标签”，两名真实生成标注A/B因机制不同，可以如实、共同系统反转、共同偏差、独立误差、独立随机、分类组成稀少、单侧假阳性、不相容或选择性缺失。对于未保留双编码对的原来源，实际`observed_A/observed_B`均写−1，原真A/B仍分隔存放在人工oracle字段，不允许纳入实际κ或α计算。

统计观察第一路线仅取S=1的实际`(A,B)`，构建2×2表和原始一致率`Po=(n00+n11)/N`、Cohen独立边际机会一致率`Pe=(nA0*nB0+nA1*nB1)/N²`、`κ=(Po−Pe)/(1−Pe)`；二元有限名义α另外计算`Do=(n01+n10)/N`、`m0=2n00+n01+n10`、`m1=2n11+n01+n10`、`De=2m0m1/[2N(2N−1)]`、`α=1−Do/De`，其中α的有限校正**不同于κ的有放回边际偶然一致**。本模型全部N、m0/m1分母有效，所有数值均Fraction严格精确。第二独立路线**不读取原CSV来源**，而从冻结人工函数完整枚举八位真原源重新列出每个S/A/B频数与κ结果，逐世界和第一次来源路径相符。T和被删除的完整原A/B只可用于隔离的人工Oracle准确率或全源一致率，与实际观察指标严格分离。

## 九世界完整原统计结果

| 冻结人工世界 | 实际双编码保留比例 | 实际Po | Cohen κ | 两名编码对隐藏T的真准确率 |
|---|---:|---:|---:|---|
| PERFECT_TRUTHFUL | 1 | 1 | 1 | (1,1) |
| PERFECT_SYSTEMATICALLY_WRONG | 1 | 1 | 1 | (0,0) |
| SHARED_SYSTEMATIC_ERROR | 1 | 1 | 1 | (3/4,3/4) |
| INDEPENDENT_QUARTER_ERRORS | 1 | 5/8 | 1/4 | (3/4,3/4) |
| BALANCED_INDEPENDENT_RANDOM | 1 | 1/2 | 0 | (1/2,1/2) |
| RARE_POSITIVE_INDEPENDENT_RANDOM | 1 | 25/32 | 0 | (1/2,1/2) |
| ASYMMETRIC_FALSE_POSITIVE | 1 | 7/8 | 3/4 | (1,7/8) |
| SELECTIVE_MISSING_DISAGREEMENTS | 3/4 | 1 | 1 | (1,3/4) |
| OPPOSING_CODERS | 1 | 0 | −1 | (1,0) |

**完整观察分布等价但真实准确性迥异：** PERFECT_TRUTHFUL人工A=B=T、PERFECT_SYSTEMATICALLY_WRONG人工A=B=1−T、SHARED_SYSTEMATIC_ERROR人工A=B=T XOR(E1∧E2)。这三个世界的完整`P(S,A,B)`逐格严格一样，所有两编码实际完全一致、Po=1、κ=1、完整配对nominal α=1。然而人工真值T的两个编码员正确率分别(1,1)、(0,0)、(3/4,3/4)。**完美相互一致本身没有提供独立金标准的正确性信息**；若历史资料出现两人完全一致，也不能忽略共同编码规则错误、共同模板偏差或相同误解。

**稀少正标签令原始一致高但κ仍为零：** BALANCED_INDEPENDENT_RANDOM让两个编码都是独立p=1/2的Bernoulli，Po=1/2、Pe=1/2、κ=0。RARE_POSITIVE_INDEPENDENT_RANDOM让A/B两名标注员独立各以p=1/8标正类，原始Po变为`(1/8)^2+(7/8)^2=25/32`，**Pe也等于25/32，所以κ仍为0**。把更高原始一致率当作更强的超机会独立复现能力会误读不同正类组成。同一世界名义α由于冻结有限配对无放回修正为1/512，不与κ强行相同。

**共同系统偏差 vs 独立错误：** 两人各有真准确率3/4，在SHARED_SYSTEMATIC_ERROR世界两者误差完全共享，从而κ=1，却在INDEPENDENT_QUARTER_ERRORS世界分别由独立E1∧E2及E3∧E4发生，各人工3/4准确，原始一致率仅5/8、κ=1/4；后者有限配对nominal α=`515/2048`。因此**一致率高低也不能单独界定个体正确性**，两个来源的误差相关机制会改变统计结果。

**选择性删除不一致案例虚增可靠性：** SELECTIVE_MISSING_DISAGREEMENTS真实全原来源A=T、B=T XOR(E1∧E2)，全256来源真两编码一致率为3/4。但人工观测设计只保留A=B的192种来源，占比3/4，丢掉全部不一致原来源；在所保留的192个双编码单位上观察Po=1和κ=1。完整`P(S,observed_A,observed_B)`中的S缺失率1/4给出应当审查缺失机制的证据，**不能从选中资料κ=1推断原全体编码完美可靠**。同理本R只对有完整两个编码的S=1单位计算α，不对已删数据尝试不存在的Krippendorff通用缺失校准。

**编码边际不对称与强负一致：** ASYMMETRIC_FALSE_POSITIVE中A=T但B将部分T=0误编码为1，B的标1边际5/8而A为1/2，原始Po=7/8、κ=3/4；OPPOSING_CODERS中B永远反转A，Po=0、Pe=1/2、κ=−1（有限nominal α=−255/256，差别来自校正方式与有限单位）。这些是精确人工组合，不是评价真实编码员伦理或能力的证据。

## 首轮失败归档、再次全通过与永久原源

[原生完整Python生成式](r240_exact_intercoder_reliability.py) · [全部2304独立人工编码原来源CSV](R240_ALL_2304_ORIGINAL_TWO_CODER_ANNOTATION_ATOMS.csv) · [九世界观察2×2/κ/α及真准确Oracle JSON](R240_EXACT_RESULTS.json) · [来源SHA256机器收据](R240_FINAL_MACHINE_ACCEPTANCE.json)。

首轮[CI run39887482918](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39887482918)的Python3.11/3.12两个模型测试作业均为success，但第三完整原档作业**failure**，其Python验证片段误将编码表`sum(table.values())`整数与JSON中`selected_source_units`字符串直接比较，触发错误AssertionError，故首次run总体failure、来源尚未归档。人工机制与数据校验生成完全正常；独立修复仅把JSON计数字符串显式`int(...)`转换，提交[ba0c4776](https://github.com/edwardsage419/Psychohistory-Research/commit/ba0c4776add4d4fc63aebe629db8c7fb838ab081)，没有更改被冻结的九种模型、所有统计公式或结果。

修复后[CI run39887571982](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39887571982)总体completed/success，三job均completed/success；Python3.11/3.12实际运行日志各`Ran 84 tests`并`OK`，合计**168次真实测试通过**。第三独立来源审计确认2304源行、九世界各256完整0/1潜原源、2×2表计数、三观察等价世界和不同真正确率、稀少边际Po=Pe=25/32且κ=0、选择缺失使原真实Po=3/4而观察Po=1、有限名义α计算和全部文件SHA；真实日志输出`R240_ALL_2304_CODER_ATOMS_AND_EXACT_KAPPA_ALPHA_ACCURACY_PREVALENCE_ALIASES_VERIFIED`。机器人永久提交源CSV、完整结果及SHA机器凭证 [262e0b9d](https://github.com/edwardsage419/Psychohistory-Research/commit/262e0b9d2305c80f8cbdb164d0c011365fca954d)。

原来源CSV SHA256 `2118e490a2af7a031b912e2f6ea778d65125cd583d033afc7cc71e4004fecd7a`；九世界结果JSON SHA256 `edbd242b3eff200667da686dba6cacf7448a8a371a7d4e0631d15ab76ba1de22`。

**科学边界：** 本研究只复验两名二元人工编码者在完全指定数学概率世界的agreement正确公式、原观察分布别名和人工真值效度缺口；没有任何历史文本内容标签、真人标注、训练前后标注员验证、语言跨期概念解释、社会历史数据E3。新增E2=0、E3=0；R073/PESEN v0.1保持冻结。下一原239目录跨入 `11-001 Ordinary Differential Equations`，拟R241。遵守原R先全部完成、其后统一分类、最后模型熔炼。
