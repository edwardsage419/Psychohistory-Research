# MKT032 OpenDecision 本地决策评分、校准退化与拒绝回答阈值

研究日期：2026-10-25（UTC+08）。轨道：market。状态：COMPLETE_BOUNDED_SOURCE_AND_REPORT_AUDIT。
写入前 main HEAD：cecc2c5c35150170136b4dbe902ea74b1c76217b。上一轮 MKT031；本轮没有覆盖任何既有 market、R、E、F、TH、C 文件。
外部项目：GuilhermeBianeck/OpenDecision；固定 GitHub main commit `e5e096e9a96eea14375ce5ee0554e46d7aa32eb4`。本轮只审阅英文公开资料、固定源码与作者发布的基准报告，没有下载模型权重、安装依赖、调用 API、启动 CI 或输入用户数据。

## 1. 选题去重与真实增量

MKT005 已完整审查 Dcider 的价值权重、评分、结果追踪和云端隐私。2026-10-25 再查 Dcider 英文官网，仍只提供价值重要性评分、AI 方案分析、结果回顾等高层说明；本轮未获得可核实的新算法、权重更新公式或效果验证。避免将既有 MKT005 内容重新包装为新发现。

转而选取新出现的开源候选 OpenDecision，深读固定源码 `src/opendecision/calibration.py`、`confidence.py`、`docs/calibration.md`、`docs/benchmarks.md`、`SECURITY.md`、`docs/model-licenses.md` 与同一测试集的未校准及校准报告。**新增的可检验机制：校准可以保持选项排序不变，同时改变拒绝回答的覆盖率，并在独立测试集上恶化整体 NLL、Brier 和 ECE。** 这与未来个人决策基准线的数值解释及安全退出直接相关。

## 2. 产品机制与输入输出

输入：文本或结构化状态、一个问题、至少两个有限候选项；可指定候选说明、选择阈值和差距阈值。输出：各候选原始分数、softmax 归一化分布、可选温度校准分布、最高候选、前两项概率差、拒答标志及元数据。模型后端包括 NLI、重排序器、奖励模型和本地 decoder；其原始分数具有不同训练目标，不能自动解释为个人长期选择的成功概率。

源码 `confidence.py` 实现 `softmax(scores/T)` 和最高两项概率差；`calibration.py` 默认对候选数量分别拟合温度，单一数量至少25条校准样本，缺少专属温度时回退到总体温度。温度优化目标为校准集 NLL。温度为正，所以同一候选集内的原始分数排序保持不变。拒答阈值基于变换后的概率和差距，可能改变哪些问题获得回答。

目标：在本地对有限选择作类型化评分并允许拒答。反馈与自我修正：公开文档支持离线基准、独立校准集拟合和人工更新 profile；没有证据表明产品自动从使用者真实人生结果中持续学习。解释性：输出分数、校准状态、模型身份和阈值，未提供可靠的个体反事实因果解释。费用：源码 MIT，公开仓库免费；模型权重另行下载且各有许可，部分权重体积超过 3GB，部分使用 LFM-1.0，需逐一核实。没有使用任何付费服务。隐私：正常本地评分不需要外部 API；显式 pull 才下载权重；本地 HTTP 服务默认 loopback 且无内建用户身份隔离，外网部署需额外安全网关。供应商自述无遥测，本轮未独立监测网络行为。

## 3. 固定作者报告的定量差异

两份报告均标注生成于 2026-09-18，使用同一 `tasksource/ModernBERT-base-nli` 固定模型 revision `de4ab7e77845098b7fab7f6ab9d370ddff27b19c`、相同 1726 条 test 决策、144 个基础情景、25 个语义组、相同数据 SHA256 `43c4923ea72329e0f060e88cfb10f7418e89551e29deee5edb1fef7bbeaed5a4`。其中 1158 条计入客观任务汇总。下列数值直接摘录自作者提交的报告，尚未在本轮运行模型复算。

