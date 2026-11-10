# D004 补充：EIA 表格来源差异与舍入误差上界审计

日期：2026-11-10；track: theory；subflow: D；状态：PARTIAL。
研究键：(theory-D,EIA-EPA-2025-T4.6-T4.7B,2025,source-provenance-and-rounding-bound)。
写前观察 main HEAD：a5ab201791c59fd0c0033c734892ea7051d72b00。

## 实读官方原始范围
EIA Electric Power Annual 2025，Table 4.6 全部风电、太阳能容量变化行及 Notes/Source；Table 4.7.B 表头、U.S. Total 行及末尾 Sources/Values are final。访问2026-11-10。
https://www.eia.gov/electricity/annual/html/epa_04_06.html
https://www.eia.gov/electricity/annual/html/epa_04_07_b.html

## 新增来源区别
Table 4.6 页尾来源仅列 Form EIA-860 Annual Electric Generator Report；Table 4.7.B 页尾同时列 Form EIA-860 和 Form EIA-860M Monthly Update。故“同一年度报告”不意味着两个表完全使用相同的上游报表集合。该事实提出一个可检验的来源版本/更新竞争解释，但未证明任何残差来自 EIA-860M。Table 4.6 注释还明确以主要能源来源归类多燃料发电机，Existing Capacity changes 包含 uprates、derates、repowerings 和既有报告容量修正。

## 舍入误差的严格上界（构造性数学审计）
假定每一个展示的一位小数 MW 数字由真实同口径数值独立四舍五入到0.1 MW，每项舍入误差绝对值不超过0.05 MW。风电残差为
R_w=(159032.1-152097.3)-(6082.0-20.0+771.1)=101.7 MW。
五个输入项的误差绝对值总和上界为5×0.05=0.25 MW。因此仅由显示位数舍入产生的残差至多0.25 MW，无法解释101.7 MW。

太阳能合计使用2025及2024光伏与太阳能热发电各两项，以及新增、退役、调整三项：
R_s=[(151958.0+1392.0)-(122060.1+1392.0)]-(29459.1-8.1+282.8)=164.1 MW。
七个输入项误差绝对值上界为7×0.05=0.35 MW。即使保守计入四项存量舍入，单纯舍入也无法解释164.1 MW。

上述上界依赖一位小数常规舍入及相同被测对象的条件。实际统计分类、样本范围、历史修订和来源集合差异尚未核实。若来源对象不同，代数差值依旧可算，但“应该闭合”的前提尚未成立。

## 竞争解释及证据边界
候选解释包括 EIA-860M 月度更新与年度报告数据集合差异、历史容量修订、技术归类、纳入范围、报告时点差异。仅从汇总表无法分配各候选因素的贡献。这里是来源注释核验及构造性舍入上界，非发电机级实证复算，也非政策因果证据。

C015 2026-11-10 已有正式研究，未新增C编号。D004 2026年第46周仍PARTIAL。R073/PESEN v0.1保持冻结。原始数据复算NOT_RUN；CI NOT_RUN；付费服务调用NOT_RUN；实际账户账单NOT_VERIFIED。下一步固定EIA-860与EIA-860M源版本、核对容量字段及发电机集合，再尝试微观桥接。
