# R221 因果中介分析（09-012）：六人工结构因果模型与不可识别中介来源E1结题

日期2026-10-22。原239目录 **09-012 Causal Mediation Analysis（P2）**。限定科学结题 **CLOSED_BOUNDED_E1_ARTIFICIAL_SIX_MEDIATION_SCM**，没有真人或真实历史因果识别。

[冻结协议](../../protocols/R221_CAUSAL_MEDIATION_6_SCM_48_ORIGINAL_SOURCES_PRESCORE_FREEZE_2026-10-22.md) · [完整科学报告](R221_SCIENTIFIC_REPORT_2026-10-22.md) · [六人工世界Fraction结果JSON](R221_EXACT_RESULTS.json) · [48条完整原外生源/随机处理/观测与自然反事实CSV](R221_ALL_48_ORIGINAL_MEDIATION_SCM_SOURCES.csv) · [源SHA机器验收](R221_FINAL_MACHINE_ACCEPTANCE.json) · [正式机器结题及CI元数据差异](R221_FINAL_ACCEPTANCE_STATUS.json) · [39项标准库单测与全原源重演](r221_exact_causal_mediation.py)。

四潜在类型U各1/4，T独立Bern(1/2)真实人工随机分配，六个固定SCM×八可能原来源，完整48条真可能观测联合来源。真自然总效应TE按两套恒等分解NDE0+NIE1及NIE0+NDE1计算；实际观察gformula只读T/M/Y，不看真机制潜在U。强反例：PURE_INDIRECT和LATENT_COMMON_CAUSE_NO_MEDIATION具有**完全相同完整P(T,M,Y)**，随机T与全部T×M格支持均满足，但前者真(TE,NDE0,NIE1)=(1/4,0,1/4)，后者=(1/4,1/4,0)；只由实际数据构造的gformula对两者都给(0,1/4)，后一机制的自然中介解释彻底误判。存在T×M交互时总效应3/4也可分解为NDE0=1/2+NIE1=1/4或NIE0=0+NDE1=3/4，直接/间接份额依反事实基准而变。

[GitHub Actions 39784385018](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39784385018) **run总状态success**，Python3.11和3.12真实job日志分别`Ran 39 tests`和`OK`，共78测试执行成功，第三完全原数据生成及永久入库job结论success，[机器人原结果提交70c08466](https://github.com/edwardsage419/Psychohistory-Research/commit/70c0846604fe1d00e0dc933da675f753d7b9fbd5)。**审计例外：GitHub jobs API仍将Python3.11作业显示queued/null，尽管其实际日志正常且run总conclusion=success**；这一来源不一致已诚实写入[机读收据](R221_FINAL_ACCEPTANCE_STATUS.json)，不得笼统宣称三作业API字段均success。科研结果仅由完整程序、源资料及已验证数学等式支持，不把job显示差异当作额外科学证明。

E1人工有限，新增真人E2=0、历史E3=0。R073/PESEN v0.1冻结。下一原239目录 **09-013 Causal Inference with Interference（P1）**，研究编号R222，历史R17关联仅代表文献定位，不表示该条目已完成新模型复算。持续先完成全部原R、再归纳分类、最后熔炼。
