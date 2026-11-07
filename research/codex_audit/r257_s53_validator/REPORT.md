# Codex R257 S53 严格数学收据检查器
run_date: 2026-10-29 UTC
track: codex; subflow: engineering-validation
status: COMPLETE（有界工程实现）；完整科学验收：PARTIAL
observed_head: c3ce3cdfff07050b0b6d496860b5c7c4310901b8

## 任务和跨轨同步
最新main新增TH122、MKT118/E087/F008。已读五份必读项目文件、最新v7.8索引元信息/154项队列、S53冻结协议、原R257验收、S53收据及盲态偏差补充、E087和market短交接。导航和README含历史快照；不据其旧“下一项”覆盖最新提交。完整读取来源身份见source_manifest.json；239项逐条科学验收未执行。
E087明确读取Codex PR #1/#2并承认其未合并，避开既有变异测试，把严格比较器留给Codex。本轮实现该互补任务，不重做其治理审计。已观察market一轨采用新交接方式，不宣称另两轨已采用或全局同步已闭环。
既有PR #1和#2仍开放；本交付不依赖它们合并，也不修改其他轨文件。没有事前盲态认领，本次在已看R/B及PR #1结果后设计检查器。

## 方法与验收范围
独立新目录下的Python标准库程序，不导入R/B原优化器。冻结参数表固定八世界、五个delta和两个step。每层检查字段及唯一完整集合；允许列表重新排序。精确Fraction验证：
- delta与C0/C身份、正容量和点的可行性；
- 目标值与点坐标一致；
- 容量松弛时lambda=0，绑定时由正坐标的互补条件求lambda；
- mu_x=2(x-a)+lambda、mu_y=2(y-b)+lambda非负及互补，构成严格凸二次目标的全局唯一最优证书；
- 基线最优值、lambda、local_derivative=-lambda、支持线下界与32项割线；
- 研究ID、E1、固定计数、零新增E2/E3、原负例标签。计数127仅校验原收据自报身份，不冒充重新数得127项检查。

生产验证使用显式ValueError，无assert依赖；CLI拒绝重复JSON键，失败exit=1/status=BLOCKED。
成功只表示数学收据检查COMPLETE，输出仍为blinded_prescore_order=FAIL，full_scientific_acceptance=PARTIAL，source_authentication=NOT_RUN。输入收据不能证明运行者、执行时间或信息隔离。原非凸例只核验标识，本轮未重审原225来源CSV/负例原始程序，因此不声称完整冻结协议验收或原R257重新结题。

## 真实测试及执行
Python 3.12.14，Linux，随机种子N/A；精确有理数、确定性输入。归档收据Git blob 37f33083b45435e18c66641ef693c6f0c779a680，SHA256 d4a33b47f4d818a8b4358a809b977c49aaad19c1656570e97947f0f3d30cd8e4。
先写测试，对no-op骨架实际执行：31项，28失败、2错误、1通过，exit=1；错误来自尚未实现的正例/CLI输出；负例明确因未抛ValueError失败。原始red.log保留，未将其计为通过。
首轮实现31项普通/-O均通过。代码审查后补互补条件专项回归：临时删除该检查，新增测试实际失败（1项失败，exit=1），恢复生产代码后完整32项在普通和-O模式各通过32，失败/错误均0，最终合计64次成功测试执行，不是64个独立科研命题。包括PR #1六类假阳性、错误minimum、可行非最优点、不可行点、错误割线、重复步长、缺失/未知世界、错误基线、计数和bool混用、float/小数/零分母、字段缺漏/额外字段、畸形结构、负例标识，以及实际CLI和-O失败退出、重复JSON键。
命令在本目录执行：
`python -m unittest discover -v`
`python -O -m unittest discover -v`
`python validate_receipt.py ../../validation/R257_S53_EXACT_RECEIPT_2026-10-29.json`
`python -O validate_receipt.py ../../validation/R257_S53_EXACT_RECEIPT_2026-10-29.json`
本目录在research/codex_audit/r257_s53_validator，退两级为research。实际本地运行使用/workspace/strict-s53/research/validation/下同名固定字节文件。普通及优化模式成功JSON一致；结果见validation.json和validation_optimized.json。
本次无完整Git检出，无法运行全仓库测试（NOT_RUN）；只对新增隔离模块运行完整发现套件，未修改现有模块。源快照通过连接器固定SHA读取；Git代理失败问题未修复、不规避网络策略。日志与execution.json保留真实环境、命令、失败和hash。

## 科学限制及交付
本次是非盲态内部不同方法数学证书核验，仅有界人工E1；真人E2=0，历史E3=0，外部研究团队复现=0。不恢复原B盲态资格，不修订冻结协议、原结果、原验收或R073/PESEN v0.1。原程序仍具旧检查缺口，新检查器须显式调用，不宣称main已经修复。
输出全部新增在research/codex_audit/r257_s53_validator/及一份research/coordination/codex/交接。专用分支及PR交付；commit/PR以最终交接为准，远端需回读，不自行合并。
ci_status: NOT_RUN，不触发Actions，提交/PR加[skip ci]。新增收费操作0；账单/免费额度未独立核验。没有外部API计算、订阅或第三方数据再分发。
next_action: 由E088或项目所有者审阅新验证器及测试；后续可做R256 Node CLI/其他跨运行时缺口，不在本轮重复或扩大科学资格。
