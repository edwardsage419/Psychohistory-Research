# R077：全新第四项真人重复囚徒困境数据的前结果来源与信息集门

日期：2026-10-17。性质：**锁定数据可及性、实验独立性和结果不可提前窥视的候选来源**。在任何第四项真实人类 M0–M6 评分结果第一次生成之前建立；本文件不宣布获得第四项 E3。

## 背景和已使用的数据

R073、R074、R075分别使用 Montero-Porras 2022、Dal Bó/Frechette 2011、Fudenberg/Rand/Dreber 2012三项独立作者真人重复囚徒困境。R076为研究者已查看R074/R075结果后执行的跨研究**严格source-only数值转移**，其科学等级回顾性、不是新未见E3；详见 `research/R076/README.md`。R077必须首先确定第四项不重用这三个实验样本的**真实真人行为原始来源**；不得为了得到积极结果挑选数据集。R073七模型原始Git blob `c8a0b47fd27bf05e7be5b87419a0824355fc911a`、alpha20、TFT/WSLS固定0.05、teacher-forced同一局内t>=3及Brier/logloss均冻结。主要唯一donor若选择数值迁移，将使用R073全部12场已训练源参数，不得先比较/挑选R073 fixed或shuffled的优胜版本。

## 新增来源候选，所有都尚未查看真人模型结果

候选C1首选：Barreda-Tarrazona, Jaramillo-Gutiérrez, Pavan, Sabater-Grande (2026), *Exploiting the machine: Human cooperation with artificial agents in prisoner's dilemma*, Journal of Economic Psychology 116, 102925, DOI `10.1016/j.joep.2026.102925`。正式论文明确有真人对真人的 Humans 对照，随后三次每次10轮同伙伴的 repeated PD，以及真人对由人收益关联的人工代理的另一处理。原始实验代码、z-Tree和全部数据公开位置 [OSF 4HTQ3](https://osf.io/4htq3/) （DOI 10.17605/OSF.IO/4HTQ3）。**只考虑真人对真人 repeated PD**, 不把人机条件机器动作当另一个真人决策；原始 session/partner/time字段、真正先前行为反馈、是否存在同一真人跨session以及下载许可证等均 `UNKNOWN`。10轮比赛必须不跨game串联历史。论文已公开定性处理差异，但R077实际 M0–M6 分数和场次对比尚未计算；因此可以冻结新的外部评价但不能宣称过去论文对研究者全盲。

候选C2备用：Kasberger, Martin, Normann, Werner (2026), *Algorithmic cooperation: A comparison with human play in the infinitely repeated prisoner's dilemma*, Games and Economic Behavior 159,113–130, DOI `10.1016/j.geb.2026.06.001`。研究者2022–2023在Düsseldorf/Potsdam多场真实实验共240人，每原session20或30人，多局随机匹配，但算法Q-learning实验的模拟决策不能混入真人目标；论文有真实人类事前注册 [OSF zcv6x](https://osf.io/zcv6x/)，发表页说原始数据 `available on request`，不等于已取得开放原始逐轮字节。请勿从文章示例表构造伪真人行动。

候选C3备用：2019年 *Cooperation in the Prisoner’s Dilemma: an experimental comparison between pure and mixed strategies* (Royal Society Open Science)，论文数据声明OSF `https://osf.io/p4dgz/`。未核查真实场次、人员隔离及数据字节等价。

## 资格/可复现/隐私门

- G1 源资格：原作者、学会或作者指定公开原始档案；固定文件版本、真实大小、SHA256/来源Git blob和材料许可，公开下载失败为 `BLOCKED_SOURCE_ACCESS`，不能直接使用研究者脑补原始CSV。
- G2 真人决策及暴露：明确human-human vs human-agent、玩家与同伙伴配对、同局 t-1、t-2 实际能看见的行动；未知互动信息则禁用该目标、不偷看当轮对手动作。其他实验(独立参与者群)不与先前三个源重叠。
- G3 统计单元：恢复研究者原生 session 与人员处理范围，训练/测试不可以共享整场人员数据；若仅有同一人多局，supergame LOOG 不等价 session。某处理只1场，不能强行同处理 LOSO；仅独立 source-only迁移时可预先定义所有原场次完整评分，但不能冒称被试实体隔离。
- G4 **先于第一次实际模型评分再另交一份一手字段映射与计分协议**，锁定合格子样本、E3定义、预定主要模型对比M3-M1和M4-M3、每场等权Brier及logloss、反例、失败条件；模型未正式执行前不允许窥视选好的源上的表现。已见公开论文处理主结论不等于我们的模型结果完全盲。不得根据历史R076两目标正负改超参。
- G5 公开仅匿名实验级总体计数和全部模型宏结果；不保留个人原始行动、逐轮路径、场次ID、单人或单场得分。默认读到原始数据应在GitHub CI临时目录执行，不提交源人类行。

本阶段目标限于合法可读取的来源文件可达性和安全格式审计，不进行真人模型评分。任何未获得源数据与session结构的候选标 `SOURCE_NOT_ELIGIBLE_YET`，**禁止宣称R077新独立E3 PASS**。若三个候选当前都无可审计来源，报告负结果并尝试下一真实来源；不降低证据要求。

`R077_PRE_MODEL_RESULT_SOURCE_GATE=FROZEN`
`R077_NEW_FOURTH_HUMAN_EXPERIMENT_SCORED=NO`
`R077_E3=OPEN`
`R076_RETROSPECTIVE_RESULTS=NOT_PROSPECTIVE_FOURTH_STUDY`
`PESEN_v0.1=FROZEN`
