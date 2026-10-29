# Codex R257 S53 工程审计（2026-10-29）

status: COMPLETE（本次有界检查器审计）；项目/科学总体验收：PARTIAL。
track: Codex independent engineering; subflow: receipt coverage and protocol consistency.
observed_head: b3425ef23ec9a63957a466659ad1a805c08a3566
run_date: 2026-10-29 UTC

## 问题、方法及实际读取范围

审计 B 比较器是否能证明冻结协议的完整输入身份及覆盖范围。此前已读取 R/B 输出、程序及偏差声明，本次属于非盲态工程反例测试；不声称盲态或外部研究团队复现。路径与固定 Git blob 身份见 source_manifest.json；所有来源属于本仓库，固定于 observed_head，可用 https://github.com/edwardsage419/Psychohistory-Research/tree/b3425ef23ec9a63957a466659ad1a805c08a3566 回读。未使用第三方实验数据。无随机数，seed=N/A。

先读取 README、项目规范及历史导航，结合近期8条提交、完整路径树、v7.8交叉索引及154项待核队列判断任务。v7.8 counts仍区分236主链接/3共享数学证据；不据此宣布239项科学结题。索引只检查导航与计数，未开展239项逐条科学验收。开放PR搜索结果为空；不能由此断言定时任务当前没有执行中工作。选题限于新增检查器变异反例，避免重复归档已有72项数学比较。本轮没有系统扫描其他S阶段同类缺陷。

## 实际执行与结果

环境 Python 3.12.14、Linux，标准库，命令：
`python research/codex_audit/2026-10-29-r257-s53/probe_comparator.py .`

本地固定来源位于 /workspace/audit-source，实际命令将末尾 . 替换为该绝对路径。程序自身实际路径位于 /workspace/codex-delivery 下。stdout存入 results.json；exit=0。

R程序重跑输出与完整归档JSON逐字段相等（报告127项内部断言，非127个unittest）；B原始比较返回72（不是72个unittest）。7个反例预期检查通过、失败0；其中正确拒绝错误minimum的控制1项，错误接受无效收据6项。没有将错误接受计为科学门通过。

1. 八世界全部替换为首世界的八份深拷贝，比较仍返回72，漏掉七世界。
2. 第一世界第五容量情景替换为首情景，遗漏容量仍返回72。
3. baseline_lambda改为999仍返回72。
4. delta改为999（与capacity及C0不一致）仍返回72。
5. local_derivative改为999仍返回72。
6. evidence改为E3仍返回72。

原因可直接定位于B的compare：遍历收到的列表但不校验世界/容量唯一完整集合；不校验delta、乘子、导数和证据标签。脚本末尾n==72只能核查总次数，无法证明唯一覆盖。后3项中标签是证据元数据检查需求，不能推断数学值错误。现有正确归档在本轮未发现数值不一致；这些缺口是可构造的验收假阳性，并非历史收据遭篡改的证据。

## 协议及证据声明

事前冻结要求先B计算再看R收据，偏差补充已明确失败，不能事后恢复盲态。旧B报告的INTERNAL_INDEPENDENT_EXACT_PASS必须与补充记录一起解释。B机读收据只有方法、72、错误注入及外部团队数，缺少盲态失败和协议级开放状态，也无来源哈希字段；单独消费该JSON无法获知限制。新增报告仅记录问题，不修改原协议、原程序、原收据、原R257验收或历史报告。

数学证据仍为有限人工E1；new E2=0、new E3=0。无外部独立团队复现、样本外预测、真人推断或因果验证。R073/PESEN v0.1保持冻结。新增程序是审计复现器，尚未实现严格验收器修复。

## 同步、费用及未解决事项

Git clone因继承代理proxy:8080无法连接而失败；GitHub连接器读取正常，采用固定SHA来源快照，不伪称已完整克隆或建立worktree。本地原工作区无项目检出，未修改他人工作树/索引。远端新目录在基线树不存在；仅新增专用审计文件。发布前重读main仍同上SHA。通过连接器构造增量树和专用分支；最终commit/PR与远端回读身份以本轮交接消息为准，避免自引用提交SHA。没有修改main，不合并。

ci_status: NOT_RUN。本轮未请求Actions运行；main当前SHA的runs查询为0。最近5次历史run completed/success属于其他SHA，不能替代本轮验收。提交使用[skip ci]，PR使用草稿并加skip指令，发布后还需回读实际runs。
billing_checked: 未启用任何计费API、第三方订阅或云任务，实际操作仅现有会话、本地轻量Python和GitHub仓库API；新增费用操作0。账户账单与Actions免费额度未独立核验，不触发计算工作流。

output_paths: 本目录probe_comparator.py、results.json、source_manifest.json、REPORT.md。
blockers: 原生Git网络路径失败；不阻断连接器增量交付。严格盲态B验收继续开放。
next_action: 在Codex独立目录实现显式异常、固定世界/容量集合及重复检查的严格收据检查器，用本轮6个假阳性作回归；额外检查python -O关闭assert的风险。另行设计未公开目标和信息隔离后才可开展新的盲态实验。
