# 第七轮配对样本规划勘误（2026-11-24）

原提交 bf6bff99868a61da2efcc12fee61c7192d3488f6 的 value_probe.js、results.json、README.md 保留原样。其 planning 字段中的假设胜率0.75双侧检验条件功效使用了错误的第二尾部阈值，导致功效大于1；原功效值无效。最低胜对数与双侧零假设p值不受影响；324组合数学实验及12评分负控也不受影响。本勘误只替换样本规划数值，不修改历史记录或冻结协议。

设 X~Bin(n,0.75)，双侧对称拒绝域 X>=k 或 X<=n-k。功效为 P(X>=k)+P(X<=n-k)=P(Bin(n,0.75)>=k)+P(Bin(n,0.25)>=k)。原式第二项误用 n-k。实际重新计算并用直接下尾公式复核，各功效在[0,1]内。

[
  {
    "discordant": 10,
    "minimumWins": 9,
    "twoSidedP": 0.021484375,
    "powerIfWinProbabilityPoint75": 0.24405479431152344
  },
  {
    "discordant": 20,
    "minimumWins": 15,
    "twoSidedP": 0.041389465332031264,
    "powerIfWinProbabilityPoint75": 0.6171764674145381
  },
  {
    "discordant": 30,
    "minimumWins": 21,
    "twoSidedP": 0.04277394525706769,
    "powerIfWinProbabilityPoint75": 0.8034069187820486
  },
  {
    "discordant": 40,
    "minimumWins": 27,
    "twoSidedP": 0.038477308284200255,
    "powerIfWinProbabilityPoint75": 0.8967682946505678
  },
  {
    "discordant": 60,
    "minimumWins": 39,
    "twoSidedP": 0.027340133868077945,
    "powerIfWinProbabilityPoint75": 0.9701991300610822
  },
  {
    "discordant": 80,
    "minimumWins": 50,
    "twoSidedP": 0.03299261842647618,
    "powerIfWinProbabilityPoint75": 0.9954180144333701
  }
]

value_probe_corrected.js 为仅修正尾部方向的可复跑版本；results_corrected.json 保留原实验结果并替换 planning 字段。实际本轮重算了全部六项规划值，校对了原始结果，未运行真实AI比较或独立样本。该功效以独立不一致对、指定条件胜率0.75为假设，不能直接换算总题数，相关案例变体不可视作独立。建议未来先小型独立试点估计不一致对比例，再由独立验收确定样本量。