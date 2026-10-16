# R065 Phase K：原作者七模型原生目标函数执行关口

日期：2026-10-16。协议身份：R065 第十阶段之后的 **技术复现预检**。本协议在新增七模型原生执行得分产生之前独立提交。该研究不属于预注册外部检验，不改变 R065 完整拟合关口，也不解除 PESEN v0.1 冻结。

## 固定资料与样本

1. 作者仓库 `arielevy8/obs-learning-fishing`，提交 `fd5f435b5368b69916e7acc6a9991aa5f46b3ddb`。
2. 作者原始 `model_fitting/objectives.py` Git blob `5e98133fa274ef2a112b24f6fdcd802d4f9d3eec`，`model_fitting/fit_utils.py` Git blob `6046f083a1181b10a7d991c8c9fd2e53c1f2b487`。原始文件完整字节使用 Git blob SHA1 检查；未经核对不得加载。
3. `research/R065/R065_PHASE_J_SCREENED_24_RESULTS.json` 规定的同一 24 名合格参与者、相同选择顺序、24 个个人原始 CSV Git blob、作者处理后数据 Git blob。仅 `phase=experimental` 的每人 136 条连续试次，汇总 `play` 共 1327 次。
4. 不在本仓库分发原作者个人逐行数据；仅公开原始来源哈希和聚合成绩。运行环境固定 Python 3.11、numpy 1.26.4、pandas 2.2.3、scipy 1.14.1。

## 主测试

执行原作者未改动的 `get_model_specs(1..7)` 和七个 `model_*_objective`，将每个模型参数的**无约束参数向量全部设为 0**，使用作者原始 `transform=True`，仅检验源代码与数据是否能运行，检查目标函数为有限非负 NLL。所有模型使用同一批 24 份原始记录及同一实验阶段筛选。报告仅给出各模型所选固定参数下的总 NLL 以供技术审计，**禁止按此数值做模型优劣排名**，因为其参数位置和模型自由度不可直接比较。

## 数学语义交叉核验

对 Model 3 另外使用 Phase J 已知的作者时钟全样本最优 `beta=0.4991210117528604`，执行原作者 `model_3_objective([beta], data, transform=False)`。聚合 native NLL 除以 1327 须与 Phase J `models.author.in_sample_mean_nll=0.6765811147513738` 在绝对误差 `1e-8` 以内一致。还对 `beta=5` 交叉核验既有固定参数总损失。每个测试输入须在模型执行前完成来源字节、唯一身份、连续试次、实验 `play` 总数及来源 SHA1 的校验。任何缺失或不符即 fail closed。

## 边界及后续

此阶段只建立七模型 native Python 运行的可验证环境、同源选择样本、Model 3 数值同构锚点。未优化其余六个模型，未运行作者层级 EM/iBIC，未评估受试者留出泛化；不能称作完整七模型重拟合。正式拟合须事先单独冻结优化预算、随机种子、多起点、收敛失败处理、样本和受试者折划分、两套重置方案的模型同构性以及跨模型一致评分。

验收准则：离线人工构造输入测试 PASS；有单独 GitHub Actions 原始来源回放成功作业，且每个 native 模型及两项 Model 3 交叉核验 PASS；来源完整校验失败时必须直接拒绝。作业失败时报告对应阻塞原因，不能转成通过宣告。

`R065_FULL_SEVEN_MODEL_EQUAL_FIT = OPEN`

`R065_INDEPENDENT_PREDICTION = OPEN`

`PESEN_v0.1 = FROZEN`
