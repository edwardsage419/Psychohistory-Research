# D005 候选：联合国WPP2024净迁移测量与长期情景识别边界

track: theory
subflow: D
run_date: 2026-11-16 (Asia/Singapore)
week: 2026-W47
observed_head_before_write: 980ee6b638f49bf4d4d6a2104de43fff898fbeb5
target_key: (theory-D,UN-DESA-WPP2024-Methodology,2024,net-migration-inflow-outflow-nonidentification-and-projection)
status: PARTIAL; PRIMARY_OFFICIAL_METHOD_EXCERPT; CONSTRUCTIVE_IDENTIFICATION_ARGUMENT; NO_HISTORICAL_VALIDATION

## 原始来源与实际阅读范围
United Nations, Department of Economic and Social Affairs, Population Division (2024), *World Population Prospects 2024: Methodology of the United Nations Population Estimates and Projections*. 联合国官方方法报告，未见该报告独立 DOI，稳定官方 PDF：https://population.un.org/wpp/assets/Files/WPP2024_Methodology-Report_Final.pdf 。
2026-11-16 实际核对可检索的官方报告第26页有关净迁移的段落，以及第47页 Section E, “Projecting international migration in the medium scenario” 的方法描述和步骤1。该范围是官方原始报告的可检索正文节录，尚未逐页核验PDF扫描版全部公式、图表、其余步骤及附录。

## 直接来源命题
第26页：WPP2024使用净国际迁移量，通常没有可独立分解为移入和移出两项的观测资料。由于多数国家迁移流入/流出资料不足，某些国家的净迁移量由两次普查人口变动扣除自然增长及覆盖/质量调整后的残差估计。故净迁移序列有时含人口普查、出生死亡估计及调整的复合误差，不能将其自动视作独立直接测得的跨境流量。
第47页：国际迁移相较其他人口组成部分具有较高不确定性，部分国家的迁移方向可能迅速反转。2024版首次在中位方案中使用基于Azose与Raftery方法的贝叶斯分层概率净迁移率预测，历史输入为1950至2023年国家年度净迁移率，模型使用一阶自回归结构；该预测为条件情景，不是确定性事件预言。

## 新的构造性不可识别性论证
令 I_t 为移入，E_t 为移出，N_t=I_t-E_t。观察N_t=0时，(I_t,E_t)=(0,0)与(100000,100000)都满足观测；净值无法识别双向流动规模。更一般地，任意非负k使(I_t+k,E_t+k)产生相同N_t。仅有净迁移的历史时间序列，即使长度任意增加，仍不能在缺少额外约束时恢复总流量 I_t+E_t。此为代数构造性反例，非人口行为实验。

若人口存量满足 P_{t+1}-P_t=B_t-D_t+N_t+u_t，则用残差计算的净迁移估计为 Nhat_t=ΔP_t-Bhat_t+Dhat_t-uhat_t。出生、死亡、人口覆盖误差和残差迁移的误差可能混合，不能把迁移估计与上述输入视为独立测量后再作因果归因。

## 竞争解释、可检验条件与适用边界
竞争解释：真实双向高周转但净流量低；真实低周转；人口普查漏计、出生死亡统计偏差；边境政策或冲突冲击；长期经济与人口年龄结构变化。区分这些解释需独立流入/流出记录、登记或抽样覆盖校准、年龄性别分层、政策时点与外部冲击证据。
历史覆盖：WPP2024方法中的历史输入1950至2023，覆盖多个国家；研究仅核查方法说明，未下载或分析国家级原始数列。未来至2100年属于模型投影，不能以模型区间直接解释真实世界预测准确率。
可证伪/诊断：比较有高质量独立流入和流出登记的国家净值与人口残差法；预先固定年份、行政边界、年龄性别口径；对历史修订、人口普查覆盖、战争及政策结构断点做敏感性分析；采用时间外验证评价概率区间校准。仅凭净值不能检验双向流动机制。
局限：第47页后续9步及参数细节、国家原始数据、跨国测量可比性、实际样本外性能尚未审读或复算。不可宣称完成D005科学验收、历史预测验证或R证据升级。

## 协作与状态
此前D004为2026-W46的EIA电力容量专题，已读其跨表残差与舍入上界审计；本次选题为2026-W47独立人口迁移测量问题，避免重做D004。C014已在2026-11-08归档Robins等(2000)关于IPTW正值性与失访的原著研究；不再重建C014。
C当日：未核实2026-11-16有正式合格记录，PARTIAL。
D本周：本文件是第47周新专题候选的原始方法阅读和识别论证，PARTIAL，后续须完成更多原始页章与竞争解释方可判断合格完成。
Tests: NOT_RUN. CI: NOT_RUN. Billing: no paid API, cloud, CI or purchase triggered; account charges NOT_VERIFIED. R073/PESEN v0.1 frozen; R E1/E2/E3 and MARKET unchanged.
Next: 核查WPP2024 Section E其余预测步骤和人口残差法限制，并找独立登记数据/竞争论文进行比较；不得从净迁移推断移民总流量。
