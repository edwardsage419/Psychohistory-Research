# R067：Montero 2022 长期重复囚徒困境真实原始文件门

日期 2026-10-16。本协议在本研究第一次完整下载/检查 Dryad 的 fix/rand 行记录之前冻结。研究身份：E2 来源可达性与行为表结构调查，**不拟合演化博弈策略、不重现 HMM，也不写实时个人轨迹**。

## 既有可独立核验的事实

Dryad DOI `10.5061/dryad.37pvmcvmk`，原始数据公开 2022-05-25，Dryad API 确认 dataset identifier 和 CC0 v8 目录。论文 DOI `10.1038/s41598-022-11654-2`。原作者研究 12 场实验，188 名真人：固定伙伴 92、每轮变更伙伴 96；实际支付 `R=3, T=4, S=0, P=1`，**不同于 R067 E1 教材矩阵**。源页面列 `fix.csv`, `rand.csv`, `README.txt`, `Instructions_of_the_experiment.docx`, `UserInformation.csv`。

源公共下载入口由 Dryad 页链接明确得到：
- fix.csv `https://datadryad.org/downloads/file_stream/1514373`
- rand.csv `https://datadryad.org/downloads/file_stream/1514372`
- README.txt `https://datadryad.org/downloads/file_stream/1514376`。
以上仅为当期入口，不等于版本固定的内容哈希（本轮若可取得必须记录下载字节/ SHA256，后续才能冻结数值）。

## 运行门

1. 优先固定 Dryad v8 API，GET 元数据与三份公开文件；对 file_stream GET 同时采用有限回退 API 链接，禁止认证/脚本提交/下载人像、问卷或个人说明文件；每个文件大小上限 3 MB，超时 20 秒。
2. 如果远端 403/429/503 或网络/TLS 失败，记录每个目标最后的实际 HTTP 代码及尝试的入口类别，只能 `SOURCE_DOWNLOAD_UNRESOLVED`，不能伪造哈希或宣称真实文件已读取。CI 若无法获取仍可以 `completed/success`，但科学状态必须是 BLOCKED；不能仅凭 CI 成功声称来源成功。
3. 如果可取得 fix.csv/rand.csv，逐个 SHA256、字节数、原始 CSV 列数/行数/表头安全洗净，统计每列的**总缺失率**和名称暗示身份/策略/轮次的候选字段；不输出原始参与者值。表格按 UTF-8 解码，若实源使用特殊编码，应 FAIL/OPEN 另冻协议，不能擅自改解码。
4. 如 README 可取得，仅输出总行数和代表字段说明的行号，不输出整段用户数据，不根据文件名猜测 `0/1` 是否对应 C/D。需要单独结合说明书核对行为编码、用户/伙伴标识、轮次起点与实际 payoff 后才有权运行真人策略演化模型。
5. 禁止重复使用无关的 R047 非二元提取作为 PD 数据。选择最少资源的独立源校验，在确认真实来源前不对 E1 的复制子/Logit/最佳反应公式修改以优化损失。

科学验收：`FIX_RAND_SOURCE_SCHEMA_PASS` 要求两真实数据文件均可核验及解析；`PARTIAL_SOURCE_OPEN` 要求有任一来源缺失；`SOURCE_DOWNLOAD_UNRESOLVED` 说明下载受阻；`HUMAN_BINARY_PD_DATASET_MODEL_IDENTIFICATION=OPEN` 始终保留，直到新的模型协议有真拟合和验证。

`R067_DRYAD_SOURCE_PROTOCOL=FROZEN`
`R067_REAL_PD_FIT=NOT_AUTHORIZED`
`PESEN_v0.1=FROZEN`
