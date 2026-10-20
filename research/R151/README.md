# R151 — 年龄结构人口模型 / Leslie matrices and age-composition dynamics

**状态：CLOSED_BOUNDED_E1（数学和机器证据），不是现实人口预测结题。** 日期2026-10-20，目录P1/06-009。

一手出版记录：P. H. Leslie (1945), *Biometrika* 33(3):183–212 DOI [10.1093/biomet/33.3.183](https://doi.org/10.1093/biomet/33.3.183)；Leslie (1948) *Biometrika* 35(3–4):213–245 DOI [10.1093/biomet/35.3-4.213](https://doi.org/10.1093/biomet/35.3-4.213)；N. Keyfitz (1971), *Demography* 8:71–80 DOI [10.2307/2060339](https://doi.org/10.2307/2060339)。**只核对了出版方/书目原始记录，未逐页阅读全文。所有数学参数是项目自定义，未复现作者原数值或历史人口数据。**

原创三年龄组人口投影矩阵J'=A+O/2，A'=3J/4，O'=2A/3。基准替代特征根1与稳定份额(4/9,1/3,2/9)，不变生殖价值向量(1,4/3,1/2)；同为900初始总量，如果都在幼年/生育年龄/老年组，长期人口极限分别900/1200/450。即使初始2期总量均为900，初始(400,300,200)与(120,360,420)的第三个总量也不同：900 vs1395/2。外生增加2名幼年组与2名生育年龄组对应长期人口总量差异+2与+8/3。仅是项目年龄组机制例子，不含实际人口惯性参数或现实移民效果。

**全覆盖**：91个J+A+O=12年龄组合×3种生育率×2×2种存活参数=**1092组**，每组13时点年龄向量、12期出生/死亡流量，完全标准库Fraction；双重独立状态更新与完整闭式校验。105项真实不同方法测试（其中50个不同年龄结构自动命名），Python3.11及3.12分别通过。

材料：[事前冻结协议](../../protocols/R151_LESLIE1945_KEYFITZ1971_AGE_COHORT_MOMENTUM_1092_CASES_PRESCORE_FREEZE_2026-10-20.md)｜[完整科学报告](R151_SCIENTIFIC_REPORT_AGE_COHORT_MOMENTUM_E1_2026-10-20.md)｜[永久 ZIP（源码＋105测试＋全JSON）](R151_Leslie_Keyfitz_1092_Cohorts_105_Tests.zip)｜[原始全1092轨迹JSON](R151_EXACT_RESULTS.json)｜[正式机器收据](R151_FINAL_MACHINE_ACCEPTANCE.json)｜[GitHub双环境及永久归档CI run39423735601](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39423735601)。

ZIP和三个内部原件SHA256已固定；本期E1数学结果不视作原著复现或实证预测。新E2=0、新E3=0，R073/PESEN v0.1冻结。后续R152 P1/06-010 Gravity Models of Migration；原R研究完毕后再统一分类，最后熔炼。
