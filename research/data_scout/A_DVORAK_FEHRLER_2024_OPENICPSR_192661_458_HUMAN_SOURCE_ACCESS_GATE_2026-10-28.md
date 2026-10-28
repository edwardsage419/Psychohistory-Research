# A轨：Dvorak与Fehrler 2024重复囚徒困境真人数据资格审查

日期：2026年10月28日。证据类型：公开原始研究元数据与论文来源审查，尚未取得逐轮真人行为文件。与R235 S31人工E1研究独立。

## 固定来源与实读证据
原论文：Dvorak, Fabian 与 Sebastian Fehrler (2024), Negotiating Cooperation under Uncertainty: Communication in Noisy, Indefinitely Repeated Interactions, American Economic Journal: Microeconomics 16(3), 232至258，DOI 10.1257/mic.20210117。
官方数据及代码存档：openICPSR project 192661, version V1, DOI 10.3886/E192661V1，2024年7月3日发布。
来源链接：https://www.openicpsr.org/openicpsr/project/192661/version/V1/view?flag=follow&pageSelected=2&pageSize=10&sortAsc=true&sortOrder=%28%3Ftitle%29
原论文链接：https://www.aeaweb.org/doi/10.1257/mic.20210117
公开工作论文：https://www.iza.org/en/publications/dp/11897/negotiating-cooperation-under-uncertainty-communication-in-noisy-indefinitely-repeated-interactions

2026年10月28日实际读取openICPSR项目页面：研究总体标为458名参与者，实验数据采集时间2016年1月18日至4月28日，地点德国Konstanz，实验室招募学生，官方元数据注明无失访。该458人是整个归档的研究总体，不能直接视为某一特定处理组的独立验证样本。

项目页面标记总计14条文件记录；当前可访问的分页仅显示README.pdf（157.3KB）、Results.R（34.1KB）、SFEM.R（12KB）和config.R（825字节）。其余文件的名称、字段、逐轮记录数和原始许可尚未取得逐项证明。

## 数据与独立性门槛
研究为真人反复囚徒困境，含完美、公共噪声、私人噪声监测及沟通条件，适合研究历史行动、监测误差、承诺和合作策略的变化。论文层面的超博弈与逐轮决策单位存在；具体数据表的字段、轮次、对手ID、场次ID、训练轮排除和配对稳定性均未逐行核验。

官方项目下载链接实际访问转入ICPSR登录页面，当前无需账户的读取路径未取得文件字节。遵守不注册付费账户及不访问非公开私人数据约束，未尝试绕过访问控制。公开网页未能确认文件级再分发许可。状态：RAW_ACCESS_BLOCKED；FIELD_SCHEMA_UNKNOWN；SESSION_IDENTITY_UNVERIFIED；LICENSE_UNVERIFIED。

研究与R073原Montero 2022数据来源在论文作者、实验年份、实验题目及存档DOI上不同，可登记为来源身份不同的真人研究候选；是否完全独立及是否存在参与者重叠，仍需原始文件和研究设计证据。R073冻结协议要求100轮特定固定或轮换对手结构及原评分定义；本候选为不定期结束的超博弈及不同沟通处理，当前直接复评分资格NO。禁止跨实验重训或事后调整R073阈值。

## 可执行的后续复现准备
只有在无需付费、无需访问受限私人数据的正式公开文件入口可用时，才进一步核验字段：participant_id、session_id、supergame_id、round、own_action、partner_action、partner_id、treatment、monitoring_signal、communication_timing；这些是需求字段名称示例，未宣称原始文件存在同名字段。冻结原数据哈希、区分同一场次与真正独立场次、验证时间先后及信息可见性，再决定能否进行其他模型的独立E2预测。

本轮新增来源资格审查1项；实际真人记录读取0行，R073独立E2复评分0，外部独立复现0。未购买、未注册、未上传个人级数据。
