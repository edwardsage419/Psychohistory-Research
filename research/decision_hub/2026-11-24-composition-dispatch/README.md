# 智能决策中枢第四轮：按需组合调度与有类型依赖

2026-11-24。RESEARCH_CANDIDATE，合成开发集。起始 main 51038155e420e3ecd602bf3c412dea1efe273853，v0.6 PR #61 HEAD 96b4293aa6b4d3c4cf16ece126e4dff07f25874f，仍为 Draft。本轮核查 v3.1、AGENTS、同步规程、近期提交、开放PR、产品轨近期协调清单、前三轮专项研究。源码锁定 main 版本：decision_registry.py 8046de09674af850a456bbccc534e5f6c2511497；decision_hub.py a97de30f5241063862dbc0ce797c214cbc4d405f；decision_v05.py bc27cc42e4a8224c86c3113d044a328ae5eeba3e；decision_planner.py f2d3d21b853afe9dc757a33e83cd3d6160f8dd7b；decision_regret.py e56689a54897d95eaa126540c23fca51cc0eede7；decision_scoring.py 7832116703246bafc98831a6039d14c0d691cdd1；decision_timing.py 4ed9fa430dcb993cc5005656c8b1744276fe7c33；decision_voi.py a69571fcf6df9a779ed317e76c5dcac6933d2728。

## 源码审查与新增范围
现有中枢已有硬约束优先、精确方法版本、全注册表拓扑排序、依赖未执行时拒绝下游、模型异常隔离、原生适用性校验、当前/结构可行集区分、条件性领导集合和一般分歧提示。不得把这些重计为新成果。decision_registry.execution_order 遇任意循环抛错、遇缺失依赖跳过其拓扑访问；decision_hub.analyze 对全部方法逐个尝试，依赖门控依据 executed 字典成员。数学结果 UNKNOWN 仍可能拥有工程 EXECUTED 状态（例如 timing_actions）。这不是当前内置方法已错误计算的证明；新增依赖若只要求特定可解析量，需在原生适用性前增加类型与结果资格检查。当前已有原生验证器，不能把本轮模拟的缺口认定为实际产品绕过。planner 已区分后悔值与最坏效用的一些分歧；扩展目标是明确语义比较合同，而非重复现有提示。

## 实验
同一 JS 函数在本轮工具中实际执行，脚本与结果一起归档。重放 node dispatch_probe.js。输出摘要：
{
  "graph": {
    "cases": 32,
    "baseline_attempts": 192,
    "candidate_attempts": 128
  },
  "faults": 8,
  "edges": {
    "cases": 128,
    "baseline_allows": 64,
    "candidate_allows": 3,
    "baseline_false_allows": 61,
    "candidate_false_allows": 0
  },
  "criteria": {
    "cases": 625,
    "counts": {
      "AGREE": 445,
      "DIFFERENT_CRITERIA_OVERLAP": 160,
      "DIFFERENT_CRITERIA_DISJOINT": 20
    },
    "example": {
      "u": [
        [
          0,
          4
        ],
        [
          1,
          1
        ]
      ],
      "worst": [
        1,
        3
      ],
      "floors": [
        0,
        1
      ],
      "mr": [
        "A"
      ],
      "mm": [
        "B"
      ],
      "relation": "DIFFERENT_CRITERIA_DISJOINT"
    }
  },
  "comparisons": 12
}
六节点为自构示意图，不是实际注册表的依赖映射。G为硬约束，P为可比性，W为加权，R为后悔，T为时机，I为调查；32种请求子集，强制G，独立固定点闭包核对依赖覆盖与拓扑先后。全表尝试次数只是调用入口数量基线（每次六个），不等同实际执行次数或延迟。8个故障案例包含循环、缺失依赖、未准入、未知请求、关键G故障；候选仅隔离无效请求的依赖子图。整个受信注册表的完整性或签名不可信时必须全局失败，不能用局部隔离绕过。Python官方 graphlib 文档 https://docs.python.org/3.13/library/graphlib.html （公开摘录，拓扑排序与循环错误）。128个有类型边组合按两个消费者合同各64组枚举；基线仅复现 executed 成员检查，未运行原生验证器。允许 UNKNOWN 的消费者必须明确传播 UNKNOWN，不把它换为点值；数字端口须有合格的数值。625个二行动、二情景整数效用矩阵，逐一复算后悔值与最坏效用；不设概率，不表示现实频率。12个对比合同状态例，识别相同合同分歧、不同准则、不同假设、不同范围、过期及未知。后悔值运算已存在，仅作为组合结论语义的测试夹具；非新数学模型或科学结题。独立留出与实际工程延迟均未执行。

## 接入规格
请求来自确认的目标及上一轮检索准入，展开受信注册表定义的依赖闭包；硬约束为不可省略的全局前置。节点带固定方法身份、输入快照、候选行动范围、必要数据、输出端口、证据/假设与适用期。边带输出类型、允许未知与否、同一版本及可比口径；不可用结果阻止依赖链，但独立有效链可继续。禁止从检索文本发明依赖或授权。按需调度不能抑制硬约束、重要风险或模型冲突；用户未明确的决策准则不得自动固定。跨模型结果收据应包含分析版本、输入和依赖摘要、方法身份、输出摘要、证据状态及授权代次；同一比较合同才讨论结果一致性。不同准则展示条件性差异，不机械平均，不把重叠领导集合视作完全一致。研究代码没有执行生产模型、签名或真实凭证。实际收据校验、并发、撤回、完整模型覆盖、回退与原生验证需要工程及独立验收。

下一责任方：独立验收轨使用未见案例审查闭包、失败、跨版本、不同范围和数学未知的传播；模型轨提供真实端口与依赖条件；产品轨统一显示分歧及最少追问；本窗口下一轮研究基于可能行动集合的最少追问，累计完整版本交接。无个人数据、训练、CI、PR合并、部署、费用、冻结协议变更。未修改正式源码。
