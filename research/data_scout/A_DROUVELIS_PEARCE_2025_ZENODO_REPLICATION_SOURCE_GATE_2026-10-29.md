# A轨：Drouvelis与Pearce 2025重复囚徒困境复制实验公开数据核验

日期2026年10月29日。状态PAPER_CODE_METADATA_VERIFIED，RAW_DTA_UNREAD，FILE_LICENSE_UNKNOWN。

论文Drouvelis与Pearce (2025), *Intelligence and strategy choice in indefinitely repeated prisoner's dilemma games: A replication of Proto, Rustichini & Sofianos (2022)*, European Economic Review 178, 105075，DOI `10.1016/j.euroecorev.2025.105075`。大学英文原始登记：https://research.birmingham.ac.uk/en/publications/intelligence-and-strategy-choice-in-indefinitely-repeated-prisone/

作者Zenodo v1数据归档于2025年5月19日发布，DOI `10.5281/zenodo.15462528`，https://zenodo.org/records/15462528 。官方登记 `cleandata.dta` 约1.5MB，MD5 `4cce04ea68b7a0492c242b206efebe53`；`number 1.do` 23.7KB，MD5 `0ee6ace76d2ea9a8daf7ab1f7ef026e6`；另有 `number 2.do` 和 `power.do`。官方说明完整复现还需要Proto等2022年原研究数据。

实际读取公开英文Stata脚本 https://zenodo.org/records/15462528/files/number%201.do?download=1 。原研究字段 `choice` 1合作0背叛，`partnerchoice` 当轮对手行动，`partnerchoice2` 上一轮对手行动，`period` 轮次，`no_repeated` 重复场次，`id` 和 `session` 身份及实验会话。复制研究段落载入 `cleandata.dta`，使用 `ID`、`Session`、`Group`、`Period`、`practiceperiod`、`game`、`left`、`otherleft`、`p2otherleft`，并以 `egen matchid=group(Session Group Period)` 生成匹配单元。复制研究宽表策略计算设 `global v=34`，当前代码结构无法证明存在固定双人100轮独立场次。

原始dta二进制内容未取得，未核验参与者数、完整身份配对、逐轮缺失、真实轮次数及文件MD5。Zenodo页面License栏没有可见明确许可内容，论文CC BY不能自动外推至数据文件。R073直接独立复验资格当前为NO，若未来取得数据须先核验独立性与固定评分兼容性。发表论文对Proto研究的外部复制不能计为本项目R073的外部独立复现。没有购买数据、使用私人信息或再分发原始参与者数据。新增E2预测0。

下一步：零费用核验dta字节、文件级许可、ID与配对键、每个supergame轮次及跨场次滞后泄漏风险。未取得则维持RAW_DTA_UNREAD。
