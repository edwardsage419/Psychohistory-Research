# A轨：Cason、Riedl、Schram、Ule 2026 间接互惠实验，来源及原始数据门槛

审计日期：2026-10-28。证据性质：英文一手数据存档页面及公开README字段级审计，原始行为CSV未读取，正式真人E2预测=0。

## 来源与去重
官方Dryad数据 DOI [10.5061/dryad.mcvdnckd6](https://doi.org/10.5061/dryad.mcvdnckd6)，2026-01-20公开，题目 *Data from: Local competition promotes hurtful behavior towards unknown others*，作者 Timothy Cason、Arno Riedl、Arthur Schram、Aljaz Ule。研究为局部与全球竞争下的间接互惠行为。与原R073 Montero 2022双人固定或轮换对手囚徒困境属于不同的原始实验。已检查项目现有 data_scout 文件名与近期登记，未发现本 DOI 既有专项审计。

## 实际核验内容
官方数据页面列出 `CRSU_rawdata.csv` 2.75 MB、`README.md` 7.57 KB、`Strategy_Class.csv` 24.57 KB、Stata分析脚本、伦理批准PDF等十项文件。页面嵌入的README全文可读，并明确原始数据在 `CRSU_rawdata.csv`，策略分类表每位参与者一行，共156位参与者。

论文方法和README明确：156位真人在阿姆斯特丹大学CREED实验室参加，按每组6人形成26个实验组；每名参与者只参加一个session。每场100轮，每轮六人组随机分成三对，每对一名捐赠者A和一名接受者B。接受者该轮不行动，捐赠者选择help、snub或hurt三种行动。局部/全球竞争条件改变收益排名范围。README明确每组6人为独立观察单位；同组不同轮记录存在关联。

官方README列出原始CSV字段：`ida`, `idb`, `round`, `adecision`, `session`, `group`, `cohort`, `indivIDa`, `indivIDb`, `R1dum`, `R2dum`, `round10`, `acumearn`, `bcumearn`，以及帮助、伤害、拒绝的历史累计数、过去2或3轮统计、是否点击查看对方历史及历史可见行为变量。注意历史查看字段受主动点击机制影响，不能把未查看的对方行为当作当时已知信息。按实际轮次和角色重建信息集，禁止使用全样本未来统计作特征。

## 访问与许可
官方数据页面及嵌入README已读取。点击原始README文件下载链接 `/downloads/file_stream/4563250` 时公开读取工具返回HTTP 403，尚未取得原始CSV字节；未注册账户或尝试受限访问。原始CSV真实行数、轮次连续性、身份重复、行动编码、缺失值、配对唯一性、处理组独立性及文件SHA256均未完成逐行核验。不能将156×100当作已经验证的行为记录数，也不能将26组直接当作可独立留出数据已经复现。

Dryad官方[数据重用说明](https://datadryad.org/help/guides/reuse)称平台发表数据统一适用CC0；此为平台级公开许可声明，当前未取得文件字节级授权元数据。原始参与者数据没有复制进项目仓库。

## 复现准备判定
`SOURCE_METADATA=VERIFIED`；`README_SCHEMA=VERIFIED_FROM_PUBLISHER_PAGE`；`RAW_BYTES=BLOCKED_HTTP_403`；`ROW_LEVEL_REPLAY=NOT_RUN`；`REUSE_POLICY=DRYAD_PLATFORM_CC0`；`RESEARCH_E2_READY=NO`。

R073冻结协议要求双人重复囚徒困境、每场100轮、双方行动与对手历史的严格时间信息集。本研究虽然有100轮和两人配对，但每轮重新匹配、仅一方行动、三种行动且为间接互惠。故 `R073_DIRECT_SCORE_ELIGIBILITY=NO`。严禁改变R073模型、评分或事后改造任务使其看似符合。未来可另立研究考察局部与全球竞争下的间接互惠、历史可见性和分组留出，但须另行冻结协议。

## 下一步
在无需账户且无新增费用的公开渠道取得原始CSV时，先核验下载SHA、字段类型、156位身份、26组×100轮的完整性、A/B角色与配对、行动值、历史信息泄漏，再按整组留出设计独立预测；若继续403则维持BLOCKED。此报告仅来源与字段门槛审计，E2=0、E3=0、外部独立复现=0。

来源：[Dryad原始数据页](https://datadryad.org/dataset/doi:10.5061/dryad.mcvdnckd6)，[Dryad CC0重用规则](https://datadryad.org/help/guides/reuse)。
