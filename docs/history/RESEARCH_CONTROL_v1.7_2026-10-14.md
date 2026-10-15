# 心理史学研究主控台 v1.7

日期：2026-10-14 | 累计 R001 至 R026 | 上游 v1.6 保存、PESEN v0.1 冻结。

## R026 更新

1. **原始数据仍未到位**。Zenodo DOI 10.5281/zenodo.16109520 的五份 CSV 已核对官网 MD5 与文件名。浏览器可以查看部分数据行，但当前本地容器无法经 DNS 下载文件。没有任何 R026 新真人效应复现。
2. **实验设计确认**。Oswald et al.（Science Advances，2025）520人随机分配六个私密 Reddit 讨论社区，三种干预各有2社区。331人真实发表评论共5,819条。作者代码还分出92名静默但随访者、97名没有评论和随访者。原文报告后测与至少一次随访共同完成者369人。需要保持基于520人的保守“零值保留”分析口径。
3. **新发现的识别风险**。作者时滞反馈脚本根据存档的历史评论分数推测未来发言，当前公开 CSV 缺少得分实际生成时点，具有潜在信息回填风险；代码的时滞样本从已发言者建立，不覆盖首次开口决定。每周感知来自当周讨论后的问卷，不能当同周行为的基线。Zenodo CSV 网页至少展示一条2024-07-08的评论，晚于报告讨论窗口2024-07-05，需全量时间戳核对。
4. **复现依赖澄清**。五份原始CSV充足用于按作者01/02脚本生成 `sample_anon.csv`、`full_data_waves.csv`、`scaled_sample.csv`。缺少派生文件是可补步骤，而非确定的外部数据失踪。
5. **独立高优先级对照发现**。Matias 2019 PNAS DOI 10.1073/pnas.1813486116，2,190个讨论随机展示规则，真实新人发言参与，源码与数据见 mitmedialab/CivilServant-Analysis 的 r_science_2016。论文作者报告对参与的影响；项目尚未重算。其较大处理单位规模对“规范提示影响公开行为”更适合，仍不直接识别私人信念或惩罚压力。

## 质量状态

- `R026_SOURCE_AUDIT = COMPLETE`
- `R026_RAW_SOURCE_MD5 = NOT_VERIFIED`
- `R026_NEW_EMPIRICAL_EFFECT_REANALYSIS = NOT_DONE`
- `R026_DESCRIPTIVE_PIPELINE = IMPLEMENTED_AND_TESTED`
- `R026_TESTS = 9 PASS`
- `PESEN_V0_1 = FROZEN`
- `ORIGINALITY = UNCONFIRMED`
- `EXTERNAL_REPOSITORY_WRITES = NONE`

## R027 优先事项

先检查 GitHub `mitmedialab/CivilServant-Analysis/papers/r_science_2016` 的源码、数据、随机化实现和许可，尝试跨本地环境可复验的原始数据入库。若取得，预先锁定“随机化讨论单元是否公示规则 → 新人真实评论数与合规率”，并审核空讨论与同时多个结果。并行支持用户本地运行本轮 R026 Zenodo 一键抓取＋校验；不得因没有取得数据而编造复现结论。

首课题仍为群体规范形成与行为扩散；保留每周约10小时资源约束和五年领域研究目标。