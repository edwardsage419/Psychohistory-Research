# MKT088：决策日志CSV导出遗漏原始推理的源码审计

日期：2026年10月28日。MARKET E1。主动新增费用0。

## 固定来源
上游公开仓库 https://github.com/SifisoScS/decision-journal ，固定提交 fc93269ab65bf3425b7b0dec1492faa491ba7ad1 （2026年1月31日），app.py Git blob ffb9141344344f15ef044ca3b57b4ffa9fdee1c5，README.md blob cd430202e4f2e5f371c7958a21802234266db423。已读取固定源码及README，未安装或运行完整Streamlit应用。

## 新增发现
README称原始决策日志不可变，反思可追加，完整日志可导出JSON或CSV。源码的决策表保留title、context、timestamp、confidence；反思另表存储，标签可编辑。应用UI没有直接更新或删除决策正文的SQL路径，但SQLite数据库没有防篡改触发器，不能推定存储层不可变。

JSON导出查询为 SELECT d.*, GROUP_CONCAT(t.name) as tags，包含context。CSV决策导出查询为 SELECT d.id, d.title, d.timestamp, d.confidence, GROUP_CONCAT(t.name) as tags，遗漏context。另一个反思CSV采用 SELECT * FROM reflections，同样没有原始决策context。若只保存两个CSV作完整备份，事前决策推理正文无法从这些CSV恢复。固定源码字段遗漏已确认，完整应用实际下载和用户影响尚未验证。

## 产品机制
输入为决策标题、事前推理、信心1至10、标签、后续反思和结果评分。状态采用SQLite decisions、reflections、tags及关联表。算法包含筛选、分组统计、时间线和导出，没有已验证的预测校准算法。目标为记录事前判断与事后学习，长期改善效果属于README主张，缺独立验证。反馈方式为追加反思和修改标签。JSON保留原文，CSV丢失原文。源码公开，可用本地Python、Streamlit和SQLite；仓库根目录没有发现LICENSE，许可范围待核验。未使用云服务，云端免费额度和持久化条件未知。

隐私提示：公开仓库根目录跟踪一个decisions.db文件。本轮只确认文件存在，未读取数据库内容，无法判断是否含真人个人资料。README同时建议本地运行和Streamlit Community Cloud部署，两种模式的访问控制与数据生命周期须分别审查。

## 实际测试
GitHub连接器固定源码16项静态断言PASS。Python标准库SQLite使用一条人工决策与一条人工反思，重演相同SQL，11项断言PASS，0失败。人工context仅出现在JSON结果中，两个CSV均缺失。脚本 research/market/mkt088_csv_export_contract_20261028.py 不依赖第三方库；直接运行完成11项合成检查，传入固定上游app.py还可核对Git blob和6项源码条件。

证据等级MARKET E1。没有真人使用数据、真实产品执行或长期决策改善验证。候选控制为跨格式导出字段一致性、事前记录来源版本、恢复测试和人工纠错。保留R系列优先、随后分类归纳与模型熔炼的顺序。下一MKT089比较Basisline或DecisionOS的原始决策收据与后续反思链接。
