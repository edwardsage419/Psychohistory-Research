# E131 R301 S97 元数据绑定范围与跨轨科研治理审计

UTC 2026-10-30。目标键：(operations, R301, S97-v1, receipt-metadata-gate-and-cross-track-integrity)。初始 main 0534e0e2a7dff15b5ab6442b27f6027b99ef04cf，审计期间 main 因理论轨提交前进。状态 PARTIAL_NONBLIND_READONLY_AUDIT_WITH_SUPPLEMENTARY_GUARD。原始R/B冻结协议、结果、索引和代码保持不变。

## 实际读取与验证
R301 S97冻结提交 b18d1cd4e149a60ebfe3732f38f09f1cb6d94e7a；结果提交 f8d63599598caab1fbe4209724bbc3247ee410cd，冻结先于结果。读取 main 持久化 CSV blob d5eabfc13aebe061dc8850f6c43b6bcfa449b922、结果 JSON blob bd79fb56ec8a0c72593daf325fe693ba15af6a46、原B检查器 blob 527193aa8cb747696a11b204c066bc07f22511b6、机器收据及R/B报告。R/A/B交接及TH166理论轨最新交接均已读取。此次为已看结果后的非盲态核查。

本轮独立 JavaScript BigInt 有理数核算了持久化288行、288唯一 (true_hazard, assumed_hazard, history, future_outcome) 键、48个真实风险率与四位历史组合；逐行复核联合质量、Brier损失、加权Brier，错误0。重新聚合9组精确风险并与持久化JSON逐项比较，9/9全等；真实风险率1/2而假设0的风险113/432。初次审计脚本出现BigInt默认分母类型错误，修正后完整重跑通过。此项是内部非盲态跨文件算术复核，与B轨独立分段枚举不同；没有执行原始Python CLI，也没有重新计算机器收据SHA256。

## 新增静态检查器覆盖问题
检查原始 B 文件中 check(rows, results) 的实际字段访问，以下8个结果元数据字段未被读取或绑定：research_id、extension、freeze_commit、external_team_replication、history_length、heldout_length、source_atoms、distinct_true_atoms。load(folder) 使用收据中的文件长度和SHA256，但没有将 receipt.freeze_commit 与冻结提交绑定，也没有要求 receipt.files 的键集合恰为预定两个文件名。

因此，原检查器的数学验证与文件字节验证不能单独证明这9个来源与范围元数据字段正确。本轮只做原始检查器静态覆盖确认，尚未运行原始检查器的实际篡改反例，不能宣称已动态复现其错误接受。当前归档原始字段值与冻结提交一致，没有发现已保存数学结果错误。

新增互补保护程序 research/operations/e131_r301_s97_metadata_gate_20261031.py，原生Python 3.13.5标准库执行人工元数据正例1项、8个结果字段的修改/删除16项、收据冻结提交的修改/删除2项，合计20项断言，18个错误输入全部拒绝。程序可使用 --folder 检查真实文件的元数据及长度/SHA256，但本轮未对原始持久化文件执行该命令。此程序仅为候选附加保护，未修改B轨原检查器或科学验收。

## 当日跨轨核对
R主线最新R301 S97为PARTIAL_NONBLIND_INTERNAL_E1，B轨内部非盲态独立分段审计已记录288项精确对应，科学有效性与归档完整性分开；未建立外部团队复现。A轨R073第二独立真人数据集仍受原始文件访问、许可与逐轮身份核验限制；不提升E2。理论轨TH166为独立理论候选研究，未见与本轨路径重叠。原239索引与pending154由R交接报告称未变化，本轮没有独立重哈希，不能将其当作本轮验收。

开放Codex PR共12项，PR #1的R257 S53检查器问题与PR #3候选修复仍OPEN且未合并，PR #2协调协议亦未合并。R299 S95先前发现的Python冻结要求与JavaScript实现差异保留为开放历史问题，本轮未完成新的正式裁决检查。没有改动其他轨、共享索引、冻结协议或原始收据。没有触发Actions；所有运行成功与科学验收边界分别记录。未执行仓库全量同名冲突扫描、账单审计或所有历史CI复核。新增真人E2=0，历史E3=0。

## 下一项
E132优先检查R302新阶段或R301 S97原始检查器真实元数据篡改运行，且需先确认目标键和最新main，避免重复R/B工作。R299 S95正式偏离裁决继续保留待核。
