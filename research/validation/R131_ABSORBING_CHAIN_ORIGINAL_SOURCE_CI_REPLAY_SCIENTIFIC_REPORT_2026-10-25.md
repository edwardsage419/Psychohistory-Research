# R131 84个精确吸收概率的正式CI重放与未修改原源码复核

日期：2026-10-25。original239 05-007。对已有R131新第三方法归档补做实际机器验证，不覆盖此前R131原始研究或冻结协议。科学证据E1。

## 事前冻结和源身份
补充冻结协议 `research/validation/R131_ABSORBING_CHAIN_ORIGINAL_SOURCE_CI_REPLAY_PROTOCOL_FREEZE_2026-10-25.md`，Git blob `148326d1e8487957725d1df1e810a665453846ff`，先于新CI创建。
独立JS源码 `research/validation/r131_independent_absorbing_chain_exact.js`，原blob `db7eed80c4210eec8c9bde1d500952da6a4873d6`；原始84行CSV `research/validation/R131_ABSORBING_CHAIN_84_EXACT_FIXATION_ROWS_2026-10-25.csv`，blob `5d2637d19abac6d963d5bac320d35c16747f4769`；原有R131 Python源码 `research/R131/r131_taylor_jonker_1978_evolutionary_game_exact.py`，blob `3c61e0c3c0fe7a6d4458eccd8fc18e9714e7152f`。全部在CI中保持未修改。

## 实际CI结果
新增工作流 `.github/workflows/r131_absorbing_chain_original_source_e1.yml`，blob `367d13806fe489b04eb78565cb829eff9670a751`。真实 GitHub Actions run `40122639038`，head `53761b1e259954388e0b628439bb5a51f3b782e7`，job `120957314032`，`completed/success`，全部作业步骤和执行日志已读取。

Node.js标准库vm实际重新执行归档JS的 `runAudit()`，核验84个内部固着概率、126个转移概率行、84个精确零残差、21个独立转写递推比较、两项负对照，并确认再生CSV与归档84行CSV逐字节完全一致。日志：`R131_JS_84_CSV_BYTE_EXACT_PASS 84 126`。

另以Python标准库核验原R131源码 Git blob身份，实际调用未修改的 `exact_project_moran_fixation_probability`，对7个N和3组适应度共21个初始单个突变者条件，与归档CSV严格Fraction相等。日志：`R131_UNMODIFIED_ORIGINAL_21_EXACT_PASS 21`。原R131 63项unittest同一作业真实通过，0失败。

正式限定状态：`PASS_BOUNDED_INTERNAL_ABSORBING_CHAIN_ORIGINAL_SOURCE_CI_E1`。已补齐此前“只在本地V8执行”和“仅转写原递推公式”的两项程序性缺口。84个内部状态并未逐项调用原Python的原递推，因为该原函数只返回初始单个突变者概率；其余状态由独立吸收链方程和精确残差检验覆盖。不得声称84项全部通过未修改原函数逐项比较。

## B方法审计与证据边界
模型参数N=2..8、适应度(3,2),(1,1),(2,3)全部预先冻结。无拟合、训练集、预测目标或泄漏风险。两种数学解法共享同一个Moran随机出生死亡假设，属于项目内部方法复核；无外部研究团队独立复现。中性1/N是精确理论对照，所有结果均为E1合成数学，新增真人E2=0、历史E3=0。数学精确概率不提供现实世界置信区间或概率校准。

不更新original239共享交叉索引或其他工作流文件。R073和PESEN v0.1冻结。仅用公开仓库免费标准Ubuntu runner、Node和Python标准库，未引入收费API、GPU、云或数据购买，未核查实际账户账单。
