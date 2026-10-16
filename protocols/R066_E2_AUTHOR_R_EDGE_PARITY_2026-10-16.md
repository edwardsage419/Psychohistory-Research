# R066 E2 原作者 R 源代码与 Python 家庭网络的逐边比较协议

日期：2026-10-16。**在本次真实 R–Python 联合执行结果出现前固定**。R066 保持 ACTIVE，不实施 DeGroot/FJ/HK 真实参数拟合。

## 原始证据

数据集 Harvard Dataverse `doi:10.7910/DVN/RAHSVM` 公开 V1.0（CC0 1.0）。固定原始数据文件 ID `14101729`（444658 字节，SHA256 `10b3e31a6d160e003ff9edf96fc1f6e1a8549ea547b8b8b08aadab1f52b40cae`）与作者 R 文件 ID `14101728`（72914 字节，SHA256 `2e7b7b22887c69c057a6f2fa1a1ff393566826fdb19e6aad6360393ea9f86ff2`）。代码本 ID `14101730`（30623 字节，SHA256 `48741e3447d27fbf57bb54c995ff68c45ade21592c89e2454e71ab840fc8d161`）。

此前失败的直接 `(village_number,ego)` 唯一节点连接状态永久保留 `FAIL_CLOSED`；此次针对作者的**家庭网络**而非把失败转换为通过。

## 完全固定的对比和通过条件

1. Python 在经过 SHA256 及原始 2,125×66 结构核验的数据上，按每村 `hhnum` 数值升序排家庭节点；成员名单取 `ego,hhh,hh1..hh11`，每条四类提名先找出源、目标成员分别所属的*所有*家庭索引、笛卡尔积扩边，然后去自环、无向去重；不得从输出反馈改掉算法以创造 PASS。
2. R 侧**从经过 SHA256 固定的作者原脚本**提取完整 `make_el <- function` 与 `convert_to_hh <- function` 定义并由真实 Rscript 执行；不抄写模型内部公式、无硬编码的第二实现。每村按 `hhnum` 升序读取同一 TSV，按四类提名生成原生个人边及家庭映射；在 R 源代码生成的原始家庭有向/重边中丢弃自环、标准化无向边、去重。
3. 比较单位是 `(村庄编号,网络类别,户序号小值,户序号大值)`。16 村与四种关系类型全覆盖，比较两个完整集合：缺任何一条或多任一条即 `EDGE_PARITY_FAIL`，绝不仅用总数相等代替逐边相等。
4. 所有受试者行、个人/家庭标识和家庭逐边集合都**只在 CI runner 临时存储**。报告/Artifact 仅记录每类 R/Python 去重边数量、只存在 R/只存在 Python 的总边数、状态及测试计数。禁止上传原始对比文件、逐村稀疏信息、用户名或边 hash。
5. 明确的界限：原始函数 `make_el` / `convert_to_hh` 的逐边等价与**作者整个 R + igraph 分析流程的相同结果**不是同一个命题。本轮若通过，称 `AUTHOR_R_CORE_EDGE_PARITY_PASS`，`FULL_AUTHOR_IGRAPH_ANALYSIS_PARITY=OPEN`。有来源丢失、函数提取不完整、R 程序依赖安装失败或运行超时，则 `UNRESOLVED`，不能等同模型失败。
6. 合成测试须确认跨村隔离、家庭多重成员匹配、无向重复边/self-loop 排除、逐边集合比较能识别总数相等的集合置换、作者源码 SHA 拒绝与源内确有两核心函数。

此工作是既有来源审计的下一级验证；不构成独立研究群体 E3，不足以直接推断网络导致态度变化。

`R066_R_CORE_EDGE_PARITY_PROTOCOL=FROZEN`
`R066_REAL_OPINION_MODEL_FIT=NOT_AUTHORIZED`
`PESEN_v0.1=FROZEN`
