# A轨：Kuper-Smith/Korn真人重复博弈的反馈时间与数据许可范围核验

日期：2026-10-26。状态：FEEDBACK_TIMING_SOURCE_VERIFIED / DYAD_IDENTITY_OPEN / DATA_LICENSE_OPEN / R073_TRANSFER_NOT_APPROVED。

固定英文原作者仓库 `dnhi-lab/losses_gains_2x2`，提交 `345348cdc0018e8e030b05fb47dc845fd3e0d29a`。本轮新增实读以下原作者实验采集源码：

* `materials/data_collection_iterated/playTheGame.m`，Git blob `c985af146613aef8bfc9d0563fe0f1f5554e1376`。
* `materials/data_collection_iterated/dispOutcome.m`，Git blob `c68ecd04f4cfd2c4364a44b70f40fb590943a646`。
* `materials/data_collection_iterated/defData.m`，Git blob `ffa4a570d977c9f75faaf95c3caa399da9eb05e3`。
* `materials/data_collection_iterated/defStudy.m`，Git blob `1bc7f0ab4b3c83136db277475aa85c7840b403a8`。
* `LICENSE`，Git blob `6bf40c69fcd7c7b046e4ff932d1786f274a0f812`。

## 新增实际核验

在采集程序 `playTheGame` 中，先显示收益矩阵，再记录参与者自己的当轮响应；多人模式 `multi_num==1` 随后交换双方响应并计算结果；`dispOutcome` 显示当轮结果并暂停1秒，之后进入下一轮。因此，在这套采集代码所描述的多人条件下，上一试次的双方行为及结果具有决策前可见的机制基础。未来预测当前轮行动时，必须严格排除当前轮对手行动与结果。

程序另有 `multi_num==0` 的单人随机对手分支，调用 `randomChoice`。只有核实实际实验记录的多人运行方式、参与者对手身份与镜像配对后，才能将每条记录归入真人对真人E2。不能把源码支持多人运行等同于所有数据行均来自真实双人交互。

`defStudy` 的多人分支固定每个收益矩阵3次，含多个收益矩阵；历史滞后字段由另一个格式化脚本逐参与者读取前一试次。由于跨对手与跨收益矩阵条件切换，上一试次对手行动不能自动视作当前对手上一轮行动，上一试次反馈虽在时间上可能可用，仍需核验实验参与者实际可见内容、有效试次与镜像配对。

许可核验：根目录MIT文本明确授予Software及相关documentation的权限，未单独说明真人CSV的数据许可和隐私再分发范围。保持数据专属许可待核，不把MIT代码许可扩展解释为真人行为记录的无条件再分发授权。此前已核原始36000行、清洗33702行，本轮没有重新取得全量字节或重跑筛选；沿用此前归档的行数，禁止记为本轮新复算。

## 后续复现准备门槛

先独立确认实验2与3多人运行的记录证据及双方镜像事件、排除名单与无效响应处理，再逐试次建立决策时点可见信息表，最后判断R073冻结的12场次、FP/SP和评分目标是否存在事前可证明的兼容映射。任何不兼容应记录为阻塞，不得通过事后改动R073模型或评分来获得可比性。当前R073独立E2预测0项，外部独立复现0项，新增费用0。
