# R001 至 R064 研究档案恢复审计

编制日期：2026-10-15。公开仓库首批补档。项目 R001 至 R064 的研究记录连续，原始电子成果的可用性仍有缺口。

## 事实等级

| 类型 | 含义 |
| :--- | :--- |
| ZIP_ARCHIVED_AND_VERIFIED | 已上传整包 ZIP，来源于当前可访问工作空间，并通过完整性检查 |
| PARTIAL_LIBRARY_TEXT_SNAPSHOTS | 从当前可检索的历史文件资料库提取出原先保存的 Python 或 JSON 文本；没有拿到该轮完整 ZIP |
| HISTORICAL_RECORD_ONLY | 在研究主控台或既往研究轮次总表中可见当年研究记录；本次未找到可确认的原始完整研究包 |

## 原始整包状态

已归档 R002、R063、R064 共 3 轮完整 ZIP。R002 为 2026-10-15 的追补研究，绝不可当作 2026-10-14 已有的旧文件。R063、R064 的源码审计、数据层级与复现局限应以各自完整报告为准。

R001 至 R064 的其余轮次，尚未取得可校验的整轮原始 ZIP。既往对话曾给出 `sandbox:/mnt/data` 形式的历史下载路径，但跨会话临时文件不保证保留。本次不通过手工拼装伪造历史 ZIP 或伪造原始数据。

## 本次新增历史文件

额外找回 20 份 Python/JSON 文本源快照，分布在 13 轮；另恢复 2 份旧版研究主控台。恢复路径见下面清单。读取采用文件资料库提取的文本，对应的 Git blob SHA 是本次提交后的版本标识。由于缺少历史原始字节，这些值不可冒充旧版本的 SHA256 原件校验。

* `research/R011/recovered_library/r011_analysis.py` | Git blob `f0c88c6996bc5ea8ed9259729870528ac421ee6e`
* `research/R020/recovered_library/r020_design.py` | Git blob `13a3bc59b77db0724cea5cc346fac18e52b4dbeb`
* `research/R023/recovered_library/r023_analysis.py` | Git blob `2b9acfd205dcd346b597fd69f04413508f269440`
* `research/R024/recovered_library/r024_analysis.py` | Git blob `059d38832ebefc1d285a36f02009535b3adad491`
* `research/R025/recovered_library/r025_analysis.py` | Git blob `b5cd6242b590ea437bc6ca43afe6b50da1e73624`
* `research/R025/recovered_library/R025_RESULTS.json` | Git blob `5a6034ab34641e1286e1e47bd16a1ebf3ee4ef43`
* `research/R053/recovered_library/R053_RESULTS.json` | Git blob `05027b373266ac9d86286024709cb0f35ff04616`
* `research/R054/recovered_library/r054_history_bench.py` | Git blob `b6eb70e74bf66eb08493c3a2f83667b481379f98`
* `research/R054/recovered_library/R054_RESULTS.json` | Git blob `bc908ed34b713bea705521879b1301997808917d`
* `research/R055/recovered_library/R055_RESULTS.json` | Git blob `e15f68b58939e565cc7168010b91ab29406825b5`
* `research/R058/recovered_library/r058_replay.py` | Git blob `494f1a5ff9db0c64ca7da8947b03ffd525fe3dff`
* `research/R058/recovered_library/R058_RESULTS.json` | Git blob `fc93a22e35c48cc7e4f6d683400773fc68facfbc`
* `research/R059/recovered_library/r059_online.py` | Git blob `d38a6aaaae0e6284eb4c421f0a5ada419399c6eb`
* `research/R059/recovered_library/R059_RESULTS.json` | Git blob `6b91cfe052b35dedf8abe019bba11f9245f7e196`
* `research/R060/recovered_library/r060_equal_online.py` | Git blob `822e572765b6ac9b1e55e4253dd3ea722deb084f`
* `research/R060/recovered_library/R060_RESULTS.json` | Git blob `c6e6a08fe8380ed2c14ba6ad24dc9684abb16fde`
* `research/R061/recovered_library/r061_replay.py` | Git blob `7e6642a026c56bf1643ad89375ec022370183477`
* `research/R061/recovered_library/R061_RESULTS.json` | Git blob `0696b9233a29e83e525084fddf3fa60885b9ea48`
* `research/R062/recovered_library/r062_adaptive.py` | Git blob `a6987b3f01c61ddd3435065280d6301dc104831b`
* `research/R062/recovered_library/R062_RESULTS.json` | Git blob `52198534fac924490c9c7f471a4110d9004be4d1`
* `docs/history/RESEARCH_CONTROL_v1.4_2026-10-14.md` | Git blob `fd73e0aee484c36412c5d9050c488fa2689ab9aa`
* `docs/history/RESEARCH_CONTROL_v1.7_2026-10-14.md` | Git blob `c765d7edfa20fb7095006f73f4bfcac6af2787cb`

## 历史研究进度来源

`docs/RESEARCH_CONTROL_v3_2026-10-14.md` 包含早期多轮研究及证据边界；`docs/history/` 保留早期主控台文本。R040 至 R062 的单轮完整成果仍需要恢复。早期主控台的“完成”仅表示曾执行或报告完成该轮工作，不能解释为代码、原始数据、计算结果均已在 GitHub 持久保存。

## 研究边界

PESEN v0.1 维持冻结。个人参与者微观数据、原始第三方实验资料、尚未核准再分发的材料均不随这次公开仓库归档。保留来源信息和现有脚本，但缺源数据依赖的脚本不能直接声称本地端到端复现。

## 进一步恢复要求

逐轮核查旧会话原始附件、个人设备上保存的 ZIP 以及合法可重新获取的第三方来源。收到完整字节后逐轮计算 SHA256、检查许可证、执行回归测试、记录实际验证级别，再提交。无论未来能否找齐，`manifests/RECOVERY_STATUS_R001_R064.csv` 中的未恢复状态应保持可审计。
