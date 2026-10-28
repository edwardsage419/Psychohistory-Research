# A轨 Mao等2017年长周期真人重复囚徒困境：来源、配对代码与复现资格

日期：2026年10月28日（Asia/Singapore）。资格：PUBLIC_PAPER_AND_CODE_VERIFIED / RAW_BEHAVIOR_BYTES_BLOCKED / DATA_LICENSE_UNKNOWN / E2_READY=NO。

## 原始来源与研究结构

Andrew Mao、Lili Dworkin、Siddharth Suri、Duncan J. Watts，2017，*Resilient cooperators stabilize long-run cooperation in the finitely repeated Prisoner's Dilemma*，Nature Communications 8:13800，DOI 10.1038/ncomms13800。英文原作者论文：https://www.nature.com/articles/ncomms13800 。论文公开说明共有94名真人，跨20个连续工作日，最多进行400场每场10轮的有限重复囚徒困境；这些是论文报告值，当前尚未以原始数据独立复核人数、总场数或完整率。论文数据可用性声明指向OSF https://osf.io/64z8u/ ，原实验程序指向 https://github.com/TurkServer/long-run-cooperation 。

实际通过GitHub连接器核验原实验代码 `TurkServer/long-run-cooperation` 的master固定HEAD `4d8ed83e7745e1ffe82ce9403064e3558fabfa6f`。逐文件读取README、`lib/constants.js`（Git blob `456c979fa975419a8a00be05704ea2a176bfb99d`）、`server/assigner.js`（`3f4bbf338dbedd09ab4d9a3f28975acc7255df1b`）、`server/server.js`（`3e135c7558c929d8a81f750694327b82ba7c5d82`）和`models/models.js`（`f55a61ee2533a6fdff8ce29b14cfcd69adee9764`）。

## 实际确认的时间、身份、行为与独立性结构

冻结代码常量 `numGames=20`、`numRounds=10`。每场游戏10轮，代码按参与者进入大厅后随机打乱并每两人分组；每次新游戏形成新的instance，`GameGroups`存储counter、timestamp、assignments、leftOut、instances、batchId。由此可以确认代码设计为每场游戏重新随机配对，不能把跨游戏的同一参与者行为当作同一固定对手的100轮轨迹。

`Actions`集合记录userId、roundIndex、action、timestamp，按游戏实例分区；`Rounds`集合记录轮次index、行动数量、ended与results。服务器通过`chooseActionInternal`插入行动，完成两人选择后计算收益；`endGame`记录finished、abandoned或torndown。模型中的`roundIndex`在每个10轮游戏内重置。复现必须使用实验实例ID和参与者身份联合索引，先处理未完成游戏、掉线、迟到、重复进入及对手变化。动作1、2在代码中对应收益矩阵两种选择，不能把它们自动转换为原R073的行动编码。

代码展示理论上可重建参与者、对手、游戏实例、日历时间、轮次及行为；这只是实验程序字段和逻辑审计，实际OSF导出的数据是否完整保留这些字段尚未验证。统计独立性单位应按参与者与游戏实例的交叉依赖及日期聚类审查，不能把每次选择作为独立样本。

## 公开数据与许可阻塞

实际尝试OSF公开页面 `https://osf.io/64z8u/`，当前网页读取返回HTTP 403；尝试OSF文件API `https://api.osf.io/v2/nodes/64z8u/files/`，读取工具报告不可访问。没有取得数据文件清单、原始行为CSV/JSON字节、文件级许可或原始SHA256。公开论文CC BY 4.0许可不能直接视为OSF全部原始数据和代码的再分发许可；GitHub仓库元数据license=null，根目录没有可确认LICENSE。未复制参与者级资料。

## R073与后续资格

本实验的10轮单场游戏、跨场重新配对、长达20天的纵向设计，具有独立的真人重复博弈研究价值，但不符合R073冻结的双人100轮固定评分及独立场次条件。R073_DIRECT=NO；不得拼接不同对手的10轮游戏制造100轮序列，也不得按该数据重新调参后宣称R073外部复现。

可行后续：在无需注册付费账户的前提下取得OSF公开原始字节和明确许可，核对唯一参与者、日期、game instance、对手、行动、超时/中断，确认与已登记实验来源没有重复后，另行预冻结面向跨游戏、跨日期留出的E2评分设计。当前R073冻结直接复验BLOCKED；新增正式E2=0，历史E3=0。

本轮只使用英文一手论文与公开源码，没有购买数据、运行收费计算或处理私人资料。