| 指标 | 未校准 | 加载候选数分组校准 profile |
| --- | ---: | ---: |
| 客观任务准确率 | 0.675302 | 0.675302 |
| NLL | 0.912443 | 1.037868 |
| Brier | 0.480724 | 0.521642 |
| ECE | 0.153740 | 0.182994 |
| 差距阈值0.5时回答覆盖率 | 0.4706 | 0.1200 |
| 差距阈值0.5时已回答准确率 | 0.827523 | 0.589928 |
| 歧义样本拒答率 | 0.5625 | 0.989583 |

重要边界：最后三行的变化同时包含样本选择集合变化，不能解读为同一批被回答样本的正确率下降。候选数分组校准使不同候选数的 margin 失去直接可比性。报告中的同一基准集含人工构造和确定性扰动，只有144个基础情景，绝非1726个独立真人决策。作者亦明确记录该校准在 validation 上改善但在 test 上退化。该现象证明必须对部署分布重新验证校准和阈值，尚不能推出所有校准都会恶化。

报告另记录 base 后端在 robustness family 上准确率约0.4161；带权威措辞的提示注入变体对配对目标准确率的变化约为负0.3298，说明输入文本污染是独立风险。未独立执行这些注入测试。

## 4. 本轮独立轻量合成检查

在连接器执行环境中使用原生 JavaScript `Math.exp` 复刻公开 `softmax` 公式，仅针对人工 logits `[2,1,0,-1]` 检查温度 T 为 0.5、1、4 的输出。六项断言全部通过，内容为每组概率和约等于1、四个选项排名严格保持不变。

| T | top probability | top1 minus top2 | margin 0.5 是否放行 |
| --- | ---: | ---: | --- |
| 0.5 | 0.864955 | 0.747896 | 是 |
| 1 | 0.643914 | 0.407031 | 否 |
| 4 | 0.349932 | 0.077405 | 否 |

这是独立复核一个公开数学机制的合成演示，没有运行 OpenDecision 软件、下载模型或复算作者基准。不能作为产品真实性能验证。

## 5. 证据分层、局限和候选研究控制

SOURCE_CODE_E1：固定源码直接支持温度和阈值算法、模型加载及服务安全边界。
AUTHOR_BENCHMARK_E1：作者固定报告支持同分割指标对照；运行收据存在，未由本轮独立复现。
SYNTHETIC_ARITHMETIC_E1：本轮六项人工算术检查。
MARKETING_E0：诸如“客观”“已校准”“安全可靠”等超出适用数据分布的泛化主张，均不提升证据等级。
INDEPENDENT_REAL_USER_VALIDATION：未找到，状态 OPEN。新增真人 E2=0，历史 E3=0。

候选控制 MKT032-C1：保留原始分数、温度、模型及 profile SHA、候选数、阈值和拒答原因，禁止只存单一“理性分数”。
MKT032-C2：按任务、候选数量和时间段报告覆盖率与已回答正确率；对偏好和不可验证结果单独处理，不能将人工标签准确率当成人生成功率。
MKT032-C3：若某次校准在独立测试集 NLL、Brier 或 ECE 退化，保留未校准版本并标记 profile 不适用；严禁静默上线。
MKT032-C4：重大个人选择须允许拒答和人工否决，模型评分不能承担权限、支付或安全边界。
MKT032-C5：本地优先、模型文件和输入最小化；明确区分源代码 MIT 与权重许可，禁止未审查外网服务和数据外传。

以上仅是候选知识储备，不修改冻结协议，不确定唯一人生效用权重，不提前开发个人决策产品。

## 6. E 当日治理增量

本日已存在 E002 和 E003 实质只读审计。本轮读取其原文、F001、MKT005/MKT031、最新 main 近期提交和 R161 研究记录，避免重复创建 E004。

