# R088 原作者171个6人组×20轮：多层级公共品合作与群体达标的评分前冻结

日期2026-10-17。本协议在任何R088原始逐人贡献值读入和评分前提交，是已发表2025-12/2026《Scientific Reports》数据的回顾性独立复算，不是原作者实验前注册。

## 来源与独立科研问题
Pilgrim, Stewart & Raihani, *Social identity and cooperation co-evolve in a multilevel public goods game*, DOI https://doi.org/10.1038/s41598-025-30979-2。原论文与研究材料一手GitHub `chasmani/PUBLIC_social_identity_and_cooperation`，唯一固定提交 `8ce2c0cac4784485232aa96295f48ff147290b05`。作者完整六人组数据 `analysis/data/data_full_groups.csv` 原Git blob `f902865203bdb465a505869b593eca432831b2fa`、2,270,643 bytes；作者排除规则 `analysis/analysis_exclusions.R` Git blob `5d7f6e65523df55a1f05bd69f48d60b9306783a9`，合作率分析 `analysis/analysis_cooperation_rates.R` Git blob `60793d82709a7807e86ceddd772fe2847733a6e2`。原始数据经作者既有排除和完整六人筛选形成（完整群体样本，非全部在线招募），原分析原始人日志到本CSV变换尚未经本项目复算。

原作者明确报告171个六人完整群体，每组有2个三人子组；GlobalOnly、Balanced、GlobalBoost三处理各57组，20轮持续同一组，实际完整群体本人1,026人、玩家轮记录20,520条。GlobalOnly可投global或self，Balanced及GlobalBoost可投global/local/other/self，其中other为对另一个本地子组投资。全球阈值是同组六名中至少4名投资global; 本地阈值至少2名投入相应子组。**此轮只计算全体group global贡献及全球阈值、每group四选择类别平均和初末差；不计算local阈值，因为跨本地group的other转移需更复杂定义，避免误计。** 社会身份融合为后续研究目标，此轮不碰问卷/身份/付款。

主要问题：一个本地投资选项与更高全球回报在不同实验条件下对应怎样的group-level全球投资率和达标表现，以及20轮之中合作是否维持？比较对象是**独立group**，不是将20520条重复人期假设独立。

## 严格原人-组-轮字段合同
来源Csv必须从固定作者SHA验证后才能拆列。每人一行，共1026行；字段 `group_id`、`subgroup_id`、`condition`，以及逐轮20列原作者原字段 `game.1.player.contribution` ... `game.20.player.contribution`。每个group_id对应恰好六行同一condition，整个CSV恰好171个group，每处理57，subgroup_id每group恰好两个且每个恰三人。不能丢失人、擅自调组、插补任意值或更改条件labels。原始group_id和subgroup_id仅在进程内使用，禁止输出。每人20轮行动恰一合法类型，GlobalOnly仅`global`/`self`，Balanced/GlobalBoost允许`global`, `local`, `other`, `self`。任何缺失、`None`、无效字符串、长度为0，全组来源失败而非剔除。来源如果实际存在另一份全量数据的自定义缺失约定必须另冻结修正而不在本次看到结果后改变科学合同。

完整组group × round (171×20=3420组轮)：global投资者计数G在0..6、global阈值是否达成（G≥4）、四行动类别数严格和为6。每处理每轮57组等权记录group-global-rate `G/6`，当轮global threshold success proportion `sum(groups G≥4)/57`。每组初末 `(G_20-G_1)/6`，三处理均值以及正负零组数（总57）和20轮轨迹保留；另各条件全20轮group平均全球投资率、总局部投资比例(local+other)/6、self率，全都由同一群体动作数计算，绝不因为“other”不是自己的local而当作self。每处理首末全球达标成功组数，整个20轮达标总组轮次数，零投资/全投资等反例和阈值临界组 G=3次数。精确比较固定 `GlobalOnly-Balanced`, `GlobalBoost-Balanced`, `GlobalBoost-GlobalOnly`三对的原始独立57组平均global合作率差（先按20轮取组均值，再对各组取平均），不在见到差异后换时间窗口/模型。它们不是随机因果效应，原作者已发表假说与事后样本筛选的影响要保留；本轮不拟合心理状态或新E3。

## 原始资料的已有分析与负面证据
论文有自有预注册和原作者统计分析计划（作者论文表2），但本冻结系2026-10-17回顾性，不能写成2025年真正预注册。条件内容不同，GlobalOnly没有local投资的可选项，不能把“local=0”作为和有本地选择条件的可因果比较的实际偏好。原作者 `analysis_exclusions.R` 明确完整组以20轮贡献非空、非掉线、六真人收齐选取，且其它个人筛选文件存在。此E2结论只能对筛过的完整组集有效，不可向所有招募者外推。实际Group-level独立单位仍可能有同一session内多组相互依赖、条件分配政策；暂不提供显著性与因果解释。论文同时研究融合身份，当前纯行动合作不是身份融合因果证据。

## 运行约定
先提交协议，再写 >=25项完全synthetic的SHA、6人、20轮、2个3人子组、3×57组源合同、信息条件类别约束、组级初末与临界阈值和不泄漏ID tests；随后GitHub Actions独立下载固定原作者GitHub提交完整CSV+处理脚本SHA，实际运行所有171组，归档仅匿名3处理/全体/每轮聚合。第二次真实完整重新下载/重新评分并对整个结果文件字节数SHA256逐字节相等后自动提交main。原始真人个人轨迹、ID、pair、完整CSV、问卷和开放源动态tokens均不得存研究Git。验收A01-A06，E2限已发布作者完整组数据，E3未建立，PESEN v0.1继续冻结。

R088_BEFORE_REAL_HUMAN_SCORES=PROTOCOL_FROZEN
R088_CAUSAL_AND_HISTORY=OPEN
