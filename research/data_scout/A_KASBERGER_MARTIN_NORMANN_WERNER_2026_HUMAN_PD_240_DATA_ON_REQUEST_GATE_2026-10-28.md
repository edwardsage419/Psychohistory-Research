# A轨：Kasberger等2026真人重复囚徒困境来源与原始数据访问门槛

日期：2026-10-28。状态：SOURCE_DESIGN_VERIFIED_RAW_BEHAVIOR_BLOCKED。禁止任何注册付费账户或索取非公开参与者数据。

## 一手来源
Kasberger, Bernhard; Martin, Simon; Normann, Hans-Theo; Werner, Tobias (2026), "Algorithmic cooperation: A comparison with human play in the infinitely repeated prisoner's dilemma", *Games and Economic Behavior*, 159:113–130, DOI https://doi.org/10.1016/j.geb.2026.06.001 。出版社公开正文含实验设计、匹配和数据可用性说明。原研究预注册入口 https://osf.io/zcv6x/ （本轮仅由论文链接确认，未取得原始注册材料）。

## 已验证的设计层信息
论文报告新开展的人类实验240人，时间2022年12月至2023年5月，Düsseldorf和Potsdam两处实验室。新增真人实验涉及四种(δ,R)处理组合：δ∈{0.9,0.95}、R∈{40,48}。参与者在同一supergame内固定配对，不同supergame间在10人匹配组内重新随机配对；实验场次20或30人，每人计划最多15个supergame，受两小时上限影响。每个supergame的轮数依结束概率而变，不是固定100轮。论文另外引用Dal Bó和Fréchette、Romero和Rosokha等既有真人实验构成跨处理比较。**240人属于本文新增实验，不能与引用的历史实验样本直接相加或视为完全独立来源。**

## 文件及字段门槛
论文明确Data availability: "Data will be made available on request." 本轮没有可直接下载的逐轮真人原始数据文件。尚未核验参与者ID、场次ID、supergame ID、对手ID、轮次、两人当轮行动、时间戳、退出/中止、缺失、数据文件SHA及文件级许可。独立实验场次与具体人数无法从原始数据逐行证实。正文可核验匹配设计，但不能替代原始数据结构审计。论文的开放获取许可不自动赋予尚未公开的数据再分发许可。未联系作者索取非公开记录。

## R073资格
新实验与R073的Montero-Porras 2022实验论文及实验室来源不同，存在值得继续侦察的独立真人来源潜力。然而R073冻结的固定长度100轮双人协议与此研究的随机长度supergame不匹配；缺少可直接访问的逐轮数据及身份/配对信息。R073_DIRECT_REPLAY_ELIGIBILITY=NO。不得截取、拼接不同supergame构造伪100轮；不得事后调整R073参数或评分规则。

## 可执行后续
只在合法无需账户的公开数据出现时继续：先核实许可与SHA，再逐行检验唯一键(session,supergame,player,period)、同场双人行动、匹配稳定性、时序、缺失及引用旧数据的来源去重。其余情况下保持BLOCKED，优先继续R系列主线。

本轮新增正式E2预测0，历史E3预测0；未取得参与者级数据，未产生额外费用。
