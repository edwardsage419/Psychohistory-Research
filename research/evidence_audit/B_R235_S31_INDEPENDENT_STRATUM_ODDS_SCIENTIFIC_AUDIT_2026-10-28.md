# B轨：R235 S31独立观察联合重算与负对照审计

日期：2026年10月28日。项目内部不同算法的程序性独立复核，非外部团队独立复现。

## 输入身份与事前门槛
原R235九世界冻结结果 research/R235/R235_EXACT_RESULTS.json，blob 068f85844f9c2fd2255e13d516f2fae62193f152。S31事前冻结协议commit c0c353ba1cd87674ad7d791370ac78df66311ccd。R主线45条件机器收据blob bf8e725116681294b11545941aca87bba33d8db2。B程序blob 33beefee35ed36b48b3791e5308d7ee2ed095f2b。

B程序 research/evidence_audit/b_r235_s31_independent_stratum_odds_20261028.js 从原R235的16格可见G,Y1,Y2,Y3联合概率直接开始。没有调用R主线的432条人工来源枚举，也不读取隐藏潜在能力计算观察统计。按同一冻结的w(G,Y2)对原可见联合重新加权与归一。

## 独立数学路线
R路线按完整432条人工来源逐条加权、构造MH的ΣAD/N与ΣBC/N。

B路线先由原冻结16格观察联合计算选择后分层四格，再以每层OR_s=(A_sD_s)/(B_sC_s)及权重h_s=(B_sC_s)/N_s计算Σh_s OR_s / Σh_s。对每条件独立比较保留总概率、16格条件联合、两组质量、两组焦点率、三层条件差、MH及原真DIF不变性。

九世界乘五规则共45条件，实际比较1261项，失败0。错误注入将一条件MH强制设为999，B程序实际检出不一致。B轨机器收据 research/evidence_audit/B_R235_S31_1261_CHECK_AUDIT_RECEIPT_2026-10-28.json。

## 审计结论与缺口
该审计支持S31人工概率计算的内部可复核性。BASE_NO_DIF在选择后出现非1 MH、NONUNIFORM_FOCAL_DISCRIMINATION真实能力差不变、BASE与GLOBAL_REANCHOR_ALIAS可见联合相同的结果均通过内部复算。

本次没有真实人类样本、独立场次、训练测试分离、预测基线、概率校准、现实数据重采样或置信区间；上述项目对人工总体精确枚举不适用，未来E2验收须另行冻结实验方案。E1人工机制检查不得提升为E2真人预测或E3历史证据。

V8 JavaScript环境已执行；Node.js CLI及GitHub Actions尚未执行，CI状态NOT_RUN。未产生新的计费计算资源使用。原R235正式验收状态、R073和PESEN v0.1保持不变。
