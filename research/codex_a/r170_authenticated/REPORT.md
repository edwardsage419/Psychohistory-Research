> 当前依赖与复现命令已升级，见 [PIN_REFRESH_20261110.md](PIN_REFRESH_20261110.md)。下文保留首次交付的历史版本记录。

# R170 #8/#9 强制组合入口

track: Codex A engineering
subflow: authenticated existing-gate composition
run_date: 2026-11-10 Asia/Shanghai
observed_head: e5f2baa7f6b13b1a2bf95f48ed49571f732e7611
status: COMPLETE_BOUNDED_ENGINEERING
full_frozen_extension_acceptance: PARTIAL
ci_status: NOT_RUN
billing_checked: 无新增付费 API、服务、计算资源、订阅或 CI dispatch；账户免费额度 NOT_VERIFIED

## 问题与实现

刷新 main 和全部开放 PR（#1–#15），检查既有 R170 工具及冻结条款。PR8 的完整状态比较会写出三项历史身份布尔字段，但并非强制拒绝其 false 值；PR9 是独立的强制字节门，默认 fixture 来自 PR8。本包解决二者须由调用者手动组合的障碍，没有重写数学验证器、状态适配器或身份算法。

先认证四份历史输入与冻结协议、PR8 的 runner/两个适配器及 PR9 门，共九份固定字节，均检查 Git blob + SHA256。原件只读，认证后复制到临时 inputs/tools 目录。运行固定 PR8，检查其 stdout 与 execution.json 的完整状态计数、三项身份布尔为 true、科学范围字段及类型，再把**本次新生成**的 B_full_receipt.json 交给固定 PR9。PR9 的返回、stdout/文件一致性、四来源、23004 字节、固定 SHA256 和科学边界均为成功的必要条件。两个门任一失败、缺失文件、超时、重复 JSON 键、伪成功、bool/float 类型混用都不能得到最终 COMPLETE。

输出仅 stdout，临时运行结果随快照清理，不写永久成功文件。调用者若自行重定向文件，需自行管理历史收据。没有修改 PR8/PR9 的任何字节，也不把它们视为 main 已采用成果。

## 固定来源与复现

分支 codex-a/r170-authenticated-composition，独立从 main 创建，未叠入 #14/#15。Python 3.12.14、Node v24.22.1、标准库。两个依赖 head：

- PR8：fd0d2c65084d1ef99b6040ce0464b237c38431b5
- PR9：89a64ecd2975a7fa0409f000cef45b1b2792a8b4

compose.py 的 SOURCES/CODE 是完整 pin 表。evidence/execution.json 记录实际命令、版本、前后 SHA256 和 Git blob；normal/optimized-cli.stdout 嵌套保留两门原执行收据、子命令、完整输出文件清单和哈希。未重复提交 PR8 已存储的全部状态导出大文件。

从仓库根运行（TOOLS 应为调用者选择的独立目录，不覆盖已有文件）：

```bash
# 若缺固定对象，先 fetch 对应 PR refs；工具本身不自动联网。
git fetch origin refs/pull/8/head refs/pull/9/head
r170_tools=$(mktemp -d /tmp/r170-tools.XXXXXX)
for name in run_audit.py export_js_states.js export_python_states.py; do
  git show fd0d2c65084d1ef99b6040ce0464b237c38431b5:research/codex_audit/r170_full_state/$name > "$r170_tools/$name"
done
git show 89a64ecd2975a7fa0409f000cef45b1b2792a8b4:research/codex_audit/r170_identity_gate/identity_gate.py > "$r170_tools/identity_gate.py"
python3 -B research/codex_a/r170_authenticated/compose.py . --pr8-dir "$r170_tools" --identity-gate "$r170_tools/identity_gate.py"
python3 -B -O research/codex_a/r170_authenticated/compose.py . --pr8-dir "$r170_tools" --identity-gate "$r170_tools/identity_gate.py"
python3 -B -m unittest discover -s research/codex_a/r170_authenticated -v
python3 -B -O -m unittest discover -s research/codex_a/r170_authenticated -v
```

## 实际结果与测试

完整组合输出：288 对状态分布、23328 项精确质量比较、每路线 5099 个非零状态项、576 次归一化检查；PR9 对本次 B 收据的 23004 字节和 SHA256 通过。两条真实组合 CLI 普通/优化模式均 exit 0，九个依赖及本包源文件前后 SHA256 一致。

测试先于实现：8 个方法对不做认证的骨架运行，15 failures（含 subTest），exit 1；原始 red.log 保留。最终 11 个方法在普通/-O 模式各通过，22 次成功执行，不等同于22个科学命题。覆盖真实两门及源文件不变、五个来源各自篡改、四个可执行依赖各自篡改且不执行子进程、缺失依赖、子进程失败/伪成功/重复键、比较成功后身份门失败、execution 身份布尔 false、身份结果浮点计数、CLI 非零退出。

**优化模式范围**：外层 compose.py、PR8 run_audit.py 和 PR9 identity_gate.py 使用 -O。固定 PR8 自身启动的历史 Python CLI/导出器只有 -B，没有 -O；本轮不宣称所有后代进程都使用优化模式，也没有为此改写固定 PR8。Node 无 Python 优化模式。

内部独立上下文工程审阅者重跑全部 11 测试两模式，未发现重要问题，指出上述优化传播边界，已显式记录。此审阅不是外部科研团队复现。

## 科学与操作边界

NONBLIND 内部人工 E1 工程复核；新真人 E2=0、历史 E3=0、外部团队复现=0。full_frozen_extension_acceptance 仍 PARTIAL；witness_order_compliance=NOT_ESTABLISHED。历史 witness 在两种已测试的名字排序下不一致，冻结条款未唯一规定完整排序键。本包不选择新历史 witness，不将它称为已证明的唯一排序违约，也不改变冻结协议。

嵌套 PR9 的 model_execution_this_gate=NOT_RUN 指**身份门自身**不执行模型；外层确实通过 PR8 执行两条历史模型 CLI 和两个状态导出适配器。摘要字段不能跨层混读。字节身份不是作者签名、历史运行时间或外部独立性认证。原始 111 项测试、原约 1MB 完整结果重审、全仓库测试、Python 3.11、CI 未执行。原生产科研 CLI 未自动调用此新入口。

私有临时快照稳定了认证后实际消费字节，但不提供全文件系统原子捕获或并发写入锁，运行时 Python/Node 本体沿用现有环境。本包只新增专用目录，不修改历史数据/结果、其他轨文件、R073 或 PESEN v0.1，不合并/关闭任何 PR，不强推。

下一队列：在现有 #1–#12、#14/#15 及本包获得审阅后，整理可逐项采用的调用命令与依赖，不擅自绑定历史生产入口或复写科学结论；先刷新并行 PR，避免重复建设。
