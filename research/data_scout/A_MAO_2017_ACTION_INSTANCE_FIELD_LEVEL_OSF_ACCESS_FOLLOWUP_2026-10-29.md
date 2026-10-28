# A轨：Mao等2017长期真人重复博弈的源代码字段与原始数据可取得性复核

日期：2026-10-29。对既有候选 [A_MAO_DWORKIN_SURI_WATTS_2017_20DAY_PD_OSF_SOURCE_GATE_2026-10-29.md](A_MAO_DWORKIN_SURI_WATTS_2017_20DAY_PD_OSF_SOURCE_GATE_2026-10-29.md) 追加字段级复核，避免将同一研究登记为新的独立数据集。

## 英文一手来源

1. Mao, Dworkin, Suri, Watts (2017), Nature Communications 8:13800, DOI 10.1038/ncomms13800，https://www.nature.com/articles/ncomms13800 。论文报告94名真人参与者，20个工作日，每日20场，每场10轮，总设计上限400场。
2. 作者原实验程序 https://github.com/TurkServer/long-run-cooperation ，只读检查 `server/server.js`、`library.py` 与 `README.md`。
3. 论文指向OSF数据入口 https://osf.io/64z8u/ 。本轮实际尝试访问OSF项目页面，返回HTTP 403；尝试公开OSF API文件集合亦未能访问。原始文件名、大小、字段、文件级许可和SHA256均未取得。

## 新增字段级代码证据

`server/server.js` 中 `chooseActionInternal(userId,action,round)` 调用 `Actions.upsert({userId,roundIndex:round},{$setOnInsert:{timestamp:new Date(),action}})`，显示采集逻辑至少包含参与者会话键、轮次索引、动作和时间戳。服务器按当前实验实例执行行动写入；这是一份软件字段结构证据，尚未证明OSF归档原始数据实际保留全部字段。

`library.py` 的 `get_rounds(instanceId)` 从 `db.actions.find({_groupId:instanceId})` 读取动作，按 `roundIndex` 分组；`get_instances` 通过batch、counter和gamegroup索引实验实例；`gen_worker_games_dict` 使用参与者worker键汇总跨场次实例。说明作者原数据库逻辑能够区分场次、轮次和个体关联。其后 `round_fracs` 只输出组内合作比例，属于汇总计算，会丢失个体动作顺序。实际OSF归档是否保留逐人动作仍为 `RAW_UNREAD`。

## R073资格与科学边界

论文与源代码共同支持真人实验身份和每场10轮、跨场重新配对结构。R073冻结评分要求特定双人100轮场次及对应留出规则，因此此候选的直接复验资格仍为 `NO`；若未来获得原始动作，可用于**独立的新E2研究协议**，不得更改R073冻结模型和评分规则后冒称原协议复现。

论文正文采用CC BY 4.0，不据此推断OSF数据文件的许可；GitHub根目录本轮未找到LICENSE文件，代码复用权限也不能由仓库公开性推定。未读取非公开个人信息，未注册账号，未购买数据。

状态：`PAPER_HUMAN_DESIGN_VERIFIED; CODE_FIELD_SCHEMA_VERIFIED; OSF_RAW_403_BLOCKED; FILE_LICENSE_UNKNOWN; R073_DIRECT_NO`。下一步若OSF恢复访问，先核验文件级许可、匿名ID、场次、轮次、行动、缺失与对手身份，再考虑E2独立预测。新增正式真人E2预测0项。
