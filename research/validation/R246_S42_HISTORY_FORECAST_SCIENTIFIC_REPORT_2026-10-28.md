# R246 S42 四格人工事件的历史信息与下一格Brier预测研究

日期：2026-10-28（Asia/Singapore）。证据等级：E1_SYNTHETIC。原R246正式科学资格保持 `CLOSED_BOUNDED_E1_FINITE_BERNOULLI_EVENT_SELF_EXCITATION_SURROGATE`。

## 先行冻结与不可变来源

先行协议 `protocols/R246_S42_HISTORY_FORECAST_BRIER_PRESCORE_FREEZE_2026-10-28.md`，独立提交 `350d3fcb6853716fb442263f63916615aec1fa9c`，先于本轮计算和结果归档。原R246九人工世界、四格观察事件和4608条完整外生来源不变。R轨使用原 `research/R246/R246_EXACT_RESULTS.json` Git blob `8aec1fd3f6dba6073f03e74f8f854f7d6a46a6c3`，B轨独立使用 `research/R246/R246_ALL_4608_ORIGINAL_BINNED_EVENT_SOURCES.csv` Git blob `f817b78f833cf13ea589bc5ab732bc6947d66a3a`。

研究问题：仅观察第4格以前的二元事件，历史长度能否改善预测第4格事件Y4。合法信息集依次为F0空、F3=(Y3)、F23=(Y2,Y3)、F123=(Y1,Y2,Y3)。全部预测为已知人工完整概率分布下的条件概率oracle，精确有理数Brier损失。禁止把未来Y4、隐藏U、生成hazard、隐藏真实事件H或外生随机位输入合法预测。

## 真实执行与九世界结果

R轨从冻结的完整16格联合PMF计算 `sum_x P(x) P(Y4=1|x)(1-P(Y4=1|x))`，仅对正概率条件组评分。隔离JavaScript V8环境实际执行R轨源码，458项显式检查全部通过，失败0。

| 冻结人工世界 | F0 | F3 | F23 | F123 |
| --- | ---: | ---: | ---: | ---: |
| IID_LOW | 3/16 | 3/16 | 3/16 | 3/16 |
| IID_HIGH | 3/16 | 3/16 | 3/16 | 3/16 |
| SELF_EXCITING_LAG1 | 255/1024 | 3/16 | 3/16 | 3/16 |
| REFRACTORY_LAG1 | 3927/16384 | 115/512 | 115/512 | 115/512 |
| STATIC_LATENT_RATE_MIXTURE | 1/4 | 15/64 | 9/40 | 195/896 |
| ALTERNATING_EXOGENOUS_RATE | 3/16 | 3/16 | 3/16 | 3/16 |
| COMMON_SHOCK_ALL_BINS | 1/4 | 0 | 0 | 0 |
| STATIC_HIDDEN_SELF_EXCITING_SENSOR_ALIAS | 255/1024 | 3/16 | 3/16 | 3/16 |
| SELF_EXCITING_TWO_LAG | 16023/65536 | 219959/998400 | 213/1024 | 213/1024 |

预冻结假设全部满足。三个独立时间格事件世界没有历史收益；一格自激世界仅Y3已足够，F0到F3改善63/1024。两格自激世界从F3到F23再改善3071/249600，F23到F123改善0。稳定隐藏率混合世界三个历史增量均为正，分别为1/64、3/320和33/4480，说明过去的可见事件逐步帮助推断未观察到的固定类别。共同冲击世界Y3完全揭示未来Y4，F3风险为0。

同一原外生source下，SELF_EXCITING_LAG1和STATIC_HIDDEN_SELF_EXCITING_SENSOR_ALIAS的四格观察Y完全一致，全部预测风险也相同，然而后者人工真事件H始终为0。观察预测能力不能独立鉴别事件自激机制和观测报告器伪事件机制。

## 科学审计与限制

B轨独立从4608条原CSV按观察前缀计数，计算组内成功数s、样本数m的精确风险贡献 `s(m-s)/(512m)`。B轨36项风险、27项历史收益与R轨全部一致，详见B轨审计。只计入正支持的条件组；COMMON_SHOCK在F23/F123仅两个可达前缀，未虚构不可达条件概率。全部世界风险随合法信息增加非增。人为使用未来Y4可令风险为0，已作为泄漏负例单独隔离。

本研究的概率校准只在人工已知分布内按定义成立，未检验真实人类样本外预测、真实点过程参数、时间连续强度、因果干预或长期历史演化。原R246每格最多发生一次Bernoulli事件，不能称为真正Poisson或Hawkes连续时间点过程的复现。新增真人E2=0、历史E3=0、外部独立复现=0。R073冻结评分和PESEN v0.1均未改变。

## 复算与费用

R脚本：`research/validation/r246_s42_observed_path_brier_20261028.js`。
R机器收据：`research/validation/R246_S42_HISTORY_FORECAST_EXACT_RECEIPT_2026-10-28.json`。
B脚本和收据在 `research/evidence_audit/`。执行方式：`node research/validation/r246_s42_observed_path_brier_20261028.js`，默认读取原R246 JSON；B轨见对应审计。当前已在隔离V8实际运行归档同源程序逻辑；独立Node.js CLI与新增GitHub Actions未运行，CI状态须单独查询。主动新增费用0，实际账单及免费额度未独立核验。

研究顺序：完成全部R系列逐项学习与正式验收，随后统一归纳分类，最后模型熔炼。个人辅助决策产品继续暂停。
