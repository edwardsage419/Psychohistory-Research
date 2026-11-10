# 候选采用与复现顺序（不执行合并）

以本轮固定 main b3b3b9a1、20 个开放草稿 PR 的快照为依据；机器可读关系见 adoption_plan.json，完整 SHA/路径/冲突见 final_sync_20261110/evidence/inventory.json。GitHub CLEAN、空 CI 检查列表、本地无文本冲突都不是科学批准，也不表示 main 已采用。

| 审阅组 | PR | 必须一起解释的内容 |
|---|---|---|
| P0 | #1 → #3 → #15 | 保留六类假阳性历史；#3 做数学证书，#15 复用 main 来源门并强制认证后调用 #3；盲态 FAIL 和科学 PARTIAL 不变 |
| P1 | #7、#5 | 覆盖完整性与持久收据绑定，独立目标、互不等待 |
| P1 | #8 → #9 → #17 | 状态比较、历史身份、强制组合；排序资格 NOT_ESTABLISHED，不能只看 #8 的 COMPLETE |
| P1 独立 | #13、#16、#18 | donor 隔离、评分泄漏、精确配对平局；原R077回归仍失败，不叠加基线执行为独立证据 |
| P1 独立 | #19、#20 | R278完整字段/协方差；R268无对数精确决策证书；不同目标，不互相替代 |
| P2 | #4、#6、#10、#11、#12 | 各目标的原生重放、结果比较和类型边界 |
| 治理 | #2 | 独立审阅同步制度；不覆盖现行用户指令 |
| 支持 | #14 | 清点、证据、离线工具；不承担科研正式验收 |

箭头表示审阅/证据关系，不一概表示 Git 合并前置条件。#15 要求 #3 的固定程序字节，#17 要求 #8/#9 固定程序字节，均可从 Git 对象导出运行。#9 默认测试 fixture 来自 #8，但允许原 B CLI 重新生成 stdout。#14 的跨 PR 测试同样读取固定 Git 对象，不要求合并它们。

## 两个已验证组合的候选调用

从完整仓库根运行，使用新临时目录，不写原科研文件，不隐式下载代码。缺固定对象时先明确 fetch 对应 PR refs；保持给定 SHA，不改成浮动最新版本。以下是候选重放命令，**不是生产 caller 已接入**的声明。

```bash
candidate_tools=$(mktemp -d /tmp/psychohistory-candidates.XXXXXX)
git show 48b9bea24a6394ae7a9cbb7d4739f151d3b85877:research/codex_a/r257_s53_authenticated/authenticate.py > "$candidate_tools/s53.py"
git show 97d5f74df5d84916917db943156120f08144f445:research/codex_audit/r257_s53_validator/validate_receipt.py > "$candidate_tools/validator.py"
python3 -B "$candidate_tools/s53.py" . --validator "$candidate_tools/validator.py"

mkdir "$candidate_tools/r170"
git show 23cf1dfb06b5c5d5341aa042937d247726473bfc:research/codex_a/r170_authenticated/compose.py > "$candidate_tools/r170.py"
for name in run_audit.py export_js_states.js export_python_states.py; do
  git show 1d8294ee81c7e23cb16bb8882ebc619089a35c65:research/codex_audit/r170_full_state/$name > "$candidate_tools/r170/$name"
done
git show 89a64ecd2975a7fa0409f000cef45b1b2792a8b4:research/codex_audit/r170_identity_gate/identity_gate.py > "$candidate_tools/identity.py"
python3 -B "$candidate_tools/r170.py" . --pr8-dir "$candidate_tools/r170" --identity-gate "$candidate_tools/identity.py"
```

本轮实际按这些固定 Git 字节重新执行两个组合，均 exit 0。前轮普通/-O 的详证仍分别保存在 #15/#17；本轮这两条候选调用只以普通模式重放，不重复计为新增算法或科研命题。R170 优化传播限制见 #17，不声称全部后代 Python 都使用 -O。

## 阻塞与检查点

- 目前未执行 17 PR 全队列逐个合并后的综合测试；190 对无文本冲突不证明整个队列顺序整合成功。
- #13/#16 的测试数来自各自已归档报告；本轮只读取并界定重叠，不伪称重新执行 B 的完整变异矩阵。
- 生产入口绑定、冻结科学验收、外部团队复现、Python 3.11、全仓库测试继续开放。
- 所有 PR 保持草稿；不自动合并、关闭或强推。不触发费用未知的 CI。

## 当前最终验证

最新main隔离副本只加载20个固定PR的新增工程路径，未覆盖任何主线文件，未生成/推送合并提交。230项局部正向方法普通/-O各通过，合计460；不是460个独立科学命题。R077原回归两模式仍各11子例失败，原始FAILED日志保留，不算PASS；#1六类旧门假阳性也仍重现。见final_sync_20261110/REPORT.md。

原用户要求“禁止自动合并”“未经确认不得直接进入main”继续有效。此处只提供可审阅的采用顺序；进入main须明确批准PR范围和顺序，并保留所有科学PARTIAL/FAIL/NOT_ESTABLISHED限制。没有CI免费额度确认，不自动运行CI。
