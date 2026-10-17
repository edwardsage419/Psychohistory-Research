# R079：真实原作者动态双人配对网络与组级方差的第一次 E2 实证

2026-10-17，**`CLOSED_BOUNDED`、E2 原作者真人清洗数据描述统计**。在 R078 已完成的纯合成“个体预测无法识别社会因果”反例基础上，R079引入第五个独立作者实验领域（并非第五项同式IPD零样本E3），检验实际双人配对的群体共变是否能够在原始数据中真实观测，以及实际组均值方差相对固定当轮个人选择的随机重组数学参考值有多大差异。

原作者 Andreozzi、Ploner、Saral 2020，[论文](https://doi.org/10.1038/s41598-020-70681-z)、[GitHub 数据/代码](https://github.com/seyhunsaral/stabilitycondcoop)，固定Git提交 `979abf87b5d3cfb7aa8be13b81ef233076c3bb75`，作者亲自清洗的 `subjects.csv` Git blob `bd4c1550002621bee7dfb50e0d15d317764d1ea9`（425,701字节，许可CC BY 4.0）。实际核验**1340条真人正式游戏记录、134个场次内人物身份槽、6个真正实验场次、10轮次、670组双人配对，全部对手身份与真实动作镜像互证**。未重新执行6份原始zTree Excel的作者R清洗过程，相关来源真实性边界保持开放。

事先冻结的唯一方法：在每个原始session×正式轮次固定所有人已实现贡献 `y=action/100∈{0,0.5,1}`，对真实二人组内的去均值行动计算`pair_cross`，和均匀随机完美重配对下的 `random_ref=−pop_var/(N−1)`比较。按场次等权的真实结果如下：

| 组级统计 | 全部6场 | CondInfo 3场 | NoCondInfo 3场 |
|---|---:|---:|---:|
| 本人平均贡献份额 | 0.328775 | 0.342588 | 0.314962 |
| 实际配对去均值交叉矩 | +0.033114 | +0.042004 | +0.024224 |
| 随机重配对数学参考交叉矩 | −0.006030 | −0.006732 | −0.005328 |
| 超额交叉矩 | **+0.039144** | +0.048736 | +0.029552 |
| 实际组均值方差 | 0.080317 | 0.091224 | 0.069410 |
| 同一组人数下随机配对组均值方差 | 0.060745 | 0.066857 | 0.054634 |

六场中超额交叉矩均为正；前5轮平均贡献0.366692，后5轮0.290859。**此处仅有实证配对相似性及有限总体随机匹配的数学参考；随机重配对并未实际进行干预，也没有识别“社会传染/同伴因果效应”**，更不能套用R078十人群体方差或将短期实验变化冒充真实历史演化。

交付：
- [正式科学报告与全部来源/配对/设计假设、负面边界](R079_REAL_HUMAN_NETWORK_DYAD_GROUP_MOMENT_REPORT_2026-10-17.md)
- [首次数值计算前独立冻结的协议](../../protocols/R079_INDEPENDENT_HUMAN_DYAD_COVARIANCE_RANDOM_MATCHING_REFERENCE_FREEZE_2026-10-17.md)，commit `91faba1f2d956aec76550028f9ce1da681bd8c54`
- [精确有理数真人配对计算程序](r079_real_human_dyad_matching_moments.py)与[34项纯合成保护测试](test_r079_real_human_dyad_matching_moments.py)
- [第一次成功取得真实真人宏统计 GitHub Actions](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38996579448)，两jobs成功；[第二次独立原作者Git blob重下载、双次字节完全重算并永久Git归档](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38996643486)，SUCCESS
- [3,771字节匿名宏统计JSON](R079_REAL_AUTHOR_HUMAN_DYAD_NETWORK_MOMENTS_E2_RESULTS.json)，SHA256 `82efe8ad7bcc6c01ac10616676d84c5208ad9f6cc83670aa4c5b72f3860ff102`
- [A01–A06正式有界结题](R079_FINAL_ACCEPTANCE_STATUS.json)
- [首次纯合成隐私测试误报失败](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38996553953)严格保留（未运行真人计算，后仅修改字符串误报断言，没有改变真人指标公式）。

下一步最值得检查 [Shirado/Christakis 2020 的64组网络、1024名真人、机器人参与的公开原始资料](https://data.mendeley.com/datasets/t963ktp6ft/1)；只有校验原始字节、人类与机器人区别、网络动态、真实受试者与组级独立单位之后才可进入完整群体研究。PESEN v0.1冻结。

`R079=CLOSED_BOUNDED`；`R079_E2_AUTHENTIC_DYAD=YES`；`REAL_CAUSAL_PEER_EFFECT=NOT_IDENTIFIED`；`R078_N10_EXTERNAL_VALIDITY=NOT_ESTABLISHED`。
