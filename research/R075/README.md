# R075：第三独立真人重复囚徒困境，原作者噪声反馈与冻结七模型外部场次复验

2026-10-17。**正式状态 `CLOSED_BOUNDED`。第三作者一手真实 E3 结构复验通过，七个 R073 冻结模型无改动，PESEN v0.1 继续冻结。**

本项正式研究由[早期来源受阻审计](R075_PHASE_A_THIRD_HUMAN_SOURCE_RECOVERY_AND_LAG_SEMANTICS_2026-10-17.md)推进至[共同作者 David Rand 亲自公开的源档案](https://davidrand-cooperation.com/s/slow-to-anger-and-fast-to-forgive-data-and-code.zip)：原 ZIP 1129409字节 SHA256 `328346c3cf88a71a3d6cf574f7d6ba741dcea460f3926c16266f1784d3a699ef`，真正24字段TXT 34446次参与者意向动作，18个原始独立实验场次、384个场次内参与者身份槽、17223次双人配对轮、可评分的26116次完整 t>=3 行动。原始个人、场次、匹配、行动轨迹均不存入 Git。

## 事先冻结的 E3 工作依据与机器执行

[最早外部来源资格协议](../../protocols/R075_THIRD_INDEPENDENT_HUMAN_IPD_SOURCE_GATE_2026-10-17.md)；[真实人类模型评分之前独立冻结的最终适配与评价协议](../../protocols/R075_COAUTHOR_ORIGINAL_HUMAN_18_SESSION_E3_TRANSFER_FREEZE_2026-10-17.md)，其先于任何真实 R075 七模型拟合的 commit 为 `c0ee924a8ca4ddfceaef2a0ca95914b4e7a0f991`。所有模型都直接导入同一个 R073 Python 本体 Git blob `c8a0b47fd27bf05e7be5b87419a0824355fc911a`，`alpha=20`，固定理论TFT/WSLS参照错误率0.05，不允许因 R075 数据重新寻优。

[原作者真实ZIP字段结构CI](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38990465782)，[同局双人历史与执行噪声审计CI](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38990601050)，[真实24列来源选择含义源码审计](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38990685555)，[首次36项合成测试与完整真人E3评分CI](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38990907812)，[独立重跑并核对18场匿名成败计数的CI](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38990975608)，以及[再次完整重算并用 SHA256 归档的 CI](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38991027657) 均已 success。

[七模型真实来源外部评分程序](r075_coauthor_real_human_e3.py)和[24项完全合成测试](test_r075_coauthor_real_human_e3.py)；[来源结构程序](r075_coauthor_original_session_structure.py)和[12项来源虚构测试](test_r075_coauthor_original_session_structure.py)。正式[19,692字节真人匿名宏结果JSON](R075_REAL_THIRD_HUMAN_18_SESSION_E3_RESULTS.json) SHA256 `eb74129bfd9af62678e9cacf910477854be694317d7b5d875e5ca33dc0f76174`。完整[科研数值、六条件反例和不能声称的推断边界](R075_REAL_THIRD_HUMAN_E3_RESULTS_AND_SCIENTIFIC_BOUNDARIES_2026-10-17.md)；[A01至A06六项机读验收](R075_FINAL_ACCEPTANCE_STATUS.json)。

## 科学结果

18个原始 `file` session严格逐场留出，同处理其它1至3个场次独立训练，每场计算完整可观察过去两轮的真人下一轮 **意向 C/D**，先场次等权再总体等权：

* `M3_JOINT_LAST - M1_OWN_LAST = -0.029117355804310772`，18场全部改善，提供第三项真实独立数据对上轮对手行动额外预测信息的支持；
* `M4_JOINT_TWO_LAGS - M3_JOINT_LAST = -0.012416864447856633`，18场15改善3恶化；在 `bc=4,error=0` 的全部3场**额外两轮历史更差**。相比R074的 M4 净恶化，本项更加说明深度收益依赖实验条件，不能将16态模型提升为普适行为律。
* 18场整体七模型Brier M0=0.226836、M1=0.170090、M2=0.169751、M3=0.140972、M4=0.128555、M5=0.211260、M6=0.376559。全部 log loss及6处理级配对胜负保存在上述原始匿名JSON。

此研究在**第三个不同原作者真人实验**上验证已经冻结的条件特征结构，所有真人历史数据只用于源内训练的其它场次，仍未检验 R073 数值参数直接外部零样本迁移。源中数字 `subject` 在不同session重用，不允许推断实体身份相同或绝对不同；当轮标签是人的意向，过去信号是已实施反馈，故与无噪声的R073/R074语义边界不同。独立社会反馈记忆的因果作用、制度与长期历史动力学仍无证据闭合。

**`R075=CLOSED_BOUNDED`、`E3_THIRD_REAL_HUMAN=PASS`、`M3_ADDITIONAL_OPPONENT_INFO=REPLICATED`、`TWO_LAG_SCOPE=CONTEXT_DEPENDENT`、`PESEN_v0.1=FROZEN`。**
