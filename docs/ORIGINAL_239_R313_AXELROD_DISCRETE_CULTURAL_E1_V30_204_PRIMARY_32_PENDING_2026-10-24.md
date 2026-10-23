# 原始239候选目录 v3.0：R313 Axelrod离散文化模仿 E1 科研边界与目录归属审计

日期：2026-10-24 Asia/Taipei。最新审计基准为R312主R映射203项、待核33项的v2.9交叉索引。用户已确认研究顺序：先完成R系列→归纳分类→最后原创模型熔炼，个人决策系统暂缓。R073及PESEN v0.1完全冻结。

## 首要结论

本阶段**新完成R313人工有限模型E1**，对应原始模型`04-014 Axelrod Cultural Dissemination`（P1）。由完整原世界枚举生成64个人工3站点2二值特征状态、256个有向接触情形、512条可能特征复制source；正概率复制原子128，吸收状态16。以预注册[冻结协议](../protocols/R313_AXELROD_THREE_SITE_TWO_FEATURE_EXACT_ONE_STEP_PRESCORE_FREEZE_2026-10-24.md)（独立早于模型输出的[commit8b69fc8c](https://github.com/edwardsage419/Psychohistory-Research/commit/8b69fc8c73a850279a3fac1a5e9314a3374c6d52)）为唯一计算域。

确切机制取自Robert Axelrod 1997 JCR, DOI https://doi.org/10.1177/0022002797041002001；JASSS公式说明 https://www.jasss.org/12/1/6/appendixB/Axelrod1997.html。只测试相似特征占比作为接触概率、主动者复制一项不同特征的方向性。此E1不模拟或验证论文的大尺度文化极化定律或真实人类数据。

## 独立软件与来源门槛

* [完整R313科学报告](../research/R313/R313_SCIENTIFIC_REPORT_2026-10-24.md)、[512 source CSV](../research/R313/R313_ALL_512_ORIGINAL_FEATURE_SOURCE_ATOMS.csv)、[64状态完整概率JSON](../research/R313/R313_EXACT_64_WORLD_ONE_STEP_RESULTS.json)。
* [R313机器来源SHA1收据](../research/R313/R313_MACHINE_RECEIPT.json)固定冻结提交、源CSV与结果JSON的Git blob SHA1，以及真正绿灯的CI；[正式E1验收](../research/R313/R313_FINAL_ACCEPTANCE_STATUS.json)只认可人工数学机制。
* [R313实际科学CI 39993794818](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39993794818)：Python 3.11主29测试、Python 3.12主29测试、独立审计完整512个source、全64行概率分布，**3/3成功**。独立脚本不import主程序；世界1三点状态`00|00|01`一步转移`0:1/6,1:3/4,5:1/12`。
* [原239 v3.0交叉索引](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v3.0_2026-10-24.json)、[32项待核优先队列](ORIGINAL_239_PENDING_32_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv)、[机器化只改一项审计](../research/catalogue_audit/verify_p1_r313_crosswalk_v3_0.py)。
* [v3.0目录CI 39994052315](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39994052315)：Python 3.11/3.12及独立审计**3/3成功**；严格核对239项原编号、名称、优先级和顺序完全未改变，R312 v2.9只有04-014变更，source Git blob SHA1全匹配，待核队列仅移除04-014。

## 原目录归属

| 来源状态 | v2.9 | **v3.0** |
|---|---:|---:|
| 已有主R关联（含大量仅README暂拟） | 203 | **204** |
| 共享有限数学研究 | 3 | 3 |
| 旧有限研究无专属主R | 1 | 1 |
| 未发现逐条主R | 32 | **31** |
| 主R来源仍需审计（旧有限1 + 未发现31） | 33 | **32** |
| 唯一原始候选 | 239 | 239 |

余下**32条：P1 5条，P2 27条**，队列第一条`04-016 Preferential Attachment Network`。203至204是目录来源归属更新，**不是204个高标准科研验证结题**；其中173条仍为`PROVISIONAL_PRIMARY_README_LINK`，要逐项维持实际证据边界。新真人E2=0，历史E3=0，全239项科学结题、分类和熔炼均未成立。

## 下一研究关口

第一优先：搜查旧研究中是否有04-016的精确BA/degree-proportional增长机制，然后若无，按预先冻结协议研究有限偏好连接网络，独立复算源事件、检查节点选择权重与不当声称幂律的风险。不得借R313文化相似性事件冒充网络生成概率模型。
