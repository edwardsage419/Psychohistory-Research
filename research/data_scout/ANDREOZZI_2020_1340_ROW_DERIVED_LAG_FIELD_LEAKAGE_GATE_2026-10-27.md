# A轨：Andreozzi、Ploner、Saral 2020公开真人数据的两个伪滞后字段

日期：2026-10-27。状态：`TWO_MISLAGGED_CURRENT_PERIOD_CLASSIFICATION_FIELDS_CONFIRMED`。沿用此前已登记的同一实验，不增加独立实验计数。原作者论文：DOI 10.1038/s41598-020-70681-z。公开仓库 `seyhunsaral/stabilitycondcoop`，固定提交 `979abf87b5d3cfb7aa8be13b81ef233076c3bb75`。真实CSV `data/csv/subjects.csv`，Git blob `bd4c1550002621bee7dfb50e0d15d317764d1ea9`。清洗程序 `code/process_raw_data.R`，Git blob `522efd459f574ccaef3d9ce1dd2b086ffb70370e`。作者README与LICENSE明确数据CC BY 4.0、软件MIT。本项目只归档聚合审计，不复制参与者记录。

## 新增的代码级证据

在作者 `code/process_raw_data.R` 的 `Lagged Variables` 小节，`opp_cond_class_wide_o_lag1` 初始确实经 `dplyr::lag(opp_cond_class_wide_o,...)` 生成，随后被 `replace(opp_cond_class_wide_o, period==1, NA)` 覆盖，右侧使用的是**当期原变量**。同样，`opp_cond_class_narrow_lag1` 最终由 `replace(opp_cond_class_narrow, period==1, NA)` 覆盖，也使用**当期原变量**。相比之下，`opp_cond_class_wide_lag1` 在覆盖首轮缺失值时正确引用自身滞后列。

## 本轮实际全量核验

通过GitHub文本连接器实际读取全部1340行、67列CSV，按134个 `subject_unq` 独立身份分组、按 `period` 升序核验。首轮134条，剩余1206条都有前一轮可对照。

| 字段 | 与当期相同 | 与上一轮相同 | 与上一轮不同 |
| --- | ---: | ---: | ---: |
| opp_cond_class_wide_o_lag1 | 1206 | 393 | 813 |
| opp_cond_class_narrow_lag1 | 1206 | 560 | 646 |
| opp_cond_class_wide_lag1 | 不适用 | 1206 | 0 |

两个错误字段在全部1206条可比较记录中均与**当期**类别完全相同。首轮滞后值缺失处理正常。2项预设错误字段负对照均检出。该发现直接来自作者清洗代码和真实CSV逐行对照；作者发表论文的模型结果是否实际使用了这两个字段，尚未核实，不能据此判定论文结论错误。

## 科学使用资格

任何预测时点仅允许使用决策之前已知的字段。若把上述两列当作上一轮对手类别使用，将把当期对手条件策略信息错误引入历史特征，形成前视泄漏风险。未来若使用此数据，应根据固定身份和真实period显式重建上一轮字段，并在留出场次前冻结映射；不能直接信任这两列的名称。原始行动为0、50、100三级，R073原二元博弈冻结评分不可直接迁移。来源已在2026-10-25完成1340行与镜像配对核验，本轮新增的是两个字段的时间语义审计。新增真人预测评分E2=0、历史E3=0。

可重放脚本：`research/data_scout/a_andreozzi_lag_field_leakage_20261027.js`，需自行从上述公开仓库取得固定Git blob CSV，使用免费Node.js运行，原始真人数据不随本项目再分发。机器聚合收据：`research/data_scout/ANDREOZZI_2020_1340_ROW_LAG_LEAKAGE_AUDIT_RECEIPT_2026-10-27.json`。费用新增0；GitHub Actions未启动。