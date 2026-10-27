# E048 R215 S11 原始768来源5736项独立精确复算及真人实验等级纠错

日期：2026-10-27（Asia/Singapore）。轨道：operations。状态：COMPLETE_READONLY_E1_SOURCE_REPLAY_AND_GOVERNANCE_DELTA。CI：NOT_RUN。主动新增费用0。

## 1. 当日预检与审计范围
读取main HEAD 50e7d9a810843642e29d0834db34fdb1aa17f5d4、market至MKT078、operations至E047、F002、最新R216 S12及B轨变异检查、A轨Miettinen数据来源报告、E006与R074/R075/R077验收。仅新增operations报告与脚本，不修改R、B、A、TH、F、原239索引、冻结协议或共享索引。此轮延续E047已登记的R215 S11独立复算待办，避免重复既有B路线的解析矩方法。

## 2. 原始来源级第三路线复算
从GitHub实际读取 research/R215/R215_ALL_768_ORIGINAL_GROUP_TIME_SHOCK_PANELS.csv，Git blob 8cc6ba9d4606cd2d71d7acfaaed6b6d87dce83ee；正式36条件CSV research/validation/R215_S11_36_CONDITION_EXACT.csv，Git blob 8b1633bb1e8e10db9196fbc236531d9d9214769e。前者12个人工世界各64个等概率来源，后者每世界阈值h=1、2、4。此处768为原人工面板，2304为重复评价槽，不是2304个独立实验。

独立JavaScript算法只读取原始CSV的六个实际观察均值Y=(T_-1,T_0,T_1,C_-1,C_0,C_1)，逐来源重新构造D=(T_1-C_1)-(T_0-C_0)、P=(T_0-C_0)-(T_-1-C_-1)、C=D-P。对照原来源记录的D、P、C和两个相对于真ATT的平方损失；以|P|<=h筛选并使用BigInt有理数计算条件均值、总体方差、MSE和相对无筛选的MSE变化，再逐字段比较正式CSV。不调用R原生成器、R/B分析程序或其函数。

实际执行5736项断言，失败0。来源级每行7项，共5376项；36个条件每行10项，共360项。另检查12世界、768来源、36结果行的结构规模。结果：
D真ATT MSE相对无筛选增加9项、降低20项、不变7项；D条件均值变化15项。
PARALLEL_NULL,h=1：接受24/64，D均值0，MSE 10/3，变化−2/3。
DIFFERENTIAL_SLOPE_FALSE,h=1：接受40/64，D均值7/5，MSE 27/5，变化+2/5。
LARGE_DIFF_SLOPE,h=1：接受20/64，D均值21/5，MSE 103/5，变化+38/5。
这条路线与B轨矩公式方法不同，仍共享同一人工模型和同一原始归档，不构成外部独立研究复现。脚本路径 research/operations/e048_r215_s11_source_csv_exact_20261027.js，Node.js标准库，两个CSV路径作命令行参数，不需要网络或付费依赖。

## 3. 冻结协议与最新R216并发检查
R215 S11协议冻结提交7a61e7c526833fd9d7ec8589bb344af4987f6478，正式结果提交35fc54511cb4a14f847536fe69de682e8d8261f5。协议在冻结提交及当前main的Git blob均为f4c1c089e416c06467849e8812b3dc76288d07da。
R216 S12协议冻结提交d1bff2f4b3b7022410c364ac0c87dbbbb18ed6ab，结果提交95e115e1e0ed8bd91deafab945714118950e71ad，B轨v2变异执行提交cffd906b26166ad0b0336e54242d8837b63396a8。协议在冻结提交与当前main的Git blob均为0137d8e0bd8f2bc133265749d55d31a09a579df8。
R216 S12记录6个人工世界×4096历史、30筛选条件，B轨已报告660字段DP比较及实际错误系数和阈值变异检出。本轮只读核验这些报告和收据，没有重算R216全部24576历史，不能将B轨检查计入本轮5736。
通过GitHub REST Actions按R215结果、R216结果、R216 B v2三个指定SHA查询，均返回total_count=0；只说明未发现这三个提交对应的运行，不能泛化到所有历史CI。没有启动Actions。

## 4. 高优先级证据等级及来源纠错
E006在2026-10-26已经核验R074、R075、R077三项不同原始真人实验的有界研究归档。此次直接重读三个FINAL_ACCEPTANCE_STATUS.json及固定Git blob：R074 6fe05c642a1d64f8fc292315f34574c274091f55，R075 1241ad79fd1f19195eb591ce60b56668ead8cd76，R077 24e45b65878ca400cb7f149ad863dd74e7fd5cd9。R074共18场次15338个合格评分目标，R075共18场次26116目标，R077共15场次1040目标，均是归档的有界真人研究，不代表本轮重新评分。R076复用原实验，不新增原始实验身份。
因此E047等近期报告笼统写“R073第二独立真人实验仍阻塞”容易误导。准确的读时状态为：R074、R075、R077已提供第二、第三、第四项不同原始真人实验的内部E2有界评估；新候选Miettinen 2020虽核实论文DOI及数据许可，但只有顺序博弈角色条件选择的公开描述，缺R073冻结所需逐轮双人历史，当前R073适配门槛为NO。旧归档中的E3真人标签属于历史口径，当前E3只指历史社会演化证据，尚未建立。保留原档，不擅自修改。
该纠错与本轮R215/R216新增人工E1独立：E2现有归档不因此升级，新增E2=0，新增历史E3=0，外部团队独立复现=0。

## 5. 日度治理问题与F周专题
本轮核对的冻结协议未发现意外改动；新增目标只位于market和operations路径，未发现同名冲突或跨轨覆盖。R214 S10冻结负对照16/18失败、R136原冻结负对照与原CSV缺口、R181既有交付偏离仍按先前登记保留；本轮未独立重跑这些事件，不宣称关闭。R216新增E1不改变先完成R系列、再统一归纳、最后模型熔炼的主线。项目账户账单及GitHub免费额度没有独立核验；未调用收费API、购买产品、注册收费服务、启用CI或租用计算资源。
2026-W44 F002已完成授权撤销、派生数据、备份生命周期专题；本轮不重复F003。MKT079的新风险为搜索预算及目标选择解释不足、过早自动执行；候选控制为目标版本化、多指标并列、人工审阅与拒绝权。没有接入真实敏感信息。

## 6. 下一项
E049优先对R216 S12的30条件收据及可重建24576来源执行第三条独立核验，尤其检查VALID_DYNAMIC与POST_EVENT_SHOCK_MIMIC的观测不可区分性和真实MSE差；继续核查原239待核队列、R136、R181与E2/E3读时映射。F003下一周研究错误偏好归因、派生记忆证据及人工纠错。

仓库参照：
https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/operations/E006_R073_R077_STUDY_LINEAGE_EVIDENCE_TAXONOMY_AND_R167_E1_2026-10-26.md
https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/data_scout/MIETTINEN_2020_SEQUENTIAL_PD_MENDELEY_SOURCE_LICENSE_AND_R073_NEGATIVE_GATE_2026-10-27.md
https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/privacy_safety/F002_CONSENT_REVOCATION_DERIVED_DATA_BACKUP_LIFECYCLE_2026-W44.md
