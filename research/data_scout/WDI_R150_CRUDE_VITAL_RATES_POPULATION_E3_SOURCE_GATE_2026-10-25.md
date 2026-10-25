# A 数据侦察：World Development Indicators 历史出生率、死亡率、人口总量的 R150 适配门

日期：2026-10-25。侦察前仓库 HEAD：`29085acad7c528da801136a465cb34e8ce9eeb4d`。状态：`SOURCE_SCHEMA_LICENSE_VERIFIED / ROW_LEVEL_EXTRACTION_BLOCKED`。没有任何新增 E3 评分。

## 英文官方来源与许可证

1. World Bank WDI 官方数据目录 https://datacatalog.worldbank.org/search/dataset/0037712/world-development-indicators ，国家级、年度、时间范围1960至2025（不同指标实际覆盖不同）。公开数据许可 CC BY 4.0，来源目录标注2026-10-09最近更新。
2. 人口总量 SP.POP.TOTL https://data.worldbank.org/indicator/SP.POP.TOTL ，原始来源涉及 UN World Population Prospects 与各国统计机构，人口总量单位为人数，展示页面有时以千人为单位，提取时必须区分。
3. 粗出生率 SP.DYN.CBRT.IN https://data.worldbank.org/indicator/SP.DYN.CBRT.IN ，单位每千人口年度出生数，页面时间范围1960至2024。
4. 粗死亡率 SP.DYN.CDRT.IN https://data.worldbank.org/indicator/SP.DYN.CDRT.IN ，单位每千人口年度死亡数，页面时间范围1960至2024。
5. API 官方文档 https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation 确认 v2 API 无需密钥和认证；许可证附加条件见 https://data.worldbank.org/summary-terms-of-use 。

以上来源均为英文官方网站，2026-10-25已读取来源目录、指标网页、API说明和许可说明。没有访问中文网站。

## 复现准备字段映射

| 项目 | 官方字段或候选映射 | 科研约束 |
| --- | --- | --- |
| 国家身份 | country ISO3 / country ID | 国家和地区汇总须排除 World、income group 等聚合行 |
| 时间单位 | date，年度 | 不等同 R150 的固定12年人工轨迹参数 |
| 人口存量 | SP.POP.TOTL | 要核对统计口径、年中人口与人口修订 |
| 出生率 | SP.DYN.CBRT.IN | API 原始值除以1000才能转为 R150 的年人头比例 |
| 死亡率 | SP.DYN.CDRT.IN | API 原始值除以1000才能转为年人头比例 |
| 迁移与残差 | 尚未选定独立来源 | 仅靠 P、出生率、死亡率无法严格封闭人口会计 |
| 来源修订 | API lastupdated / indicator metadata | 下载时固定日期、原始响应 SHA256 与许可 |

这些是公开历史汇总数据，不含个人身份、逐回合真人行动或独立实验场次。其适配对象是人口历史 E3 候选，不能作为 R073 真人重复博弈 E2 样本。

## 实际获取状态与缺口

本轮通过网页工具尝试直接访问 api.worldbank.org 的 JSON 指标端点，返回访问不可达，未取得任何可复算的逐年原始 API 行；不能填写具体国家样本量、缺失率或声称复现成功。官网展示的最新数值不能替代逐年原始行。

已核实 WDI 官网指标名称、单位、时间粒度、来源、许可和 API 不需认证。原始 CSV 或 JSON 的逐行访问、版本冻结、年份重叠、缺失值和国家汇总去重仍待完成。

**特别阻塞：** 粗率与人口存量可能来自不同底层统计源，迁移和人口修订可产生残差。不得把差额全部解释为心理机制或因果冲击。现实国家数据不能直接按 R150 的人为二值跳变率拟合后宣称事前预测成功。

## 下一步无新增费用方案

取得三套官方指标的逐年 JSON/CSV 后，先归档原始响应 SHA256、指标 metadata、国家/年份交集、缺失率和许可，再独立冻结 E3 评价协议，明确训练/留出年份、迁移残差与比较基线，最后才运行真实历史评分。任何评分前继续保持 R150 原 E1 冻结、R073/PESEN v0.1 冻结。费用状态：官网与无密钥 API 免费，未购买或调用收费 API；实际账单未核验。