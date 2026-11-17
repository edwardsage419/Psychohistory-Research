# R127 / original239 05-003 科学验收准入逐项核验记录

日期：2026-11-17。轨道：R 科学核查兼 E 质量复核，针对原始目录 P0 05-003 Coordination Game。性质：**现有冻结证据和生产调用门槛的有界审查**，没有授权、执行新的正式科学等级认定或修改冻结协议。

## 0. 快照身份

起始 `main`：`cd2d1e9bfa02089c7261252604be4c8d197b42c7`。原始待核队列 `docs/ORIGINAL_239_PENDING_154_ITEMWISE_EVIDENCE_TRIAGE_QUEUE_2026-10-25.csv`，Git blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`，实际读取 154 项，05-003 为首条 P0，状态 `PROVISIONAL_PRIMARY_README_LINK`，仍需逐项来源与科学验收核查。

历史 R127 已完成的限定科研与其真正 GitHub CI：`research/R127/R127_FINAL_ACCEPTANCE_STATUS.json` 记载 `CLOSED_BOUNDED_VAN_HUYCK_1990_ORIGINAL_MIN_EFFORT_TABLE2_AND_TWO_PLAYER_EXACT_SELECTION`。本轮实时回读原 GitHub Actions [39348775741](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39348775741)，真实 `completed / success`。仍不可把发表的 107 人聚合信息升级为本研究中新个体预测 E2。

原研究冻结协议 `protocols/R127_VAN_HUYCK_1990_MINIMUM_EFFORT_ORIGINAL_TABLE2_AND_2X2_RISK_SELECTION_FREEZE_2026-10-20.md`，Git blob `4734ede5133701d622acfda76c4f9474bf660b21`。第三方法额外冻结协议 `research/validation/R127_THIRD_METHOD_INTEGER_TENT_BEST_RESPONSE_PROTOCOL_FREEZE_2026-10-24.md`，Git blob `40d5a1eb20214bb39b890292fbf2ed92ab16b72a`。

## 1. 逐项审查结果

| 门槛 | 本轮可核实事实 | 审查状态 |
| --- | --- | --- |
| G1 原作者来源与模型机制 | 已冻结 1990 AER 最低努力支付模型、一手原刊页范围及合法合成计算，原限定 60 单测和 Actions 成功 | `COMPLETE_BOUNDED_HISTORICAL` |
| G2 原论文群体行为观察范围 | 七场十期 490 格既有两次**同一研究主体非盲**核阅，真实论文汇总 107 人。无个体轨迹，未获得真正独立第二抄录 | `PARTIAL_SOURCE_INDEPENDENCE` |
| G3 冻结后第三方法记录结构 | 冻结文本要求每条归档记录同时含 `exact comparison flag`。原 2793 行 CSV 缺少字段，补充 CSV 全部有字段，二者基础内容一致 | `FROZEN_SCHEMA_DEVIATION_RECORDED` |
| G4 真实原生数学复算 | 原 R127 60 项历史测试通过；另一项第三方法在历史报告中已有独立复算与补充校验；此次新增 100 人和 17 人严格锐界，CI success | `COMPLETE_SCOPED_INTERNAL` |
| G5 当前科研 CI 入口可靠性 | R127 原正式 workflow 仍含 33 行独立 Python `assert`，可在优化模式被忽略；仍有写旧历史收据和 `git push main` 的生产副作用。Codex 已有候选修复归档但正式 workflow 未替换 | `PRODUCTION_GATE_OPEN` |
| G6 真实个体样本外预测 | 本项目没有新增原参与者逐人场次留出或其他独立 E2/E3 预测评分 | `NOT_RUN` |
| G7 original239 正式待核队列调整 | 未修改待核队列、交叉索引或历史状态 | `DEFER_FORMAL_ITEMWISE_CLOSURE` |

这里的 G1 “已完成”只对应 R127 2026-10-20 原有的**限定机制与合成数学验收**，不能推导第三方法冻结偏差已被追认、原始论文机制被因果识别或新真实预测成立。

## 2. 实际重新读取并运行第三方法数据一致性检查

原始第三方法 CSV：
`research/validation/R127_INTEGER_TENT_2793_PROFILES_2026-10-24.csv`
Git blob `2a6706dcb047a5bf64f91651a8217d1d8009aa2c`。
头部：`group_size,efforts,minimum,payoff_numerators`。

补充旗标 CSV：
`research/validation/R127_INTEGER_TENT_2793_PROFILES_CI_FLAG_SUPPLEMENT_2026-10-24.csv`
Git blob `07021ecb761de86d9ae71061dbd17f2f0f40dc8d`。
头部在原四列之后增加 `exact_comparison_flag`。

实际通过 GitHub 连接器读取两份完整 UTF-8 原始内容，使用隔离 JS 对两个文件每一行逐一比对。结果：

* 原文件 2793 行；补充文件 2793 行，分组 n=2、3、4 依次 49、343、2401。
* 每行原有四列与补充文件同位置基础列**2793/2793 字节相同**，不符 0。
* 补充文件所有 2793 个 `exact_comparison_flag` 都为 `PASS`，不符 0。
* 用独立整数支付公式 `10u=6+2*min(e)-e_i` 重算全部行的 minimum 和个人收益分子，无语义不符。
* 故意把一项补充 `PASS` 改为 `FAIL` 后，同一校验器成功拒绝。

这是**完整内容一致性和原式独立整数检查**，与 11 月 1 日另一个工作线程已有的完整字节审计在科学问题上有重复，故本轮不提升其证据等级。新信息是把最新来源与**严格冻结行结构条件**统一成可执行的审议判据。

历史偏差仍然存在：10 月 24 日的原首版 CSV 没有冻结要求的每行比较标志；后补版增加了独立文件，对原首版的创建时间与字段完整性不做追溯式改写。只有经过明确接受历史偏差的正式裁定，才可将额外第三方法的成果计入有限逐项结题证据；不能静默视为原先一次性通过。

## 3. 新增十轮部分识别的证据界限

本 PR 增量已完成的 R127 十轮群体汇总研究从原论文表格推导：

* 九相邻轮次累计行动改变事件数锐界 262 至 857，绝对努力等级变化量下界 552；不能当成人数。
* **至少 100/107 个不同人**十轮中某时曾改变努力，完整合成轨迹给出可达性，较首末两期 89 个下界多强制 11 人。
* **至少 17/107 个不同人**十轮中曾选择努力1后又退出，完整合成轨迹给出可达性；不同于至少 23 次退出事件。
* 所有路径只是兼容发表边际的人工存在性证据；无个体身份或因果学习率估计。新 E2=0，新 E3=0。

这些新结果可以增强**部分识别**的知识储备，不能自动完成 original239 P0 05-003 的所有冻结验收条款。

## 4. 当前生产路径静态审计

直接读取最新 `main` 中 `.github/workflows/r127-van-huyck-1990-coordination-source-table-60-tests.yml`，Git blob `4b22f653dc7516bb31ead23e45dcf7f62261d79d`。

实数检查：文件共有 **33 行 Python `assert` 型科研/验收门槛**；使用 `contents: write`，执行 `receipt_path.write_text` 写历史已归档 CI 收据，随后使用 `git commit`、`git pull --rebase` 和 `git push origin HEAD:main`。Python 优化模式可能移除这些断言，且历史收据的重写与分支竞态存在治理风险。**这只证明潜在安全边界，没有证据证明旧实际历史 CI 曾经绕过门槛。**

合并归档的旧 PR #32 / PR #43 包含已准备的候选修复与本地测试，**正式 main workflow 当前并未采纳**。此阶段应先安排原生运行与来源身份绑定，明确是否保留冻结要求的机器 Git 收据和侧车版本，再由 owner 审核部署。

## 5. 对原目录 P0 05-003 的审议意见

本轮可支持继续使用原有 bounded 机制学习成果、精确最低努力数学与已经发表的群体描述。未获得足以**自动关闭**原目录正式待核记录的证据。

建议状态：
`RETAIN_P0_05_003_PROVISIONAL_PENDING_SCOPED_PROTOCOL_DEVIATION_ADJUDICATION_AND_PRODUCTION_GATE`。

这是**可核查的候选科学审议意见**，不是 owner 已批准的正式重定级。当前实际队列仍为 154 项，P0 27/P1 82/P2 45；本轮净关闭 0。不得通过改写 2026-10-24 冻结协议来追认历史首版 CSV。

下一项有实质价值的任务是检查 R127 现有候选生产修复能否通过针对最新 main 的原生安全测试，并确定是否可在不破坏冻结科研收据的情况下部署。若无需新的代码工程，保留 R 主线按 P0 证据审计继续；暂不为此频繁启动 Codex。

零新增费用；未调用付费 API、未执行新的生产工作流；只使用已有公开仓库标准 CI 的范围内的正常验证。原生 CI 在 PR #46 中验证的是新增部分识别程序，不能作为 R127 旧工作流安全性的通过证明。
