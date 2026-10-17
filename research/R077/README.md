# R077：第四独立原作者真人重复博弈 — 零目标拟合预测结构验证

**2026-10-17，正式状态 `CLOSED_BOUNDED`。** 对 [Drouvelis & Pearce（2025）](https://doi.org/10.1016/j.euroecorev.2025.105075) 的另一组真人重复囚徒困境资料，首次在R077真实评分之前冻结来源和R073固定数值参数。第四研究论文在2025年已经发表，故这**不是新招募的事前注册队列**；R077同样没有做认知因果识别。PESEN v0.1 保持冻结。

[原作者 Zenodo v1 公开资料](https://zenodo.org/records/15462528) 的 `cleandata.dta` 精确1,514,315 bytes、作者MD5 `4cce04ea68b7a0492c242b206efebe53`、本研究SHA256 `1cc9a4f68a51992808d966b118226bb5a66ee3ee6054843a132157df8eeb1985`。原文件有3,620条本人C/D，15个真正 `Session`、260个场次内本人身份和1,810个双人互动轮次；只对同一 `Session,Subject,game` 内实际具有前两个连续历史的1,040个 t≥3选择评分。全部原始双方局内数据只在CI临时内存/文件，不提交 GitHub。

来源参数唯一从R073全部12场18,424真人行为固定 `M0–M6`、`alpha=20`、理论TFT/WSLS噪声0.05，并**完全不拟合任何R077标签**。按15个原始session等权，M3双上轮对M1本人上轮 Brier差 `−0.030210760470721517`（14场改善、1场恶化），M4两轮对M3一轮 Brier差 `−0.001918699476466503`（8场改善、7场恶化）；M6固定WSLS对M0基线恶化 `+0.28792023297156216`（14场变差）。主结论限定为**过去本人/对手行动条件预测**，不是心理记忆因果、制度规律或历史预测。

**完整交付入口**
- [正式科研结题报告、七模型分数、两处理负例、A01–A06和推断限制](R077_FOURTH_REAL_HUMAN_ZERO_SHOT_E3_FINAL_SCIENTIFIC_REPORT_2026-10-17.md)
- [真实1,040个目标生成的9,835字节完整匿名评分JSON](R077_FOURTH_INDEPENDENT_HUMAN_SOURCE_ONLY_E3_RESULTS.json)，SHA256 `8d8b8413e3e55cb5d856f34b873ee20c2ba470e04190bb8577f931d25ba509a4`
- [R077 六项结题标准机读验收](R077_FINAL_ACCEPTANCE_STATUS.json)
- [最初第四来源资格门](../../protocols/R077_FOURTH_INDEPENDENT_HUMAN_DATA_SOURCE_AND_BLIND_SCORE_GATE_2026-10-17.md)；[Rev-001 初始评分前冻结协议](../../protocols/R077_ZENODO_FOURTH_AUTHOR_TRUE_HUMAN_PROSPECTIVE_MODEL_SCORE_FREEZE_2026-10-17.md)；[真模型得分出现之前提交的 Rev-002 配对历史与时间适用性修订](../../protocols/R077_PRE_FIRST_TARGET_MODEL_SCORE_SOURCE_SEMANTICS_AMENDMENT_REV002_2026-10-17.md)，commit `f79d59175098b4314c9c784394cfd5beb8083f2e`
- [真实一手文件/作者代码结构审计](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38994561545)；[初始实际数据门阻断](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38995038132)（真实模型未运行，**历史 FAIL 保留**）；[修改原因的真实结构审计](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38995148912)；[24个合成守卫+第四真人评分成功](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38995309336)；[独立字节一致 SHA 重放与 Git 永久归档](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38995401729)

初始[Phase A OSF访问失败审计](R077_PHASE_A_FOURTH_ORIGINAL_HUMAN_DATA_ACCESS_AUDIT_2026-10-17.md)仍保留当时六个端点HTTP503的事实，不能因找到 Zenodo 作者另一资料后把失败记录改写为当时来源已可用。初始 Rev-001 数据完整性门也**并未通过**：一处理130次相邻Group变化，80个人局不具备从t1完整记录，故在任何模型得分之前另交 Rev-002，完整风险集合未挑选掉会换伙伴的人。不能把 Rev-002 的通过回填为 Rev-001 PASS。

`R077=CLOSED_BOUNDED`；`FOURTH_ORIGINAL_HUMAN_E3=SOURCE_ONLY_NO_TARGET_FIT_PASS_BOUNDED`；`R077_REV001_FAIL=RETAINED`；`PESEN_v0.1=FROZEN`。
