# S53 来源身份与数学门的组合入口

track: Codex A engineering
subflow: source-authenticated existing-gate composition
run_date: 2026-11-10 Asia/Shanghai
observed_head: e5f2baa7f6b13b1a2bf95f48ed49571f732e7611
status: COMPLETE_BOUNDED_ENGINEERING；科学验收仍 PARTIAL
ci_status: NOT_RUN；不会将空检查项当作 PASS
billing_checked: 无新 API 费用、服务、计算资源、数据购买或 CI dispatch；免费额度 NOT_VERIFIED

## 根因和复用选择

PR #3 的固定验证器能验证精确 KKT 数学证书，但明确返回 source_authentication=NOT_RUN。main 已有 R/B 的 original225_source_link_gate，检查 225 行原始来源、200 行凸目标梯度、8 世界到 S53 参数/基线的关联，并有四个 Git blob pin。旧来源报告只实际运行了 V8 mock；本轮在真实 Node v24.22.1 原生 CLI 运行，返回 225/200/25/145/8 的限定通过结果。

因此没有重写数学或来源算法。本入口组合原始 Node 来源门与固定 PR #3 数学门，并在执行前验证七个仓库文件（四个来源、来源检查程序、S53 冻结协议、历史盲态失败补充）及外部传入的 PR3 检查程序的 Git blob + SHA256。固定 pin 位于 authenticate.py；实际本次身份及命令见 evidence。固定字节来自 main 或 PR #3 head 97d5f74df5d84916917db943156120f08144f445，不来自下载时的最新浮动版本。

每个文件只读取一次，先认证，再将这些字节复制到临时目录。两条原始 CLI 消费同一份临时快照。任何认证失败、子进程非零/超时、非法 JSON、重复键或成功摘要字段/类型不匹配均返回 BLOCKED/exit 1。摘要按规范 JSON 字面比较，拒绝 bool 冒充整数。生产路径不用 assert。对调用者仅 stdout 输出 JSON，不写成功文件，避免本工具留下旧成功文件。调用者重定向输出或管理历史证据仍是调用者责任。

## 复现

本任务从最新 main 建立独立分支 codex-a/r257-s53-authenticated；与 PR #14 的清点成果分开。工作目录 /workspace/codex-a/repo。必须有 Node 与 Python 3.12，以及固定 PR3 的程序字节。代码不隐式联网或下载依赖。

```bash
# 若尚无固定 PR3 Git 对象：
git fetch origin refs/pull/3/head
# 必须导出固定 SHA，不把浮动 FETCH_HEAD 当作 pin：
git show 97d5f74df5d84916917db943156120f08144f445:research/codex_audit/r257_s53_validator/validate_receipt.py > /tmp/s53-validator.py
python3 -B research/codex_a/r257_s53_authenticated/authenticate.py . --validator /tmp/s53-validator.py
python3 -B -O research/codex_a/r257_s53_authenticated/authenticate.py . --validator /tmp/s53-validator.py
python3 -B -m unittest discover -s research/codex_a/r257_s53_authenticated -v
python3 -B -O -m unittest discover -s research/codex_a/r257_s53_authenticated -v
```

导出的验证器身份若改变则失败，无需先合并 #3。PR #1 六类反例的跨门比较已在 PR #14 完成，本包不重复其算法测试。PR #13 对象为 R074/R075 场次隔离，不与本包重叠。

## 实际测试和边界

先编写测试并对未实现认证的骨架运行：9 个方法，14 failures（含 subTest）、1 error，exit 1；原始 red.log 保存。实现后增加严格输出类型与重复键测试，最终 11 方法在普通及 -O 模式各通过，22 次成功执行。覆盖真实完整组合、七个 pin 各自篡改、等语义收据重新序列化、验证器可执行内容篡改且无副作用、缺失文件、子进程伪成功/失败、布尔计数、重复键、真实 CLI 成功/失败退出与输入前后字节不变。精确命令、exit、输出、代码 hash 见 execution.json 和日志。没有把失败开发记录计作科学反例。

组合层 source_authentication=PINNED_INPUT_AND_EXECUTABLE_BYTES_VERIFIED；原 #3 嵌套结果 source_authentication=NOT_RUN 保持原样，表示数学门自身不做来源认证，不能混淆两层。source_link 与 mathematical_gate 的原结论完整保留。

历史 blinded_prescore_order=FAIL、full_scientific_acceptance=PARTIAL。非凸世界仅结构校验，未独立重算 25 个非凸目标。R/B 原程序并未重跑整个原科研协议；本轮只调用两个检查程序。没有新真人 E2、历史 E3、盲态、外部团队复现或真实预测验证。来源身份只证明读取的字节与 pin 一致，不认证作者签名、历史执行时间、Git 提交运行先后或快照读取期间的全文件系统原子性。临时副本隔离后续输入修改，但不提供并发写入锁。Node/Python 本体沿用现有环境，不做运行时二进制认证。

## 交付与剩余工作

仅新增本专用目录；不改原数据、历史报告、冻结协议、原 R/B 或 PR3 验证器、R073/PESEN。输出身份清单和执行证据不包含密钥。现有 PR 不合并、关闭、强推。新 PR 保持草稿，不代表 main 采用。

剩余：固定版本变更要显式审阅新 pin；原生产科研 CLI 尚未调用本组合入口；Python 3.11 和全仓库测试 NOT_RUN；GitHub CI 未触发。下一有界任务为 R170 #8/#9 组合入口或整合审阅，先核对并行主体的新进展，避免重复。

内部独立上下文审阅：审阅者实际运行全部 11 项普通/优化模式测试，未发现重要问题；确认先认证再执行、同一快照、输出类型严格检查、无原文件写入。审阅时的 PLAN 勾选状态已同步。该工程审阅不属于外部团队科研复现。
