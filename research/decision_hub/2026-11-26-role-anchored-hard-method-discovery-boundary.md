# 自主认知与科学方法：原文角色锚定的硬约束方法发现与权限边界
2026-11-26。RESEARCH_CANDIDATE / PREDECESSOR_CODE_EXECUTED / PUBLIC_SYNTHETIC_DEVELOPMENT / POST_INSPECTION_DIAGNOSTIC / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NO_TRAINING。
## 基线
起点main afb9e5a5ef9d1a9b129c514d157f1114ed00deab；沿用本轮已查询的25近期提交、15开放PR、v3.2及同步规程，#63固定head 734686980b19da9291bdd08b67d4e2519c011acf仍Draft，唯一交接实际路径尝试404未确认最新版本。前阶段共享档案歧义与低白话检索覆盖；旧角色候选研究已有67/67完整粗角色覆盖（非准确率），此轮不重新发明原文角色生成、调整词面或以重复测试抬高证据。新增连接实际原文约束候选与C028方法发现，检查权限、流程、撤回等约束和现实方案硬底线被混为同一种方法的风险，并与固定上一轮检索控制对照。局部查重有限。
固定输入（均research/decision_hub/下，按此顺序读取）：
2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
2026-11-25-bounded-semantic-candidate-search.md bbdc12dfe65b24aa24e6b1d25a04955766cadab4
2026-11-25-raw-text-reference-search.md 16075b3ba567ee6dc3496300beab1417172a6c42
2026-11-25-raw-field-candidate-coverage-and-numerals.md 07dcbda9532dbc3b330abfd79a399cb52aa91aeb
2026-11-25-temporal-quantity-candidate-separation.md 8a6b42f83b80283db6e215fe48f4fb2efbf8368c
2026-11-26-compositional-role-candidate-recovery.md b0bea7b4c101c170be2aaa2355973739b125e0b7
2026-11-26-clock-event-and-open-role-projection.md ef103587b216ad07c1a47102ddb7cb8d2975283d
2026-11-26-clause-level-method-discovery-and-shared-source-ambiguity.md a1e5cc2f80e61e9cb3c6322a52931f11c175d093
全部9个固定资产实际读取，核对连接器blob。调用旧研究propose源码及原依赖，原文及是否前轮作为唯一生成输入，不输入评估标签。未重审外部文献或训练，非真实用户或独立留出。
## 方法及边界
对每轮原文复用已审阅clock-event-and-open-role-projection中propose，保持原排序及全部约束跨度，不增加新正则。取每角色预算1/5/10/20/50/完整。若存在任一约束候选，只生成C028方法发现线索、原文锚、DISCOVERY_ONLY、authority NONE/outside true；无候选不证明无底线。该极简方法故意不处理适用范围，用于测直接从粗角色通往方法发现会产生的候选过载。不能注入原生精确目标字符串作为用户确认，不能调用C028，不能改写用户义务。实际方法准入必须另确认角色、主体、方向、条件、数值口径、来源、用途及是否为现实方案约束；隐私、授权、流程和用户行为边界独立保护，不能交给数学比较替代。
L评估取已有HARD/CONDITIONAL_HARD/HARD_CONSEQUENCE（排除保存/训练/原文留存），CONFIRM/REVISION暂不视为新义务，因为实际历史需另行核对；S手工选定七个含现实方案约束的轮次（含S13条件范围修订，仅作发现线索），其他流程、隐私、偏好设置、撤回与未标注轮次不作为正目标。非目标轮可能仍有相关方法需求，非空计数不等同真实假阳性。精确锚和重叠锚分别统计，后者不意味着准确解析。上一轮23条人工控制直接复用原目标及检索输出，不调词面。全部为已见合成开发材料，研究者选定评价范围和预算，不能推断真实语义能力或用户认知负担。标准JS核心实际执行两次一致。
```json
{
  "budgets": {
    "1": {
      "turns": 64,
      "positiveTurns": 20,
      "otherTurns": 44,
      "positiveReturned": 18,
      "otherReturned": 16,
      "targetAnchors": 21,
      "exactTargets": 8,
      "overlapTargets": 12,
      "candidateAnchors": 34,
      "privacyOrProcessReturns": 7
    },
    "5": {
      "turns": 64,
      "positiveTurns": 20,
      "otherTurns": 44,
      "positiveReturned": 18,
      "otherReturned": 16,
      "targetAnchors": 21,
      "exactTargets": 16,
      "overlapTargets": 18,
      "candidateAnchors": 164,
      "privacyOrProcessReturns": 7
    },
    "10": {
      "turns": 64,
      "positiveTurns": 20,
      "otherTurns": 44,
      "positiveReturned": 18,
      "otherReturned": 16,
      "targetAnchors": 21,
      "exactTargets": 18,
      "overlapTargets": 19,
      "candidateAnchors": 316,
      "privacyOrProcessReturns": 7
    },
    "20": {
      "turns": 64,
      "positiveTurns": 20,
      "otherTurns": 44,
      "positiveReturned": 18,
      "otherReturned": 16,
      "targetAnchors": 21,
      "exactTargets": 19,
      "overlapTargets": 19,
      "candidateAnchors": 571,
      "privacyOrProcessReturns": 7
    },
    "50": {
      "turns": 64,
      "positiveTurns": 20,
      "otherTurns": 44,
      "positiveReturned": 18,
      "otherReturned": 16,
      "targetAnchors": 21,
      "exactTargets": 19,
      "overlapTargets": 19,
      "candidateAnchors": 1252,
      "privacyOrProcessReturns": 7
    },
    "Infinity": {
      "turns": 64,
      "positiveTurns": 20,
      "otherTurns": 44,
      "positiveReturned": 18,
      "otherReturned": 16,
      "targetAnchors": 21,
      "exactTargets": 19,
      "overlapTargets": 19,
      "candidateAnchors": 2907,
      "privacyOrProcessReturns": 7
    }
  },
  "turns": 64,
  "targetCount": 21,
  "positiveTurns": 20,
  "otherTurns": 44,
  "privacyOrProcessTurns": 7,
  "rows": [
    {
      "id": "L01.0",
      "target": [
        "房租加停车每月最多四千"
      ],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "20",
          "pool": 20,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "50",
          "pool": 50,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "Infinity",
          "pool": 128,
          "exact": 1,
          "overlap": 1
        }
      ]
    },
    {
      "id": "L01.1",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "L02.0",
      "target": [
        "只要夜班我就不去"
      ],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 0,
          "overlap": 1
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "20",
          "pool": 20,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "50",
          "pool": 50,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "Infinity",
          "pool": 158,
          "exact": 1,
          "overlap": 1
        }
      ]
    },
    {
      "id": "L02.1",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 20,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 50,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 162,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "L03.0",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 6,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 6,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 6,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 6,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "L03.1",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "L04.0",
      "target": [
        "下周五必须交"
      ],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "20",
          "pool": 20,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "50",
          "pool": 50,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "Infinity",
          "pool": 69,
          "exact": 1,
          "overlap": 1
        }
      ]
    },
    {
      "id": "L04.1",
      "target": [
        "延期会失去报名资格"
      ],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "L05.0",
      "target": [
        "只有十天假"
      ],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 0,
          "overlap": 1
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 0,
          "overlap": 1
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "20",
          "pool": 20,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "50",
          "pool": 20,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "Infinity",
          "pool": 20,
          "exact": 1,
          "overlap": 1
        }
      ]
    },
    {
      "id": "L05.1",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 20,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 50,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 182,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "L06.0",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "L06.1",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "L07.0",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "L07.1",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "L08.0",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "L08.1",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "L09.0",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "L09.1",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 3,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 3,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 3,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 3,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 3,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "L10.0",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 20,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 42,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 42,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "L10.1",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "L11.0",
      "target": [
        "九点前到"
      ],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "20",
          "pool": 20,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "50",
          "pool": 50,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "Infinity",
          "pool": 73,
          "exact": 1,
          "overlap": 1
        }
      ]
    },
    {
      "id": "L11.1",
      "target": [
        "最早八点"
      ],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "5",
          "pool": 1,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "10",
          "pool": 1,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "20",
          "pool": 1,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "50",
          "pool": 1,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "Infinity",
          "pool": 1,
          "exact": 1,
          "overlap": 1
        }
      ]
    },
    {
      "id": "L12.0",
      "target": [
        "两项加起来只能十万",
        "不能借钱"
      ],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 2,
          "overlap": 2
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 2,
          "overlap": 2
        },
        {
          "k": "20",
          "pool": 20,
          "exact": 2,
          "overlap": 2
        },
        {
          "k": "50",
          "pool": 50,
          "exact": 2,
          "overlap": 2
        },
        {
          "k": "Infinity",
          "pool": 75,
          "exact": 2,
          "overlap": 2
        }
      ]
    },
    {
      "id": "L12.1",
      "target": [
        "不能挪到以后"
      ],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "20",
          "pool": 20,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "50",
          "pool": 50,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "Infinity",
          "pool": 122,
          "exact": 1,
          "overlap": 1
        }
      ]
    },
    {
      "id": "L13.0",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 10,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 10,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 10,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "L13.1",
      "target": [
        "如果再有人身威胁我就不联系"
      ],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 0,
          "overlap": 1
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 0,
          "overlap": 1
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 0,
          "overlap": 1
        },
        {
          "k": "20",
          "pool": 20,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "50",
          "pool": 50,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "Infinity",
          "pool": 110,
          "exact": 1,
          "overlap": 1
        }
      ]
    },
    {
      "id": "L14.0",
      "target": [
        "不发就撑不住"
      ],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "L14.1",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "L15.0",
      "target": [
        "四周最多十小时"
      ],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "20",
          "pool": 20,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "50",
          "pool": 50,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "Infinity",
          "pool": 100,
          "exact": 1,
          "overlap": 1
        }
      ]
    },
    {
      "id": "L15.1",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 20,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 50,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 69,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "L16.0",
      "target": [
        "只要有明显安全风险我就换路"
      ],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "20",
          "pool": 20,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "50",
          "pool": 50,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "Infinity",
          "pool": 219,
          "exact": 1,
          "overlap": 1
        }
      ]
    },
    {
      "id": "L16.1",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "L17.0",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 20,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 33,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 33,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "L17.1",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 12,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 12,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 12,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "L18.0",
      "target": [],
      "process": true,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 20,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 50,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 83,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "L18.1",
      "target": [],
      "process": true,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 6,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 6,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 6,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 6,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "S01.0",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "S01.1",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "S02.0",
      "target": [
        "必须离车站步行十五分钟以内"
      ],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 0,
          "overlap": 1
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "20",
          "pool": 20,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "50",
          "pool": 50,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "Infinity",
          "pool": 276,
          "exact": 1,
          "overlap": 1
        }
      ]
    },
    {
      "id": "S02.1",
      "target": [
        "步行上限改为十二分钟"
      ],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "20",
          "pool": 20,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "50",
          "pool": 50,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "Infinity",
          "pool": 73,
          "exact": 1,
          "overlap": 1
        }
      ]
    },
    {
      "id": "S03.0",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "S03.1",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "S04.0",
      "target": [
        "我们两个人都得能用厨房"
      ],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "20",
          "pool": 20,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "50",
          "pool": 50,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "Infinity",
          "pool": 53,
          "exact": 1,
          "overlap": 1
        }
      ]
    },
    {
      "id": "S04.1",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "S05.0",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "S05.1",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "S06.0",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "S06.1",
      "target": [],
      "process": true,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 10,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 10,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 10,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "S07.0",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "S07.1",
      "target": [],
      "process": true,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 10,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 10,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 10,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "S08.0",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "S08.1",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "S09.0",
      "target": [
        "必须赶上周日晚的集合"
      ],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "20",
          "pool": 20,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "50",
          "pool": 50,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "Infinity",
          "pool": 173,
          "exact": 1,
          "overlap": 1
        }
      ]
    },
    {
      "id": "S09.1",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "S10.0",
      "target": [
        "每周至少保留半天"
      ],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "20",
          "pool": 20,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "50",
          "pool": 50,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "Infinity",
          "pool": 127,
          "exact": 1,
          "overlap": 1
        }
      ]
    },
    {
      "id": "S10.1",
      "target": [],
      "process": true,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 20,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 50,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 92,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "S11.0",
      "target": [],
      "process": true,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 13,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 13,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 13,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "S11.1",
      "target": [],
      "process": true,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 20,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 36,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 36,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "S12.0",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "S12.1",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "S13.0",
      "target": [
        "准确率必须不低于九成"
      ],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "20",
          "pool": 20,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "50",
          "pool": 50,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "Infinity",
          "pool": 142,
          "exact": 1,
          "overlap": 1
        }
      ]
    },
    {
      "id": "S13.1",
      "target": [
        "准确率的要求仅用于正式交付"
      ],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 1,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 5,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "10",
          "pool": 10,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "20",
          "pool": 20,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "50",
          "pool": 50,
          "exact": 1,
          "overlap": 1
        },
        {
          "k": "Infinity",
          "pool": 219,
          "exact": 1,
          "overlap": 1
        }
      ]
    },
    {
      "id": "S14.0",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    },
    {
      "id": "S14.1",
      "target": [],
      "process": false,
      "ranks": [
        {
          "k": "1",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "5",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "10",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "20",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "50",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        },
        {
          "k": "Infinity",
          "pool": 0,
          "exact": 0,
          "overlap": 0
        }
      ]
    }
  ],
  "controls": [
    {
      "i": 0,
      "q": "判断方案是否违反底线",
      "expectedDiscovery": true,
      "rawAnchorCount": 55,
      "top1": "判断方案是否违反底线",
      "sourceRetrieval": false,
      "exact": true,
      "authority": "NONE"
    },
    {
      "i": 1,
      "q": "比较各目标的优势",
      "expectedDiscovery": false,
      "rawAnchorCount": 0,
      "top1": null,
      "sourceRetrieval": false,
      "exact": false,
      "authority": "NONE"
    },
    {
      "i": 2,
      "q": "判断权重改变是否影响选择",
      "expectedDiscovery": false,
      "rawAnchorCount": 0,
      "top1": null,
      "sourceRetrieval": false,
      "exact": false,
      "authority": "NONE"
    },
    {
      "i": 3,
      "q": "比较最坏情景的后悔值",
      "expectedDiscovery": false,
      "rawAnchorCount": 0,
      "top1": null,
      "sourceRetrieval": false,
      "exact": false,
      "authority": "NONE"
    },
    {
      "i": 4,
      "q": "比较现在行动和等待",
      "expectedDiscovery": false,
      "rawAnchorCount": 0,
      "top1": null,
      "sourceRetrieval": false,
      "exact": false,
      "authority": "NONE"
    },
    {
      "i": 5,
      "q": "两个方案有没有踩到我的最低要求？",
      "expectedDiscovery": true,
      "rawAnchorCount": 120,
      "top1": "两个方案有没有踩到我的最低要求",
      "sourceRetrieval": false,
      "exact": false,
      "authority": "NONE"
    },
    {
      "i": 6,
      "q": "每个方面分别哪个选项更占优势？",
      "expectedDiscovery": false,
      "rawAnchorCount": 54,
      "top1": "每个方面分别哪个选项更占优势",
      "sourceRetrieval": false,
      "exact": false,
      "authority": "NONE"
    },
    {
      "i": 7,
      "q": "如果我更看重时间，原来的排序会变吗？",
      "expectedDiscovery": false,
      "rawAnchorCount": 0,
      "top1": null,
      "sourceRetrieval": false,
      "exact": false,
      "authority": "NONE"
    },
    {
      "i": 8,
      "q": "情况变糟以后哪种选法的后悔最小？",
      "expectedDiscovery": false,
      "rawAnchorCount": 0,
      "top1": null,
      "sourceRetrieval": false,
      "exact": false,
      "authority": "NONE"
    },
    {
      "i": 9,
      "q": "先做还是多等一阵再做比较合适？",
      "expectedDiscovery": false,
      "rawAnchorCount": 0,
      "top1": null,
      "sourceRetrieval": false,
      "exact": false,
      "authority": "NONE"
    },
    {
      "i": 10,
      "q": "判断方案是否违反底线。比较现在行动和等待",
      "expectedDiscovery": true,
      "rawAnchorCount": 136,
      "top1": "判断方案是否违反底线",
      "sourceRetrieval": false,
      "exact": true,
      "authority": "NONE"
    },
    {
      "i": 11,
      "q": "比较各目标的优势。判断权重改变是否影响选择",
      "expectedDiscovery": false,
      "rawAnchorCount": 0,
      "top1": null,
      "sourceRetrieval": false,
      "exact": false,
      "authority": "NONE"
    },
    {
      "i": 12,
      "q": "不要判断方案是否违反底线",
      "expectedDiscovery": false,
      "rawAnchorCount": 78,
      "top1": "不要判断方案是否违反底线",
      "sourceRetrieval": false,
      "exact": false,
      "authority": "NONE"
    },
    {
      "i": 13,
      "q": "他说“比较各目标的优势”，我只是转述。",
      "expectedDiscovery": false,
      "rawAnchorCount": 0,
      "top1": null,
      "sourceRetrieval": false,
      "exact": false,
      "authority": "NONE"
    },
    {
      "i": 14,
      "q": "暂时不想判断权重改变是否影响选择",
      "expectedDiscovery": false,
      "rawAnchorCount": 0,
      "top1": null,
      "sourceRetrieval": false,
      "exact": false,
      "authority": "NONE"
    },
    {
      "i": 15,
      "q": "如果以后需要比较最坏情景的后悔值再说。",
      "expectedDiscovery": false,
      "rawAnchorCount": 0,
      "top1": null,
      "sourceRetrieval": false,
      "exact": false,
      "authority": "NONE"
    },
    {
      "i": 16,
      "q": "我没让你比较现在行动和等待",
      "expectedDiscovery": false,
      "rawAnchorCount": 0,
      "top1": null,
      "sourceRetrieval": false,
      "exact": false,
      "authority": "NONE"
    },
    {
      "i": 17,
      "q": "比较各目标的优势，不要判断权重改变是否影响选择",
      "expectedDiscovery": false,
      "rawAnchorCount": 13,
      "top1": "不要判断权重改变是否影响选择",
      "sourceRetrieval": false,
      "exact": false,
      "authority": "NONE"
    },
    {
      "i": 18,
      "q": "只想判断方案是否违反底线，暂不比较现在行动和等待",
      "expectedDiscovery": true,
      "rawAnchorCount": 199,
      "top1": "只想判断方案是否违反底线",
      "sourceRetrieval": false,
      "exact": false,
      "authority": "NONE"
    },
    {
      "i": 19,
      "q": "不要保存这段对话，也不要用于训练",
      "expectedDiscovery": false,
      "rawAnchorCount": 17,
      "top1": "不要保存这段对话",
      "sourceRetrieval": false,
      "exact": false,
      "authority": "NONE"
    },
    {
      "i": 20,
      "q": "苹果的英文怎么拼",
      "expectedDiscovery": false,
      "rawAnchorCount": 0,
      "top1": null,
      "sourceRetrieval": false,
      "exact": false,
      "authority": "NONE"
    },
    {
      "i": 21,
      "q": "帮我写一封请假邮件",
      "expectedDiscovery": false,
      "rawAnchorCount": 0,
      "top1": null,
      "sourceRetrieval": false,
      "exact": false,
      "authority": "NONE"
    },
    {
      "i": 22,
      "q": "我想理解统计推断",
      "expectedDiscovery": false,
      "rawAnchorCount": 0,
      "top1": null,
      "sourceRetrieval": false,
      "exact": false,
      "authority": "NONE"
    }
  ],
  "checks": 384
}
```
## 后续
粗约束候选到方法线索只能作为检索扩展。必须建立来源绑定的语义角色与义务类型核验，再用结构化适用条件选择方法；尤其约束撤回与授权不能机械路由数学。应停止继续在同一64轮调词面，保留外部开发与独立未见验收。未修改生产、唯一交接、冻结、证据等级、PR、训练、部署、主动CI或费用；真实原生、独立留出及真机未运行。
## 复算
9份固定文件依序传入，Node包装未运行，标准JS核心实际执行。
```js
const contents=process.argv.slice(2).map(p=>require("node:fs").readFileSync(p,"utf8"));
function experiment(contents){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const code=contents[7].split("```js\n")[1].split("\n```")[0];
 const propose=Function("contents",code.split(" const out={episodes:")[0]+"\nreturn propose;\n}\nreturn experiment(contents);")(contents.slice(0,7));
 // This is a bounded diagnostic of method DISCOVERY, never a native goal
 // confirmation. Labels below are only for evaluation, not input to propose.
 const selectedL=new Set(["HARD","CONDITIONAL_HARD","HARD_CONSEQUENCE"]);
 const excludedFields=new Set(["persistence","training","raw_text_retention"]);
 const selectedS=new Set(["S02.0","S02.1","S04.0","S09.0","S10.0","S13.0","S13.1"]);
 const budgets=[1,5,10,20,50,Infinity],stat=()=>({turns:0,positiveTurns:0,otherTurns:0,positiveReturned:0,otherReturned:0,targetAnchors:0,exactTargets:0,overlapTargets:0,candidateAnchors:0,privacyOrProcessReturns:0});
 const out={budgets:{},turns:0,targetCount:0,positiveTurns:0,otherTurns:0,privacyOrProcessTurns:0,rows:[],controls:[],checks:0};
 for(let k of budgets)out.budgets[String(k)]=stat();
 function test(t,prior,target,process,id){
  const z=propose(t,prior),all=z.all.constraint;
  ck(z.authority==="NONE"&&z.outside===true,"candidate-only");
  ck(all.every(a=>a.start>=0&&a.end<=t.length&&t.slice(a.start,a.end)===a.text),"anchor");
  const spans=target.flatMap(s=>{let i=t.indexOf(s);ck(i>=0,"reference literal");return [{start:i,end:i+s.length,text:s}]});
  out.turns++;out.targetCount+=spans.length;out.positiveTurns+=+!!spans.length;out.otherTurns+=+!spans.length;out.privacyOrProcessTurns+=+process;
  let row={id,target:target.slice(),process,ranks:[]};
  for(let k of budgets){
   let pool=all.slice(0,k),s=out.budgets[String(k)];
   let exact=spans.filter(x=>pool.some(y=>x.start===y.start&&x.end===y.end)).length;
   let overlap=spans.filter(x=>pool.some(y=>x.start<y.end&&y.start<x.end)).length;
   // Do not fill a missing method goal with a confirmed user intent.
   let method=pool.length?{method:"c028_interval_feasibility@1.0.0",status:"DISCOVERY_ONLY",authority:"NONE",outside:true,anchors:pool.map(y=>[y.start,y.end])}:null;
   ck(!method||method.authority==="NONE"&&method.outside===true&&method.status==="DISCOVERY_ONLY","authority");
   s.turns++;s.positiveTurns+=+!!spans.length;s.otherTurns+=+!spans.length;s.positiveReturned+=+(!!spans.length&&!!method);s.otherReturned+=+(!spans.length&&!!method);s.targetAnchors+=spans.length;s.exactTargets+=exact;s.overlapTargets+=overlap;s.candidateAnchors+=pool.length;s.privacyOrProcessReturns+=+(process&&!!method);
   row.ranks.push({k:String(k),pool:pool.length,exact,overlap});out.checks++;
  }
  out.rows.push(row);
 }
 const L=JSON.parse(contents[0]),S=JSON.parse(contents[1]);
 for(let c of L.cases)for(let [i,t] of c.turns.entries()){
  let target=t.claims.filter(x=>selectedL.has(x.kind)&&!excludedFields.has(x.field)).map(x=>x.span);
  // CONFIRM and REVISION deliberately not promoted: current obligation is
  // resolved by a separate ledger, which this raw-turn diagnostic does not have.
  const process=c.id==="L18";
  test(t.text,i>0,target,process,c.id+"."+i);
 }
 for(let c of S.cases)for(let [i,t] of c.turns.entries()){
  const id=c.id+"."+i,target=selectedS.has(id)?t.proposal.claims.filter(x=>x.role==="constraint"&&x.op!=="retract").map(x=>x.quote):[];
  test(t.text,i>0,target,c.id==="S11"||id==="S06.1"||id==="S07.1"||id==="S10.1",id);
 }
 const priorResult=JSON.parse(contents[8].split("```json\n")[1].split("\n```")[0]);
 const controlRows=priorResult.controlRows;
 for(let [i,c] of controlRows.entries()){
  let z=propose(c.q,false),pool=z.all.constraint;
  out.controls.push({i,q:c.q,expectedDiscovery:c.want.includes("c028_interval_feasibility@1.0.0"),rawAnchorCount:pool.length,top1:pool[0]?.text??null,sourceRetrieval:c.results.body.includes("c028_interval_feasibility@1.0.0"),exact:c.results.exact.includes("c028_interval_feasibility@1.0.0"),authority:"NONE"});
 }
 ck(out.turns===64&&out.checks===384,"cohort");
 for(let i=1;i<budgets.length;i++){let a=out.budgets[String(budgets[i-1])],b=out.budgets[String(budgets[i])];ck(a.exactTargets<=b.exactTargets&&a.otherReturned<=b.otherReturned,"nested");}
 return out;
}
console.log(JSON.stringify(experiment(contents),null,2));
```
