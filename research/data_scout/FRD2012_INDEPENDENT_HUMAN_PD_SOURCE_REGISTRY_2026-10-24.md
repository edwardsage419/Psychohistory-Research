# A 数据侦察：FRD2012 真人重复囚徒困境，2026-10-24

状态：**SOURCE_AND_METADATA_VERIFIED; RAW_BINARY_NOT_DECODED; R073_EXTERNAL_REPLICATION_BLOCKED**。本条记录属于数据侦察与复现准备，尚未获得可用于冻结 R073 外部验证的逐行原始记录。

## 来源、可得性与许可证

原研究：Fudenberg, Rand & Dreber (2012), *Slow to Anger and Fast to Forgive*, American Economic Review 102(2):720–749, DOI 10.1257/aer.102.2.720。作者实验重复囚徒困境，含行动实施噪声，区别于 R073 的 Montero-Porras 2022 独立研究。原作者数据公开存档 https://www.openicpsr.org/openicpsr/project/112512/version/V1/view ，DOI 10.3886/E112512V1，项目 V1，公开页面显示 LICENSE.txt 和数据文件夹；未实读压缩包内部数据。

第二公开可取得载体：CRAN `stratEst` 包中的 `data/FRD2012.rda`。本轮通过 GitHub 文件列表实际核验 https://github.com/cran/stratEst/blob/master/data/FRD2012.rda 的 Git blob SHA1 `6b196ca1624081850b41dc2084c762257d59dd8f`，大小 26923 bytes。其 `inst/COPYRIGHT.txt` Git blob `746332b6dd83b283135bfb35818991df756e2271` 明确把 FRD2012 数据标记为 **CC BY 4.0**，原版权所有者 American Economic Association 2012。包的 GPL-3 代码许可与内嵌数据 CC BY 4.0 分开记录。来源 https://github.com/cran/stratEst/blob/master/inst/COPYRIGHT.txt 。README 说明非商业使用免费，见 https://github.com/cran/stratEst/blob/master/README.md 。本轮没有复制或重新发布原始记录。

## 已核实的字段及适配风险

CRAN 文档 https://rdrr.io/cran/stratEst/man/FRD2012.html 记录 **13126 行，9 列**：`treatment` 六种处理、`id` 参与者、`game` 超博弈、`period` 超博弈内回合、`choice` 当期 C/D、`last.choice` 上期自身 C/D、`last.other` 上期对手 C/D、`bc` 收益比、`error` 行动实施噪声。以上是数据文档的字段声明，尚未完成逐行核验、缺失值核验或 R073 冻结规则的特征复算。当前载体没有直接文档化 `session` 和对手唯一身份；`game` 是超博弈编号，**不能擅自当独立实验场次**。参与者跨超博弈重复可能导致按 game 切分时的身份泄漏。行动实施噪声下 `choice` 是意图还是实现动作，需核对作者数据字典。

## 实际访问尝试与阻塞

GitHub 连接器成功读取目录条目、版权说明和包文档；尝试以 `fetch_blob` 读取上述二进制 RDA，返回 UnicodeDecodeError（非 UTF-8 二进制），故没有解码记录、没有数据哈希 SHA256 或可验证的个体数。不能声称已完成原始数据复现。

复现前置检查：获取该固定 blob 的真实字节并校验 SHA1；R 或可验证的 RDA 解码器读取列与类型；按 `id,treatment,game,period` 验证唯一性和排序；确认 `last.other` 与同超博弈上一期对手行动的语义；核对原始 session 与个体跨 game 的重复关系；识别可评估 t≥3 的超博弈及与 R073 冻结风险集的兼容性；明确不能直接使用 R073 原 12 场次、100 轮和 18424 目标的固定实验专属计数。若无法在保持 R073 预测器、平滑和评分规则冻结的条件下构造合法独立留出单位，应标记协议不兼容并停止评分，绝不事后修改 R073。

等级：数据来源公开且许可已核，**E2_NEW=0，E3_NEW=0**。下一步优先验证原始文件与可用独立实验场次，形成字段和分组契约。零新增费用，未使用私人数据、付费账户或计费 API。
