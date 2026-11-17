# R132 Phase A：优化模式验收保护与历史收据只读归档

日期：2026-11-17（UTC）。本轮以 main `668354c2570cc076a7e61def4a91586a7a351b43` 为起点，研究主线及冻结协议保持不变。

## 发现的真实缺口

历史工作流 `.github/workflows/r132-replicator-trajectories-source-70-tests.yml` 的第一段 Python 运行日志校验有 2 个 `assert`，第二段数学验收有 26 个 `assert`，总计 28 个。Python 优化模式会移除这些语句。在故障情形下，验收门槛可能失效；**没有证据表明历史 CI 曾使用该方式绕过门槛**。

原工作流还会覆盖 `research/R132/R132_PHASE_A_70_TEST_84_EXACT_STATES_RPS_ARTIFACT_CI_ACCEPTANCE.json` 并对 main 执行 `git commit`、`git pull --rebase`、`git push`。历史收据应保留为历史档案，不应因新的工程复算而被追认或重写。

## 实际修复范围

只修改上述 CI workflow。未改 R132 原始数学源码、70 个原有单元测试源码、科学报告、历史机器收据或任何冻结协议。

1. 将全部 28 项原有条件逐项改为执行时 `require` 显式拒绝，保持原数值阈值和原判断条件；修正正则表达式匹配对象必须显式转换为布尔值的类型问题。
2. 在普通模式（`PYTHONOPTIMIZE=0`）和优化模式（`PYTHONOPTIMIZE=1`）分别运行原 70 项单元测试，并对测试数与 `OK` 日志进行显式校验。
3. 在两种模式下分别执行 1978 年原方程涉及的有界数学检查（84 个网格状态、252 次支付平移、252 次尺度变化、RPS 与 Euler/RK4 数值对照等）。
4. 独立数学检查通过直接编译读取的源码字节执行，相关数学源码、测试源码与报告的 SHA256 均与**原历史收据记录的三项身份**核对。
5. 将新执行结果命名为 `R132_PHASE_A_V2_ENGINEERING_REVALIDATION_E1_UNCHANGED`，并仅写入 `RUNNER_TEMP` 中按优化级别分离的临时文件。旧科学收据保持原路径和历史内容。
6. 工作流权限降为 `contents: read`，取消历史 `git commit/pull/push` 步骤；每个运行器内加入 `require(False)` 预期拒绝控制，防止优化模式意外使校验函数失效。

**界限：** 原生 unittest 使用现有标准测试入口；本轮未对该入口引入额外的对抗性字节码注入测试，不能将 GitHub 新运行记录说成外部科学独立复现。本轮只验证工程执行与历史来源约束，不改变模型理论结论或 E1/E2/E3 等级。

## 实际 GitHub Actions 证据

| 运行 | 提交 | 真实结果 | 失败 / 通过原因 |
| --- | --- | --- | --- |
| [44020532355](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/44020532355) | `28e50142d0c1f7cbc5e819d3f9c2af312b3eb6f5` | FAILURE | 首次测试显示 70 项通过，但日志正则匹配对象未显式转换为布尔值 |
| [44020605202](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/44020605202) | `4c353a3cf37ce1fd97b82bc29ad4959035b20bcc` | FAILURE | 字符串替换中的特殊 `$'` 语义截断一行 YAML，工作流未能生成 job；已从原 main 文件完整重建并修正 |
| [44020775862](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/44020775862) | `73d6b3f2a2a27358e0601aef8964c13dbc69aac6` | **SUCCESS** | 两模式 70 测试均通过，两个独立数学验证步骤成功，临时工程收据 SHA256 已打印 |

最后一次成功运行的原生输出：

- 普通模式：70 tests / 0 failures；临时工程收据 SHA256 `ed67da9dc604fd52601c1cd3ba9ab3c89be103a8ef62021e35833822ae95ffeb`。
- 优化模式：70 tests / 0 failures；临时工程收据 SHA256 `97eec4c709cca8d6101045209d02b8bf9a3e9e86dac566f7768478bd3681f273`。
- 两种模式的数学验收全部通过；历史来源三文件哈希未失配。
- 没有重新写入原历史收据，没有提交数值更改，也没有执行新的真人或历史预测。

GitHub 运行器实际为标准 `ubuntu-24.04`，Python 3.11。当前公开仓库标准托管运行器在已核实的免费使用范围内。本轮没有启用收费运行器、计费 API 或云服务器。

## 状态与后续

- **COMPLETE：** R132 Phase A 的 28 项原工作流验收条件在常规和优化模式下执行；真实 GitHub CI 通过；历史收据保存；只读工作流生效于候选分支。
- **PARTIAL：** 严格对抗性多写入者、缓存伪装或任意 Python 运行时干预的安全性尚未完全证明。
- **NOT_RUN：** 原创模型熔炼、独立真人预测、历史事件 E3、正式模型重新科学验收。
- **待审批：** 合并本候选 PR 至 main。合并前以最新 main/PR 状态核对是否存在并发改变。

与此前 Phase B 修复的职责不重复：此包仅处理 R132 Phase A 工作流的剩余完整性风险。