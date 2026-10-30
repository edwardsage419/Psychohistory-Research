# A轨：Andreozzi 2020 第二个历史变量错位与六列时序核验

日期：2026-10-30 UTC。目标键：(A,Andreozzi2020,author-public-master-522efd459f+subjects-bd4c155,second-narrow-lag-and-six-column-order-audit)。来源为英文公开作者仓库 `seyhunsaral/stabilitycondcoop` 的 `data/csv/subjects.csv`，Git blob `bd4c1550002621bee7dfb50e0d15d317764d1ea9`，`code/process_raw_data.R` blob `522efd459f574ccaef3d9ce1dd2b086ffb70370e`，`code/main.R` blob `3b4f79ce3ddb2d144ea31ccbed26aa03396c9e3c`。论文 DOI `10.1038/s41598-020-70681-z`。作者数据 CC BY 4.0，代码 MIT；不重新分发原始参与者 CSV。

## 本轮实际读取与结果

通过 GitHub 连接器读取完整 425701 字符公开 CSV，使用 JavaScript CSV 引号解析器核验 1340 行、67 列、134 名主体。每名主体恰好10行，文件内 period 顺序为1到10，没有倒序、缺期或重复期。对每名主体的 period2..10，共1206个可比较行，直接与上一期的同一主体字段逐项比较。

| 声称的上一期字段 | 与真实上一期相符 | 与真实上一期不符 |
| --- | ---: | ---: |
| opp_action_lag1 | 1206 | 0 |
| opp_cond_type_lag1 | 1206 | 0 |
| opp_cond_class_wide_lag1 | 1206 | 0 |
| opp_cond_class_wide_o_lag1 | 393 | 813 |
| opp_cond_class_narrow_lag1 | 560 | **646** |
| first_player_lag1 | 1206 | 0 |

新增发现：`opp_cond_class_narrow_lag1` 有646/1206=53.57%的历史值与真实上一期不符；它在全部1206行都等于**当前期**的 `opp_cond_class_narrow`。此前发现的 `opp_cond_class_wide_o_lag1` 813/1206不符在本轮再次复核，全部1206行也等于当前期的 wide_o。646个 narrow 错位行全部包含在813个 wide_o 错位行中，二字段错位行的并集为813行，不能把两项直接相加成独立的1459行。

按处理条件分解：CondInfo 可比较594行，wide_o错位411、narrow错位328；NoCondInfo 可比较612行，wide_o错位402、narrow错位318。原清洗程序的两个覆盖行分别使用 `replace(opp_cond_class_wide_o, period==1, NA)` 和 `replace(opp_cond_class_narrow, period==1, NA)` 赋值到同名 lag1 字段，直接解释为什么最终 lag1 实际等于当前期。另四个滞后字段在当前固定 CSV 的行级比较全部相符。

## 分析路径及证据限制

原作者 `code/main.R` 第300行使用 narrow_lag1 构造 `observed_opp_cond_class`，但第306和308行展示的 Table 3 两个 glmer 公式没有包含该派生变量。静态读取不能证明这两项回归系数受到该字段错位影响。是否存在其他脚本、下游分析、报告图表引用，仍需完整复算与动态依赖审计。`order_by=subject_unq` 在组内恒定，当前 CSV 恰好按 period 单调排列，因此其余四列在当前固定版本可用；上游行顺序变化时仍存在潜在风险。

本轮归档独立标准库 Python 重放脚本 `a_andreozzi_2020_six_lag_fields_audit_20261030.py`，固定原 CSV Git blob 后检查六列。该 Python 脚本已语法编译；在本轮容器未取得原始 CSV 文件字节，完整 CSV 的 Python CLI **NOT_RUN**。实际远端完整来源行级检查通过的是独立 JavaScript 解析流程。原始六场 XLS 到 CSV 的动态重建仍 OPEN。R073 冻结100轮重复博弈复现资格仍为 NO。新增真人样本外预测 E2=0，历史 E3=0。
