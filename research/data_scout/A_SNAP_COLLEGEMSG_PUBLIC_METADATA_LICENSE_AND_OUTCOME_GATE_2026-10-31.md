# A轨：SNAP CollegeMsg 时间网络候选来源核验

UTC 2026-10-31。来源：Stanford SNAP 官方数据页 https://snap.stanford.edu/data/CollegeMsg.html ，并核对 https://snap.stanford.edu/temporal-motifs/data.html 。数据原始研究为 Panzarasa, Opsahl & Carley (2009), Journal of the American Society for Information Science and Technology 60(5), 911–932。

## 已直接核验的公开元数据

官方公布1899个节点、59835条有时间戳的定向消息事件、20296条静态图边、193天时间跨度。公开下载对象名为 `CollegeMsg.txt.gz`。格式为 `SRC DST UNIXTS`，源和目标均是用户节点ID，UNIXTS为Unix纪元秒数。消息方向由发送者指向接收者。数据页说明来自加州大学欧文分校在线社交网络的私人消息**发送关系**，未公开消息文本。事件数不是独立参与者数，也不能当作独立实验场次或意见变化。

## 来源与访问门槛

官方页面可公开读取，下载入口存在。本轮未实际获得或解压 `CollegeMsg.txt.gz`，未逐行验证记录数、重复事件、身份连续性、时间顺序、缺失值或文件摘要。未找到该数据集明确的文件级再分发许可；SNAP软件BSD许可证不等于CollegeMsg数据许可证。保留 `DATA_LICENSE_UNKNOWN`，禁止把原始记录复制到本仓库。公开数据仍需注意参与者可识别性，禁止身份重识别。

## 与项目目标的适配

潜在用途：有向时间互动网络的统计结构与预测基线，需先完成合法数据取得、许可、原始字段及匿名化审查。当前没有任何人的意见0/1状态或社会影响后的行为结果，因此不能对R310 S106进行真人E2验证。它也没有R073所需的百轮双人重复博弈双方行动序列，不满足冻结评分条件。R073独立数据复现新增0项。候选状态：`PUBLIC_METADATA_VERIFIED / RAW_ROWS_NOT_ACQUIRED / LICENSE_UNKNOWN / OUTCOME_ABSENT`。

本轮只使用英文原始机构页面，没有购买数据、访问非公开消息、注册账户或调用计费API。下一步仅在确认许可和公开可取得性后读取公开压缩包的元数据和最小必要字段。
