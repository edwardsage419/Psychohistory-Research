# R117：描述性规范、指令性规范及注意焦点的限定研究

日期：2026-10-19（Asia/Taipei）
原候选目录：P0 03-009 Descriptive and Injunctive Norms。
**正式状态**：CLOSED_BOUNDED_ORIGINAL_1990_2007_PUBLISHED_AGGREGATE_AND_SYNTHETIC_NORM_FOCUS。限定学习状态：LEARNING_COMPLETE_BOUNDED_FIRSTPARTY_AGGREGATES_AND_FOCUS_MECHANISM_SYNTHETIC。**无原始个人/家庭微观文件，新增真人预测E2=0，R073及PESEN v0.1保持冻结。**

## 一手原论文（直接核阅）

1. [Cialdini, Reno & Kallgren 1990年焦点规范理论原刊](https://doi.org/10.1037/0022-3514.58.6.1015)，[原作者1990原12页扫描PDF](https://www.researchgate.net/profile/Robert-Cialdini/publication/232483471_A_Focus_Theory_of_Normative_Conduct_Recycling_the_Concept_of_Norms_to_Reduce_Littering_in_Public_Places/links/0912f508b1982686a5000000/A-Focus-Theory-of-Normative-Conduct-Recycling-the-Concept-of-Norms-to-Reduce-Littering-in-Public-Places.pdf)。核阅原第1015-1017页，Study1原Figure1：139位真实路过行人，四组原图n=(31,50,24,34)、原刊百分比=(6,14,54,32)。**仅重算公开已发表汇总**，基于取整图表唯一逆推2/31、7/50、13/24、11/34，未取得原受试者逐行观察。
2. [Schultz、Nolan、Cialdini、Goldstein、Griskevicius 2007年节能研究](https://doi.org/10.1111/j.1467-9280.2007.01917.x)，[Stanford托管原刊全文](https://sparq.stanford.edu/sites/g/files/sbiybj19021/files/media/file/schultz_et_al._2007_-_power_of_social_norms.pdf)。核阅原429-432页：290个原家庭，退出3户，短期287户；单独描述性邻里用电反馈与附加赞许/不赞许表情的对照，原基线-随访各组均值与真人群体样本数均来自论文公开表述，**不是本项目取得原电表逐人时间序列**。

## 重要结果

1990 Study1按刊物取整百分比：干净地面协作者激活描述性焦点时乱扔垃圾比例6%，未激活14%；脏乱地面激活时54%，未激活32%。简单比例差分别−8、+22百分点，因而**刊物取整差中之差为+30个百分点**。原作者整体交互统计显著，但两个给定环境中的简单对比各自不显著；本项目没有独立SPSS-X原始统计重算。

2007短期用电量的四个已刊均值差：D-only高耗电组−1.22kWh/天、D-only低耗电组**+0.89kWh/天（不希望的回旋效应）**、D+I高耗电组−1.72kWh/天、D+I低耗电组+0.24kWh/天（作者标注不显著）。此结果不说明加上I后证明用电完全不变，也不等于新测得因果效应。

额外纯教育用途的**项目原创静态Fraction toy**：D=1/5代表群体少有人采取亲社会行动，I=9/10代表多数人赞同亲社会行动。预设规范注意焦点分离的P(A=1)=p0+w_D(D−1/2)F_D+w_I(I−1/2)F_I，p0=w_D=w_I=1/2。双焦点关闭0.5，仅聚焦D为0.35，仅聚焦I为0.70，二者都聚焦0.55。D=I=4/5时，只关注D或I的概率同为0.65；D与I反向时概率分离。**这不是作者真实参数或家庭用电单位，更不是1990/2007人类行为的数值拟合。**

## 真正执行的代码/证据

[GitHub Actions run 39245376837](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39245376837)：**CI success，39项真正运行的原作者公开汇总算术与合成模型单元测试，全部通过**；源程序、测试、正式报告三个文件SHA256由GitHub工作流记录，并将[机器收据](R117_PHASE_A_FIRSTPARTY_PUBLISHED_AGGREGATES_FOCUS_39_TEST_CI_RECEIPT.json)提交main，再次回读已核实。

- [预冻结协议](../../protocols/R117_DESCRIPTIVE_INJUNCTIVE_NORMS_CIALDINI_1990_SCHULTZ_2007_AGGREGATE_AND_FOCUS_SYNTHETIC_FREEZE_2026-10-19.md)
- [完整第一手论文摘要、原图算术和合成机制报告](R117_CIALDINI_1990_SCHULTZ_2007_FIRSTPARTY_NORM_FOCUS_BOOMERANG_SCIENTIFIC_REPORT_2026-10-19.md)
- [原作者已发表汇总及独立合成数学程序](r117_descriptive_injunctive_norms_published_aggregate_focus.py)
- [39项可复算测试](test_r117_descriptive_injunctive_norms_published_aggregate_focus.py)
- [实际机器CI收据](R117_PHASE_A_FIRSTPARTY_PUBLISHED_AGGREGATES_FOCUS_39_TEST_CI_RECEIPT.json)
- [正式科研验收结题状态](R117_FINAL_ACCEPTANCE_STATUS.json)

复算：`PYTHONPATH=research/R117 python -m unittest -v research/R117/test_r117_descriptive_injunctive_norms_published_aggregate_focus.py`。只需Python 3.11标准库，无API订阅、不获取个人数据。

**科研限制**：规范的行为发生率/信念、对行为的赞同/反对、这些规范是否被注意聚焦，应分开操作化，才能在适宜设计中比较机制。同样的社会行为可来自不同信息或奖励路径。所有者决定仍为先完成全部既定R系列学习，再统一归类，最后熔炼；当前不启动用户个人辅助决策系统、R073模型修改或PESEN融合。
