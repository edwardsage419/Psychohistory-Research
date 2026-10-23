# 心理史学 R275—R277 三项连续研究正式验收：等效机制、参数可辨识性与模型错设诊断

日期2026-10-23 Asia/Taipei。原239候选研究目录12-005 Equifinality Analysis（R275，P0）→12-006 Model Identifiability（R276，P0）→12-007 Model Misspecification Checks（R277，P0）。遵循先冻结源码/评分协议、再完整原source与独立数学推导、双Python真实单元测试、GitHub Actions第三独立来源审计并自动永久归档原CSV/结果JSON/SHA256的统一验收。三项只达到**有界人工数学E1**，新增真实人类E2=0、真实历史E3=0、R073和PESEN v0.1继续冻结。

## R275 等效机制（12-005）
[先行协议](../protocols/R275_EQUIFINALITY_3_MECHANISMS_768_COMPLETE_PAIR_SOURCE_TYPES_PRESCORE_FREEZE_2026-10-23.md) · [可运行完整源码与原source](../research/R275/README.md) · [正式科研报告](../research/R275/R275_SCIENTIFIC_REPORT_2026-10-23.md) · [机器验收](../research/R275/R275_FINAL_ACCEPTANCE_STATUS.json) · [CI run39903913659](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39903913659) · [机器人永久source提交d70cb4e5](https://github.com/edwardsage419/Psychohistory-Research/commit/d70cb4e542b47d3efe10c551a863408a2c31081e)。

IID_PAIR、COPY_PAIR、FLIP_PAIR三个机制对仅观察四个A值的**所有完整联合分布**完全一致；添加B及其与A的配对关系后可获得机制识别信息。三机制各有完整256种原四pair source，合计**768个模型标识source**（包括零质量source，实际可发生的原source配置按模型计256+16+16=288），等权先验且预冻结MAP并列选择IID规则下A-only模型平均分类正确率1/3，完整pair平均正确率23/24。有限样本仍不保证绝对辨识。Python3.11、3.12各50项真测试，共**100项通过**，第三独立full CSV审计成功，共三job success。

## R276 模型可辨识性（12-006）
[先行冻结](../protocols/R276_STRUCTURAL_IDENTIFIABILITY_192_SOURCE_ATOMS_THREE_PRODUCT_PARAMS_PRESCORE_FREEZE_2026-10-23.md) · [完整研究原source与源码](../research/R276/README.md) · [正式科研报告](../research/R276/R276_SCIENTIFIC_REPORT_2026-10-23.md) · [机器验收](../research/R276/R276_FINAL_ACCEPTANCE_STATUS.json) · [CI run39904079585](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39904079585) · [机器人全部source归档e32a4a4f](https://github.com/edwardsage419/Psychohistory-Research/commit/e32a4a4fb38ee90eea6ab7670eadf54ff3bbdbad)。

三个固定人工结构参数(1/2,1/2)、(1/4,1)、(1,1/4)的乘积θ1θ2完全一样q=1/4，因此仅观察四Y∼Bernoulli(q)的任何完整联合分布不能区分；新增两个Z∼Bernoulli(θ1)后**这三个离散候选的分布层面变得可辨识**，等候选先验有限MAP平均正确率从1/3升至11/16。三机制各64个六bit原source，共**192个模型标识完整来源配置**（正质量source数144）。这只证明三个冻结离散参数点，与连续二维参数空间的全局/局部辨识性不可混淆。双Python各50真测试，共**100项通过**，第三完整原source审计和归档job success。

## R277 模型错设诊断（12-007）
[冻结协议](../protocols/R277_MISSPECIFICATION_3_MARKOV_DEPENDENCE_WORLDS_192_FULL_SOURCES_PRESCORE_FREEZE_2026-10-23.md) · [完整原source与执行程序](../research/R277/README.md) · [科研报告](../research/R277/R277_SCIENTIFIC_REPORT_2026-10-23.md) · [机读正式验收](../research/R277/R277_FINAL_ACCEPTANCE_STATUS.json) · [CI run39904180046](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39904180046) · [全部原source永久归档12b5de59](https://github.com/edwardsage419/Psychohistory-Research/commit/12b5de59e410a5044e480b192e60df7e72436a14)。

三种人工一阶对称Markov链的保持概率s=1/4、1/2、3/4，六bit原source各64种且均正质量，共**192个模型标识完整source**。三个过程在每个时点边缘P(Xt=1)=1/2完全相同，所以冻结半概率边缘预测器每行Brier=1/4不随真实机制改变。5个保持转移之和T~Binomial(5,s)，可显示不同依赖结构：在IID真机制中预定高T≥4诊断触发概率3/16；在高持续s=3/4机制中为81/128。同样，低T≤1对反持续机制触发81/128、在IID中3/16。两个方向若同时监控，IID下联合区域概率3/8，不能说仍有3/16家庭误报率。完整来源与独立组合路径及第三CSV完整PMF全部一致，双Python各50真测试共**100通过**，第三审计和归档job success。

## 三阶段有界结题与实际验收凭证
三项合计**9个人工冻结世界**、768+192+192=**1152带机制/参数/真实DGP标签原source配置**。其间包括0质量的形式占位配置，及跨不同世界共享观测空间，严禁将1152称为独立真人样本、实证复验或具有时间可外推的历史证据。全部Python双版本真实日志均核验到`Ran 50 tests ... OK`：三项目各2×50项，共**300真实单元测试运行通过**，三个GitHub CI每个3 job completed/success，合计**9成功CI job**。三项目源CSV、完整JSON结果、SHA256凭证分别经GitHub机器人实际永久commit和当前main核验。

方法学新增成果是三项对应三个不同层次：**相同边缘分布对应不同机制（R275）→ 有效观测通道决定参数结构是否可辨（R276）→ 单点预测评分无法排除联合过程错设（R277）**。这给未来原生心理历史模型和实证比较提供审计原则，不能因为数学E1反例成功就称已有现实心理历史预测准确率；目前没有更新R073跨场次/跨实验真人E2，也无E3。

原239候选目录下一项已确认 **12-008 Model Averaging and Ensembles（P2，拟R278）**。项目继续原R系列学习完成后统一归纳分类，最后模型熔炼；个人辅助决策系统仍暂缓。
