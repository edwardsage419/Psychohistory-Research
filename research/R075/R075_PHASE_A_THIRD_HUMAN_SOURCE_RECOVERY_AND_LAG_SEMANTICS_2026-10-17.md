# R075：第三独立真人重复博弈来源恢复与历史动作语义审计，阶段 A

日期：2026-10-17。性质：**真实外部来源适用性审计，仅限来源与时间语义**。无 R075 真人概率模型计算。本阶段仍为 `ACTIVE_SOURCE_GATE`，R075 E3 是 `OPEN`，不构成外部实验成功复现。

## 1. 研究目的及已有发现的边界

R073 在第一实验12场18424次个人下一步选择中，M3较M1的场次等权 Brier 改善0.009439，M4较M3改善0.004212；R074在第二独立作者实验18场15338次决策中，M3较M1改善0.022915，M4较M3反而变差0.003171。原作者外部复验资料、R073七族 M0–M6、不调 `alpha=20`、固定TFT/WSLS噪声0.05、t>=3的同局双方两轮历史、teacher-forced一步概率预测、完整真实实验场次留出与场次等权 Brier/log loss都继续冻结。

[R075来源审计预冻结协议](../../protocols/R075_THIRD_INDEPENDENT_HUMAN_IPD_SOURCE_GATE_2026-10-17.md) 先于任何 R075 真实模型得分提交 Git `626bcb965cd4b7f09e21a776da8f9a4df89c8fe7`，授权只做来源和信息集核验。

## 2. 两条第三作者候选与当前阻塞

C1 是 Fudenberg, Rand & Dreber 2012，*Slow to Anger and Fast to Forgive: Cooperation in an Uncertain World*，AER DOI `10.1257/aer.102.2.720`，官方 openICPSR DOI `10.3886/E112512V1`。论文明确指出设计包含意向行动的执行噪声；当轮可见结果必须与本人原始选择、对手实际执行的动作区分。其它论文 Nishi et al. 2016 DOI `10.1038/srep29622` 提到这个实验18个 session、384人和其特定数据子集30,038次行为；不能据此声称已读到2012原始数据。

[官方端点真实 GitHub Actions 审计 CI 38989471263](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38989471263) 及[后续HTML链接定向审计 CI 38989532405](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38989532405) 均 success（仅指探测代码成功）：
* `https://www.aeaweb.org/aer/data/april2012/20100629_data.zip` 和 `https://ftp.aeaweb.org/aer/data/april2012/20100629_data.zip` 都 HTTP 403。
* `https://www.openicpsr.org/openicpsr/project/112512/version/V1/view` 与 `.../download` 都 HTTP 403。
* AEA 的 `/journals/dataset?id=10.1257%2Faer.102.2.720` HTTP 200，但内容是HTML，未发现可下载的直接官方 ZIP 链接。
* 来源归档存在的公共网站记录与**当前CI无法读取原始字节**是不同事实。不能断言作者数据已经丢失，更不能据此认定数据本身无效。

C2 是 Kamei & Nesterov 2024，Economica DOI `10.1111/ecca.12539`。论文报告16场、360名参与者、无跨场重复、五种报告和公开信誉处理，潜在价值很高。当前仅发现作者发布的补充PDF，没有独立获取其逐人逐轮原始数据与场次映射，因此不可开展评分。

附加的 C3 是 Mao, Dworkin, Suri & Watts 2017，*Resilient cooperators stabilize long-run cooperation in the finitely repeated Prisoner’s Dilemma*，Nature Communications DOI `10.1038/ncomms13800`，数据指向作者论文公布的 `https://osf.io/64z8u/`。它在20天中跟踪同一批人：**不能把20天当成独立参加者场次，必须按不跨组的人群设计留出**；原文提到分为两个持续跟踪的场次人群，实质上只有两个潜在独立群组。[真实官方端点探测 CI 38989640797](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38989640797) 的 OSF项目及公开文件 API 均 HTTP 503，原始行为文件无法进一步核验。

## 3. 第三方真实整理数据的固定字节结构审计

预先已可获得的 `cran/stratEst` 公开整理版固定 Git commit `a6373b23d80dc816a63f18f973d372c9e8421914`，`data/FRD2012.rda` Git blob `6b196ca1624081850b41dc2084c762257d59dd8f`，26,923字节。**这是第三方的加工数据，不是原作者 ZIP 的等价证明。**