R161 新增第三方法协议先冻结于 `4761f0e87f97d9975d0d80bb012047cafa383c23`，随后主算法和 B 轨独立算法形成 8 核、48 人工初始世界的期望吸收时间内部 E1 证据。最新 B 轨纠错提交 `43b696b60ecf23c4d8c0d281832ab9139e0071db` 说明：早期 B 报告把两项布尔哨兵判断称为“负对照已检测”，实际上未执行错误变异计算。随后 `r161_b_mutant_controls.js` 真实执行两个变异，登记 16/16 与 32/32 检测。应将早期两项标为 UNSUPPORTED_SENTINELS，实际执行的48项标为新增 E1；原 B 审计文本仍有未经纠正的字面“detected”描述，必须阅读后续更正，防止下游报告误引。该更正是透明的追加证据，不倒填首次验收。直接查询纠错提交关联 Actions，total_count=0；新增方法 remote CI NOT_RUN，不能宣称远端成功。

直接读取 original239 v7.8：239条、逐项证据审计待办154条；内部日期字段仍为 2026-10-24，与文件名2026-10-25不同。R136 冻结负对照 FAILED_NONDISCRIMINATING 继续 OPEN。R 主线未见本轮被改写；未做全仓冻结文件逐字节审计，不能断言全仓无意外改动。没有修改其他轨、索引、协议或研究结果。

## 7. F 本周专题与归档边界

2026-W43 F001 已归档，覆盖人工否决、解释和最小采集；本轮无重复专题。为 F002 登记新的候选风险：本地服务若意外暴露公网会扩大敏感状态访问面；归一化分数可能被误解为真实成功概率；不同候选数共用拒答阈值可能制造系统性选择偏差。F002 应与授权撤销、缓存、衍生数据删除共同研究。未接入真实敏感数据。

本轮主动新增费用为0。账户账单、免费额度未独立核验。未注册、购买、运行计费 API、租用云或 GPU、触发 CI。GitHub 仅按 market 独立路径追加本文件。提交 SHA 由写入结果及随后远端回读核验，不预填。

## 8. 原始来源（全部英文）

Dcider 官网：https://dcider.app/
OpenDecision 固定版本：https://github.com/GuilhermeBianeck/OpenDecision/tree/e5e096e9a96eea14375ce5ee0554e46d7aa32eb4
校准源码：https://github.com/GuilhermeBianeck/OpenDecision/blob/e5e096e9a96eea14375ce5ee0554e46d7aa32eb4/src/opendecision/calibration.py
置信度源码：https://github.com/GuilhermeBianeck/OpenDecision/blob/e5e096e9a96eea14375ce5ee0554e46d7aa32eb4/src/opendecision/confidence.py
校准说明：https://github.com/GuilhermeBianeck/OpenDecision/blob/e5e096e9a96eea14375ce5ee0554e46d7aa32eb4/docs/calibration.md
基准设计：https://github.com/GuilhermeBianeck/OpenDecision/blob/e5e096e9a96eea14375ce5ee0554e46d7aa32eb4/docs/benchmarks.md
未校准报告：https://github.com/GuilhermeBianeck/OpenDecision/blob/e5e096e9a96eea14375ce5ee0554e46d7aa32eb4/benchmarks/reports/base-mps-test.md
校准报告：https://github.com/GuilhermeBianeck/OpenDecision/blob/e5e096e9a96eea14375ce5ee0554e46d7aa32eb4/benchmarks/reports/base-mps-test-calibrated.md
安全说明：https://github.com/GuilhermeBianeck/OpenDecision/blob/e5e096e9a96eea14375ce5ee0554e46d7aa32eb4/SECURITY.md
权重许可：https://github.com/GuilhermeBianeck/OpenDecision/blob/e5e096e9a96eea14375ce5ee0554e46d7aa32eb4/docs/model-licenses.md
R161 B 更正：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R161_NEGATIVE_CONTROL_EXECUTION_CORRECTION_ADDENDUM_2026-10-25.md

下一项 MKT033：审查 OpenDecision 在提示注入、候选数量变化和拒答阈值下的实际测试覆盖与源代码保护边界；若无可核实新证据，转向 ARDA 或新的本地决策日志开源项目。E 继续只读检查 R161 纠错传播，F 在新周启动 F002。核心顺序维持 R 系列全部完成、系统归纳、模型熔炼。