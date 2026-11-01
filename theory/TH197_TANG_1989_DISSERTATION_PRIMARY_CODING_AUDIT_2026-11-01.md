# TH197补记：Tang 1989原始博士论文中的47案例分类、观察单位与绩效口径

track: theory
subflow: main
run_date: 2026-11-01 (Asia/Singapore)
source_checked_date: 2026-11-01
target_key: (theory,Tang1989_dissertation,primary-scanned-v1,47_case_classification_selection_time_slices)
baseline_head: b3b928b870d0e08baaaf9c2692f8becefc786c51
status: COMPLETE_PRIMARY_1989_SELECTED_PAGES; PARTIAL_1994_AND_2010_RECONCILIATION
evidence_scope: ORIGINAL_DISSERTATION_SCANNED_PAGE_VISUAL_INSPECTION; NONBLIND; NO_MICRODATA_REESTIMATION
r_e1_e2_e3_upgrade: NONE
ci_status: NOT_RUN
billing_checked: NOT_VERIFIED

## 原始来源与实际阅读范围

Shui-Yan Tang (1989), *Institutions and Collective Action in Irrigation Systems*, Indiana University dissertation, Digital Library of the Commons, https://hdl.handle.net/10535/3596 ，馆藏原始扫描PDF https://dlc.dlib.indiana.edu/dlc/bitstreams/9a8fe27b-ddc5-49ce-a389-6ff9229e1d8c/download 。本轮通过机构公开PDF的逐页图像直接阅读印刷pp60–68、78–82，特别核对p62编码表说明、p63抽样和重编码、p64样本总数与重复时间切片、pp65–68 Tables 3.1–3.3、p79 Table 4.1、p81 Table 4.2、p82结果解释。扫描PDF的零起算页号=印刷页号+12，例如印刷p64对应PDF第76页（零起算）。原PDF正文为扫描图像，未使用自动OCR，未下载或转载第三方原文。

版本边界：此为1989年原始博士论文；Tang (1992) *Institutions and Collective Action: Self-governance in Irrigation* 为后续著作；Tang (1994) “Institutions and Performance in Irrigation Systems”, in *Rules, Games, and Common-Pool Resources*, pp225–246，仍未核验正式章节pp229–234。不能推定三个版本的样本、绩效口径完全一致。

## 新增可直接确认的原作者事实

1. **全47案例的原始分类已从二手转述升级为原作者一手确认。** Tang1989 p64明确为29个community systems、14个bureaucratic systems、4个由local governments治理的其他系统；Tables 3.1–3.3的标题分别写N=29、N=14、N=4。29+14+4=47。此前TH197交叉核验中NRC2002 p98的29/14/4分类如今在1989原始版本得到独立原文核实；仍不能据此修订Ostrom2010 p650的25/12口径。
2. **样本选择具有资料完整性条件。** p63说明47个案例从数百份项目收集文献中选取，优先纳入具有较完整物理、社区和制度属性信息的案例。该选择机制使47例无法被当作灌溉系统总体的概率样本。
3. **观察单位不全是独立灌溉设施。** p62将operational-level form定义为相对稳定的时间切片，规则或环境变化可产生新的切片；p64明确San Antonio (1)/(2)、Tanowong (T)/(B)、Lurin Sayoc (1)/(2)代表同一设施不同运作时期或条件。对47条记录直接采用独立同分布假设存在风险；具体设施去重数和依赖结构尚未重建。
4. **地理与工程类型高度不均衡。** p64称47例中42例位于亚洲，29个simple、18个complex。p60解释complex系统可能只分析某个取水区，而simple系统分析整体取水资源；跨组比较的空间层级并不统一。
5. **测量存在明确的离散化。** p63说明将原编码表若干四档或五档变量压缩为二档，例如供水量五档压为adequate/inadequate。这可能丢失阈值附近的信息，且编码选择需与原始案例材料交叉核验。
6. **绩效不能简单等同供水充足。** p79 Table 4.1按维护、遵守规则、供水充足三维给出五个实际模式，计数依次21、8、4、13、1，总数47；p80称46/47满足所采用的累积模式，p79报告系数CR=1-1/(47×3)约0.99。p81 Table 4.2在供水充足的21例中21例均有规则遵守和良好维护；供水不足的26例中8例仍同时具有良好遵守与维护。p82原作者明确供水不足可由外部环境、上游供水分配决定，不能自动归咎于本地集体行动失败。

## 竞争解释与可检验后果

原作者制度解释：地方参与者的行动规则、维护合作和供水条件相互关联。竞争解释包括地理水资源约束、上游行政放水、案例入选的资料完整性、同一设施跨时间重复、simple与complex空间单位差异，以及研究者把连续信息二值化带来的阈值误差。

构造性识别反例：若同一设施前后两个时期分别记为两条案例，按47个独立设施估计方差会遗漏同一设施内的相关性。仅有表3.1至3.3的系统名称不足以恢复真实协方差；应追溯每个case的设施ID和时间区间。这是由原作者编码规则推得的方法风险，未实施实际方差重估。

四层联系：个体层是灌溉者遵守规则与劳动投入；群体层是维护协作及上游下游利益；制度层是水权、治理主体、操作规则；历史层是同一设施随时期改变的规则、环境和行政关系。各层关系为研究假设，未进行跨层因果识别。

## 对TH197先前疑点的更新

1989原始版的29/14/4分类：COMPLETE（选定原始页和表核验）。
Ostrom2010 p650的47总体、25农民、12政府及7/12与40%矛盾：仍PARTIAL。原始1989分类无法确定2010是否使用有结果子样本、不同定义或出版错误。
Tang1994 p229–234正式版及高绩效定义：NOT_READ。NRC2002仍属二手来源。
表4.1的算术与197补记数字：5项Python Fraction/整数断言PASS，含29+14+4=47、21+8+4+13+1=47、CR=140/141、42<47、7/12≠2/5；这些仅验证指定算术。

## 证据与后续

研究范围仅为原作者扫描页视觉核验和算术。没有原始47案例电子数据、没有因果重新估计、没有独立历史预测、没有R E1/E2/E3提升。尚未逐页审读论文其余章节，特别是pp83–193的统计分析、规则机制和结论。下次优先核查Tang1994正式章节p229–234的样本筛选与绩效分母，或在授权条件允许时逐项核对1989 Tables 4.9–4.11中的类别与绩效；Scott1998可读性理论原著亦保留为跨学科队列。

C009在2026-11-01已完成；D002在2026-W44于2026-10-26完成。本轮两者只读。R最新P0八模型验收入口仍有采纳阻塞，不能当成E1/E2/E3科研验收。开放Codex PR未经合并不构成main成果。无付费API、无CI触发，账户实际账单未核验。
