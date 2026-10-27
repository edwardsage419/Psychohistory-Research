# E055 Akata真人博弈合作变量来源复核与R224 S20治理增量

日期：2026年10月28日（Asia/Singapore）。轨道：operations。只读治理审计，新增主动费用0。起点main HEAD `e8d2bc05d68c0e62bf6203fbf56496541c571f97`。已检查最新提交、MKT085、E054、F003、R224 S20、A轨Akata和Kuper-Smith候选。没有修改其他轨、冻结协议、研究索引或原始数据。

## 一、独立读取Akata公开原始来源

原作者英文仓库 https://github.com/eliaka/repeatedgames ，读取：
* `human_experiment/analysis/repgames.csv`，Git blob `2dd67c6ff80f2d7aa07a70b470e26fe3592c6d95`；
* `human_experiment/analysis/repeated_games.Rmd`，Git blob `ca9991b6d0917156672e1e2fea923548562d945e`；
* `human_experiment/experiment/js/script.js`，Git blob `4b7be85e8b3b964bfd0722d796f5ed6c2b8f0a19`。

本轮直接通过GitHub连接器读取完整97945字符CSV及两个原作者源码，独立JavaScript逐行解析，得到3900行为记录、195匿名ID、PD1950行、BoS1950行；PD条件Base970行、Prompted980行。PD的(action|score)完整分布：0|10为235、1|0为213、0|5为783、1|8为718、0|0为1。action=1有931行，score=5有783行，两者交集0。若用(score==5)代替(action==1)作为合作标签，1950条PD记录中有1714条标签不同，占87.8974%。

原实验脚本 `calculate_points_pd` 明确 playerChoice=1 与对手J时得8，playerChoice=0 与对手F时得5。Rmd第299行使用 `dpd$cooperated<-ifelse(dpd$score==5, 1, 0)`。因此原Rmd这一变量与原实验源码的玩家合作动作定义相反或不一致，A轨先前的测量冲突获得本轮独立来源级复核。单条action=0且score=0的异常来源保留为待解释，不能自行归因于超时。未重算论文图表及主结论，不对其受影响程度下确定结论。

归档 `research/operations/e055_akata_pd_action_score_source_audit_20261028.js` 为独立可复现脚本，要求用户在本地提供三份固定Git blob原始文件，先校验Git blob SHA1，再检查上述统计。脚本不下载数据、不上传参与者级记录。上述数值已在本轮连接器读取原始CSV后直接执行JavaScript统计；仓库脚本的本地三文件重跑仍待有原始文件的环境执行，不能虚报为已执行。

## 二、R224 S20冻结与独立性

最新R224 S20冻结协议提交 `036c04fd069ff47c3ea8bb309258532bd754fea4`，正式计算与B独立审计提交 `5696c88cec44d17d59c466b65fc9e224417ba3bc`，后续单独Node重放提交 `9762ff7d3efa1e2c6c79b4922e974683c80b658f`。本轮分别读取冻结提交和main中的协议，Git blob均为 `88c2dcc70b5da6137cd3b1e01ae1a22cb5559e09`。冻结提交时间先于计算提交。R轨在8个人工世界与5个测量核上产生40条件，B轨报告320项字段精确比较、184项附加断言、2项错误注入检出；本轮读取其报告和提交文件清单，未重新执行这504项计算，故不将其记为E055新复算。R224 S20维持人工E1。

指定R224结果提交 `5696c88...` 的GitHub Actions REST head_sha查询返回total_count=0，故该提交CI未发现运行记录；不能宣称CI成功。仓库总体免费额度和实际账单尚未独立核验。

## 三、跨轨证据等级与开放事项

R074、R075、R077已归档不同真人实验的有界内部E2评估；Akata真人对GPT-4每游戏10轮、缺原生轮次及对手逐轮行动，不符合R073冻结真人双人100轮协议，直接准入NO，新增E2评分0。A轨Kuper-Smith 2023候选含300试次与部分对手ID，但原始3MB级CSV未完成字节与场次核验，R073资格UNKNOWN_BLOCKED。未改动R073冻结模型和评分。

E011已明确R172存在历史来源的回顾性留出E3证据，同时披露历史数据可得性与独立前瞻验证限制。本轮没有新增E3历史数据或前瞻评分。应保留R172已有E3_SOURCE_HISTORICAL_RETROSPECTIVE的限定等级，避免写成整个项目历史E3为零。外部独立研究团队复现仍未由本轮建立。

R136冻结负对照、R181交付偏离、R214 S10负对照失败和R170跨路线状态比较等既有开放事项保留。未做全库逐文件普查，不能断言所有研究轨均无遗漏或冲突。

## 四、F本周状态与下一步

2026年第44周F002授权撤销及F003派生记忆语义证据专题已完成，未重复建立专题。MKT086新增多来源旧revision互相充当有效证据的候选风险，可供未来F004检查。无真实敏感数据接入，无个人决策产品开发。

下一E056：检查R224 S20独立重放的原始来源身份校验、最新R轨冻结顺序及A轨Kuper-Smith数据获取条件；继续跟踪R136与R170开放项。保持完整R系列、系统归纳、最后熔炼的顺序。