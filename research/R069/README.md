# R069：网络集体行动的局部阈值、随机级联与宏观创新扩散

建立日期：2026-10-16。状态：**ACTIVE；E1 三机制数学基线 PASS，真实网络采纳数据 E2 OPEN，外部独立 E3 OPEN**。从 [R068 文化学习有限结题](../R068/R068_FINAL_ACCEPTANCE_AND_CLOSURE_2026-10-16.md)转向与短期选择明显不同的社会传播/技术制度采纳机制。

## 文献锚和冻结协议

[独立数学协议](../../protocols/R069_NETWORK_CASCADE_THREE_MECHANISMS_2026-10-16.md)已在首次测试结果出现前提交。四条经典文献线索：
- Granovetter (1978), *Threshold Models of Collective Behavior*, DOI [10.1086/226707](https://doi.org/10.1086/226707)；
- Watts (2002), *A simple model of global cascades on random networks*, DOI [10.1073/pnas.082090499](https://doi.org/10.1073/pnas.082090499)；
- Kempe, Kleinberg & Tardos (2003), *Maximizing the spread of influence through a social network*, DOI [10.1145/956750.956769](https://doi.org/10.1145/956750.956769)；
- Bass (1969), *A New Product Growth for Model Consumer Durables*, DOI [10.1287/mnsc.15.5.215](https://doi.org/10.1287/mnsc.15.5.215)。

本研究自己明确写出**六节点固定路径网络**，并不冒充复现 Watts 的随机大图临界相变、Kempe 的影响力优化理论证明或 Bass 的真实产品销量推断。

## 已真实完成的 E1

[纯 Python 三机制运行程序](r069_network_cascade_baselines.py) · [22 项数学边界测试](test_r069_network_cascade_baselines.py) · [机读结果](R069_E1_NETWORK_CASCADE_RESULTS.json)。[GitHub Actions run 38872162843](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38872162843) `completed/success`，22 tests OK。

固定 6 个节点的路径 `0−1−2−3−4−5`，初始仅节点 0 采纳：

| 机制 | 固定规则 | 结果 |
|---|---|---|
| Watts 同步局部阈值 | `φ=0.5`，邻居采纳比达到阈值即不可逆采纳 | 5 轮后 6/6 节点采纳 |
| 高阈值对照 | `φ=0.75` | 5 轮后仍只有 1/6 种子 |
| 独立级联 IC | 有向路径，每边单次 `β=0.5` 成功机会 | 精确穷举 32 种活边，最终采纳期望 **1.96875** 节点；每节点采纳概率 `[1,.5,.25,.125,.0625,.03125]` |
| Bass 宏观创新＋模仿 | `p=.03,q=.4,dt=1,x0=1/6` 离散 Euler | 第 1 步比例 `0.2472222`，第 5 步 `0.6807123` |

三种传播规则使用不同信息结构：局部阈值依赖邻居采纳比例，IC 依赖单次独立传播机会，Bass 是没有节点网络的总体采纳微分方程数值近似。因此不能仅按数字高低判定哪一个反映真实社会传播。

## 下一 E2 数据输入门

需要可合法复核的**节点间真实关系、起始种子、按时间的首次采纳/暴露、未观察或终止观察的风险集**。仅凭社交图和帖文转发不能直接说明感染、独立级联边传播或某个阈值导致采纳。应先冻结测量与匿名性/知识产权约束，然后校验至少两种机制在同一事件级时间数据上的可识别性与风险集，才可开展真人预测。

`R069_ACTIVE=YES`
`R069_E1=PASS`
`R069_E2_NETWORK_ADOPTION=OPEN`
`R069_E3=OPEN`
`PESEN_v0.1=FROZEN`
