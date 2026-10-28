# A轨：OpenNeuro ds007822 33个匿名槽位完整行为事件复核及作者论文来源闭合

日期：2026-10-29（Asia/Singapore）。本报告为既有 A_OPENNEURO_DS007822_33_TRIAD_40_TRIAL_EVENTS_PROVENANCE_LICENSE_GATE_2026-10-29.md 的增量。仅保存公开匿名行为的汇总统计和Git blob标识，不复制参与者级原始记录。E2正式预测新增0。

## 新增一手论文证据
Kim, H., Jun, S. C., & Nam, C. S. (2026), *A reproducible EEG hyperscanning dataset for triadic social decision-making during an iterated 3-player Prisoner's Dilemma*, Data in Brief 68, 113064。DOI https://doi.org/10.1016/j.dib.2026.113064 ，PubMed https://pubmed.ncbi.nlm.nih.gov/42541318/ 。论文明确将11个三人组、33人、每人40次决策与OpenNeuro数据集 DOI https://doi.org/10.18112/openneuro.ds007822.v1.0.0 关联；报告GIST实验采集来源、EEG同步设备及1=合作、2=背叛的行动编码。论文作者来源与公开数据集标识之间的引用关联现已找到，替代上一轮“未找到作者论文”的状态。仍未独立核验原始采集链及每名受试者的真实性，故证据级别仅为公开论文与文件交叉验证。

## 本轮实际逐行检查
从 https://github.com/OpenNeuroDatasets/ds007822 的 main 分支实际读取全部33个 `task-pddecision_events.tsv`，11组三人、每人40条，合计1320条。逐行检查八列字段、组号/槽位与路径一致、trial为1至40、duration=4.0、onset=4×(trial−1)相对秒、choice仅1或2、triad_outcome与个人choice的标签映射。每组三个槽位同轮均有记录。所有文件读取成功；字段或时间结构异常0，缺失轮次0。

| 范围 | 文件 | 决策 | 合作 | 背叛 | 三人选择不一致的组内轮次 | 全体同选的组内轮次 |
|---|---:|---:|---:|---:|---:|---:|
| G01至G03 | 9 | 360 | 262 | 98 | 39 | 81 |
| G04至G06 | 9 | 360 | 269 | 91 | 44 | 76 |
| G07至G09 | 9 | 360 | 278 | 82 | 54 | 66 |
| G10至G11 | 6 | 240 | 215 | 25 | 23 | 57 |
| 合计 | 33 | 1320 | 1024 | 296 | 160 | 280 |

440个组内轮次中160个出现不同参与者行动，然而原始文件中每行的`triad_outcome`始终与该行个人choice相同，1320次映射检查0不一致。因此这个字段不应作为三人共享结果直接使用；计算三人组合行动需先以group+trial连接三个槽位。每组40轮是相对实验序号，4秒onset是事件相对时间；绝对采集日期未知。三人同组的40轮具有依赖，推断时独立单位最多为11个三人组，不能将1320条记录当1320个独立真人样本。

### 原始Git对象身份
九组新增24个文件及原九文件全部实际读取，以下为每组三个槽位依S01/S02/S03顺序的Git blob SHA：
G01: 594269370f3bb11ed54b5c02ff978fb762de5381, 9aff7fc7ca02f36fe250f607fca4e96e8689695e, a2908aa3237c757cbf5a53724a48158696846821。
G02: 5f58698e8b1cdf51af82653554512106ad159ea7, 5b5a20a6b2e0286a9cacee5034dd930f4e68ba38, 452e0a4bd702cf2f5ac752ea9fe0040ce403dab5。
G03: b0df19d08f47b39aca285e77c5298037fb42a08b, c4b1497d07c400ab4099979c932ab355fc86739b, 293a067dbbc1a850f2b61179f8381562a1210ab5。
G04: aac5f0be428ea3d65a6657363ce1df55040e8721, d294abfc6216e0c7c57d30ce0611e3d17f53582b, b448d395e8ac7128f7049f0f578dbba02c963d1b。
G05: 5b110018f08c68f69534b5403a898da8fc870be4, a82ff8313f74ada5cedbd88cd30d0e2501a35dff, ae1949b7e2080071612d6ad3d4f5b463f8c1fbfd。
G06: c21f121619e5892824db454fb80f409733b3650d, 4d7441e5756d61f2784548ec8c2c28b32dfcfad1, 835262a35b5b543bc13ac088625acb904c98132f。
G07: 6f5213a857cbd10e94b503dcef703901b9b1c167, 62a4f2bfe8690c4ad1d09ce0e5dfc97b0fd073d0, 05952d2f6034645f0f3314625e5e8cbe67a59e90。
G08: 8a0bf081cab7624e769551da07d6afccd2857044, 92c521b4c10dd426f3908cacd08fa011971e8823, a49b3eea2e4d6718220969eba6b5f407b5eb1396。
G09: e5d6925429d0a42554f3a06d66c8353946f8bfdb, bacafb87bfda352f273bd8ab83a7fc6d07783497, 3fbdf0d6409f72dc5dc593bcc34569e2021f55e2。
G10: 2455792142113bbc43a31028008db9dfd4f9809a, ea0dc98fe1e79a82ecbce419a221c0273f9713b6, 9b48cca00d07e221146e80d78334b482b5bd4b18。
G11: 055b29ddfbd5271b954a90a5f682e101e17c5c54, cb12f93ae955315e64bf095460c48e47f9518150, bf602f89007953aec862b07855005e97e1a59771。

## 许可与科研资格
数据集 `dataset_description.json`（blob c6d51a07c3a5b3821b8ffabea51a502ea99835e4）标注 `License: CC0`，仓库 `LICENSE`（blob 7cf9928dd50e0b154c7e5d09f91f16674dff64fc）声明原始文件未提供许可信息。论文为CC BY开放文章，文章许可不能自动代替数据文件许可。数据文件再分发权限仍为LICENSE_CONFLICT_OPEN；本轮只保存不含个体记录的汇总结果。

A轨来源状态：AUTHOR_PAPER_LINK_VERIFIED；ALL_33_DECISION_EVENT_FILES_READ；BEHAVIOR_SCHEMA_VERIFIED；LICENSE_CONFLICT_OPEN；RAW_EEG_NOT_READ；INDEPENDENT_COLLECTION_VERIFICATION_OPEN。R073冻结要求真人双人100轮，当前是三人40轮，直接复验资格NO。可以在许可和伦理门槛澄清后另立三人组级研究，预冻结按三人组留出，禁止将同一组三人的轮次拆散至训练与测试。没有新增E2、E3或个人产品开发。未购买数据或运行计费API。
