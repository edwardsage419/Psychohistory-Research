# A轨：Nay与Vorobeychik 2016数据包原始二进制文件及身份键复核

日期：2026-10-29 UTC。状态：`PACKAGE_BINARY_BLOB_LOCATED_RAW_ROWS_UNREAD_R073_DIRECT_NO`。目标键：(A,NayVorobeychik2016,JohnNay/datafsm@c2e55eab,原始数据文件存在性与独立实验身份)。

## 新增实际读取范围
本轮读取公开英文原作者GitHub仓库 `JohnNay/datafsm` 的master分支元数据、`R/data.R` 原始字段说明、`DESCRIPTION`、`README.md`、`LICENSE.md` 以及 `data/` 目录。仓库HEAD `c2e55eab12f1a24d3a5b09a9b42aeefff8bc5be4`。直接定位真实存在的 `data/NV_games.rda`，Git blob `36a961908385a7fe33ba688479b5dfc7b0a6b609`，GitHub登记大小761556字节。文件是R二进制序列化数据（.rda），先前登记中的“尚未读取原始CSV”需要细化为“可见R包二进制数据存在，但尚未解码任何行”。尝试通过当前GitHub只读文本获取该二进制文件，返回HTTP 400，接口仅接受UTF-8文本，故实际行数、缺失值、身份键与原始字节SHA256仍未验证。

`R/data.R`（blob `2a1dc849c34036026f45d1238d586376b876ec5f`）声明 `NV_games` 为168386行、51字段，引用 Nay与Vorobeychik 2016 `10.1371/journal.pone.0155656`。字段说明含 `period`、`my.decision`、九期本人及对手历史动作、九期历史收益、`risk`、`delta`、`error`、`data`、`group` 等。关键语义：`group` 被作者文档描述为“Which group (version of the game) is being played?”，属于博弈版本标签，**没有证据可作为唯一配对/独立场次/个人身份键**。`data` 是上游实验来源标签，不能自动视为独立参与者。原文档没有列出 `participant_id`、`opponent_id`、`session_id` 或唯一配对键。预计算历史列的实际组边界和时间排序必须在解码后独立检查，禁止直接据此声称逐场无泄漏。

`DESCRIPTION` 显示软件版本0.2.4，`LICENSE.md` 明确MIT许可覆盖软件及文档；原上游真人实验数据再分发权利没有单独完成核验。README指向迁移维护地址 `jonathan-g/datafsm`；本轮已检查该地址存在，GitHub API的旧路径返回Moved Permanently，因此此次文件身份以明确可读的原作者旧仓库master blob为准。

## 科研资格与后续
原论文报告最长重复互动38轮，直接不满足R073冻结的100轮条件，`R073_DIRECT_REPLAY_NO`。本轮新增E2真人预测0，E3历史预测0，外部独立复现0。软件包的168386行不能计为168386个独立实验；与已有R074等来源可能重合，未来需按来源实验去重。若以后可合法获取RDA字节，先核对blob、用免费R或开放解析器在隔离环境解码，检查真实字段、场次和历史滞后构造，再决定是否值得另行冻结其他研究问题。

来源：
1. https://github.com/JohnNay/datafsm/tree/master/data
2. https://github.com/JohnNay/datafsm/blob/master/R/data.R
3. https://github.com/JohnNay/datafsm/blob/master/DESCRIPTION
4. https://github.com/JohnNay/datafsm/blob/master/LICENSE.md
5. https://doi.org/10.1371/journal.pone.0155656

无中文语言网站、无私人数据、无注册/采购。原二进制未取得，不复制或重新分发。
