# TH135 威斯康星州1998至1999年败血症年龄分层原始表与跨机构分母差异

研究日期：2026-10-30（Asia/Singapore）；英文来源检索日期：2026-10-30。状态：THEORY_NOTE_BOUNDED。
目标键：(theory,NCHS_GMWKIII_WISCONSIN_1998_1999_SEPTICEMIA,theory-v1,age-specific cause-count reconciliation and cross-vintage transport)。
本轮读取main索引TH134、C006、D002、R269/R270短交接和开放Codex PR摘要。TH134已读，为非盲态后续独立官方原表核对。未修改R系列、冻结协议或Codex PR。

## 一、原始出处与实际读取范围

A1 [A级，官方原始PDF，直接核对页图及文本，1998年PDF零基页358至359，原表PLT A/B PG180] CDC/NCHS, *Table III: Deaths from 282 Selected Causes, by 5-Year Age Groups, Race, and Sex: U.S. & Each State, 1998*, 1998 mortality worktable GMIII_1_98, Septicemia ICD-9 038. 无DOI。原始PDF https://www.cdc.gov/nchs/data/mortab/98gm3_01.pdf ，官方目录 https://www.cdc.gov/nchs/nvss/mortality/historical_gmwkiii.htm 。1998 Wisconsin总数314，分龄见下。只读该病因Wisconsin两页，未审读627页全文。
A2 [A级，官方原始PDF，直接核对页图，1999年PDF零基页430至431，原表PLT A/B PG216] CDC/NCHS, *Table III: Deaths from 358 Selected Causes, by 5-Year Age Groups, Race, and Sex: U.S. and Each State, 1999*, 1999 mortality worktable GMIII_1_99, Septicemia ICD-10 A40–A41. 无DOI。原始PDF https://www.cdc.gov/nchs/data/statab/VS00199_TABLEIII.PT1.pdf ，官方目录 https://www.cdc.gov/nchs/nvss/mortality/gmwkiii.htm 。1999 Wisconsin总数382。只读该病因Wisconsin两页，未审读2628页全文。
A3 [A级，官方州级原始PDF，继承TH134并再次交叉比较所报两总数] Wisconsin Department of Health Services, *ICD-10/ICD-9 Comparability Ratios for 113 Selected Causes of Death*, Septicemia行。无DOI。https://www.dhs.wisconsin.gov/stats/deaths/icd10-9comparetable.pdf 。州表1998为317，1999为376；与A1/A2分别差+3及−6。尚未确认原因。
A4 [A级，官方互动查询入口，直接核验表单可选年份、年龄组及隐私规则；未成功执行交互查询] Wisconsin DHS, *WISH Mortality Module Detailed Groups*, 网页最后修订2026-05-06。无DOI。https://www.dhs.wisconsin.gov/wish/mortality/detail.htm 。支持1990至1998 ICD-9、1999至2024 ICD-10、年龄行列、死亡数及年龄调整率；小于5的细胞可能被抑制。
A5 [A级，官方原始方法/分母，继承TH134的直接审读] U.S. Census Bureau, Population Division (2002-04-11), *Time Series of Intercensal State Population Estimates*, Table CO-EST2001-12-00, Wisconsin 1998=5,297,672、1999=5,332,666。无DOI。https://www2.census.gov/programs-surveys/popest/tables/1990-2000/intercensal/st-co/co-est2001-12-00.pdf 。该州总人口分母不足以完成分年龄率。
A6 [A级，官方原刊，继承TH134已读比率] Anderson RN et al. (2001), *Comparability of Cause of Death Between ICD-9 and ICD-10: Preliminary Estimates*, NVSR 49(2). 无DOI。https://www.cdc.gov/nchs/data/nvsr/nvsr49/nvsr49_02.pdf 。全国1996初步败血症可比率C=21258/17791=1.1948738126；没有证据证明它对Wisconsin各年龄层恒定。
A7 [A级，官方历史分龄表入口] CDC/NCHS, *Historical GMWKIII*, https://www.cdc.gov/nchs/nvss/mortality/historical_gmwkiii.htm ，及 *1999–2007 GMWKIII*, https://www.cdc.gov/nchs/nvss/mortality/gmwkiii.htm 。无DOI。不同版本列示282和358病因，历史类别不能按显示名称直接等同。
所有来源为英文官方原始资料；网站检索日期2026-10-30。PDF读取的文本同时用页图人工核对。未下载原始逐人死亡数据、未取得匹配分龄人口，也未运行交互式WISH查询。

## 二、原始年龄分层数字与直接复核

以下年龄组是官方原表Wisconsin州合计行。空横线在该表格作为零计数用于本轮算术；没有将race/sex的包含关系重复相加。

| 年龄 | 1998 ICD-9 038 | 1999 ICD-10 A40–A41 |
|---|---:|---:|
| <1 | 3 | 1 |
| 1–4 | 2 | 1 |
| 5–9 | 0 | 0 |
| 10–14 | 1 | 2 |
| 15–19 | 1 | 0 |
| 20–24 | 1 | 1 |
| 25–29 | 1 | 0 |
| 30–34 | 1 | 3 |
| 35–39 | 3 | 0 |
| 40–44 | 4 | 0 |
| 45–49 | 5 | 6 |
| 50–54 | 8 | 9 |
| 55–59 | 6 | 10 |
| 60–64 | 16 | 17 |
| 65–69 | 21 | 33 |
| 70–74 | 32 | 45 |
| 75–79 | 39 | 62 |
| 80–84 | 59 | 73 |
| 85–89 | 57 | 64 |
| 90–94 | 40 | 36 |
| 95–99 | 14 | 16 |
| 100+ | 0 | 3 |
| 年龄未陈述 | 0 | 0 |
| **合计** | **314** | **382** |

