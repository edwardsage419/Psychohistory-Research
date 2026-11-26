# 自主认知与知识：白话分句检索、共同档案歧义及方法发现边界
2026-11-26。RESEARCH_CANDIDATE / REAL_REPOSITORY_TEXT_RETRIEVAL / SYNTHETIC_DEVELOPMENT / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NO_TRAINING。
## 基线
起点main cb188c0c3011b958277d88c2155276c45e228cee；本轮初始main 856ae2abaed5baa2391cd3e73c14d806b43c7c45，已核对25近期提交、15开放PR、v3.2和同步规程；#63固定head 734686980b19da9291bdd08b67d4e2519c011acf仍Draft。唯一交接尝试路径404，未确认最新版本。前轮真实来源审计 da528f2b26429f6c2c29729d0181c50b7ccf8f66，R28正文检索36ca07db56fc64865d6cc7a5db87384583604844（16文档20人工查询，已有中英文扩展和BM25），R67固定原生discover、联合角色与原文关系研究94f6de457f60655cabb8f65dd90c6e4be81591cb。此轮不重计全文索引、既有词法或通用BM25；具体比较固定五个原生显式目标对真实共享档案的候选歧义、原始64轮分句和累计上下文及负向控制。未证明全库查重。
固定资产（路径、Git blob、读取commit）：
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb cb188c0c3011b958277d88c2155276c45e228cee
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132 cb188c0c3011b958277d88c2155276c45e228cee
research/decision_hub/2026-11-24-method-corpus-index/corpus_index.json 6862d5a2cd3c7eb3f2da9a85d79c8b3386f2a102 cb188c0c3011b958277d88c2155276c45e228cee
platform/future_model/src/psychohistory/decision_knowledge_planning.py d32854c4909df858ee851634747234ed5dec657b 734686980b19da9291bdd08b67d4e2519c011acf
research/decision_methods/C028_INTERVAL_HARD_CONSTRAINT_FEASIBILITY_2026-11-20.md 7cb8d5e3631dd17c0650cec06139d88b5bfcc700 cb188c0c3011b958277d88c2155276c45e228cee
research/decision_methods/C004_DYNAMIC_UTILITY_MULTI_OBJECTIVE_ROBUST_2026-10-27.md 0d04c633a26437ad6017946cd528c4dc68db3d83 cb188c0c3011b958277d88c2155276c45e228cee
research/decision_methods/C029_SCENARIO_MINIMAX_REGRET_INFORMATION_BOUNDARY_2026-11-20.md a2588cfdd47e547a46a7ee8cde2644caf81198d9 cb188c0c3011b958277d88c2155276c45e228cee
research/decision_methods/C009_OPTION_VALUE_INFORMATION_REVERSIBILITY_2026-11-01.md 5048081b0a277f4bc511aff2293020268fd5c57c cb188c0c3011b958277d88c2155276c45e228cee
research/decision_methods/BUEHLER_GRIFFIN_ROSS_1994_PERSONAL_COMPLETION_TIME_FORECAST_BOUNDARY_2026-11-21.md e7e1002f00aab5bf782a5f2845fbfac2cb80969b cb188c0c3011b958277d88c2155276c45e228cee
research/decision_methods/VOI_DELAY_DEADLINE_OPPORTUNITY_COST_2026-11-21.md c5214371527e058eec64049522b605150d7c496d cb188c0c3011b958277d88c2155276c45e228cee
research/decision_methods/C030_INTERVAL_BOUNDED_SCENARIO_REGRET_2026-11-20.md 57301fb2a1dbda8e99510b44d6fcfb2e5f4a191e cb188c0c3011b958277d88c2155276c45e228cee
research/decision_methods/VOI_IMPERFECT_BINARY_SIGNAL_METHOD_CARD_2026-11-20.md bd494e2e1200a526dcb11d454e423ff9aebccd33 cb188c0c3011b958277d88c2155276c45e228cee
连接器全部12份内容读取并核对报告blob，不独立重算全字节。8档案为154索引中人工选定子集，部分是五方法以外的对照；不重新分发全文。两语料为既有公开合成开发语料，非真实用户、训练或独立留出。
## 方法
从固定原生GOALS字典提取五个登记目标与方法键，JS模拟原生精确分句匹配（未执行原生Python discover）。仅对五个方法进行候选发现，绝不因检索命中推断适用性、许可、用户目标或执行。真实档案到方法关系来自固定manifest；不以共享文献推断独立科学证据。对全文原句、原生目标短语分别用已有Han bigram/英文token、BM25 k1=1.2 b=.75（JS NFKC，与原生token规则对应的研究实现），档案分值取关联档案最大；分句融合对各句的正分及并列排名取倒数排名最大，避免简单相加使长句重复贡献，不调参。并列按方法键排序仅作计数，不应据此选方法。共享档案导致方法得分结构性相同，额外适用合同不可省略。所有候选只读authority NONE/outside true；未实现作用域、否定、隐含意图、撤权后历史检索、安全许可或科学准入。累计历史只作故意未过滤的研究对照，不能在用户撤回、修订或主体变化时直接使用。
## 评价
64轮原文，不使用标注训练；研究者在查看语料后按18情节人工标记有限发现方向，36轮仅为弱相关性标签（同情节两轮不代表每轮真实意图），其余28轮只记录非空候选，不判为错误。分别原句与累计两轮，对比精确短句、档案正文、原生目标短语、分句倒数排名融合。另23条人工控制（5精确目标、5白话变体、2多目标、5否定/转述/条件、2混合、4范围外或非授权目标），故意包含无目标及部分目标；评价候选覆盖和非空误触发，不把相关发现当用户授权或科学执行。所有目标及控制由本轮研究者选择，未冻结独立留出；不宣称真实语言准确率。输出排序分数不是概率。代码实际运行两次一致。原生完整路径、真实用户、独立留出、真机和训练未运行。
```json
{
  "docs": 8,
  "methods": [
    "c028_interval_feasibility@1.0.0",
    "pareto@1.0.0",
    "weight_sensitivity@1.0.0",
    "C029@1.0.0",
    "timing_actions@1.0.0"
  ],
  "realSharedSourceGroups": [
    {
      "path": "research/decision_methods/C004_DYNAMIC_UTILITY_MULTI_OBJECTIVE_ROBUST_2026-10-27.md",
      "methods": [
        "pareto@1.0.0",
        "weight_sensitivity@1.0.0"
      ]
    }
  ],
  "development": {
    "raw": {
      "exact": {
        "queries": 36,
        "targets": 42,
        "hit1": 0,
        "hit3": 0,
        "recall3": 0,
        "all3": 0,
        "empty": 36,
        "tiesAt1": 0,
        "negativeReturns": 0,
        "totalReturned": 0
      },
      "body": {
        "queries": 36,
        "targets": 42,
        "hit1": 5,
        "hit3": 11,
        "recall3": 11,
        "all3": 5,
        "empty": 5,
        "tiesAt1": 16,
        "negativeReturns": 0,
        "totalReturned": 87
      },
      "goal": {
        "queries": 36,
        "targets": 42,
        "hit1": 3,
        "hit3": 6,
        "recall3": 6,
        "all3": 2,
        "empty": 28,
        "tiesAt1": 0,
        "negativeReturns": 0,
        "totalReturned": 18
      },
      "clauseFusion": {
        "queries": 36,
        "targets": 42,
        "hit1": 4,
        "hit3": 11,
        "recall3": 12,
        "all3": 6,
        "empty": 5,
        "tiesAt1": 22,
        "negativeReturns": 0,
        "totalReturned": 94
      }
    },
    "context": {
      "exact": {
        "queries": 36,
        "targets": 42,
        "hit1": 0,
        "hit3": 0,
        "recall3": 0,
        "all3": 0,
        "empty": 36,
        "tiesAt1": 0,
        "negativeReturns": 0,
        "totalReturned": 0
      },
      "body": {
        "queries": 36,
        "targets": 42,
        "hit1": 7,
        "hit3": 12,
        "recall3": 12,
        "all3": 6,
        "empty": 3,
        "tiesAt1": 16,
        "negativeReturns": 0,
        "totalReturned": 95
      },
      "goal": {
        "queries": 36,
        "targets": 42,
        "hit1": 3,
        "hit3": 8,
        "recall3": 8,
        "all3": 3,
        "empty": 26,
        "tiesAt1": 0,
        "negativeReturns": 0,
        "totalReturned": 25
      },
      "clauseFusion": {
        "queries": 36,
        "targets": 42,
        "hit1": 5,
        "hit3": 12,
        "recall3": 13,
        "all3": 7,
        "empty": 3,
        "tiesAt1": 26,
        "negativeReturns": 0,
        "totalReturned": 105
      }
    }
  },
  "controls": {
    "exact": {
      "queries": 23,
      "targets": 16,
      "hit1": 7,
      "hit3": 7,
      "recall3": 9,
      "all3": 7,
      "empty": 16,
      "tiesAt1": 2,
      "negativeReturns": 0,
      "totalReturned": 9
    },
    "body": {
      "queries": 23,
      "targets": 16,
      "hit1": 3,
      "hit3": 9,
      "recall3": 10,
      "all3": 8,
      "empty": 1,
      "tiesAt1": 7,
      "negativeReturns": 8,
      "totalReturned": 61
    },
    "goal": {
      "queries": 23,
      "targets": 16,
      "hit1": 11,
      "hit3": 13,
      "recall3": 15,
      "all3": 13,
      "empty": 5,
      "tiesAt1": 0,
      "negativeReturns": 5,
      "totalReturned": 52
    },
    "clauseFusion": {
      "queries": 23,
      "targets": 16,
      "hit1": 11,
      "hit3": 14,
      "recall3": 16,
      "all3": 14,
      "empty": 1,
      "tiesAt1": 18,
      "negativeReturns": 8,
      "totalReturned": 82
    }
  },
  "controlRows": [
    {
      "q": "判断方案是否违反底线",
      "want": [
        "c028_interval_feasibility@1.0.0"
      ],
      "results": {
        "exact": [
          "c028_interval_feasibility@1.0.0"
        ],
        "body": [
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0",
          "timing_actions@1.0.0"
        ],
        "goal": [
          "c028_interval_feasibility@1.0.0",
          "weight_sensitivity@1.0.0"
        ],
        "clauseFusion": [
          "c028_interval_feasibility@1.0.0",
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0",
          "timing_actions@1.0.0"
        ]
      }
    },
    {
      "q": "比较各目标的优势",
      "want": [
        "pareto@1.0.0"
      ],
      "results": {
        "exact": [
          "pareto@1.0.0"
        ],
        "body": [
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0",
          "timing_actions@1.0.0"
        ],
        "goal": [
          "pareto@1.0.0",
          "timing_actions@1.0.0",
          "C029@1.0.0"
        ],
        "clauseFusion": [
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0",
          "timing_actions@1.0.0",
          "C029@1.0.0"
        ]
      }
    },
    {
      "q": "判断权重改变是否影响选择",
      "want": [
        "weight_sensitivity@1.0.0"
      ],
      "results": {
        "exact": [
          "weight_sensitivity@1.0.0"
        ],
        "body": [
          "timing_actions@1.0.0",
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0"
        ],
        "goal": [
          "weight_sensitivity@1.0.0",
          "c028_interval_feasibility@1.0.0"
        ],
        "clauseFusion": [
          "timing_actions@1.0.0",
          "weight_sensitivity@1.0.0",
          "c028_interval_feasibility@1.0.0",
          "pareto@1.0.0"
        ]
      }
    },
    {
      "q": "比较最坏情景的后悔值",
      "want": [
        "C029@1.0.0"
      ],
      "results": {
        "exact": [
          "C029@1.0.0"
        ],
        "body": [
          "timing_actions@1.0.0",
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0"
        ],
        "goal": [
          "C029@1.0.0",
          "pareto@1.0.0",
          "timing_actions@1.0.0"
        ],
        "clauseFusion": [
          "C029@1.0.0",
          "timing_actions@1.0.0",
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0"
        ]
      }
    },
    {
      "q": "比较现在行动和等待",
      "want": [
        "timing_actions@1.0.0"
      ],
      "results": {
        "exact": [
          "timing_actions@1.0.0"
        ],
        "body": [
          "timing_actions@1.0.0",
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0"
        ],
        "goal": [
          "timing_actions@1.0.0",
          "pareto@1.0.0",
          "C029@1.0.0"
        ],
        "clauseFusion": [
          "timing_actions@1.0.0",
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0",
          "C029@1.0.0"
        ]
      }
    },
    {
      "q": "两个方案有没有踩到我的最低要求？",
      "want": [
        "c028_interval_feasibility@1.0.0"
      ],
      "results": {
        "exact": [],
        "body": [
          "timing_actions@1.0.0",
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0"
        ],
        "goal": [
          "c028_interval_feasibility@1.0.0"
        ],
        "clauseFusion": [
          "c028_interval_feasibility@1.0.0",
          "timing_actions@1.0.0",
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0"
        ]
      }
    },
    {
      "q": "每个方面分别哪个选项更占优势？",
      "want": [
        "pareto@1.0.0"
      ],
      "results": {
        "exact": [],
        "body": [
          "timing_actions@1.0.0",
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0"
        ],
        "goal": [
          "pareto@1.0.0"
        ],
        "clauseFusion": [
          "pareto@1.0.0",
          "timing_actions@1.0.0",
          "weight_sensitivity@1.0.0"
        ]
      }
    },
    {
      "q": "如果我更看重时间，原来的排序会变吗？",
      "want": [
        "weight_sensitivity@1.0.0"
      ],
      "results": {
        "exact": [],
        "body": [
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0",
          "timing_actions@1.0.0"
        ],
        "goal": [],
        "clauseFusion": [
          "pareto@1.0.0",
          "timing_actions@1.0.0",
          "weight_sensitivity@1.0.0"
        ]
      }
    },
    {
      "q": "情况变糟以后哪种选法的后悔最小？",
      "want": [
        "C029@1.0.0"
      ],
      "results": {
        "exact": [],
        "body": [
          "timing_actions@1.0.0",
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0"
        ],
        "goal": [
          "C029@1.0.0"
        ],
        "clauseFusion": [
          "C029@1.0.0",
          "timing_actions@1.0.0",
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0"
        ]
      }
    },
    {
      "q": "先做还是多等一阵再做比较合适？",
      "want": [
        "timing_actions@1.0.0"
      ],
      "results": {
        "exact": [],
        "body": [
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0",
          "timing_actions@1.0.0"
        ],
        "goal": [
          "pareto@1.0.0",
          "timing_actions@1.0.0",
          "C029@1.0.0"
        ],
        "clauseFusion": [
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0",
          "timing_actions@1.0.0",
          "C029@1.0.0"
        ]
      }
    },
    {
      "q": "判断方案是否违反底线。比较现在行动和等待",
      "want": [
        "c028_interval_feasibility@1.0.0",
        "timing_actions@1.0.0"
      ],
      "results": {
        "exact": [
          "c028_interval_feasibility@1.0.0",
          "timing_actions@1.0.0"
        ],
        "body": [
          "timing_actions@1.0.0",
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0"
        ],
        "goal": [
          "c028_interval_feasibility@1.0.0",
          "timing_actions@1.0.0",
          "weight_sensitivity@1.0.0",
          "pareto@1.0.0",
          "C029@1.0.0"
        ],
        "clauseFusion": [
          "c028_interval_feasibility@1.0.0",
          "pareto@1.0.0",
          "timing_actions@1.0.0",
          "weight_sensitivity@1.0.0",
          "C029@1.0.0"
        ]
      }
    },
    {
      "q": "比较各目标的优势。判断权重改变是否影响选择",
      "want": [
        "pareto@1.0.0",
        "weight_sensitivity@1.0.0"
      ],
      "results": {
        "exact": [
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0"
        ],
        "body": [
          "timing_actions@1.0.0",
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0"
        ],
        "goal": [
          "weight_sensitivity@1.0.0",
          "pareto@1.0.0",
          "c028_interval_feasibility@1.0.0",
          "timing_actions@1.0.0",
          "C029@1.0.0"
        ],
        "clauseFusion": [
          "pareto@1.0.0",
          "timing_actions@1.0.0",
          "weight_sensitivity@1.0.0",
          "c028_interval_feasibility@1.0.0",
          "C029@1.0.0"
        ]
      }
    },
    {
      "q": "不要判断方案是否违反底线",
      "want": [],
      "results": {
        "exact": [],
        "body": [
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0",
          "timing_actions@1.0.0"
        ],
        "goal": [
          "c028_interval_feasibility@1.0.0",
          "weight_sensitivity@1.0.0"
        ],
        "clauseFusion": [
          "c028_interval_feasibility@1.0.0",
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0",
          "timing_actions@1.0.0"
        ]
      }
    },
    {
      "q": "他说“比较各目标的优势”，我只是转述。",
      "want": [],
      "results": {
        "exact": [],
        "body": [
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0",
          "timing_actions@1.0.0"
        ],
        "goal": [
          "pareto@1.0.0",
          "timing_actions@1.0.0",
          "C029@1.0.0"
        ],
        "clauseFusion": [
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0",
          "timing_actions@1.0.0",
          "C029@1.0.0"
        ]
      }
    },
    {
      "q": "暂时不想判断权重改变是否影响选择",
      "want": [],
      "results": {
        "exact": [],
        "body": [
          "timing_actions@1.0.0",
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0"
        ],
        "goal": [
          "weight_sensitivity@1.0.0",
          "c028_interval_feasibility@1.0.0"
        ],
        "clauseFusion": [
          "timing_actions@1.0.0",
          "weight_sensitivity@1.0.0",
          "c028_interval_feasibility@1.0.0",
          "pareto@1.0.0"
        ]
      }
    },
    {
      "q": "如果以后需要比较最坏情景的后悔值再说。",
      "want": [],
      "results": {
        "exact": [],
        "body": [
          "timing_actions@1.0.0",
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0"
        ],
        "goal": [
          "C029@1.0.0",
          "pareto@1.0.0",
          "timing_actions@1.0.0"
        ],
        "clauseFusion": [
          "C029@1.0.0",
          "timing_actions@1.0.0",
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0"
        ]
      }
    },
    {
      "q": "我没让你比较现在行动和等待",
      "want": [],
      "results": {
        "exact": [],
        "body": [
          "timing_actions@1.0.0",
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0"
        ],
        "goal": [
          "timing_actions@1.0.0",
          "pareto@1.0.0",
          "C029@1.0.0"
        ],
        "clauseFusion": [
          "timing_actions@1.0.0",
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0",
          "C029@1.0.0"
        ]
      }
    },
    {
      "q": "比较各目标的优势，不要判断权重改变是否影响选择",
      "want": [
        "pareto@1.0.0"
      ],
      "results": {
        "exact": [],
        "body": [
          "timing_actions@1.0.0",
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0"
        ],
        "goal": [
          "weight_sensitivity@1.0.0",
          "pareto@1.0.0",
          "c028_interval_feasibility@1.0.0",
          "timing_actions@1.0.0",
          "C029@1.0.0"
        ],
        "clauseFusion": [
          "pareto@1.0.0",
          "timing_actions@1.0.0",
          "weight_sensitivity@1.0.0",
          "c028_interval_feasibility@1.0.0",
          "C029@1.0.0"
        ]
      }
    },
    {
      "q": "只想判断方案是否违反底线，暂不比较现在行动和等待",
      "want": [
        "c028_interval_feasibility@1.0.0"
      ],
      "results": {
        "exact": [],
        "body": [
          "timing_actions@1.0.0",
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0"
        ],
        "goal": [
          "c028_interval_feasibility@1.0.0",
          "timing_actions@1.0.0",
          "weight_sensitivity@1.0.0",
          "pareto@1.0.0",
          "C029@1.0.0"
        ],
        "clauseFusion": [
          "c028_interval_feasibility@1.0.0",
          "pareto@1.0.0",
          "timing_actions@1.0.0",
          "weight_sensitivity@1.0.0",
          "C029@1.0.0"
        ]
      }
    },
    {
      "q": "不要保存这段对话，也不要用于训练",
      "want": [],
      "results": {
        "exact": [],
        "body": [
          "timing_actions@1.0.0"
        ],
        "goal": [],
        "clauseFusion": [
          "timing_actions@1.0.0"
        ]
      }
    },
    {
      "q": "苹果的英文怎么拼",
      "want": [],
      "results": {
        "exact": [],
        "body": [
          "timing_actions@1.0.0"
        ],
        "goal": [],
        "clauseFusion": [
          "timing_actions@1.0.0"
        ]
      }
    },
    {
      "q": "帮我写一封请假邮件",
      "want": [],
      "results": {
        "exact": [],
        "body": [],
        "goal": [],
        "clauseFusion": []
      }
    },
    {
      "q": "我想理解统计推断",
      "want": [],
      "results": {
        "exact": [],
        "body": [
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0"
        ],
        "goal": [],
        "clauseFusion": [
          "pareto@1.0.0",
          "weight_sensitivity@1.0.0"
        ]
      }
    }
  ],
  "unlabelledReturns": {
    "exact": 0,
    "body": 24,
    "goal": 5,
    "clauseFusion": 24
  },
  "checks": 279
}
```
## 接入边界
保留原文锚与候选检索来源，必须经过独立语义义务、当前主体/条件/否定、参数和版本资格确认才能调用数学；不能把多方法共享档案或排名并列当作互换方法。原生exact策略保持不动，研究候选不得覆盖其保守行为。未修改生产、交接、冻结、证据等级、PR、训练、部署、主动CI或费用。
## 复算
固定12份文件按上列顺序读入，标准JS核心实际执行；Node文件包装未运行。
```js
const inputs=[["research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json","be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb","cb188c0c3011b958277d88c2155276c45e228cee"],["research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json","05c239f3f3b1f46235fa2464d2945c21c6c08132","cb188c0c3011b958277d88c2155276c45e228cee"],["research/decision_hub/2026-11-24-method-corpus-index/corpus_index.json","6862d5a2cd3c7eb3f2da9a85d79c8b3386f2a102","cb188c0c3011b958277d88c2155276c45e228cee"],["platform/future_model/src/psychohistory/decision_knowledge_planning.py","d32854c4909df858ee851634747234ed5dec657b","734686980b19da9291bdd08b67d4e2519c011acf"],["research/decision_methods/C028_INTERVAL_HARD_CONSTRAINT_FEASIBILITY_2026-11-20.md","7cb8d5e3631dd17c0650cec06139d88b5bfcc700","cb188c0c3011b958277d88c2155276c45e228cee"],["research/decision_methods/C004_DYNAMIC_UTILITY_MULTI_OBJECTIVE_ROBUST_2026-10-27.md","0d04c633a26437ad6017946cd528c4dc68db3d83","cb188c0c3011b958277d88c2155276c45e228cee"],["research/decision_methods/C029_SCENARIO_MINIMAX_REGRET_INFORMATION_BOUNDARY_2026-11-20.md","a2588cfdd47e547a46a7ee8cde2644caf81198d9","cb188c0c3011b958277d88c2155276c45e228cee"],["research/decision_methods/C009_OPTION_VALUE_INFORMATION_REVERSIBILITY_2026-11-01.md","5048081b0a277f4bc511aff2293020268fd5c57c","cb188c0c3011b958277d88c2155276c45e228cee"],["research/decision_methods/BUEHLER_GRIFFIN_ROSS_1994_PERSONAL_COMPLETION_TIME_FORECAST_BOUNDARY_2026-11-21.md","e7e1002f00aab5bf782a5f2845fbfac2cb80969b","cb188c0c3011b958277d88c2155276c45e228cee"],["research/decision_methods/VOI_DELAY_DEADLINE_OPPORTUNITY_COST_2026-11-21.md","c5214371527e058eec64049522b605150d7c496d","cb188c0c3011b958277d88c2155276c45e228cee"],["research/decision_methods/C030_INTERVAL_BOUNDED_SCENARIO_REGRET_2026-11-20.md","57301fb2a1dbda8e99510b44d6fcfb2e5f4a191e","cb188c0c3011b958277d88c2155276c45e228cee"],["research/decision_methods/VOI_IMPERFECT_BINARY_SIGNAL_METHOD_CARD_2026-11-20.md","bd494e2e1200a526dcb11d454e423ff9aebccd33","cb188c0c3011b958277d88c2155276c45e228cee"]];
const contents=process.argv.slice(2).map(p=>require("node:fs").readFileSync(p,"utf8"));
function experiment(contents,inputs){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),index=JSON.parse(contents[2]);
 const goals=Object.fromEntries([...contents[3].split("GOALS = {")[1].split("\n}")[0].matchAll(/"([^"]+)": "([^"]+)"/g)].map(m=>[m[2],m[1]]));
 const keys=Object.keys(goals);ck(keys.length===5,"goal contract");
 const docs=inputs.slice(4).map((x,i)=>({path:x[0],body:contents[i+4],linked:index.methods.filter(m=>m.sources.some(s=>s.path===x[0])).map(m=>m.key).filter(k=>keys.includes(k))}));
 function tokens(s){return [...s.normalize("NFKC").toLowerCase().matchAll(/[a-z]+[0-9]*|[\u3400-\u9fff]+/g)].flatMap(m=>/^[a-z]/.test(m[0])?(m[0].length>1?[m[0]]:[]):Array.from({length:m[0].length-1},(_,i)=>m[0].slice(i,i+2)))}
 function bm(rows){
  const freqs=rows.map(s=>{let m=new Map();for(let t of tokens(s))m.set(t,(m.get(t)||0)+1);return m}),lengths=rows.map(s=>tokens(s).length),avg=lengths.reduce((s,n)=>s+n,0)/rows.length||1;
  const df=new Map();for(let f of freqs)for(let t of f.keys())df.set(t,(df.get(t)||0)+1);
  return q=>freqs.map((f,i)=>[...new Set(tokens(q))].reduce((s,t)=>{let n=f.get(t)||0;return s+(n?Math.log(1+(rows.length-(df.get(t)||0)+.5)/((df.get(t)||0)+.5))*n*2.2/(n+1.2*(.25+.75*lengths[i]/avg)):0)},0));
 }
 const body=bm(docs.map(d=>d.body)),goal=bm(keys.map(k=>goals[k]));
 const order=(score)=>keys.map((key,i)=>({key,score:score[i]})).filter(x=>x.score>0).sort((a,b)=>b.score-a.score||a.key.localeCompare(b.key));
 function docScore(q){let v=body(q);return keys.map(k=>Math.max(0,...docs.map((d,i)=>d.linked.includes(k)?v[i]:0)))}
 function clauses(q){return q.split(/[。！？!?；;，,\n]+/u).map(s=>s.trim()).filter(Boolean)}
 function exact(q){return [...new Set(q.normalize("NFKC").split(/[。;!?\n]+/).map(s=>s.trim()).flatMap(s=>keys.filter(k=>goals[k]===s)))].sort()}
 function scores(q,mode){
  if(mode==="body")return docScore(q);
  if(mode==="goal")return goal(q);
  // Rank fusion uses only positive tied ranks. Shared document can give tied
  // evidence to several methods; no arbitrary single winner is authorized.
  const s=keys.map(()=>0);
  for(let clause of clauses(q))for(let a of [docScore(clause),goal(clause)]){
   let pos=a.filter(n=>n>0).sort((x,y)=>y-x);
   for(let i=0;i<a.length;i++)if(a[i]>0)s[i]=Math.max(s[i],1/(1+pos.filter(n=>n>a[i]).length));
  }return s;
 }
 // Method relevance labels for the existing public development turns are
 // assigned at EPISODE level only for plausible discovery directions, not
 // ground truth intent. Excluded episodes have no evaluation target.
 const K=keys,hard=K[0],pareto=K[1],weight=K[2],regret=K[3],timing=K[4];
 const targets={L01:[hard],L02:[hard],L04:[hard],L05:[hard],L08:[regret],L11:[hard],L12:[hard],L14:[hard],L15:[hard,pareto],L16:[hard],S01:[pareto],S02:[hard],S04:[hard],S07:[pareto],S09:[hard,timing],S10:[hard],S13:[hard,pareto],S14:[timing]};
 const controls=[
 [goals[hard],[hard]],[goals[pareto],[pareto]],[goals[weight],[weight]],[goals[regret],[regret]],[goals[timing],[timing]],
 ["两个方案有没有踩到我的最低要求？",[hard]],["每个方面分别哪个选项更占优势？",[pareto]],["如果我更看重时间，原来的排序会变吗？",[weight]],["情况变糟以后哪种选法的后悔最小？",[regret]],["先做还是多等一阵再做比较合适？",[timing]],
 ["判断方案是否违反底线。比较现在行动和等待",[hard,timing]],["比较各目标的优势。判断权重改变是否影响选择",[pareto,weight]],
 ["不要"+goals[hard],[]],["他说“"+goals[pareto]+"”，我只是转述。",[]],["暂时不想"+goals[weight],[]],["如果以后需要"+goals[regret]+"再说。",[]],["我没让你"+goals[timing],[]],
 ["比较各目标的优势，不要判断权重改变是否影响选择",[pareto]],["只想判断方案是否违反底线，暂不比较现在行动和等待",[hard]],
 ["不要保存这段对话，也不要用于训练",[]],["苹果的英文怎么拼",[]],["帮我写一封请假邮件",[]],["我想理解统计推断",[]]
 ];
 const modes=["exact","body","goal","clauseFusion"],stat=()=>({queries:0,targets:0,hit1:0,hit3:0,recall3:0,all3:0,empty:0,tiesAt1:0,negativeReturns:0,totalReturned:0});
 const out={docs:docs.length,methods:keys,realSharedSourceGroups:[],development:{raw:{},context:{}},controls:{},controlRows:[],unlabelledReturns:{},checks:0};
 for(let m of modes){out.development.raw[m]=stat();out.development.context[m]=stat();out.controls[m]=stat();out.unlabelledReturns[m]=0}
 function candidates(q,m){if(m==="exact")return exact(q).map(key=>({key,score:1}));return order(scores(q,m))}
 function measure(row,want,s){let top=row.slice(0,3).map(r=>r.key);s.queries++;s.targets+=want.length;s.hit1+=+(want.length>0&&want.includes(row[0]?.key));s.hit3+=+(want.length>0&&want.some(k=>top.includes(k)));s.recall3+=want.filter(k=>top.includes(k)).length;s.all3+=+(want.length>0&&want.every(k=>top.includes(k)));s.empty+=+!row.length;s.tiesAt1+=+(row.length>1&&row[0].score===row[1].score);s.negativeReturns+=+(!want.length&&row.length>0);s.totalReturned+=row.length}
 for(let d of docs)if(d.linked.length>1)out.realSharedSourceGroups.push({path:d.path,methods:d.linked});
 for(let c of [...JSON.parse(contents[0]).cases,...JSON.parse(contents[1]).cases]){
  for(let [i,t] of c.turns.entries()){
   for(let m of modes){
    let raw=candidates(t.text,m),ctx=candidates(c.turns.slice(0,i+1).map(t=>t.text).join("。"),m);
    ck(raw.every(r=>keys.includes(r.key))&&ctx.every(r=>keys.includes(r.key)),"registered discovery only");
    if(targets[c.id]){measure(raw,targets[c.id],out.development.raw[m]);measure(ctx,targets[c.id],out.development.context[m])}else out.unlabelledReturns[m]+=+(raw.length>0);
    out.checks++;
   }
  }
 }
 for(let [q,want] of controls){
  let row={q,want,results:{}};
  for(let m of modes){let r=candidates(q,m);measure(r,want,out.controls[m]);row.results[m]=r.map(x=>x.key)}
  out.controlRows.push(row);
 }
 // Source-only scores cannot separate methods whose observed source sets coincide.
 for(let i=0;i<keys.length;i++)for(let j=i+1;j<keys.length;j++){
  let a=docs.filter(d=>d.linked.includes(keys[i])).map(d=>d.path),b=docs.filter(d=>d.linked.includes(keys[j])).map(d=>d.path);
  if(eq(a,b))for(let [q] of controls){let s=docScore(q);ck(s[i]===s[j],"identical source sets imply identical relevance");out.checks++}
 }
 return out;
}
console.log(JSON.stringify(experiment(contents,inputs),null,2));
```
