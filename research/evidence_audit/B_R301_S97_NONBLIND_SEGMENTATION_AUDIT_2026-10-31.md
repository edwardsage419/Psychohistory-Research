# B轨 R301 S97 内部非盲态独立数学复核

UTC 2026-10-30。预先阅读R301 S97冻结提交b18d1cd4e149a60ebfe3732f38f09f1cb6d94e7a及原R301协议。已读R路线完整输出，属于非盲态内部独立算法复核，没有外部研究团队参与。

B算法不导入原R301代码及本轮R代码。每个四位观测历史独立穷举2^3种分段，每个五位观测历史穷举2^4种分段。各段按Beta(1,1)边际积分乘积计算联合概率，乘固定边界风险先验，五位证据除以四位证据得到下一位预测。与R路线逐项比较真实历史概率、真实与假定预测、未来联合质量、Brier损失及加权损失。

结果：288条人工原子全部一致；九组汇总风险、九组超额风险精确Fraction一致；各真实风险率下16个唯一历史证据总质量1。Brier超额风险等于候选与oracle预测差平方的历史概率加权和，九组全部通过。R路线8项测试通过。B路线9项测试通过，其中完整正例1项、预定篡改拒绝7项、分段归一化1项。篡改覆盖重复来源、缺失来源、联合概率、候选预测、第五位结果、汇总风险及错误提升E2等级。

复算：`python research/evidence_audit/b_r301_s97_independent_segmentation.py --folder research/validation`；`python research/evidence_audit/b_r301_s97_independent_segmentation.py --test`。B脚本使用Python标准库，独立读取归档CSV、JSON及SHA256收据。

未运行GitHub Actions，CI=NOT_RUN。原R301历史588项测试本轮未重新执行。有限人工全体穷举的精确风险无样本抽样置信区间。真人样本外预测、经验校准、外部团队独立复现均未建立。原R301正式验收、R073及PESEN v0.1冻结不变。
