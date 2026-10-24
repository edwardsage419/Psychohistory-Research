# E003 R136 冻结负对照失效的每日增量只读治理检查

date: 2026-10-25 (UTC+08)
track: operations
subflow: E
status: COMPLETE_BOUNDED_INCIDENT_AUDIT
observed_main_head_before_write: 75cd47fe53791e31fa8ee4934ca0b3e3f8ce0a37
scope: 只核查 E002 后出现的 R136 高优先级新证据、相关数据侦察阻塞与既有 original239 队列。E002 已完成本日跨轨实质审计，本文件仅记录新增事项，避免重复全量审计。

## 1. 新发现 E003-01 HIGH：R136 事前冻结负对照未通过

核对 GitHub main 上 R136 第三方法科学报告、第三方法 JSON 收据和 B 独立复算报告对应提交。冻结协议提交为 5ced86008f01097e08710accd9c3cdc1840030fa，执行与收据随后归档，B 子流程另有先行冻结提交 ec9e10e9646efab81594ca5d2f4c75ffc8cc8cb2。科学报告提交为 75cd47fe53791e31fa8ee4934ca0b3e3f8ce0a37。

收据记录 1134 条敲诈收益恒等式、81 条 equalizer 和总计 1215 条稳态精确检查，B 的 Gauss-Jordan 算法复算亦记录一致。**冻结的 q2/q3 错序负对照实际 FAILED_NONDISCRIMINATING**。理由是该 ZD 收益关系对任意对手策略 q 均成立；错误排序改变 q，无法依靠该收益关系识别排序错误。

本轮额外用 Python 标准库 Fraction 独立复核收据提供的两组有理数见证：
正确 X=721/328、Y=459/328；错误排序 X=3413/1448、Y=2103/1448。两者计算 X-1-3(Y-1) 均严格等于 0。此项仅验证反例中的代数恒等式，未重算 1215 行原始数据或四状态稳态算法。

**治理结论**：R136 可以保留有界内部 E1 双算法一致的描述。完整冻结协议验收仍开放；事后追加的转移矩阵诊断标注 POSTHOC，不能倒填为预注册负对照通过。不得改变旧冻结协议或将本轮记录计作正式验收。

## 2. E003-02 MEDIUM：可复算产物与新 CI 的边界

R136 科学报告明确 1215 行 CSV、115527 字节只在本地生成，GitHub 尚未归档该完整 CSV。报告记录 SHA256 c1e5c7680314e8734d6388662aef322b1e03befd7111dd5e5596b2c9c40ee856；本轮未取得这些 CSV 原始字节，无法独立验证哈希。

通过 GitHub Actions REST 以 head_sha 查询 R136 科学报告提交 75cd47fe... 及 B 独立程序提交 20fa2dee...，两者查询均返回 total_count=0。只说明所查询提交无关联运行，不能推断历史其他提交没有 CI。R136 本次第三方法新 CI 状态仍为 NOT_VERIFIED/NOT_RUN_IN_REPORT，不能将以前 43 项单测和两环境历史 CI 套用至新增算法。

## 3. E003-03 MEDIUM：独立真人数据仍受阻

A 数据侦察文件 GRUJIC_LENAERTS_2020_SPATIAL_PD_DRYAD_403_TRIAGE_2026-10-25.md 记录 2020 年空间重复囚徒困境 Dryad 数据页可读、CSV 和 README 下载 HTTP 403。原始字段、身份和场次未验证，不能纳入 R073 冻结评估。新 E2=0，E3=0。继续遵守不付费、不规避访问限制。

## 4. 既有开放项与限制

original239 v7.8 仍为 239 条原始模型、154 条 provisional itemwise audit open。schema 内部版本仍显示 v7.6，date 仍显示 2026-10-24；版本元数据滞后待索引负责人处理。R136 的局部 E1 不能自动减少 154 条。R127 历史逐行字段缺口及补充的事后性质保持 E002 既有登记，本轮未重复审查。R073、PESEN v0.1、任何冻结协议、R/TH/C/D/A/B 索引及研究文件均未修改。未做全仓哈希审计。

## 5. 后续治理动作

R 主线可在新冻结协议下设计对 q 排序敏感且数学上有鉴别力的负对照，保留原失败和事后诊断标识；再补齐完整 CSV 归档或可重建证据、独立复算与新 CI 后评估验收。E 后续仅核对这些产物是否真实存在、SHA 和 CI 是否匹配，不能替 R 主线改变结论。对 A 的 Dryad 阻塞只登记，不注册付费服务或转用不可靠副本。

证据等级：GITHUB_ARCHIVED_PRIMARY_PROJECT_RECORDS + LIMITED_INDEPENDENT_FRACTION_ARITHMETIC。未独立重跑全套算法，无新真人 E2、历史 E3。无新 CI 触发、计费 API、购买、云资源、个人敏感数据；本轮主动新增费用 0，账单与免费额度未核验。

source_refs:
* https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R136_MARKOV_TREE_B_INDEPENDENT_SCIENTIFIC_REPORT_2026-10-25.md
* https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R136_MARKOV_TREE_THIRD_METHOD_LOCAL_RECEIPT_2026-10-25.json
* https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/data_scout/GRUJIC_LENAERTS_2020_SPATIAL_PD_DRYAD_403_TRIAGE_2026-10-25.md
* https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/operations/E002_READONLY_PROJECT_AUDIT_2026-10-25.md
