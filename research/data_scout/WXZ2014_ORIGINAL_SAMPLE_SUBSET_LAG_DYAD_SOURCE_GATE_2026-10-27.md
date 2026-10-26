# A轨：WXZ2014原研究总体与stratEst子集的样本边界、历史字段和双人配对核验准备

日期2026-10-27。新增来源比较：原作者2014年Scientific Reports论文`https://www.nature.com/articles/srep05830`的Methods和Results明确说明360名真人、60个互不重叠的六人实验组，每组300轮，组内随机两两配对，五种收益参数。来源英文全文`https://pmc.ncbi.nlm.nih.gov/articles/PMC5376050/`。

stratEst官方R包WXZ2014说明`https://search.r-project.org/CRAN/refmans/stratEst/html/WXZ2014.html`明确是72名真人、300轮、21600行、六字段的包内数据。72/360=1/5，若各组完整则对应12/60个实验组。**该包内数据覆盖原论文总样本的一部分**。具体是哪12组、收益参数如何分布、是否另有排除规则尚未核验，禁止将包内21600行描述成原论文全部实验数据。两个RDA固定Git blob身份沿用前一份A报告，不重复提交二进制。

软件作者公开示例`https://fdvorak.com/stratEst/`显示`stratEst.data(data=WXZ2014,choice="choice",input=c("choice"),input.lag=1,id="id",game="game",period="period")`。衍生`input`只编码上一轮**自己的行动**，第一轮缺失；它没有包含上一轮对手行动。原始`other.choice`记录当轮对手行动，必须按同一参与者与game的上一轮构造历史对手行动，严格在时间上向后移动。

原六字段缺少明确的`opponent_id`。即使同一game与period内六条记录的行动对称多重集一致，也无法在存在相同行动时唯一恢复对手身份。独立双人事件镜像资格继续阻塞。

新增可执行门槛`research/data_scout/a_wxz2014_game_round_gate_20261027.js`：接受解码后JSON记录，检查12组、72个game|id身份、每人300轮、21600行、各组六人每轮6条、行动对称多重集、结果胜负关系，以及若提供衍生input则严格检查上一轮自身行动和第一轮缺失。已实际执行4个合成测试：正常镜像通过，故意破坏对手行动、历史input、结果字段分别检出。**真实RDA尚未解码，所有真人行级检查均未执行**，不能据合成通过宣布E2数据验收。

复现难度：中等。需在无费用环境取得并解码固定RDA，先检查game标识和收益处理映射，再运行此门槛。数据单独再分发许可仍未知，不能再分发原始参与者记录。R073二元囚徒困境冻结模型直接迁移资格仍为BLOCKED；三行动RPS只适用于未来单独事前冻结的新评价。新增E2预测评分0，E3历史预测0。

所有引用均为英文研究原文、英文R包文档及英文软件作者说明。