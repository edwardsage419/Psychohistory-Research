# MKT111 OR-Tools CP-SAT 无可行解状态与冲突解释边界
日期：2026-10-29（Asia/Singapore）。轨道：market。证据：MARKET E1 文档与人工枚举。费用：0。

## 去重与问题
MKT110已经说明目标和最低储备可能没有共同可行解。本轮研究开源求解器如何区分已经证明无解、未求得答案、模型无效和存在非最优可行解，重点审计不可行假设集合的解释边界。

## 英文一手来源
S1 Google OR-Tools CP-SAT官方指南 https://developers.google.com/optimization/cp/cp_solver/ ：OPTIMAL、FEASIBLE、INFEASIBLE、MODEL_INVALID、UNKNOWN五种状态；CP-SAT使用整数约束。
S2 上游稳定分支故障排查 https://github.com/google/or-tools/blob/stable/ortools/sat/docs/troubleshooting.md ：可使用假设文字与 enforcement literal 分析不可行，所得集合虽有缩减但不保证最小；使用假设解释应采用单线程，优化问题的假设核心可能包含全部假设。
S3 上游协议字段 https://github.com/google/or-tools/blob/stable/ortools/sat/cp_model.proto ：sufficient_assumptions_for_infeasibility 只在 INFEASIBLE 状态填充，返回的是足以维持无解的假设子集，不能自动当作最小冲突或唯一原因。
S4 官方开源仓库 https://github.com/google/or-tools ：Apache License 2.0。公开源码和文档可免费阅读，使用时应核对本地安装、依赖和环境。

## 输入、状态、目标、反馈和可验证性
官方支持整数变量、约束、可选目标函数、求解参数和终止状态；假设文字可映射到冲突解释。求解器本身不学习个人长期偏好、不具备个人财务账户读取权限、不授予支付或交易权限。状态标签及求解证据需由调用者记录；用户授权、申诉、费用、隐私和数据生命周期应由上层系统另行治理。

## 人工反例与执行结果
自包含脚本 research/market/mkt111_cp_sat_status_core_manual_20261029.js 只使用Node.js原生枚举，不安装或执行OR-Tools。变量x取0到10整数。A为x>=7，B为x<=5，C为x<=9，D为x>=0。四个条件全部开启时无解；仅A与B已足以无解，C和D冗余。枚举16个假设子集，恰有4个无解，最小不可满足集合为{A,B}。完整集合{A,B,C,D}也足以证明无解，但它不是最小解释。19项人工检查通过，0失败。该结果是人工集合枚举，不能冒充OR-Tools返回了哪组核心。

## 候选拒绝与解释规则
C1 INFEASIBLE：拒绝自动执行，提供冲突约束和适用版本，允许人工修改条件后重新求解。
C2 UNKNOWN：保留未判定，不能显示为无解或可行；MODEL_INVALID：阻断并修正模型。
C3 FEASIBLE：明确未证明最优；OPTIMAL：仍须独立权限审查，优化成功不代表用户授权。
C4 所有核心解释标明“充分冲突子集”，不宣称最小、唯一或政策优先级。若需要最小核心须另行验证。
C5 用户可自主决定约束放松方向，不预设单一人生效用权重。任何支付、交易和隐私数据读取须独立授权。

## 证据与费用边界
官方文档为软件接口与算法说明，人工枚举为内部E1演示。OR-Tools二进制未运行，真实调用状态、运行时性能、跨环境稳定性、人生决策效益和第三方独立验证均UNKNOWN。没有购买、注册、计费API、云计算或收费CI。下一项MKT112：比较CP-SAT最小冲突解释与线性规划松弛量的可读性。
