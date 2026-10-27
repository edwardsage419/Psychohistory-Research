# A轨 2026年10月28日：Akata等真人对战语言模型的重复博弈数据来源及行为编码审计

## 固定公开来源与实际获取

原作者仓库： https://github.com/eliaka/repeatedgames 。
完整公开CSV： https://github.com/eliaka/repeatedgames/blob/main/human_experiment/analysis/repgames.csv ，Git blob `2dd67c6ff80f2d7aa07a70b470e26fe3592c6d95`，97945字节。本轮通过GitHub读取全部CSV字节，实际解析3900条行为记录和七字段 `id,game,action,score,opponent,guess,coordination`。分析程序 `human_experiment/analysis/repeated_games.Rmd` Git blob `ca9991b6d0917156672e1e2fea923548562d945e`；实验源码 `human_experiment/experiment/js/script.js` Git blob `4b7be85e8b3b964bfd0722d796f5ed6c2b8f0a19`；实验说明 `human_experiment/experiment/README.md` Git blob `77115c8edb43dbc7ef8bc46e596f67d58f2c8f81`。

## 已执行的字段与身份审计

195个匿名id，每个id共20行，PD与BoS各10行。PD1950行，BoS1950行。PD条件Base为970行（97个id），Prompted为980行（98个id）；每个id的条件标签在两种游戏中一致。实验README明确每个游戏10轮。CSV没有显式轮次列、独立实验场次列或对手逐轮行动列；本轮只核验行顺序与每id/游戏计数，不能把推定轮次追认为原生字段。实验对手是GPT-4语言模型，属于真人对AI实验，不是独立真人双人互博。

PD源码 `calculate_points_pd` 明确 `action=1` 代表J（合作），`action=0` 代表F（背叛），双方J/J得8，F/F得5。全部1950行PD中 `action=1` 有931行，`score=5` 有783行且全部 `action=0`；其交集为0。PD的动作/得分分布：0|10为235，1|0为213，0|5为783，1|8为718，0|0为1。最后一条与常规收益矩阵不符，可能来自超时随机动作无报酬机制，尚未取得逐轮超时原始字段，不作确定归因。

## 明确的可复核测量缺口

作者R分析脚本在PD段写有 `dpd$cooperated<-ifelse(dpd$score==5,1,0)`。依据同仓库实验源码，得分5对应双方F/F，属于共同背叛；用此式作为合作指标将783行共同背叛标为1，931行真实合作动作标为0。这一变量定义与源码行动语义冲突。不能直接引用该Rmd的 `cooperated` 变量来评价真人合作率。此处只报告代码及数据层面的测量冲突，尚未独立复算论文图表或推断论文主结论受到何种影响。

## 许可、R073准入与复现准备

仓库顶层MIT许可文件主要声明软件许可；本轮未发现针对人类行为CSV独立明确的许可与受试者同意再分发说明，因此只归档来源Git blob、脚本与聚合统计，不复制参与者级原始CSV。无需账号或购买即可通过GitHub读取，当前可获得性=YES，逐行结构核验=YES，匿名id与10轮结构核验=YES；会话独立性、原始实验同意、对手逐轮行为完整性=UNKNOWN。

R073冻结协议针对双人真人重复囚徒困境且为100轮；此候选为真人对GPT-4且仅10轮。R073直接独立真人复验资格=NO。可作为未来另行预注册的真人与AI互动E2候选，当前新增E2预测评分0项。证据等级不得与E1合成或E3历史混用。下一步需要许可确认、异常超时行来源审查和独立真人对真人实验。
