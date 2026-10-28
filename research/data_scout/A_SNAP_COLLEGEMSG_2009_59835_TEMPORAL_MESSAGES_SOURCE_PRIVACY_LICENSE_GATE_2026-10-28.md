# A轨 SNAP CollegeMsg 时间网络数据来源及复现门槛

日期2026-10-28。来源：Stanford SNAP官方英文页面 https://snap.stanford.edu/data/CollegeMsg.html ，引用Panzarasa, Opsahl & Carley (2009), JASIST 60(5), 911–932。页面报告1899个节点、59835条带时间戳有向消息边、20296条静态边，覆盖193天。原文件名CollegeMsg.txt.gz；字段SRC（发送者ID）、DST/TGT（接收者ID）、UNIXTS（Unix秒时间戳）。来源为加州大学欧文分校线上社交平台用户之间的消息元数据，原始消息内容不在官方字段说明中。

本轮实际读取官方网页，验证统计量、数据链接、三字段及时间单位。文件级许可证、再分发范围、研究参与者同意与去标识化保护的具体条款未从该官方页面确认，均记UNKNOWN。原始gzip文件未取得和解析，未核验59835行、时间排序、用户ID唯一性、重复事件、缺失值或实际下载SHA。当前容器对外网络DNS不可用，HEAD请求失败；不声称原文件已读取。未复制任何用户级通信记录。

适用：未来有明确权限和伦理审查后，可用于人际通信事件间隔、时间网络和跨日历史预测的独立数据复算。限制：没有囚徒困境行动、合作标签、对手收益、实验场次、固定双人100轮结构；R073冻结协议直接资格NO。消息本身涉及私人通信，需先确认许可、隐私和合理用途，避免重新识别与公开逐人时间轨迹。状态METADATA_VERIFIED_RAW_UNREAD_LICENSE_UNKNOWN_PRIVACY_GATE。E2正式预测0，E3正式预测0。

官方英文来源 https://snap.stanford.edu/data/CollegeMsg.html 。本次未使用中文语言网站。