## 三、12项条件命题、机制及四层联系

T135-01 [A1,A2] 官方跨期原始表确实公开了年龄细分死因数，TH134的“尚未取得年龄分层死亡数”阻塞现已部分解除。
T135-02 [A1,A2,A3] 不同官方机构发布的同州同年败血症总数存在差异；须固定登记总体、居民定义、版本及处理规则后才能决定哪个数作为目标。
T135-03 [A1,A2] ICD-9 038与ICD-10 A40–A41是历史对应候选，不能以名称相同证明逐条分类等价。
T135-04 [A6] 全国可比率仅是样本汇总桥接系数；各年龄层可能具有不同编码转移概率。
T135-05 [A1,A2] 65岁以上死亡占比的观察变化可能反映疾病年龄构成、编码变化、人口结构或登记差异；单靠计数无法分解。
T135-06 [A5] 全州总人口分母不能用于计算各年龄组死亡率；必须取得同版、同地理、同居民口径的年龄分母。
T135-07 [A1,A2,A5] 选择不同官方计数来源，可能使同一桥接假设下粗率变化方向不同，属于来源选择敏感性。
T135-08 [A4] 互动表的低频格抑制可能限制分年龄/种族交叉复算；公开PDF中的分龄数不自动解除其他来源的隐私限制。
T135-09 [A1,A2] 原表的ALL OTHER包含BLACK，不能将两者相加；男女与种族行需要先确认互斥层级。
T135-10 [竞争解释] 1998至1999变化同时可能来自疾病真实风险、人口年龄结构、诊断与填报习惯、ICD转换及不同统计发布时间；现有数据没有因果识别。
T135-11 [跨尺度] 个体层为死亡证明及死因赋码；群体层为年龄构成；制度层为州与联邦发布规则；历史层为ICD版本切换。各层是待检验机制链。
T135-12 [理论边界] 历史测量等值必须区分类别阈值、抽样框、年龄分母及跨期解释。可观测总数一致也不充分证明构念不变。

## 四、8项可复算审计与反例

E135-01 [A1原表] 1998两页年龄合计22+292=314，原表总数314，核对一致。
E135-02 [A2原表] 1999两页年龄合计14+368=382，原表总数382，核对一致。
E135-03 [A1,A2] 1998年龄65+计数262，占262/314=83.43949%；1999年龄65+计数332，占332/382=86.91099%。这只是死因计数的年龄组成，不能当作人群风险变化。
E135-04 [A1,A2,A3] 1998州表317减联邦314=+3；1999州表376减联邦382=−6。差异方向相反，尚未归因于州外死亡、最终修订、ICD或居民范围。
E135-05 [A1,A2,A3] 联邦原表粗计数变化382/314−1=+21.65605%；州表376/317−1=+18.61199%。不能将任一百分比直接解释为风险率或编码净效应。
E135-06 [A1,A2,A5,A6] 固定2002 Census总人口和全国初步C，联邦原表条件性1998修正粗率314*C/5297672*100000=7.08217，1999粗率382/5332666*100000=7.16340；条件性变化+1.14685%。TH134采用州表317/376时同一规则得−1.38404%。**同一桥接假设下，来源选择改变方向**，为真实公开汇总数字敏感性结果；不证明任一方向为真实风险变化。
E135-07 [A1,A2,A5,A6] 联邦原表两年粗率相等的桥接阈值C*=382*5297672/(314*5332666)=1.2085772，比全国初步C高约1.14685%。此阈值属于代数条件，尚未估计州级桥接因子。
E135-08 [人工不可识别] 两年龄层各有10例和20例死因死亡，人口可以是(10000,10000)或(100000,1000)，对应年龄率差异极大；仅有年龄死亡计数不能推得年龄率，更不能完成2000年标准人口加权。

## 五、竞争解释、验证设计与阻塞

来源差异至少存在四个未排除解释：州与联邦统计冻结日期不同、居住/发生地纳入规则不同、病因最终修订不同、原始记录链接与质量控制不同。均未确认；应检查技术附录及WISH历史数据字典，不能将差异直接归因。
下一步先取得与A1/A2同版的1998/1999 Wisconsin年龄人口分母，检查5年年龄组对应关系及2000标准人口权重；并核对A3州表的总数定义与A1/A2的居民死亡覆盖范围。再以年龄分层桥接参数的敏感性区间计算年龄标准化上下界。不要假定全国比率在各年龄层恒定。若原始数据不可访问，保持公开分层计数与方法界限，不无限追逐大型ZIP。
科学证据：原始官方汇总表逐格非盲态人工读取及算术复核；无原始个体死亡记录、无独立因果估计、无历史事件预测。R系列E1/E2/E3新增均为0。无用户敏感资料、无新增费用、无CI。
下一理论专题TH136：跨历史制度与心理测量的等值性理论，对比分类阈值漂移、潜变量标尺及锚定策略，减少同一医学案例的重复。
