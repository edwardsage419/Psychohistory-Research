# 第50轮：智能决策中枢完整研究整合及研发条件复审
2026-11-24。基准main d209adb337a9f52a98bd590a06a3804d12bff613，PR #61 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e open Draft, 未合并。继承第34轮完整候选规格 4b3205e91e627819782e2d1fda50f2de16f0e608 及其12项范围，不缩减、不拆分、不授权开发。已核对v3.1、AGENTS、同步规程、近期提交、开放PR及唯一产品交接（blob 5e74f4f0b37141d631740e844ad8bbbfed232e07）。本轮对49项研究入口做身份和依赖索引核查，不重复执行49轮实验，不将研究覆盖视为产品完成率。
## 证据核对
第34轮固定manifest blob 58163b4cd93b4b6cbd7212d599283ae8133a105a 中33项入口与4项勘误，使用第34轮提交到当前main的compare（19项变更，未见原路径变更）继承已核身份；未逐一重读33份历史原文件。第34至49轮16项入口分批实际读取最新固定文件，14项与此前固定blob比较，35/43轮另读原提交核对身份，全部匹配。首次整合脚本超过单次工具调用限制停止，未写入；分批读取后完成。第39/40轮外部来源核查历史工具记录不充分，本轮未重验出版商摘要，保留数学研究及原始文档，不追认文献审阅。完整索引如下。本轮仅验证清单及状态规则，12项突变全部拒绝；同一研究者定义检查，非独立科学验收。第50轮为整合工件，49个前序入口加本轮共50轮，不把第50轮自指加入清单。
## v0.6基线状态
两次查询mergeable先false后true，不把该瞬时状态当正式可合并证明。compare以PR head为base、main为head，返回diverged，main ahead 54、behind 5，文件169，main侧平台源码路径变更0。尚未执行真实合并或三方冲突测试。#59/#60仍待审且已被#61复用，不重复合并。AGENTS旧版本描述与现有v0.5基线不一致，历史记录保留，实际开发基线须明确授权。
定向修复：V06_CONFIRMATION_REPAIR_2026-11-24.md blob 91f3d3f63260133b53e195800bb5079d6e1b2c77，58合成检查，38阻断，27新增阻断；A35-01/04修复候选、A35-02/03仅有限缓解。V06_SESSION_INVALIDATION_REPAIR_2026-11-24.md blob 9ba4ceb31db6132668bfe17a82d0c4ba29af0aad，80受控线程执行，旧30个异常启动复活、修复30个拒绝；未完成支持环境全API/React/移动回归，新集成测试未运行。首次取消孤立会话（R36）仍为源审及合成模型，不能把全局clear修复视作网络取消和隐私擦除。作者原v0.6测试证据不能自动继承至最新head。
## 完整版本目标
12项B01-B12全部保留第34轮scope与acceptance原文，附本轮新增关联及验收责任。新增研究首先服务共同接口、版本/证据/义务传递、受控计算与解释，并提供可插拔候选方法。不得要求所有R项完成，也不得把16轮有限数学原型全数直接上线。候选注册、隔离复算和独立准入是完整产品架构的一部分；未经验证的具体方法维持研究状态。B02白话、B03本地推理、B04证据检索、B05可信投影、B06模型调度及B07表达必须构成同一用户决策闭环。B08/09贯穿全程；B10持续科学储备；B11/12检验是否真实产生产品价值。当前14项门均未通过（沿用10项，加4个细化门，非14个独立统计样本）。
## 后续优先级与防止重复
P0：锁定基线及完整支持环境验收，读取最新真实PR并复现第35/36轮问题与已修复边界；实际Mac/Ollama自然语言开发集和真实iPhone连接/离线检查；独立轨预先冻结未见情节、指标、盲评方法。设备和权限不可假设可用；缺失时受阻并转向可完成的独立研究。
P1：实际全文索引构建及基准、确定性输入与证据接口的完整入口验证、真实跨系统比较（普通ChatGPT、同Qwen、现有平台、完整候选、透明基线）。不再以更多任意合成数量替代上述证据；公开开发集不充当独立留出。对先前失败的语言泛化与约束遗漏优先测量，只有结果支持才研究训练。使用者无需自行选模型或填写技术表格。
P2：模型轨按实际决策缺口审查新候选，数据轨补真实设计、许可、独立外部验证；理论轨提供必要边界；产品轨维护唯一近期交接；独立轨审查证据与真实效果。手动窗口优先减少实际工程和证据阻塞，避免继续重复相同有限枚举。没有重大开发授权，当前不发布Codex执行命令，不调整五工作流、不合并、不部署、不启动CI或训练；零新增费用及冻结协议保持。正式版本应整体授权，Codex可在范围内自行排序；后续产品效果不确定。
## 机器可读整合
```json
{
  "version": "R50 integration addendum",
  "base": "d209adb337a9f52a98bd590a06a3804d12bff613",
  "pr61": {
    "head": "4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e",
    "draft": true,
    "merged": false,
    "mergeableObservations": [
      false,
      true
    ],
    "compare": {
      "status": "diverged",
      "aheadMain": 54,
      "behindMain": 5,
      "files": 169,
      "mainSidePlatformChanges": 0
    }
  },
  "priorManifest": {
    "commit": "4b3205e91e627819782e2d1fda50f2de16f0e608",
    "blob": "58163b4cd93b4b6cbd7212d599283ae8133a105a",
    "oldAssets": 33,
    "corrections": 4,
    "compareFiles": 19,
    "changedOldPaths": []
  },
  "assets": [
    {
      "round": 1,
      "path": "research/decision_hub/2026-11-24-confirmed-constraint-projection-coverage.py",
      "blob": "ba614d3df300c3a890d23e090c3709dfa746e025",
      "stage": "understand",
      "capability": "coverage",
      "evidence": "SYNTHETIC",
      "priority": "core",
      "description": "确认硬约束不得丢失",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityMatched": true,
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 2,
      "path": "research/decision_hub/2026-11-24-semantic-revision/README.md",
      "blob": "801d48d62a05659d3afedf1f56a555afa12c5236",
      "stage": "understand",
      "capability": "revision_condition",
      "evidence": "SYNTHETIC",
      "priority": "core",
      "description": "修订及条件树",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityMatched": true,
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 3,
      "path": "research/decision_hub/2026-11-24-retrieval-routing/README.md",
      "blob": "c0301e9a0c9371cc41a3fdecff2b2e9f18492912",
      "stage": "discover",
      "capability": "registry_gate",
      "evidence": "SYNTHETIC",
      "priority": "core",
      "description": "发现与执行隔离",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityMatched": true,
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 4,
      "path": "research/decision_hub/2026-11-24-composition-dispatch/README.md",
      "blob": "8953af15d57350d892c5dddd401c5c2bdd6f237d",
      "stage": "compute",
      "capability": "typed_dependency",
      "evidence": "SYNTHETIC",
      "priority": "core",
      "description": "类型和依赖闭包",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityMatched": true,
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 5,
      "path": "research/decision_hub/2026-11-24-minimal-clarification/README.md",
      "blob": "762053d80d444145e5b76ddd96a2266919174b52",
      "stage": "understand",
      "capability": "question_policy",
      "evidence": "SYNTHETIC",
      "priority": "core",
      "description": "有限世界最少追问",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityMatched": true,
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 6,
      "path": "research/decision_hub/2026-11-24-integrated-analysis/README.md",
      "blob": "9f3294756c22b012a53863df47984043065f4de7",
      "stage": "compute",
      "capability": "snapshot_receipt",
      "evidence": "SYNTHETIC",
      "priority": "core",
      "description": "确认后计算链",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityMatched": true,
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 7,
      "path": "research/decision_hub/2026-11-24-product-value-evaluation/README.md",
      "blob": "1050e4beac46e9045d782117e497e25abbb4aeb5",
      "stage": "validate",
      "capability": "comparative_evaluation",
      "evidence": "DESIGN_SYNTHETIC",
      "priority": "core",
      "description": "端到端独立对照设计",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityMatched": true,
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 8,
      "path": "research/decision_hub/2026-11-24-method-corpus-index/README.md",
      "blob": "ce48cbbe0f922b96e166fc50326e9d57462d66cd",
      "stage": "discover",
      "capability": "source_index",
      "evidence": "INVENTORY_PARTIAL_REVIEW",
      "priority": "core",
      "description": "154文档身份与15方法映射",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityMatched": true,
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 9,
      "path": "research/decision_hub/2026-11-24-language-evidence-corpus/README.md",
      "blob": "27ba2f09121efdc4bf57f78a0039877d1bc86f92",
      "stage": "understand",
      "capability": "language_dev_corpus",
      "evidence": "SYNTHETIC_CORPUS",
      "priority": "core",
      "description": "36轮白话开发材料",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityMatched": true,
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 10,
      "path": "research/decision_hub/2026-11-24-external-evidence-conflict/REVIEW_V2.md",
      "blob": "d15a063f9c01524ca64745121d5a96791939b5fe",
      "stage": "evidence",
      "capability": "source_scope",
      "evidence": "REPORTED_AGGREGATES_SYNTHETIC_GATE",
      "priority": "core",
      "description": "外部证据口径及冲突",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityMatched": true,
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 11,
      "path": "research/decision_hub/2026-11-24-evidence-parameter-bounds/README.md",
      "blob": "c864cb58cb6ca7f327bcefe251ef5227493850ee",
      "stage": "evidence",
      "capability": "counterfactual_bounds",
      "evidence": "CONDITIONAL_ALGEBRA",
      "priority": "research",
      "description": "联合反事实范围",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityMatched": true,
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 12,
      "path": "research/decision_hub/2026-11-24-learning-schedule/README.md",
      "blob": "72d7ae55999a34e1dabbfeab116dfcf199254ce1",
      "stage": "compute",
      "capability": "retention_schedule",
      "evidence": "SOURCE_MODEL_SYNTHETIC",
      "priority": "research",
      "description": "复习期限",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityMatched": true,
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 13,
      "path": "research/decision_hub/2026-11-24-adaptive-resource-allocation/README.md",
      "blob": "7485bf6a5e6d4ea037fedebed0b752655f047000",
      "stage": "compute",
      "capability": "adaptive_allocation",
      "evidence": "SYNTHETIC",
      "priority": "research",
      "description": "有限资源动态规划",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityMatched": true,
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 14,
      "path": "research/decision_hub/2026-11-24-real-learning-prediction/README.md",
      "blob": "0c4a40989cfa88bf4a49ed05da0156bf75b56ab5",
      "stage": "predict",
      "capability": "learner_holdout",
      "evidence": "REAL_DEV_PREDICTION",
      "priority": "research",
      "description": "已见来源学习预测",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityMatched": true,
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 15,
      "path": "research/decision_hub/2026-11-24-forgetting-model-competition/README.md",
      "blob": "be570b1e02504b02d398daef536269783bde716d",
      "stage": "predict",
      "capability": "model_competition",
      "evidence": "REAL_DEV_PREDICTION",
      "priority": "research",
      "description": "遗忘与简单基线",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityMatched": true,
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 16,
      "path": "research/decision_hub/2026-11-24-nested-predictive-combination/README.md",
      "blob": "e9cff27fdd84ab17c1add3221018ed5d48ebc8eb",
      "stage": "predict",
      "capability": "nested_combination",
      "evidence": "REAL_DEV_PREDICTION",
      "priority": "research",
      "description": "动态残差修正",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityMatched": true,
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 17,
      "path": "research/decision_hub/2026-11-24-online-model-tracking/REVIEW_V2.md",
      "blob": "ab81e05240187bc4504f869aadf62db243377ebc",
      "stage": "learn",
      "capability": "online_tracking",
      "evidence": "REAL_REPLAY_SYNTHETIC",
      "priority": "research",
      "description": "对数域模型组合勘误",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityMatched": true,
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 18,
      "path": "research/decision_hub/2026-11-24-feedback-replay-and-rollback/README.md",
      "blob": "f55a6fb6a801bb765b96530ce71b45e58d802852",
      "stage": "learn",
      "capability": "feedback_receipt",
      "evidence": "SYNTHETIC",
      "priority": "core",
      "description": "反馈修订与代次隔离",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityMatched": true,
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 19,
      "path": "research/decision_hub/2026-11-24-sequential-model-admission/README.md",
      "blob": "a2decfe7ff548aa98c94477c247bb50b6961a49f",
      "stage": "learn",
      "capability": "sequential_review",
      "evidence": "DERIVATION_SYNTHETIC",
      "priority": "research",
      "description": "连续比较与错误率预算",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityMatched": true,
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 20,
      "path": "research/decision_hub/2026-11-24-prediction-to-action-value/README.md",
      "blob": "e59e6da8e2c00899d5d23ee20e1c187853a06b94",
      "stage": "decide",
      "capability": "cost_loss",
      "evidence": "REAL_REPLAY_HYPOTHETICAL",
      "priority": "research",
      "description": "预测和行动损失分离",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityMatched": true,
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 21,
      "path": "research/decision_hub/2026-11-24-offline-policy-evaluation/README.md",
      "blob": "6e7ed462df54b6d763f01fd91bab245173542105",
      "stage": "validate",
      "capability": "offline_policy",
      "evidence": "REAL_ROW_LEVEL_BLOCKED",
      "priority": "blocked",
      "description": "NSW身份和设计未核",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityMatched": true,
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 22,
      "path": "research/decision_hub/2026-11-24-capability-integration/README.md",
      "blob": "93b85fb9ce9da73a1166beebac9d15a8e0c73af5",
      "capability": "接口与资格传递",
      "evidence": "SYNTHETIC_CONTRACT",
      "identityMatched": true,
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 23,
      "path": "research/decision_hub/2026-11-24-native-option-role-audit/README.md",
      "blob": "8b184edb783c69a59d2e9867c007b184afc16961",
      "capability": "原生语言反例",
      "evidence": "NATIVE_FRAGMENT_CHALLENGE_FAILED",
      "identityMatched": true,
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 24,
      "path": "research/decision_hub/2026-11-24-semantic-proposal-contract/README.md",
      "blob": "f7aee2c6392fa4588b717bb0c311cb253c48dd1e",
      "capability": "多轮语义候选",
      "evidence": "SYNTHETIC_CONTRACT",
      "identityMatched": true,
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 25,
      "path": "research/decision_hub/2026-11-24-local-model-evaluation-runner/README.md",
      "blob": "25a8d05c03ad9f30cc6f307277725cee99ea03c6",
      "capability": "本地对照评价",
      "evidence": "MOCK_CORE_ONLY",
      "identityMatched": true,
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 26,
      "path": "research/decision_hub/2026-11-24-constraint-omission-local-repair/README.md",
      "blob": "7e9c9003fefd22d39010d92e6ca39f9d9ebf6aac",
      "capability": "约束遗漏和局部修复",
      "evidence": "SYNTHETIC_SCANNER_FAILED",
      "identityMatched": true,
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 27,
      "path": "research/decision_hub/2026-11-24-partial-analysis-dispatch/README.md",
      "blob": "08051d3b029ebb3acca1380bdf5b92ad99d8a44d",
      "capability": "局部分析与依赖失效",
      "evidence": "SYNTHETIC_FINITE",
      "identityMatched": true,
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 28,
      "path": "research/decision_hub/2026-11-24-content-method-retrieval/README.md",
      "blob": "36ca07db56fc64865d6cc7a5db87384583604844",
      "capability": "双语正文检索",
      "evidence": "REPOSITORY_SUBSET",
      "identityMatched": true,
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 29,
      "path": "research/decision_hub/2026-11-24-native-method-contract-index/README.md",
      "blob": "585bce3e9c878e2ead241e9fefc6f93937780790",
      "capability": "原生接口索引",
      "evidence": "STATIC_SOURCE_AND_PARTIAL_INDEX",
      "identityMatched": true,
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 30,
      "path": "research/decision_hub/2026-11-24-native-state-feasibility-bridge/README.md",
      "blob": "0b56dae921c6e16850a1b9681b69344329db3f99",
      "capability": "原生状态和底线",
      "evidence": "UNSUPPORTED_RUNTIME_FRAGMENT",
      "identityMatched": true,
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 31,
      "path": "research/decision_hub/2026-11-24-native-regret-validation/README.md",
      "blob": "a04076828e5094365f3efcbb1b22f5dc8b58cd44",
      "capability": "原生后悔",
      "evidence": "UNSUPPORTED_RUNTIME_FRAGMENT",
      "identityMatched": true,
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 32,
      "path": "research/decision_hub/2026-11-24-native-scoring-validation/README.md",
      "blob": "222642e89b38b2927b56b54854a55d380e3a9bdc",
      "capability": "原生权重和评分",
      "evidence": "UNSUPPORTED_RUNTIME_FRAGMENT",
      "identityMatched": true,
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 33,
      "path": "research/decision_hub/2026-11-24-native-voi-timing-core/README.md",
      "blob": "77d269d669df170f767b90111b3430449a2b0078",
      "capability": "原生信息价值和时机",
      "evidence": "UNSUPPORTED_RUNTIME_FRAGMENT",
      "identityMatched": true,
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED",
      "identityBasis": "round34 verified manifest; compare confirms unchanged paths"
    },
    {
      "round": 34,
      "path": "research/decision_hub/2026-11-24-version-integration-specification/README.md",
      "blob": "66e7d855f548663fed140ec3df6f3fb5ac3d6453",
      "capability": "完整版本规格",
      "evidence": "DESIGN_CONSOLIDATION",
      "requirements": [
        "B01",
        "B02",
        "B03",
        "B04",
        "B05",
        "B06",
        "B07",
        "B08",
        "B09",
        "B10",
        "B11",
        "B12"
      ],
      "identityMatched": true,
      "identityBasis": "read fixed current blob; match prior receipt or original commit",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED"
    },
    {
      "round": 35,
      "path": "research/decision_hub/2026-11-24-v06-baseline-audit/README.md",
      "blob": "29724f195d719519fa418a80b5467342cfeb973e",
      "capability": "v0.6条件投影及确认缺陷",
      "evidence": "NATIVE_FRAGMENT_DEFECTS",
      "requirements": [
        "B01",
        "B02",
        "B05",
        "B07",
        "B11"
      ],
      "identityMatched": true,
      "identityBasis": "read fixed current blob; match prior receipt or original commit",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED"
    },
    {
      "round": 36,
      "path": "research/decision_hub/2026-11-24-v06-first-turn-cancellation.md",
      "blob": "093c01a5a44e9b3b64b7652d15204492c2b02787",
      "capability": "首次请求取消及孤立会话",
      "evidence": "SOURCE_AUDIT_SYNTHETIC",
      "requirements": [
        "B03",
        "B09",
        "B12"
      ],
      "identityMatched": true,
      "identityBasis": "read fixed current blob; match prior receipt or original commit",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED"
    },
    {
      "round": 37,
      "path": "research/decision_hub/2026-11-24-safe-contingent-regret.md",
      "blob": "5bb0dc068a0c1a1487efa161acbefef051ed0608",
      "capability": "联合情景下安全条件策略",
      "evidence": "DERIVATION_SYNTHETIC",
      "requirements": [
        "B05",
        "B06",
        "B07",
        "B10"
      ],
      "identityMatched": true,
      "identityBasis": "read fixed current blob; match prior receipt or original commit",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED"
    },
    {
      "round": 38,
      "path": "research/decision_hub/2026-11-24-cross-criterion-agreement-regions.md",
      "blob": "8e2eb5732d90565e16ee8344c3ed0a99480c70dd",
      "capability": "跨准则共同最优及分歧",
      "evidence": "DERIVATION_SYNTHETIC",
      "requirements": [
        "B06",
        "B07",
        "B08",
        "B10"
      ],
      "identityMatched": true,
      "identityBasis": "read fixed current blob; match prior receipt or original commit",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED"
    },
    {
      "round": 39,
      "path": "research/decision_hub/2026-11-24-evidence-qualified-difference-bounds.md",
      "blob": "c7e4a2ff83c836cdd81f94dbc6ae84336096eda6",
      "capability": "差分约束与证据冲突",
      "evidence": "DERIVATION_SYNTHETIC_SOURCE_REVIEW_UNCONFIRMED",
      "requirements": [
        "B04",
        "B05",
        "B06",
        "B08",
        "B10"
      ],
      "identityMatched": true,
      "identityBasis": "read fixed current blob; match prior receipt or original commit",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED"
    },
    {
      "round": 40,
      "path": "research/decision_hub/2026-11-24-cost-sensitive-clarification.md",
      "blob": "56b1885f277b70797974ad48e80884a2d99dde81",
      "capability": "有限成本追问及拒答",
      "evidence": "DERIVATION_SYNTHETIC",
      "requirements": [
        "B02",
        "B05",
        "B06",
        "B07",
        "B10"
      ],
      "identityMatched": true,
      "identityBasis": "read fixed current blob; match prior receipt or original commit",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED"
    },
    {
      "round": 41,
      "path": "research/decision_hub/2026-11-24-qualified-alternative-synthesis.md",
      "blob": "7398d951f617d938ce27bcc46252e8dc84144797",
      "capability": "候选行动组合及前缀可行性",
      "evidence": "DERIVATION_SYNTHETIC",
      "requirements": [
        "B02",
        "B05",
        "B06",
        "B07",
        "B10"
      ],
      "identityMatched": true,
      "identityBasis": "read fixed current blob; match prior receipt or original commit",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED"
    },
    {
      "round": 42,
      "path": "research/decision_hub/2026-11-24-robust-longitudinal-planning.md",
      "blob": "1d69fe923238f56fb8fb1f822c366335182f89ed",
      "capability": "长期鲁棒可行策略",
      "evidence": "DERIVATION_SYNTHETIC",
      "requirements": [
        "B06",
        "B07",
        "B10"
      ],
      "identityMatched": true,
      "identityBasis": "read fixed current blob; match prior receipt or original commit",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED"
    },
    {
      "round": 43,
      "path": "research/decision_hub/2026-11-24-partial-observation-robust-planning.md",
      "blob": "0eb4141f42b9e1607c8f4fe4122f6cc6cb699320",
      "capability": "部分观察及支持失效",
      "evidence": "DERIVATION_SYNTHETIC",
      "requirements": [
        "B05",
        "B06",
        "B07",
        "B08",
        "B10"
      ],
      "identityMatched": true,
      "identityBasis": "read fixed current blob; match prior receipt or original commit",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED"
    },
    {
      "round": 44,
      "path": "research/decision_hub/2026-11-24-paired-policy-feedback-bounds.md",
      "blob": "93ba01e1fb71e32e0f7ed7e57c5acc76afb9b091",
      "capability": "配对反事实界及退步门",
      "evidence": "DERIVATION_SYNTHETIC",
      "requirements": [
        "B08",
        "B09",
        "B10",
        "B11"
      ],
      "identityMatched": true,
      "identityBasis": "read fixed current blob; match prior receipt or original commit",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED"
    },
    {
      "round": 45,
      "path": "research/decision_hub/2026-11-24-context-qualified-model-routing.md",
      "blob": "dcc14692b2c92d1f5d256e969e4d9fd135ac714e",
      "capability": "分领域模型调度",
      "evidence": "DERIVATION_SYNTHETIC",
      "requirements": [
        "B04",
        "B06",
        "B08",
        "B10",
        "B11"
      ],
      "identityMatched": true,
      "identityBasis": "read fixed current blob; match prior receipt or original commit",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED"
    },
    {
      "round": 46,
      "path": "research/decision_hub/2026-11-24-model-conflict-compatible-branches.md",
      "blob": "f16000fc95a7dbb7de76dac2adebdda6d68d1a46",
      "capability": "最大相容假设与事实隔离",
      "evidence": "DERIVATION_SYNTHETIC",
      "requirements": [
        "B04",
        "B05",
        "B06",
        "B07",
        "B08",
        "B10"
      ],
      "identityMatched": true,
      "identityBasis": "read fixed current blob; match prior receipt or original commit",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED"
    },
    {
      "round": 47,
      "path": "research/decision_hub/2026-11-24-budgeted-analysis-planning.md",
      "blob": "d99676bf1241e852a7c035fe092f1eabbf124c7e",
      "capability": "预算及共享依赖",
      "evidence": "DERIVATION_SYNTHETIC",
      "requirements": [
        "B04",
        "B06",
        "B07",
        "B08",
        "B09",
        "B10",
        "B11"
      ],
      "identityMatched": true,
      "identityBasis": "read fixed current blob; match prior receipt or original commit",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED"
    },
    {
      "round": 48,
      "path": "research/decision_hub/2026-11-24-partial-regret-publication-certificates.md",
      "blob": "84a8abdd595152a81b270f7cc21c8361ceee71f8",
      "capability": "部分计算停止及发布证书",
      "evidence": "DERIVATION_SYNTHETIC",
      "requirements": [
        "B05",
        "B06",
        "B07",
        "B08",
        "B10",
        "B11"
      ],
      "identityMatched": true,
      "identityBasis": "read fixed current blob; match prior receipt or original commit",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED"
    },
    {
      "round": 49,
      "path": "research/decision_hub/2026-11-24-faithful-conditional-explanation.md",
      "blob": "0377f7f24cfa45014f4536b770d292872266a080",
      "capability": "最简条件表达与回读",
      "evidence": "DERIVATION_SYNTHETIC",
      "requirements": [
        "B02",
        "B05",
        "B06",
        "B07",
        "B08",
        "B11"
      ],
      "identityMatched": true,
      "identityBasis": "read fixed current blob; match prior receipt or original commit",
      "productionAdmission": "NOT_GRANTED_BY_THIS_RESEARCH",
      "independentAcceptance": "NOT_ESTABLISHED"
    }
  ],
  "requirements": [
    {
      "id": "B01",
      "title": "基线与兼容",
      "rounds": [
        7,
        22,
        25,
        29,
        30,
        31,
        32,
        33,
        34,
        35
      ],
      "scope": "复核#61独立验收、现main与待审分支差异；经所有者授权才确定基线；复用v0.5/v0.6、手机、API/CLI与恢复路径；禁止重复合并#59/#60。",
      "acceptance": "锁定真实提交、依赖与运行环境；支持Python3.12及固定Pydantic；旧功能完整回归、移动跨端契约和恢复通过；不以作者报告替代独立验收。",
      "implementation": "NOT_AUTHORIZED",
      "acceptanceState": "NOT_RUN"
    },
    {
      "id": "B02",
      "title": "开放白话入口与语义账本",
      "rounds": [
        1,
        2,
        5,
        9,
        23,
        24,
        25,
        26,
        34,
        35,
        40,
        41,
        49
      ],
      "scope": "本地Qwen可选提议角色、主体、时态、逻辑极性、条件、量值、归属、单位、候选及修订；保留原文证据、冲突、未知；可信宿主核对覆盖，明确确认与撤回；不能只依赖正则或逐字匹配。",
      "acceptance": "固定独立情节，测角色/条件/约束遗漏、错确认、撤回、重复锚点、假设及第三方；初答无强制技术字段，通常至多一个关键追问；重大风险需要补问时说明原因。",
      "implementation": "NOT_AUTHORIZED",
      "acceptanceState": "NOT_RUN"
    },
    {
      "id": "B03",
      "title": "本地推理和降级",
      "rounds": [
        23,
        24,
        25,
        34,
        36
      ],
      "scope": "复用现有环回传输、白名单及逐轮授权；完成实际JSON输出与请求限额；无服务、超时、非法输出、拒绝授权时提供可用规则/结构化降级；禁止自动训练或调用计费API。",
      "acceptance": "实机记录Ollama版本、模型digest、量化、资源和原始公开样本响应；完整对照原规则、自然回复、结构化回复、同份回复核验；失败/拒答计入分母。",
      "implementation": "NOT_AUTHORIZED",
      "acceptanceState": "NOT_RUN"
    },
    {
      "id": "B04",
      "title": "科学检索与来源资格",
      "rounds": [
        3,
        8,
        10,
        11,
        22,
        28,
        29,
        34,
        39,
        45,
        46,
        47
      ],
      "scope": "构建最新许可合规全文索引；保留路径、blob、来源版本、证据类型和适用边界；语言模型只提出检索线索，真正的执行资格来自原生注册表；先本地库，可选用户授权免费外部查证，离线明确限制。",
      "acceptance": "对固定154份历史清单按blob重建，更新版本另记；盲测正负及多意图检索；同编号、来源变更、冲突、因果迁移和未核验引用不能授权；timing_actions变更隔离待审。",
      "implementation": "NOT_AUTHORIZED",
      "acceptanceState": "NOT_RUN"
    },
    {
      "id": "B05",
      "title": "可信输入投影与覆盖",
      "rounds": [
        1,
        2,
        6,
        24,
        26,
        30,
        34,
        35,
        37,
        39,
        40,
        41,
        43,
        46,
        48,
        49
      ],
      "scope": "原文候选到正规化量值和DecisionState；结构化义务覆盖、单位/周期/时域/币种、严格/非严格比较、选项与测量引用、来源身份。联合约束未获方法资格则保持未知。",
      "acceptance": "独立测试每一已确认底线必须有有效投影，漏项不能使未知变通过，错误局部不得静默删除，联合预算反例必须保留UNKNOWN；不生成虚构概率或共同尺度。",
      "implementation": "NOT_AUTHORIZED",
      "acceptanceState": "NOT_RUN"
    },
    {
      "id": "B06",
      "title": "按需模型调度与局部分析",
      "rounds": [
        3,
        4,
        5,
        6,
        22,
        27,
        29,
        30,
        31,
        32,
        33,
        34,
        37,
        38,
        39,
        40,
        41,
        42,
        43,
        45,
        46,
        47,
        48,
        49
      ],
      "scope": "稳定方法端口，版本化依赖DAG、缺口代码和目标适配；注册表原生describe/validate/execute；局部描述和条件性结论独立出口，计算收据与当前修订绑定；全局安全门控优先于优化。",
      "acceptance": "15个既有入口分别跑合法、缺项、不适用、异常、边界及独立数值基线；阻断未授权、错误依赖、未确认和过期输出；允许局部结果不被无关未知阻塞。",
      "implementation": "NOT_AUTHORIZED",
      "acceptanceState": "NOT_RUN"
    },
    {
      "id": "B07",
      "title": "解释、图表和行动规划",
      "rounds": [
        5,
        6,
        7,
        11,
        20,
        27,
        31,
        32,
        33,
        34,
        35,
        37,
        38,
        40,
        41,
        42,
        43,
        46,
        47,
        48,
        49
      ],
      "scope": "首答直接给有依据的差异、关键限制、条件性建议；模型选择理由、可行性、区间、权重反转、后悔、信息价值及等待边界按需展开；图表、文字与结果快照一致；用户选择及行动授权分离。",
      "acceptance": "用户修改参数后图文同修订，旧结果不可覆盖；未确定权重时仍做分维度比较；没有证据的未知不得改为概率；确认已知范围后才显示阈值；真实首次用户测试操作与理解。",
      "implementation": "NOT_AUTHORIZED",
      "acceptanceState": "NOT_RUN"
    },
    {
      "id": "B08",
      "title": "可追溯证据及派生结果",
      "rounds": [
        10,
        11,
        20,
        21,
        22,
        27,
        30,
        31,
        32,
        33,
        34,
        38,
        39,
        43,
        44,
        45,
        46,
        47,
        48,
        49
      ],
      "scope": "每个输出记录原始证据身份、模型和版本、输入、假设、scope、cutoff及真实父依赖；区分来源报告、合成、观察、预测、因果、条件建议；保留冲突、证据许可及审计。",
      "acceptance": "负控：来源文字非空、相同编号、过期材料、合成预测、未选反事实、情景变事实、无条件效应外推不能获得现实计算资格；跨模块语义资格不能只由布尔标记声称。",
      "implementation": "NOT_AUTHORIZED",
      "acceptanceState": "NOT_RUN"
    },
    {
      "id": "B09",
      "title": "隐私、记录、复盘及恢复",
      "rounds": [
        2,
        7,
        18,
        19,
        22,
        24,
        27,
        34,
        36,
        44,
        47
      ],
      "scope": "默认临时分析；本地保存、跨会话使用、反馈、研究和训练单独授权；事件时间与修订历史；原预测不重写，未选结果未知；撤回/删除/恢复以真实持久化权限状态为准；模型回退另立版本。",
      "acceptance": "跨会话、过期回调、重复请求、并发、断电、备份/旧版本恢复、授权代次、删除、导出验证；真实设备缓存与VoiceOver/冷启动检查；无私人数据公开。",
      "implementation": "NOT_AUTHORIZED",
      "acceptanceState": "NOT_RUN"
    },
    {
      "id": "B10",
      "title": "科研候选与可扩展接口",
      "rounds": [
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        19,
        20,
        21,
        22,
        34,
        37,
        38,
        39,
        40,
        41,
        42,
        43,
        44,
        45,
        46,
        47,
        48
      ],
      "scope": "提供独立研究候选适配及版本登记接口；学习预测、资源分配、在线更新、决策价值及因果部分识别只在隔离沙盒；NSW维持阻塞；C035/C036及其他候选不自动上线。",
      "acceptance": "测试候选无法成为生产执行入口、无默认权重变动、无自动更新；独立验收和所有者明确授权后逐方法晋级。",
      "implementation": "NOT_AUTHORIZED",
      "acceptanceState": "NOT_RUN"
    },
    {
      "id": "B11",
      "title": "真实产品增量与独立验收",
      "rounds": [
        7,
        9,
        23,
        24,
        25,
        26,
        28,
        29,
        34,
        35,
        44,
        45,
        47,
        48,
        49
      ],
      "scope": "锁定开发集、独立留出、对照臂与评审；同原始问题/证据、同回答预算，盲评普通ChatGPT、原始Qwen、v0.6、候选及规则基线；结构化能力与端到端分开。",
      "acceptance": "预注册主指标、分母、最小改善和样本计划；零关键错误为固定验收门槛而非现实零风险；报告正确可操作覆盖、正确未知、漏拒、耗时及真实负担，优越性不足保留UNKNOWN。",
      "implementation": "NOT_AUTHORIZED",
      "acceptanceState": "NOT_RUN"
    },
    {
      "id": "B12",
      "title": "Mac与iPhone端到端",
      "rounds": [
        7,
        22,
        25,
        27,
        34,
        36
      ],
      "scope": "先真实Mac本地推理，再授权范围内实现手机到Mac安全连接；不开放公网、不默认转发个人数据；保留手机离线确定性分析，Mac关机或网络断开可降级。",
      "acceptance": "真实设备、认证、连接撤销、网络故障、离线冷启动、隐私与一致性；托管macOS和模拟浏览器不能代替实体设备；无法取得实机则明确受阻，不发布完成结论。",
      "implementation": "NOT_AUTHORIZED",
      "acceptanceState": "NOT_RUN"
    }
  ],
  "corrections": [
    {
      "path": "research/decision_hub/2026-11-24-product-value-evaluation/CORRECTION.md",
      "blob": "49cb38571f963c64358bfcb7840672b681d134e1",
      "rule": "USE_CORRECTION_FOR_AFFECTED_CLAIMS; preserve historical results"
    },
    {
      "path": "research/decision_hub/2026-11-24-external-evidence-conflict/REVIEW_V2.md",
      "blob": "d15a063f9c01524ca64745121d5a96791939b5fe",
      "rule": "USE_CORRECTION_FOR_AFFECTED_CLAIMS; preserve historical results"
    },
    {
      "path": "research/decision_hub/2026-11-24-online-model-tracking/REVIEW_V2.md",
      "blob": "ab81e05240187bc4504f869aadf62db243377ebc",
      "rule": "USE_CORRECTION_FOR_AFFECTED_CLAIMS; preserve historical results"
    },
    {
      "path": "research/decision_hub/2026-11-24-constraint-omission-local-repair/CORRECTION.md",
      "blob": "427b56f4966efb1e8f65953ad2395aff985fe7df",
      "rule": "USE_CORRECTION_FOR_AFFECTED_CLAIMS; preserve historical results"
    },
    {
      "path": "research/decision_hub/2026-11-24-evidence-qualified-difference-bounds.md",
      "blob": "c7e4a2ff83c836cdd81f94dbc6ae84336096eda6",
      "rule": "Historical source review not independently confirmed; round40 correction also lacks independently rechecked original abstract in round50; mathematical proof/experiment retain scope; no retroactive source credit"
    }
  ],
  "gates": [
    {
      "id": "baseline_independent_review",
      "state": "NOT_RUN",
      "owner": "独立验收轨"
    },
    {
      "id": "owner_baseline_and_development_authorization",
      "state": "NOT_GRANTED",
      "owner": "所有者"
    },
    {
      "id": "frozen_holdout_and_metric_plan",
      "state": "NOT_ESTABLISHED",
      "owner": "独立验收轨"
    },
    {
      "id": "supported_runtime_full_registry",
      "state": "NOT_RUN",
      "owner": "Codex及独立验收轨"
    },
    {
      "id": "real_mac_ollama",
      "state": "NOT_RUN",
      "owner": "产品轨及用户控制设备"
    },
    {
      "id": "real_iphone",
      "state": "NOT_RUN",
      "owner": "产品轨及用户控制设备"
    },
    {
      "id": "implementation_and_regression",
      "state": "NOT_RUN",
      "owner": "Codex"
    },
    {
      "id": "independent_product_comparison",
      "state": "NOT_RUN",
      "owner": "独立验收轨"
    },
    {
      "id": "privacy_and_recovery",
      "state": "NOT_RUN",
      "owner": "独立验收轨"
    },
    {
      "id": "owner_merge_and_deploy_authorization",
      "state": "NOT_GRANTED",
      "owner": "所有者"
    },
    {
      "id": "baseline_current_head_regression",
      "state": "NOT_RUN",
      "owner": "独立验收轨",
      "detail": "两次修复后尚未运行完整支持环境测试"
    },
    {
      "id": "first_turn_cancellation",
      "state": "NOT_RUN",
      "owner": "产品及独立验收轨",
      "detail": "R36范围取消尚无生产验证"
    },
    {
      "id": "real_language_generalization",
      "state": "NOT_ESTABLISHED",
      "owner": "产品及独立验收轨",
      "detail": "R23/R26失败；R25仅mock；真Qwen未验"
    },
    {
      "id": "corpus_full_coverage",
      "state": "NOT_RUN",
      "owner": "模型与数据轨",
      "detail": "24/154正文子集；全库构建未运行"
    }
  ],
  "formalDevelopmentAuthorization": "NOT_GRANTED"
}
```
## 结构校验函数与测试
```js
function validate(d){const rs=d.assets.map(a=>a.round).sort((a,b)=>a-b);if(rs.length!==49||rs.some((v,i)=>v!==i+1)||new Set(d.assets.map(a=>a.path)).size!==49)return false;if(d.requirements.length!==12||new Set(d.requirements.map(x=>x.id)).size!==12)return false;if(d.formalDevelopmentAuthorization!=="NOT_GRANTED"||d.requirements.some(x=>x.implementation!=="NOT_AUTHORIZED"||x.acceptanceState!=="NOT_RUN"))return false;if(d.assets.some(x=>x.productionAdmission!=="NOT_GRANTED_BY_THIS_RESEARCH"||x.independentAcceptance!=="NOT_ESTABLISHED"))return false;const rr=new Set(d.requirements.flatMap(x=>x.rounds));return rr.size===49&&d.gates.length===14&&d.gates.every(x=>["NOT_RUN","NOT_GRANTED","NOT_ESTABLISHED"].includes(x.state))&&d.corrections.length===5&&d.assets.every(x=>x.identityMatched===true);}
```
实际统计：{"assets":49,"oldUnchanged":33,"newVerified":16,"requirements":12,"links":177,"gates":14,"corrections":5,"mutations":12}。仅清单一致性测试，不能替代源码、科学或产品验收。
