# A轨：Romero与Rosokha 2018公开重复博弈数据的20策略时间信息审计

日期：2026-10-27。状态：PUBLIC_SOURCE_CODE_STATIC_AUDIT_COMPLETE / ORIGINAL_CSV_ROW_AUDIT_BLOCKED / R073_EXTERNAL_E2_INELIGIBLE。

## 英文公开来源与固定身份

论文：Romero and Rosokha (2018), *Constructing strategies in the indefinitely repeated prisoner's dilemma game*, European Economic Review 104, 185–219，DOI 10.1016/j.euroecorev.2018.02.008。作者公开GitHub仓库：`https://github.com/yaroslavrosokha/sfem`，master分支。

本轮实际重新读取三个作者文件：

1. `input/action_data_RR2018.csv`：GitHub目录元数据确认文件大小1,789,540字节、Git blob `84ed4bc262757efe891683609063ca3ab00cca46`。当前工具仍未取得完整CSV正文，逐行人数、配对、场次和轮次核验继续阻塞。
2. `sfem.ipynb`：Git blob `c18a3e4746db12c2e055c8ebd93808ba1a10b77e`。原Notebook直接从上述CSV读取`subject,supergame,period,action,opponentAction`；保留supergame 31至50、每场period前20轮；将所有被选受试者的行动及对手行动组织成矩阵，并对每个受试者拟合候选策略。原作者筛选用于策略混合模型估计，不能自动当作独立测试协议。
3. `input/strategies.py`：Git blob `c013118c8a772778fdf8b08baaaea9794b0cb9b8`，实际读取10,299字节。

## 新增的实际源代码审计

本轮新增可运行静态扫描程序`research/data_scout/a_rr2018_strategy_lag_static_audit_20261027.js`和机器收据`research/data_scout/A_RR2018_STRATEGY_LAG_STATIC_AUDIT_RECEIPT_2026-10-27.json`。扫描作者20个`s01`至`s20`策略函数，发现34处显式`actions[t-1]`、`actions[t-2]`或`actions[t-3]`滞后读取，未发现任何`actions[t]`直接用于策略决定的索引表达式。20个函数都在输出端使用`out[np.isnan(actions)] = np.nan`，此掩码读取当期对手行动的缺失状态。静态结果表明策略的显式历史行动引用遵守滞后索引；若用这些函数做未来轮预测，仍须审查当期缺失状态是否在预测时已知，不能将当期对手行动或其缺失信息不加审查地纳入输入。

Notebook对全部筛选受试者估计策略混合权重，尚未看到与R073同一场次隔离标准相容的冻结训练测试分割。此为源代码静态检查，未执行作者策略的动态测试，未逐行验证CSV，也未检查原作者全部实验流程。

## 复现准备与明确阻塞

原始CSV仍受1.79MB读取限制，未取得行数、实验场次标识、subject跨session唯一性、每场supergame的配对与真实轮数、两人行动镜像、缺失模式及独立实验身份。原公开仓库没有在本轮确认独立数据再分发许可，不复制数据。论文采用不定长supergame与0.95继续概率，和R073原100轮固定协议不直接兼容。

下一步应先获取原始CSV字节并固定来源哈希，执行受试者和session分组、轮次与双方行动互证、当前轮对手信息泄漏测试；随后审查数据许可和独立实验来源。R073原模型及评分冻结，禁止用本数据后验调参。当前R073第二独立真人E2资格仍为NO，新增真人评分0、历史E3=0。无付费数据、私人信息或收费计算。
