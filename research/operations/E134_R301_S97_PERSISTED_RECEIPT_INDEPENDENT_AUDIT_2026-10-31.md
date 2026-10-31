# E134 R301 S97 原始持久化证据独立字段与字节审计

日期 2026-10-31 UTC。目标键 (operations,R301,S97-v1,persisted-original-atom-risk-receipt-independent-audit)。基线 main f23038027379166a7456692a912d84a11a4f7f2f。读过 E131 静态覆盖、E132 原 B 动态20项错误接受及 R301 交接，属于已知结果后的非盲态互补复核。原始 B Python CLI 完整执行仍为 NOT_RUN。

## 实际读取与计算

通过 GitHub 连接器直接读取 main 四份真实归档文件：
research/validation/R301_S97_ALL_288_HELDOUT_ATOMS.csv，Git blob d5eabfc13aebe061dc8850f6c43b6bcfa449b922，20810字节；
research/validation/R301_S97_EXACT_HELDOUT_RESULTS.json，Git blob bd79fb56ec8a0c72593daf325fe693ba15af6a46，2831字节；
research/validation/R301_S97_RECEIPT.json，Git blob 3f343e98d754c3766f92ead28c1c600b26141f86；
research/evidence_audit/b_r301_s97_independent_segmentation.py，Git blob 527193aa8cb747696a11b204c066bc07f22511b6。

在连接器 JavaScript V8 中独立使用 BigInt 精确有理数重新核对 288 条来源的组合唯一性、字段范围、每条 weighted_brier = joint_mass × brier_loss、九组联合质量归一、九个风险聚合、oracle 与 excess 关系、证据标签及来源数量。第一次执行1197项检查，其中1194项通过，3项与SHA256实现有关的检查失败。故障原因是审计器手写 SHA256 压缩状态移位错误，标准空串和 abc 测试向量也失败，不能把初次错误摘要视为仓库数据问题。修正手写实现后独立再次执行两个标准向量、两个文件 SHA256 和两项字节长度检查，六项均 PASS。数学与结构检查首次已全部通过，九组风险精确一致。

重新计算 CSV SHA256=107c62ddab089875592717f3c3a070db8911164d50003971de5b5bf87f4bcb13；JSON SHA256=84ddaec8ff4e2f8399cd8cca1c1ef1ec99e1317fb6d5c9089083dedd8a342652；均与原始收据相符。此处实际读取 GitHub 持久化原始字节对应的 UTF-8 文本，没有通过 Python 原 B CLI 执行原始全文件命令。不能将字段聚合复核写成原生 B CLI 重放完成。R301 S97 科学验收维持 PARTIAL，数学一致性是 E1 人工源内工程复核，真人E2=0，历史E3=0。

## 当日跨轨检查

实时 main 在开工时为 f23038027379166a7456692a912d84a11a4f7f2f，R304 S100 冻结 04424fe2798d8b03efe90d582ac6a29ed0ccdbfd 在结果 f23038027379166a7456692a912d84a11a4f7f2f 前。GitHub compare 显示结果提交仅新增8份 R/A/B/交接文件。R304 216原始人工世界、1296噪声标签来源原子、B非盲态审计与8项反例为已有记录，原生Node及外部复现仍 OPEN，科学验收 PARTIAL。A轨 Xu/Potters/Suetens 2020 数据仅确认官方元数据，原始数据字节与许可未核验，不能升级 E2 或称为 R073 资格数据。

12个开放 Codex PR 已核对，PR #1 R257 S53 旧检查器问题和 PR #3 候选修复均未合并；PR #2 同步协议也未合并。R299 S95 的冻结 Python 路线与实际 JavaScript 差异仍无已核验正式批准。TH169 理论轨在本轮检查时新增4份独立文件，与本轨目标无路径冲突。未修改 original239、pending154、冻结协议、R/B/A文件、研究接受状态或其他轨交接。

## 费用、边界与待办

未触发 GitHub Actions、付费API、购买或新增订阅；实际账户账单与免费 CI 额度未核验。没有完整CI历史审计，不能推断提交没有任何CI运行。下一轮 E135 优先在可取得原始程序与原始数据字节的同一可执行环境中运行原 B Python CLI；如条件不足，记录阻塞并审计最新 R304 的未验证元数据覆盖。保留 E132 20项假阳性、R299 协议差异与 R073 第二独立真人数据门槛。
