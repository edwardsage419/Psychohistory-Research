# R235 差异项目功能（10-009）：九人工IRT世界432源，MH匹配假阳性与假阴性

日期2026-10-23。真实239目录 `10-009 Differential Item Functioning`（P1）。科学状态 `CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_DIF_MH_MATCHING_LIMITS`。

[原机制冻结协议](../../protocols/R235_DIF_9_3ITEM_WORLDS_432_ORIGINAL_RESPONSE_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [完整科学报告及首次失败复验审计](R235_SCIENTIFIC_REPORT_2026-10-23.md) · [全部432人工原结构来源](R235_ALL_432_ORIGINAL_DIF_ITEM_RESPONSE_SOURCES.csv) · [可复现Python原生程序](r235_exact_differential_item_functioning.py) · [九模型人口MH及oracle结果](R235_EXACT_RESULTS.json) · [机器SHA256来源验收](R235_FINAL_MACHINE_ACCEPTANCE.json) · [正式结题收据](R235_FINAL_ACCEPTANCE_STATUS.json)。

低/高潜在能力上的真实交互焦点题差分别−2/15和+2/15，中间能力0；虽然完整人工能力条件DIF非零，两个群体的焦点总体通过率都1/2、按两个固定锚题得分合并的人口MH OR却等于1，隐藏非均匀真实DIF。另一世界焦点题在每个真实能力水平完全无DIF，但G1能力组成更强使观察总体焦点率5/9相对1/2，按有限不完美锚题匹配的MH OR却为1304723/1069477。锚题本身难度漂移也令实际不变焦点产生伪MH偏离1。全局潜在原点与项目难度同时平移是完全观测等价的单位重参数化，不能未经共用量尺锚定认定真项目偏差。

首轮[CI run39882331741](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39882331741)因为源码零常量误引用Z而两作业failure、原档归档skipped，公开留痕；修复提交[b05febb9](https://github.com/edwardsage419/Psychohistory-Research/commit/b05febb9e9fcf41915f8b72ee26db95b282bb865)只纠正同一Fraction常量引用，不更换九模型源机制/评分。最终[CI run39882474328](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39882474328)全部3作业success，Python3.11/3.12各77项单测共154通过，原完整CSV/JSON/SHA机器人永久归档[bb940f7a](https://github.com/edwardsage419/Psychohistory-Research/commit/bb940f7a327b37e55dd514892ac597014e02c632)。

仅人工E1，真人E2和真实历史E3新增0。R073与PESEN v0.1冻结。下一原目录条目 `10-010 Survey Response Bias Models`（R236），完成全部原R后才统一分类，最后模型熔炼。
