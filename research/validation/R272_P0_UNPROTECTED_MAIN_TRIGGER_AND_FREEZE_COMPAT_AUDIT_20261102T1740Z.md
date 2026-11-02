# R272 P0：main 强制验收约束及真实触发覆盖的独立核验

track: R+B
subflow: P0 production enforcement independent metadata review
run_date_utc: 2026-11-02
local_date: 2026-11-03 Asia/Singapore
target_key: (R+B,R272,2026-10-23-prescore-freeze,production-required-checks-and-path-trigger)
observed_main: 94ebed32b11f9b88acd8b6041b4801e6a5638936
status: COMPLETE_BOUNDED_READONLY_API_AND_TRIGGER_AUDIT / PRODUCTION_P0_OPEN
evidence_grade: INTERNAL_NONBLIND_E1_ENGINEERING_METADATA_ONLY
CI: NOT_RUN
billing_checked: ACCOUNT_BILLING_AND_ACTIONS_FREE_QUOTA_NOT_VERIFIED
paid_actions: NONE

## 1. 新增且经实时 API 确认的 P0 事实

GitHub REST `GET /repos/edwardsage419/Psychohistory-Research/branches/main` 返回 `protected=false`、`required_status_checks.enforcement_level=off`、`contexts=[]`、`checks=[]`。同一时点 `GET /repos/.../rulesets` 返回空数组。由此可以确认该时点 main 没有通过这些配置强制执行状态检查。未调用管理员写接口，未改变分支设置。

这是生产强制验收关闭条件的实际阻塞。即使未来候选工作流执行成功，当前分支配置也不能证明科研验收是 main 合并或写入的必经关口。当前生产工作流仍是 blob `3132b08cf4ee64b55f5112d2249894ea0ec9d42d`，候选 YAML blob `a84b3d13d7d6bc8da45dc523454d7804520ca79c` 仅位于研究目录，尚未采纳。此结论只针对所读时点，不代表后续设置不变。

## 2. 实际触发路径独立对照

直接解析生产和候选 YAML 的 `paths`，用严格相等和 `/**` 目录前缀规则对六个具体文件逐项比较：

| 文件 | 当前生产 push 触发 | 候选 push/PR 触发 |
| --- | --- | --- |
| `research/R272/R272_MACHINE_RECEIPT.json` | NO | YES |
| `research/R272/R272_EXACT_RESULTS.json` | NO | YES |
| `protocols/R272_OUT_OF_SAMPLE_9_BERNOULLI_WORLDS_576_FULL_SOURCE_PRESCORE_FREEZE_2026-10-23.md` | NO | YES |
| `research/validation/r272_single_entrypoint_failclosed_20261102.py` | NO | YES |
| `research/R272/r272_exact_train_test_prediction.py` | YES | YES |
| `.github/workflows/r272-exact-train-test-oos-e1.yml` | YES | YES |

当前生产 `push.paths` 只包含 R272 原生成器和自身 YAML，六个样本文件中仅2个命中；收据、结果、冻结协议及新单入口的单文件变更均不会因这些路径触发该工作流。候选覆盖6/6，但 `paths` 是触发筛选，无法代替受保护分支的必需状态检查。当前生产无 `pull_request` 触发，候选具有。

本轮未制造真实 GitHub push 事件，触发结果是依据 GitHub YAML 路径规则的离线确定性判定。没有证据证明历史上某次恶意修改已被合并或 CI 曾错误接受。

## 3. 冻结协议与单入口候选兼容性待审

冻结协议 blob `9fbdb0078a58c4a9c0a548643227e30da5731119` 在“三路线和验收”段要求三 job 全部 completed/success，第三路线需重新解析完整576行原始 CSV。候选 YAML 定义一个 job，使用 Python 3.11/3.12 矩阵；内部单入口调用独立验收器。历史三 job 成功记录需要原样保留。生产替换方案是否保持冻结的三 job 验收口径，尚需逐条审查；不能仅以候选静态测试 PASS 宣称冻结兼容或追认历史结题。

## 4. 实际验证、反例及限制

新增标准库离线审计程序 `r272_production_enforcement_readonly_audit_20261102.py`，读取本轮公开 API 规范化快照，计算触发矩阵和保护配置。独立执行 CPython 普通、`-O`、`-OO` 三模式，均 PASS。每模式十项确定性检查：观察到的保护、状态检查、规则集、事件、2/6触发覆盖，以及“仅打开保护而没有必需检查”“保护且增加必需检查”“存在未解析规则集”等条件控制。程序不用 `assert` 作为验收条件。共三模式各十项检查，不等同于30次 Actions。

限制：快照是 API 字段的规范化摘录；当前未读取 GitHub 账单、未在完整 checkout 执行 R272 单入口、未安装生产 YAML、未触发 Actions、未更改 branch protection。真实强制执行还取决于分支规则、必需检查身份、路径过滤、维护权限和费用核实。历史 R272 E1 有限数学结果保留，新增真人 E2、历史 E3 均为0。

## 5. 队列、去重和建议关闭条件

original239 v7.8 blob `36f24235901172642c46853298aebb421f1a3552`，待核 CSV blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`。逐行解析154项，P0=27、P1=82、P2=45，净减少0。Codex PR #1/#3 的 R257 S53 仍属于未合并候选，未将其计作 main 验收。E168 已审查当前生产 YAML 写权限和归档前生成，本轮新增证据集中在实时分支保护与强制检查缺失，不重复 E 的治理实现。

下一步先在可信完整 checkout 完成 R272 单入口原生执行和错误注入；由 owner/维护者审查工作流替换是否保留冻结三 job 口径、固定第三方 Actions SHA、移除生产写回权限。核实零新增 CI 费用后再决定采用和配置 required checks，并独立回读生效规则。未经上述验证，R272 P0 保持 OPEN。

公开来源：
* https://api.github.com/repos/edwardsage419/Psychohistory-Research/branches/main
* https://api.github.com/repos/edwardsage419/Psychohistory-Research/rulesets
* https://github.com/edwardsage419/Psychohistory-Research/blob/main/.github/workflows/r272-exact-train-test-oos-e1.yml
* https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/r272_single_entrypoint_caller_candidate_20261103.yml
