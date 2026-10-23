# R245 更新过程：九个人工离散间隔世界、4608完整来源与更新方程的独立性边界

日期2026-10-23（Asia/Taipei）。原目录 `11-005 Renewal Processes`（P2）；状态 `CLOSED_BOUNDED_E1_FINITE_ARTIFICIAL_RENEWAL_AND_NONIID_GAPS`。真实人类E2、历史E3新增均0。本报告只对应有理数可精确枚举的人工四间隔与时间0…4，不是实际人类事件间隔样本，也不对长时间更新奖励定理作经验主张。

## 原理、先冻结机制及研究边界

原教材 MIT 6.262 [*Discrete Stochastic Processes, Chapter 4: Renewal Processes*](https://ocw.mit.edu/courses/6-262-discrete-stochastic-processes-spring-2011/931ffa0940899c27f34b71ad64fd2bb0_MIT6_262S11_chap04.pdf) 以及 NPTEL [*Renewal Function and Renewal Equation*](https://archive.nptel.ac.in/content/storage2/courses/111103022/module8/lec3.pdf) 分别给出更新事件时间S_k、累计计数N(t)与IID间隔下的更新函数。这里严格限定四个可能的原间隔W_i∈{1,2}，t∈{0,1,2,3,4}，每个world九个独立二位人工来源U、四对R，全部512个外生源×九world＝**4608个完整原source类型**、每行1/512。事件生成真实隐藏H、伪观察Y和用于生成或报告的W/S标记各自分离，绝不视作真人或社会历史行为。

[事前冻结协议](../../protocols/R245_RENEWAL_9_WORLDS_4608_ORIGINAL_GAP_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md)先于代码/CI独立提交[80160fbb](https://github.com/edwardsage419/Psychohistory-Research/commit/80160fbbe01d801fe27cc020bf59a63c7b503759)，冻结九世界、两路径积分、IID更新方程与隐藏别名预期，未根据结果改写人工机制或评分门槛。

## 实际完整源与独立数学验收

第一路径按九bit来源枚举全部512×九world，R两bit等概率0..3和事先固定阈值独立抽出四间隔（或共同shock/隐藏类型混合），由S_k=ΣW_i得到全部原事件时刻，通过N(t)=#{k:S_k≤t}得到可见五时点报告事件累计计数。第二路径**不读取来源CSV**，对全部16种四间隔序列计算独立条件间隔乘积分布；隐藏U混合的是两整个四间隔乘积Law的1/2混合；共同shock的只有1111、2222两整gap轨道各概率1/2；时间交替的每个位置另用自己的p(W=1)。两个算法推送到每world全部观察五元计数路径完整联合概率后**逐格有理数完全一致**。

第三方法对真正IID五world（IID_FAIR, IID_SHORT_3OF4, IID_LONG_1OF4, DETERMINISTIC_UNIT, DETERMINISTIC_TWO），以及**仅在可见报告层与IID_FAIR同分布的STATIC_HIDDEN_EVENT_SENSOR_ALIAS**，独立以`m(t)=F(t)+Σ_{s∈{1,2},s≤t}p(s)m(t−s)`、m(0)=0，计算全部五时点的理论期望E[N(t)]并与完整来源观察概率积分逐格一致。对隐藏混合、time-alternating与共同shock模型，**错误强行使用单一间隔边际当作IID公式**会得到可审计偏差，属于模型假设不成立而不是更新等式推导错误。

## 九世界结果及非独立反例

| 冻结人工间隔机制 | 首次短间隔概率 | 可见E[N(1)] | 可见E[N(2)] | 强行假定IID的E[N(2)] |
|---|---:|---:|---:|---:|
| IID_FAIR | 1/2 | 1/2 | 5/4 | 5/4 |
| IID_SHORT_3OF4 | 3/4 | 3/4 | 25/16 | 25/16 |
| IID_LONG_1OF4 | 1/4 | 1/4 | 17/16 | 17/16 |
| DETERMINISTIC_UNIT | 1 | 1 | 2 | 2 |
| DETERMINISTIC_TWO | 0 | 0 | 1 | 1 |
| LATENT_RATE_MIXTURE | 1/2 | 1/2 | 21/16 | 5/4 |
| ALTERNATING_RATE | 3/4 | 3/4 | 19/16 | 25/16 |
| COMMON_GAP_SHOCK | 1/2 | 1/2 | 3/2 | 5/4 |
| STATIC_HIDDEN_EVENT_SENSOR_ALIAS | 1/2（报告器） | 1/2 | 5/4 | 5/4（报告层） |

**单个间隔边际相同，完整更新过程不同。** IID_FAIR的四间隔各自独立，Pr(W_i=1)=1/2，`E[N(1)]=1/2,E[N(2)]=5/4`；LATENT_RATE_MIXTURE每个人有冻结隐藏类型U=0或1，分别让间隔短概率3/4或1/4，且U对四个间隔始终相同。所有单个W_i边际短率仍1/2，但观察过短的第一间隔后对第二间隔短的条件概率是5/8；观察过长的第一间隔后则是3/8。四间隔在**群体混合后并不独立**，因此E[N(2)]=21/16，多于照搬单间隔边际IID公式5/4的1/16；这准确量化了未测量的个体持久差异对重复事件预测的影响。

**两个非IID机制的反例：** ALTERNATING_RATE中奇数间隔p短3/4、偶数1/4，独立但不等分布，E[N(2)]=19/16，不能像IID_SHORT那样得到25/16（偏差−3/8）。COMMON_GAP_SHOCK中四个间隔共享第一对R决定的同一短/长类别，因此每个gap单独边际短率1/2，但四gap完全相关；E[N(2)]=3/2，比假设独立的5/4高1/4。由此观察短间隔边际、事件累计数或某次事件激增时，必须分辨IID更新、隐藏持久类型、跨间隔共同冲击和非齐次机制。

**完整可见计数和真实隐藏事件非同一问题。** STATIC_HIDDEN_EVENT_SENSOR_ALIAS的所有真实隐藏累计事件数H0…H4严格是0，而报告器采用和IID_FAIR完全一样的原九bit外生源生成“观察更新”Y0…Y4。对于每条相同源，所有可见计数**逐字相同**，完整可见路径分布也完全相同。因此“观察到IID更新过程”不独立证明现实真实事件真的存在；该例明确依赖允许外部报告器模拟虚假事件的假设，若有独立物理传感器校验或真正事件记录则不必成立。

**无支持条件的正确处理。** DETERMINISTIC_UNIT里W1必为1，因此`P(W2=1|W1=2)`无定义；DETERMINISTIC_TWO里W1必为2，因此`P(W2=1|W1=1)`无定义。曾经的初版machine-readable结果把Python None序列化成字符串`"None"`，语义仍非零但机器类型不规范。原程序在不修改冻结机制或来源下追加回归测试，改为正确JSON `null`；首CI run39891559836 success但由二次归档run39891651106重算了结果JSON及SHA，这份报告严格引用**最终run**，不将初版结果SHA当最终凭证。

## 实际执行、永久来源与科研验收

[原生Python源码](r245_exact_finite_renewal.py) · [完整4608条九位原来源CSV](R245_ALL_4608_ORIGINAL_RENEWAL_GAP_SOURCES.csv) · [九世界全部五时点观察分布及期望/违反项JSON](R245_EXACT_RESULTS.json) · [原来源SHA256收据](R245_FINAL_MACHINE_ACCEPTANCE.json)。

最终[GitHub Actions run39891651106](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39891651106)总体completed/success，3项jobs全success，Python3.11/3.12真实单测各`Ran 85 tests`、`OK`，合计**170次真实测试通过**。第三独立审计检查每world512九bit唯一原类型、全部源概率1/512、观测完整五元联合、单/双间隔条件、IID与非IID期望对照、隐藏事件报告别名及CSV/JSON SHA，日志`R245_ALL_4608_RENEWAL_NINEBIT_SOURCES_IID_EQUATION_NONIID_ALIASES_VERIFIED`；最终原CSV与JSON由机器人永久归档main，[45fab069](https://github.com/edwardsage419/Psychohistory-Research/commit/45fab069902237d354a45fb5140ab216f4aef3e5)。

完整原CSV SHA256 `355f67634c49bd3480ad37e5efc6cd18d4ee8410237dd2ac5e2ce399b8b7d23b`；最终结果JSON SHA256 `6995bb7fb37a12a137e0eaea5c2790fc2f9444ed39a01489488551b3daa4d96f`。

结题只为有限人工E1：没有真实人群事件间隔、历史项目更迭或连续时间Poisson模型证据，不能把形式化所有原结构来源完整性视为外部经验复现。新E2=0、E3=0，R073和PESEN v0.1均冻结。下一原239目录11-006 Poisson and Hawkes Processes，拟R246。研究依原R全部完成后分类、最后熔炼。
