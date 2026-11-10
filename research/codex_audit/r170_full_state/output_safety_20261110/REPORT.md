# PR8 R170 完整状态重放的输出别名保护

track: Codex A engineering
subflow: standalone replay output safety / dependency compatibility
run_date: 2026-11-10 Asia/Shanghai
base_pr8: fd0d2c65084d1ef99b6040ce0464b237c38431b5
status: COMPLETE_BOUNDED_LOCAL_FIX；远端交付以本提交及最终回读为准
ci_status: NOT_DISPATCHED
billing_checked: 无付费API/资源/订阅/依赖安装/CI；免费额度NOT_VERIFIED

## 问题与复用修复

刷新main、19个开放PR及#17 review（空）。#19为Codex B的R278完整收据/协方差检查，与本轮R170文件写入不同，不重复实现其数学核。

在临时来源副本中，5个真实CLI负例（首JSON stdout symlink、stderr symlink、stdout hardlink、execution.json alias、悬空stdout symlink）对旧runner全部失败；其中JSON stdout会把副本中的B历史执行摘要覆盖为R重放收据，stderr会截断副本来源，悬空链接会向副本来源目录添加文件。execution别名本应拒绝而旧版本接受。raw red.log保留；真实科研文件未做变异，不推断历史数据已被篡改。

复用#4固定提交9ba7e2ad24a0936e7893e9721e1c806e29053286已审阅的lstat/nlink预检与同目录临时文件replace函数，仅将check适配为require。R170 stdout不是label.stdout，而是四份具名JSON：R_replayed_receipt.json、B_full_receipt.json、JS_full_state_export.json、Python_full_state_export.json。显式枚举上述4文件、4个stderr及execution.json，共9目标。

全部预检在mkdir、旧成功撤销和任何子进程之前。已有目标仅允许单链接普通文件；symlink（含悬空）、hardlink与非普通文件拒绝。日志和最终收据写前再检查，以原子替换发布。未改状态/数值/收据判断、适配器、历史witness或排序约定，没有新增共享运行依赖。

不安全别名拒绝时优先保护输入，旧路径可能仍保留COMPLETE内容；必须检查本次退出码与新收据身份，不能把旧文件当作本次成功。正常普通输出的失效/覆盖语义保留。每轮使用新且稳定的输出目录，并发使用不同目录；本补丁不提供父目录并发锁或历史日志的永久留存。

## 实际验证

- 原10+新5共15个方法，普通与-O各通过，共30次成功执行；直接执行测试文件也覆盖15项。
- 完整新replay exit0，执行2条历史模型CLI和2个状态导出器；288对完整分布、23328项精确质量比较、每路线5099非零项、576归一化检查保持。
- 四份历史输入前后SHA256相同，Git blobs与最后抓取main相同；两适配器未修改。具体code/source hash、命令、输出清单及完整收据见evidence/execution.json/replay-execution.json。
- 独立上下文内部审阅者实际重跑两模式15项，无发现；确认9输出覆盖完整，数学和witness逻辑未改。

```bash
python3 -B -m unittest discover -s research/codex_audit/r170_full_state -v
python3 -B -O research/codex_audit/r170_full_state/test_full_state.py -v
python3 -B research/codex_audit/r170_full_state/run_audit.py . --output /tmp/new-r170-safe-output
```

示例目录需新建或明确允许覆盖，不指向历史归档。优化模式覆盖测试和runner；原runner调用的历史Python子进程保持原-B参数，不能推广为所有后代都使用-O。原111项/约1MB结果重审、全仓库、Python3.11与CI未运行。

## #9 / #17 依赖实测

本轮没有修改#9/#17或放宽任何pin。额外功能检查独立计数，不当作新增科学结果：

1. 固定#9（89a64ecd2975a7fa0409f000cef45b1b2792a8b4）实际验证新runner生成的B_full_receipt.json，exit0，23004字节、固定SHA256和四来源身份一致；full_frozen_extension_acceptance仍PARTIAL。
2. 固定#17（c37470c24bc3e85059c768ed7cb15a235cc50552）加其原固定#8（fd0d2c65）与#9执行，exit0。原组合仍可通过导出固定Git字节运行，不依赖最新#8分支。
3. 把本次新runner交给同一个旧#17，exit1/status=BLOCKED，原因明确为run_audit.py身份不匹配；在新代码执行前拒绝。这是预期版本保护，不是科学计算失败。记录在pr17-refuses-new-runner.stdout。

旧#17把旧runner放入新建私有临时输出目录，因此本次直接调用的预置输出别名实验没有改变其已验证使用场景。新runner并不会自动成为#17依赖；如果下一包更新pin，必须显式记录新版本并重跑组合/篡改回归，不能以浮动head替代固定SHA。

## 交付与科学边界

独立分支codex-a/r170-output-safety，目标快进更新现有 https://github.com/edwardsage419/Psychohistory-Research/pull/8 。先核对原head未并发变化；不新增重复PR，不合并/关闭/强推。只改Codex runner/test并新增本日期证据；原报告、日志、历史提交、R/B科研程序、原数据、冻结协议、R073/PESEN保持。

NONBLIND_INTERNAL_ARTIFICIAL_E1；新E2/E3/外部团队复现0。排序资格NOT_ESTABLISHED、完整冻结扩展科学验收PARTIAL不变；不替换历史witness，也不声称某一排序解释已唯一证明协议违约。字节身份不是作者签名、历史时间认证或真实预测验证。

剩余：owner/reviewer采用决定、可另行验证的#17新pin版本、生产caller绑定及费用未确认的CI。不能把本次写入保护当成上述事项自动完成。
