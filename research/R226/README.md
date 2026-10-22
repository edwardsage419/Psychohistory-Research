# R226 选择与社会影响识别（09-017）：八人工网络世界完整来源结题

日期2026-10-22。原239目录09-017 P0；本轮科研E1人工模型 **CLOSED_BOUNDED_E1_ARTIFICIAL_NETWORK_SELECTION_INFLUENCE**。GitHub CI元数据存在保留异常，详情见正式验收。

[冻结协议](../../protocols/R226_SELECTION_INFLUENCE_8_WORLDS_128_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-22.md) · [科学报告](R226_SCIENTIFIC_REPORT_2026-10-22.md) · [128原结构来源CSV](R226_ALL_128_ORIGINAL_SELECTION_INFLUENCE_ATOMS.csv) · [Python完整代码](r226_exact_selection_vs_influence.py) · [八世界Fraction结果](R226_EXACT_RESULTS.json) · [SHA机器收据](R226_FINAL_MACHINE_ACCEPTANCE.json) · [正式验收和CI元数据审计](R226_FINAL_ACCEPTANCE_STATUS.json)。

两对来源世界具有**完全相同的观察联合P(E,A0,B0,B1)**，但同伴真实干预效果不同：PEER_COPY与SHARED_LATENT_SHOCK真总体同伴效果分别1和0，HOMOPHILY_ONLY与HOMOPHILY_WITH_COPY分别0和1/2。原已成边同质连接中发送者、接收者动作始终一致，缺少直接辨别模仿机制的信号支持。独立随机发送者行动的人工世界恢复行动差异支持，受控同伴效果可在该限定人工构造下解释。

[GitHub Actions run39792729144](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39792729144) 的两份实际Python job日志各显示61 tests OK（总122），第三归档作业真实日志显示全128源和两对观察等价的校验成功；[机器人归档提交f90aa32b](https://github.com/edwardsage419/Psychohistory-Research/commit/f90aa32bbc3e85eeda00b2713509af668d74da3d)完成永久保存。**审计期间GitHub run/jobs接口继续返回queued/null，与真实日志和入库提交不同**。不应将API三作业状态伪改为success；只准确声明实际日志与已入库成果。

真人E2新增0，历史E3新增0，R073与PESEN v0.1冻结。下一真实目录10-001 Classical Test Theory（R227）。沿既定顺序完成全部原R，之后统一分类和熔炼。


## GitHub API 后续状态复核（2026-10-22）

在本研究最早的真实日志完成但run/jobs仍显示queued/null的审计之后，GitHub运行总体接口后续已转为 **completed/success**。jobs详情随后显示Python3.11与原来源归档job均completed/success，但Python3.12的jobs元数据仍暂显示in_progress/null，其真实独立日志已显示61 tests OK。最终[正式验收](R226_FINAL_ACCEPTANCE_STATUS.json)新增`later_ci_metadata_audit`字段以保留前后两个真实时间截面，禁止将后一状态反写到早期审计记录。科学范围仍仅人工E1。
