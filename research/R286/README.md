# R286 标准TD(0)时序差分学习——原239目录02-002的P0补缺研究

**状态：CLOSED_BOUNDED_E1_SYNTHETIC_TD0_TIMING_AND_HELDOUT_BRIER**。不是新添加的第240个模型，而是原02-002 Temporal Difference Learning此前仅有早期学习卡/R063相关模仿学习机制、尚无独立主R模型学习验收的补缺。

[先冻结协议](../../protocols/R286_TD0_TWO_STATE_5_EPISODE_3_POLICY_576_ORDERED_SOURCE_PRESCORE_FREEZE_2026-10-23.md) · [完整TD0/MC/更新顺序模型源码](r286_exact_td0_learning.py) · [576个原六bit含独立未来奖励来源CSV](R286_ALL_576_ORIGINAL_TD0_SIXBIT_FUTURE_SOURCES.csv) · [九组精确风险JSON](R286_EXACT_TD0_RESULTS.json) · [SHA256机器收据](R286_MACHINE_RECEIPT.json) · [正式科学报告](R286_SCIENTIFIC_REPORT_2026-10-23.md) · [有界验收](R286_FINAL_ACCEPTANCE_STATUS.json)。

两个状态A→B→终端：每个训练回合最终奖励一个Bernoulli bit，前三个真p=1/4、1/2、3/4，每个真p完整五次训练+第六独立未来奖励六bit共64来源，三策略总**576模型标识完整来源**。未来目标必须在训练结束后保持未观察。当前研究验证标准在线TD0应先更新A、后收到当回合奖励并更新B；不与以整回合终奖更新A的MC和把B更新到A之前的错序算法混称。所有来源预测与无需模拟器的独立线性系数推导逐Fraction一致。以p=1/2为例未来Brier：标准TD0 155/512、MC 683/2048、反向错序2445/8192；**数值较低不代表机制时序正确**。只限此短链固定学习率及人工独立数据。

[正式成功GitHub Actions run39909168454](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39909168454)三个job completed/success，双Python3.11/3.12各93真实unittest共186成功，第三576原source/未来独立性/解析风险/哈希审核成功，机器人永久原CSV与结果归档[commit cdf9c6ee](https://github.com/edwardsage419/Psychohistory-Research/commit/cdf9c6ee74630e5ed1fddd26dc25e069b485281c)。

仅有数学E1，新增真人E2=0、真实历史E3=0；R073/PESEN v0.1仍冻结。正式主目录覆盖应在新239逐项映射补充表里将02-002链接到R286，R063保持相关而非取代其主归属。
