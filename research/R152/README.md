# R152 人口迁移引力模型｜54种人工空间流量分配与OD不可识别反例

2026-10-20，原固定候选目录 **P1 / 06-010 Gravity Models of Migration**。**本阶段CLOSED_BOUNDED_E1**，仅代表项目自建模型被精确复算，**不代表历史人口迁移预测或原作者论文实证复现**。

研究一手学术源（均出版方/原期刊目录核对，未得到全文扫描或作者原始数据）：
- G. K. Zipf (1946), *The P1 P2/D Hypothesis: On the Intercity Movement of Persons*, ASR 11(6):677–686，DOI [10.2307/2087063](https://doi.org/10.2307/2087063)，JSTOR [当年原期刊目录](https://www.jstor.org/stable/i310017)。
- S. A. Stouffer (1940), *Intervening Opportunities: A Theory Relating Mobility and Distance*, ASR 5(6):845–867，DOI [10.2307/2084520](https://doi.org/10.2307/2084520)，JSTOR [原期刊目录](https://www.jstor.org/stable/i336314)。
- A. G. Wilson (1967), *A statistical theory of spatial distribution models*, Transportation Research 1(3):253–269，DOI [10.1016/0041-1647(67)90035-4](https://doi.org/10.1016/0041-1647(67)90035-4)，Elsevier原刊条目。

**原创理论范围：** 四地人口2/3/5/7、两布局×三距离衰减指数×三吸引力配置×三出发地总迁出预算=54个**完全Fraction**的迁移流量配置。归一化出流严格固定起点流量预算，不把未归一化Zipf-like强度错说为已约束迁移量。两套独立权重/整数公共分母算法在全部54套逐一完全匹配，自动核对所有4×4流量、路由概率与地区迁入/迁出收支。α从0到2的特定基准下，全网流量加权迁移距离从3.60126下降至2.69859（均为人工距离单位）。

**聚合数据非识别**：三地有序边际均(2,3,4)时，恰有两种不同的零自循环有向整数迁移表。它们具有相同的每地迁出入总量、每对地区无向总量以及 α=0/1/2 下完全一致的人工对称引力评分；加入方向性奖励后可区分。引力乘积评分**不是完整的个体似然模型**，不由此宣称所有原始人口记录均无法识别有向迁移。

材料：[计算前冻结协议](../../protocols/R152_ZIPF1946_STOUFFER1940_WILSON1967_SPATIAL_GRAVITY_OD_IDENTIFIABILITY_PRESCORE_FREEZE_2026-10-20.md)（先于程序，提交373b058）｜[完整科学研究报告](R152_PRIMARY_GRAVITY_54_CASES_AND_OD_IDENTIFIABILITY_SCIENTIFIC_REPORT_2026-10-20.md)｜[完整源码/126项测试/54结果ZIP](R152_Gravity_Migration_54_Cases_126_Tests.zip)｜[全54原始结果JSON](R152_EXACT_RESULTS.json)｜[正式机器验收收据](R152_FINAL_MACHINE_ACCEPTANCE.json)｜[GitHub CI第二轮成功与永久归档](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39430207335)。

**机器身份:** ZIP SHA256 `1a421b359602a4c2a3e1aca995e325c264d16b166c0d92616a00a92adbbc5442`，完整JSON SHA256 `1f79b445cb14a25d1101aaec4eff9c9a3b127b7ec829f3ef7f553c16331fb23a`。Python3.11/3.12在两次完整CI中均126测试/环境，共504次实际执行、0失败（只有126种不同测试）。独立发布任务四项哈希校验成功并永久提交JSON/ZIP入库。复算：`python -m unittest -q test_r152_gravity_od_exact.py` 和 `python r152_gravity_od_exact.py > replay.json`，将replay与仓库原JSON字节比较。压缩研究包采用标准库ZIP_LZMA，使用Python标准库解压。

新增真人E2=0、历史迁移E3=0；R073/PESEN v0.1 FROZEN。下一目录已核对：R153 P2/06-011 Spatial Interaction Models。继续先完成全部R系列，再统一归纳分类，最后熔炼。