[真实13,126行动与本人历史字段核对CI 38989793680](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38989793680) 已 success；在 GitHub Actions 临时源目录解码真实 RData，不导出任何参与者ID、session编号或行为轨迹。原始数据的匿名结构为：
* 6种处理；384个 treatment+id 人员标签；1536条受试者与supergame组合；全部13,126条当前意向行动C/D；
* 11,590个同一 `treatment,id,game` 且 t 与 t-1 连续的本人上一选择核对，前一轮本人 `last.choice` 与紧邻上一记录的 `choice` 存在 **1,163个不同**（约10.03%）；此差异很可能与原设计的行动执行噪声有关，**不能直接判断数据损坏，也不能未经原作者字典把 `choice` 或 `last.choice` 写成「可见实际结果」**。
* 所有11,590条连续历史的 `last.choice` 和 `last.other` 均无缺失，所有1536个 supergame 首轮 lag 均为空，13,126记录构成连续完整的局内个人轮次，未发现重复轮次。
* 可具有完整前两轮 `last.other` 的 t>=3 结构性候选样本为 **10,054**。**并没有进行任何 R073 模型拟合/留出评分**。
* 最关键的**真实独立实验 session 识别字段仍然没有出现**。supergame 和 participant 不能被擅自重命名为原始 session，防止同场互相训练和测试。预冻结的完整留场次 E3 资格继续阻塞。

本轮新增 R 源数据语义审计与 synthetic 对照测试：
[审核程序](r075_frd2012_lag_schema_audit.R)、
[合成回归保护](test_r075_frd2012_lag_schema_audit.R)、
[官方来源网络/ZIP审计程序](r075_first_party_archive_probe.py)、
[来源网络10项合成测试](test_r075_first_party_archive_probe.py)。
真实来源和人类行只存在CI runner临时内存与临时文件，结果是匿名宏元数据。

## 4. 有界科学判断与下一门

当前第三项独立真人实验的作者一手完整 session/局/人员时序和噪声可见信号联结没有恢复。**不能发表 R075 E3 的第三次真人外部复验值**；同一R整理版的 subject-level 留出也不能替代先前要求的完整独立 session 留出。

优先进一步检查六种处理的 `last.choice` 与之前 `choice` 的错位率是否与公开 `error` 编码一致。即使吻合，该相关性只能增强噪声解释的可信度，不能单独证明意向与实际动作的字段映射，仍需原作者一手字典或能够独立确认的原始档案。

若官方来源持续受403/503访问限制，下一步选择其它**独立、可获得、含完整真实 session 的真人双人重复博弈数据**，不得为了发表正面结论而放宽独立性条件；禁止任意使用论文已公开结果反推最适当拟合参数。

`R075_PHASE_A=SOURCE_AND_LAG_SCHEMA_AUDITED_BOUNDED`
`THIRD_PARTY_FROZEN_BLOB=AUDITED`
`AUTHOR_ORIGINAL_SESSION_LINK=OPEN`
`INTENDED_VS_REALIZED_ACTION_LINK=OPEN`
`R075_REAL_MODEL_E3_SCORING=NOT_RUN`
`R075_E3=OPEN`
`PESEN_v0.1=FROZEN`

## 5. 六个噪声处理的来源语义检查（实际新证据）

[真实独立重跑 CI 38989913654](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38989913654) 的 single job success。原程序按 treatment + id + game 严格核验同一 supergame 连续动作，不涉及任何概率模型评分。

| treatment | 公布的 error 字段 | 相邻轮次核对 | 上一轮本人字段不一致 | 实际比例 |
|---|---:|---:|---:|---:|
| 1 | 0.125 | 2268 | 290 | 12.787% |
| 2 | 0.125 | 1590 | 208 | 13.082% |
| 3 | 0.125 | 1958 | 244 | 12.462% |
| 4 | 0.125 | 2716 | 337 | 12.408% |
| 5 | 0.0625 | 1618 | 84 | 5.192% |
| 6 | 0 | 1440 | 0 | 0% |
| **合计** | 不同条件 | **11590** | **1163** | **10.035%** |

数据表现与 error 列设置高度吻合：0噪声处理严格零错位、12.5%组接近12.5%、6.25%组接近6.25%。支持此处的 `last.choice` 和紧邻 `choice` 之间存在**来源内真实实施噪声语义差异**。原作者原始数据字典尚未恢复，**禁止把这个数值匹配当成原作者明确确认的字段语义**。若直接强行从 `choice[t-1]` 替代 `last.choice[t]`，有超过千处行的历史动作与实际公开前轮字段不同，会使拟合目标与已观察信息集错位。更不得因此在R075看到结果后修改R073冻结模型评价。

最新核验仅提高 G2 中噪声风险的可解释性，原始 session 及原作者字节等价这两个 G1/G3 必需证据缺口依旧 OPEN。最终 E3 状态不改变。
