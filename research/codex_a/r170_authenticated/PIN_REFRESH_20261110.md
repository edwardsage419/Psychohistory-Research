# PR17 固定依赖升级：采用 PR8 输出安全版本

track: Codex A engineering
run_date: 2026-11-10 Asia/Shanghai
base_pr17: c37470c24bc3e85059c768ed7cb15a235cc50552
new_pr8_pin: 1d8294ee81c7e23cb16bb8882ebc619089a35c65
unchanged_pr9_pin: 89a64ecd2975a7fa0409f000cef45b1b2792a8b4
status: COMPLETE_BOUNDED_PIN_REFRESH；远端以本提交和回读为准
ci: NOT_DISPATCHED；无新增付费操作

当前CLI依赖以上新PR8版本；原REPORT.md记录的是首次交付的旧版本，不用旧示例替代本迁移命令。原历史证据保留；首次artifact清单另存pin_refresh_20261110/evidence/previous_artifact_hashes.json，其条目应对原提交c37470c校验，不是对当前文件校验。

## 变更与测试

仅更新CODE中run_audit.py的Git blob/SHA256，以及测试fixture的固定PR8 SHA；两适配器、PR9、五份来源pin、状态/数值/收据/排序验收代码均不改。新增pinned_pr8_commit/pinned_pr9_commit记录pin来源，指固定代码来源版本，不声称查询了用户运行目录的HEAD。

新runner blob=2573ba5d823449dff43c038bce61754baeea8184，SHA256=58318bfe802d7e5b77fb5f75093398afe89cd9820c004bbacc7b3a8c835fab27。原旧runner不会被新CLI静默接受，专门回归验证此策略；没有兼容性自动降级或浮动head下载。

先更换fixture和加入旧runner拒绝测试，保留旧生产pin，12方法实际7失败/2错误；red.log保存。更新pin后12方法普通/-O各通过，24次成功执行，两个真实CLI组合也通过；五来源与最新抓取main b3b3b9a1的Git blobs一致。精确命令、版本和代码SHA在pin_refresh_20261110/evidence。内部独立上下文审阅复核全部4个执行文件pin、重跑12测试两模式，无代码问题；PLAN.md的旧依赖说明已同步。

## 当前复现

在仓库根，缺对象时先fetch对应PR，使用新临时目录：

```bash
r170_tools=$(mktemp -d /tmp/r170-pins.XXXXXX)
for name in run_audit.py export_js_states.js export_python_states.py; do
  git show 1d8294ee81c7e23cb16bb8882ebc619089a35c65:research/codex_audit/r170_full_state/$name > "$r170_tools/$name"
done
git show 89a64ecd2975a7fa0409f000cef45b1b2792a8b4:research/codex_audit/r170_identity_gate/identity_gate.py > "$r170_tools/identity_gate.py"
python3 -B research/codex_a/r170_authenticated/compose.py . --pr8-dir "$r170_tools" --identity-gate "$r170_tools/identity_gate.py"
python3 -B -O -m unittest discover -s research/codex_a/r170_authenticated -v
```

12方法包含新旧版本隔离、认证前拒绝篡改、缺文件、源保持、真组合、身份门失败、false身份字段、伪成功、重复键和浮点计数拒绝。原PR8自身15方法的证据属于#8，不重复算进此处。-O仍不等于每个历史后代进程均使用-O。

排序资格NOT_ESTABLISHED、科学PARTIAL、非盲态内部E1及新E2/E3/外部团队复现0不变。未改科研文件、历史数据、冻结协议、R073/PESEN；未绑定生产caller或合并任何PR。该工程升级不恢复盲态或验证真实预测。全仓库/原111测试/Python3.11/CI未运行。
