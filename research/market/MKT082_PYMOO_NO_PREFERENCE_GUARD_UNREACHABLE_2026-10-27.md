# MKT082 pymoo PI NSGA II 全部并列偏好的守卫条件审计

日期：2026-10-27（Asia/Singapore）。轨道market。证据等级MARKET E1。新增CI NOT_RUN。主动新增费用0。

## 去重与固定来源
启动读取main、MKT080、MKT081、E050、F002、R218 S14至R220 S16。MKT080和MKT081分别审查名次阈值索引、拟合失败后的候选身份错配。本轮只检查“没有可区分偏好”的检测与控制流。
上游anyoptimization/pymoo固定提交 `23110c155aa8f31b5f1b86928227fb3931ba7f00`，`pymoo/algorithms/moo/pinsga2.py` blob `207726ffba920eca75f739b2d0cccaf0c23d92b8`；`tests/algorithms/test_deterministic_moo.py` blob `5ad77aeb58797a8f72ab0bb3ff221bc14f19ac5a`。核对上游main同一源码blob。官方文档 https://pymoo.org/algorithms/moo/pinsga2.html 。

## 本轮源码新发现
算法每tau代显示eta个Pareto候选，用户可两两比较或给出绝对名次。两两比较回答c时，`group.append(i)`将候选放入同一偏好组，全部并列可产生全1的`dm_ranks`。
在收集`dm_ranks`后，源码检查`if len(set(rank)) == 0:`并准备输出“No preference between any two points provided”及重置偏好。这里的`rank`来自此前`rank, F = self.pop.get("rank", "F")`，表示种群非支配层级。只要种群非空，set(rank)至少含一个元素，因此这一守卫永远为假。并列偏好输入将继续走向价值函数拟合。拟合实际结果与最终解是否受损未知，未运行完整优化器。
官方文档支持偏好交互机制，固定源码支持变量来源和守卫事实，独立穷举只证明条件不可达。已检查的固定确定性测试文件使用按第一目标排序的自动决策者，未见明确全并列断言；其他测试未全面审计。

## 离线验证
标准库Node脚本 `research/market/mkt082_pymoo_no_preference_guard_20261027.js` 检查五项源码表达式，穷举n=2至6共1089个三值种群层级向量，并验证五种全并列偏好输入。1099项断言通过，失败0。此为条件性控制流证明，不能视作真实用户错误率。脚本要求固定上游两个Git blob原文并验证SHA，不安装或运行pymoo。
真实输入为候选目标向量、种群层级、决策者名次及优化参数。反馈是定期重新排序并拟合价值函数。源码没有为长期人生偏好校准、撤销授权、敏感数据保存提供已验证保证。Apache 2.0开源，审查免费。

## 风险及候选控制
MKT082-C1 将种群rank与用户dm_ranks采用独立类型和命名；全并列状态必须直接识别。
MKT082-C2 测试全并列、部分并列、重复候选、空输入、拟合失败及重试后的候选身份；记录来源和版本。
MKT082-C3 不预设永久唯一效用权重；保留用户更正、撤回和人工批准。
风险为固定源码守卫不可达，真实生产损害及概率UNKNOWN。下一MKT083检查并列输入传入价值函数拟合器后的实际约束和异常分支。R系列、F002本周状态和零费用约束保持不变。
