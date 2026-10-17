# R076 — 三个真人重复博弈实验之间的源模型零样本数值参数转移冻结协议

日期：2026-10-17。**冻结于首次执行 R076 跨实验真人数值迁移之前**。标注：`RETROSPECTIVE_SCOPE_DECISION`。研究者已见过 R073–R075 的留整场模型评分和主要配对差，所以这些目标数据**不是新鲜研究者盲样**。R076 不得宣称是新实验预注册式 E3，也不得借本次结果自动升级 PESEN v0.1。

## 目标、来源与冻结数值规则

唯一主要科学问题：在 R073 原始 Montero-Porras 2022 真人实验的全部 12场、188名受试者、18,424个 t>=3 完整两轮历史目标上**一次拟合**的 R073 冻结 M0–M6 模型，**完全不使用任何 R074 或 R075 行动标签训练**，能否在 Dal Bó/Fréchette 2011 (R074) 和 Fudenberg/Rand/Dreber 2012 (R075) 各自真实原始18场样本上取得优于同一个 R073 源拟合 M0 的 Brier 分数，以及 M3 是否在源拟合 M1 之上更优、M4 是否在源拟合 M3 之上更优。必须保留失败、逆转、所有预测家族及各实验/六处理的完整结果。

源资料须严格固定 `eladiomontero/PairwiseStrategies` tag submission commit `4743f74d8a03a031b8f70aff64956f8ad5155182`：
- `fix.csv` 988279字节，Git blob `3bf78bf85f6642afee18d6f1965dca7272582f40`；
- `rand.csv` 1112614字节，Git blob `f5a86cd033b739da45d3fc7c5019068f612146a2`。
R073 Python 核心 Git blob `c8a0b47fd27bf05e7be5b87419a0824355fc911a`，必须在程序内再次校验，所有 M0–M6 定义、`alpha=20` 平滑、TFT和WSLS理论预测噪声0.05、四状态/16状态向量、`brier()`、`logloss()`及一轮 teacher-forced 历史完全保持原 R073 字节定义。源拟合的每一族都严格使用统一 t>=3 完整前两轮风险集，不能包含 t=1/2以外目标；当前R076仅重算从冻结 R073 模型族构成的源状态频数和合作基率，**不得**反向读取 R074/R075 统计量拟合、重设参数或选择 donor treatment。

**主要 donor `R073_ALL_12_POOLED`：** 将原 R073 `fix` 六场与 `rand` 六场的共18424个来源风险事件合并计算单一 `p0` 与 M1–M4 每个离散状态的源C/n计数；M0 只给这个源 `p0`；M5/M6仍固定公式，无训练。对目标 `R074`、`R075` **同一份冻结参数，任何目标实验都不重估源参数**，尤其不得按目标实验合作率修改 `p0`、按目标错误率修改固定噪声0.05。

两个**预先指定而非挑选胜者**的次要 donor：`R073_FIXED_6_ONLY` 仅用 fix六场训练；`R073_SHUFFLED_6_ONLY` 仅用 rand六场训练。必须并列报告这三种 donor 在两份目标实验上的全部七模型、主对比和负结果，不事后择优或平均后掩盖。

## 目标原作者全部样本、信息映射、不可泄漏定义

R074 Dal Bó & Fréchette 原作者网站 `https://gfrechette.com/data/Dal_Bo_2011a_data.txt`，固定 SHA256 `357a12968546a8d9002c912c1f499e02e93d59113d2a0928de2dee48323a0ae6`，18个 `date` 原生实验场次，15338个 `match` 局内 t>=3 下一真人已执行C/D目标，6种收益×继续概率处理。只经已有 R074 source parser + session builder 的前置完整性守卫，从源转入匿名评估事件；不得重用目标的 `fit_other_sessions()` 或其他统计来训练 R076。

R075 Fudenberg/Rand/Dreber 原作者 David Rand 公开 ZIP `https://davidrand-cooperation.com/s/slow-to-anger-and-fast-to-forgive-data-and-code.zip`，1129409字节 SHA256 `328346c3cf88a71a3d6cf574f7d6ba741dcea460f3926c16266f1784d3a699ef`，内部24列 TXT SHA256 `ff552ba21a92c254e2d867670910f908f5ea8e3aa34b4fa6c05443a020fa56b7`，18个 `file` 原始session，26116个同一互动局 t>=3 完整前两轮真人**意向**C/D，先前动作是伙伴及自己已**执行**反馈。目标来源使用现有 R075 `prepare_original_sessions()` 从作者固定源解析；**不**调用其拟合函数。

每个目标 R074/R075 的所有真实18场均各自作为评价场次，**无目标训练折、无目标标注拟合**；每场内平均Brier和logloss，18场等权；每个六处理的完整场次等权均值与按场次配对差 better/equal/worse 必须输出；R074与R075之间分别报告，不因为 R075 有更多t>=3行为而赋更大权重。不在源内选择最佳 donor、不仅报告更好模型。原始个人信息、原始行、单场指标、逐场编号、训练状态表均禁止写入Git或 Actions artifact。所有原始来源在runner临时文件，退出时删除。

## 冻结比较与成功条件

每个 donor×目标实验共 3×2=6 组，预先所有7个模型都计算两个等权损失。必须执行6个固定配对Brier：
1. `M3_JOINT_LAST − M1_OWN_LAST` （上一对手反馈增量）；
2. `M4_JOINT_TWO_LAGS − M3_JOINT_LAST` （第二轮双方历史增量）；
3. `M1_OWN_LAST − M0_TREATMENT_PREVALENCE`；
4. `M2_OPPONENT_LAST − M0_TREATMENT_PREVALENCE`；
5. `M5_TFT_NOISY − M0_TREATMENT_PREVALENCE`；
6. `M6_WSLS_NOISY − M0_TREATMENT_PREVALENCE`。

额外 `M3−M0`, `M4−M0` 的宏平均Brier只作已明示的派生对照，不挑选。**成功一项只能按特定 donor 和特定目标实验的18场宏平均 Brier 增量为负表述；两目标的主 donor 要同时负才能说“在两个已观察的目标实验中改善”，不能推为所有制度泛化保证。** 任何恶化都如实写进科学报告。M5/6三个 donor 的预测公式不依赖源参数，理论上得分应完全相同；若不同自动 FAIL，以防不一致样本/事件集合。

**主要证据等级：retrospective third-party-original-source cross-study numerical parameter transfer，不能算新未见实验的E3。** 本次使用过往公开原始实验并且原有模型和两个目标已被研究者观察；未来须用全新第四实验才可以升级前瞻验证。不同研究真实选择目标具有执行/意向差别：R074实际合作；R075当前意向合作，先前历史为实际合作，不能把不同基准错误解释为学习机制因果。源 `fix/rand` vs 目标六处理的行为基率差异可能造成强烈失配，这是此检验真实对象，禁止通过后见归一化/局部重校准隐藏它。

`R076_PROTOCOL_FROZEN_BEFORE_NEW_CROSS_STUDY_SCORES=YES`
`R076_DATA_ALREADY_OBSERVED_IN_R073_TO_R075=YES`
`R076_EVIDENCE_LEVEL=RETROSPECTIVE_NUMERICAL_TRANSFER_NOT_NEW_E3`
`R076_MODELS=UNCHANGED_R073_M0_TO_M6`
`R076_ZERO_TARGET_LABELS_IN_FIT=MANDATORY`
`PESEN_v0.1=FROZEN`
