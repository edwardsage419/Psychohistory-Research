# R066 E2：Larson–Lewis V1.0 意见指标、身份、关系网络可连接性审计

日期：2026-10-16。**基于已见的 2,125 × 66 数据结构，尚未观察完整列名与变量字典前确定的方法**，属于继续深入的源语义审查，不构成模型拟合或独立预注册结果。

## 固定身份

作者数据集 DOI `10.7910/DVN/RAHSVM`，Harvard Dataverse `V1.0` 公开 CC0，发布 `2026-07-29T00:35:44Z`。本轮必须先校验每份来源 SHA256：
- 数据 tab：`10b3e31a6d160e003ff9edf96fc1f6e1a8549ea547b8b8b08aadab1f52b40cae`；
- 作者 R：`2e7b7b22887c69c057a6f2fa1a1ff393566826fdb19e6aad6360393ea9f86ff2`；
- DOCX 代码本：`48741e3447d27fbf57bb54c995ff68c45ade21592c89e2454e71ab840fc8d161`。
沿用三个 Dataverse 公共文件 ID `14101729/14101728/14101730`，源码及原始问卷行只保存在 CI 临时目录，不在 GitHub 输出原始访谈/受试者名单/网络边。

## 字段映射程序设计

1. 用 CSV 严格解析完全源表，按事先确认的 `2125` 行、`66` 列检验；记录全部经过字符集白名单的列名（变量名而非受试者数据），每列的总非缺失计数、固定缺失 token 集合 `{"","NA","NaN","\\N","."}` 下的缺失数；此约定仅用于结构审计，不断言学科原始编码就等于该集合。
2. 将代码本 DOCX `word/document.xml` 解析成段落（不复制全文）。按字段名的**字面严格边界**在代码本段落文本中查找，输出该列名出现于几个段落、相关指示标签 `baseline/endline/attitude/network/neighbor/treatment/village` 是否出现，不输出被访者答案或原问卷整段。
3. 对作者 R 脚本做静态 token 检查：逐列 `name` 标识符出现次数、确切的网络构造函数名出现次数（`graph_from_data_frame`, `graph_from_edgelist`, `graph_from_adjacency_matrix`, `as_adjacency_matrix`, `graph_from_incidence_matrix` 等）。只记录安全汇总；如未匹配某函数不等于不存在其它实现。
4. 记录全部 66 列名用于作者同一固定数据集的*变量字典*；如果出现个人姓名、邮箱/路径等非安全列名则删除并用 `[redacted]` 代替。无任何逐人数据记录或相邻身份标识离开 runner。
5. 结果属于初步机器可读语义索引；不根据字段名直接宣布存在匹配的个体态度量表/社交边。**研究验收解释需要独立核查作者代码如何将表列与 igraph、个体基线末次及实验处理连接。** 特别注意同一张长/宽表是否足以重建完整关系邻接，以及村庄内节点 ID 缺失/网络反向提名的影响。
6. 若任何 SHA/行列结构、UTF-8 或 DOCX 包检查失败则 `FAIL_CLOSED`。正例只可记 `VARIABLE_INDEX_COMPUTED`，`MODEL_IDENTIFICATION_READY` 必须 OPEN，下一阶段需另有协议才能评分 DeGroot/FJ/HK。

预先设计的逻辑测试应覆盖源 SHA 拒绝、字段名洗净、代码本边界匹配、R 标识符频数、缺失值计数、字段匹配负例与返回值不泄漏个体行。

`R066_SEMANTIC_MAPPING_PROTOCOL_FROZEN=YES`
`R066_REAL_FIT=NOT_AUTHORIZED`
`PESEN_v0.1=FROZEN`
