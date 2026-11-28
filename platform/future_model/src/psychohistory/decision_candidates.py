"""Versioned research discovery for personal decisions."""

from dataclasses import asdict, dataclass
import re


@dataclass(frozen=True)
class CandidateSource:
    path: str
    git_blob: str
    license: str = "UNVERIFIED"


@dataclass(frozen=True)
class ResearchCandidate:
    candidate_id: str
    version: str
    title: str
    evidence: str
    sources: tuple[CandidateSource, ...]
    applicability: str
    inputs: str
    outputs: str
    formula: str
    failure_example: str
    baseline: str
    replay: str
    missing_admission: tuple[str, ...]

    @property
    def key(self) -> str:
        return f"{self.candidate_id}@{self.version}"

    def describe(self) -> dict:
        return {
            **asdict(self),
            "key": self.key,
            "admission": "NOT_ADMITTED",
            "authority": "NONE",
        }


class CandidateRegistry:
    """Store metadata by exact identity, including superseded versions."""

    def __init__(self) -> None:
        self._candidates: dict[str, ResearchCandidate] = {}

    def register(self, candidate: ResearchCandidate) -> None:
        if not isinstance(candidate, ResearchCandidate):
            raise ValueError("需要研究候选登记契约。")
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_.-]{1,63}@[0-9]+\.[0-9]+\.[0-9]+", candidate.key):
            raise ValueError("需要固定的研究候选身份和版本。")
        if candidate.key in self._candidates:
            raise ValueError("该研究候选版本已经登记。")
        metadata = candidate.describe()
        sources = metadata.pop("sources")
        conditions = metadata.pop("missing_admission")
        if not all(isinstance(value, str) and value.strip() for value in metadata.values()):
            raise ValueError("研究候选缺少描述。")
        if not sources or any(
            not source["path"].startswith("research/")
            or ".." in source["path"].split("/")
            or not re.fullmatch(r"[0-9a-f]{40}", source["git_blob"])
            or not source["license"].strip()
            for source in sources
        ):
            raise ValueError("研究候选需要固定来源和许可状态。")
        if not conditions or any(not item.strip() for item in conditions):
            raise ValueError("研究候选需要记录尚未完成的准入条件。")
        self._candidates[candidate.key] = candidate

    def get(self, key: str) -> ResearchCandidate:
        try:
            return self._candidates[key]
        except KeyError:
            raise ValueError("未知的研究候选精确版本。") from None

    def describe(self, key: str | None = None) -> dict | tuple[dict, ...]:
        if key is not None:
            return self.get(key).describe()
        return tuple(candidate.describe() for candidate in self._candidates.values())

    def versions(self, candidate_id: str) -> tuple[str, ...]:
        return tuple(candidate.key for candidate in self._candidates.values() if candidate.candidate_id == candidate_id)


_ADMISSION = ("可信原生输入与适用边界核验", "独立数学及使用范围验收", "来源许可及纳入审查")

_BUILTINS = (
    ResearchCandidate(
        candidate_id="C035", version="1.0.0", title="耦合证据下的联合硬约束可行性",
        evidence="ANALYTIC_SYNTHETIC_CANDIDATE",
        sources=(CandidateSource(
            "research/decision_methods/C035_JOINT_HARD_CONSTRAINT_FEASIBILITY_COUNTEREXAMPLE_2026-11-23.md",
            "4f2c077e297a4b2733fa26309c99a510329ec6f4",
        ),),
        applicability="联合可行域有明确依据、非空，所有底线针对同一口径的资源。",
        inputs="带共同单位的变量、联合可行域和逐项硬约束。",
        outputs="条件性确定满足、确定违反或待定，以及适用时的可行见证。",
        formula="若所有 z∈S 满足全部底线则确定满足，若 S 与全部底线无交则确定违反。",
        failure_example="x+y=10 且二者均需至少 6。分别判定会遗漏联合矛盾。空证据域表示冲突。",
        baseline="C028 分别检查区间硬约束。",
        replay="复算卡片中的整数资源合取，以及空域与边界情景。",
        missing_admission=_ADMISSION,
    ),
    ResearchCandidate(
        candidate_id="C036", version="1.0.0", title="两阶段可调整鲁棒可行性",
        evidence="ANALYTIC_SYNTHETIC_CANDIDATE",
        sources=(
            CandidateSource(
                "research/decision_methods/C036_TWO_STAGE_ADJUSTABLE_FEASIBILITY_QUANTIFIER_BOUNDARY_2026-11-23.md",
                "d2438afcc93f8568cb3a0ef00285fa2f66b34f23",
            ),
            CandidateSource(
                "research/decision_methods/C036_TRANSFER_LOSS_FULL_CAPACITY_BOUNDARY_2026-11-23.md",
                "86a02e8e82f345d931a3544e18d0778fbff14d8e",
            ),
            CandidateSource(
                "research/decision_methods/C036_SYMMETRIC_POLICY_GLOBAL_FEASIBILITY_PROOF_2026-11-24.md",
                "b37f83574ec6b60ff86cae8f76c8957cc76965f9",
            ),
        ),
        applicability="有限情景、可追溯的约束和损失，按时观察且已获调整授权。",
        inputs="共同单位的资源、情景、初始配置、供方转移上限、损失率和期限。",
        outputs="条件性策略存在性、可行初始配置及调整见证。",
        formula="存在初始配置 a，使每个可观察情景 s 均存在合规的事后调整 x_s。",
        failure_example="总量恰好用尽时，任意正转移损失可使无损可行策略失效。",
        baseline="不可调整的单一配置，以及无损转移的两阶段配置。",
        replay="枚举原卡的整数配置，复算 k=2 与正损失、满容量、松弛边界。",
        missing_admission=_ADMISSION,
    ),
    ResearchCandidate(
        candidate_id="robust_longitudinal_dp", version="1.0.0", title="有限期鲁棒长期规划",
        evidence="SYNTHETIC_RESEARCH_CANDIDATE",
        sources=(CandidateSource(
            "research/decision_hub/2026-11-24-robust-longitudinal-planning.md",
            "1d69fe923238f56fb8fb1f822c366335182f89ed",
        ),),
        applicability="有限时域与充分可观察状态，阶段扰动支持及联合结构有明确依据。",
        inputs="有限期数、状态、行动、路径与终点底线、转移支持、可比较的效用。",
        outputs="阶段可生存状态集合，以及有共同效用尺度时的最坏累计值和并列首行动。",
        formula="V_t(s)=max_a[r_t(s,a)+min_{s'∈T_t(s,a)} V_(t+1)(s')]，先筛路径和终点底线。",
        failure_example="跨期相关扰动若按独立阶段组合，会产生原支持中不存在的最坏轨迹。",
        baseline="固定开环计划与只检查下一期安全的贪心行动。",
        replay="对候选档案的三阶段合成状态，比较逆向递推和反馈表路径穷举。",
        missing_admission=(*_ADMISSION, "真实跨期联合支持及预算上限验证"),
    ),
    ResearchCandidate(
        candidate_id="ledger_robust_planning", version="1.0.0", title="账本驱动的有限情景规划",
        evidence="SYNTHETIC_RESEARCH_CANDIDATE",
        sources=(CandidateSource(
            "research/decision_hub/2026-11-25-integrated-ledger-planning-candidate.md",
            "907f12081ddce7bb752ae498bcf21f4b4b218a60",
        ),),
        applicability="单一账户、按当前双时间边界对账、有限整数现金和时间情景。",
        inputs="当前余额依据、已观察到账、时间、计划余量、费用及候选情景。",
        outputs="有条件的共同可行路径、期末余额及未知来源或覆盖缺口。",
        formula="以期初余额加截止前已观察且确认的到账，作为候选路径的现金起点。",
        failure_example="未对账的预测到账不能作可支配现金，已失效的来源不能回退至旧版本。",
        baseline="在两个固定情景中直接枚举共同的开放环路径。",
        replay="按候选档案的账本投影与 R99 序列枚举复算。",
        missing_admission=(*_ADMISSION, "可信账本与用途绑定、适用域及人工回放验收"),
    ),
    ResearchCandidate(
        candidate_id="conditional_model_coverage", version="1.0.0", title="有限情景内的竞争模型覆盖",
        evidence="ANALYTIC_SYNTHETIC_CANDIDATE",
        sources=(CandidateSource(
            "research/decision_hub/2026-11-25-conditional-model-alternative-coverage.md",
            "8fa6c050fd71d60823e4dc99d4f4f7310b579a0d",
        ),),
        applicability="共同目标、范围及硬约束均已核对，有限联合情景及竞争解释已穷尽。",
        inputs="版本化情景、行动、适用模型、来源及各模型的并列最优集合或未计算状态。",
        outputs="条件共同及可能最优集合、逐情景分歧及缺失覆盖。",
        formula="按情景分别取适用模型最优集合的交集和并集，再组合所有情景。",
        failure_example="仍可能成立的模型缺少结果时，不能忽略它并宣称其余模型有共同最优。",
        baseline="逐情景逐行动按所有适用假设直接核验成员关系。",
        replay="platform/future_model/scripts/v08_composition_replay.py",
        missing_admission=(*_ADMISSION, "原生模型适用域与联合覆盖来源核验"),
    ),
    ResearchCandidate(
        candidate_id="joint_threshold_composition", version="1.0.0", title="按共同情景连接持续收益证据及预算续算",
        evidence="ANALYTIC_SYNTHETIC_CANDIDATE",
        sources=(
            CandidateSource(
                "research/decision_hub/2026-11-25-world-bound-multistage-result-join.md",
                "af4daae1aaeee5a36a140d8a0f272a48c064368b",
            ),
            CandidateSource(
                "research/decision_hub/2026-11-25-resumable-budgeted-world-join.md",
                "d4a85f1e92744d1179f76a47cf56926d17b18cf3",
            ),
        ),
        applicability="同一账户、单位、时域、用途及可信有限世界，每端口在各世界内最多一个值。",
        inputs="逐情景整数收益与最低收益阈值，可缺失。宿主提供当前来源、权限及预算。",
        outputs="相同情景支持的阈值比较、计数边界、缺失证据及可验续算状态。",
        formula="只比较共享情景支持的收益与阈值，使用已知通过及失败数分别约束全域计数。",
        failure_example="把未观察情景移出世界域或把不同世界的收益与阈值拼接会产生虚假见证。",
        baseline="逐世界核对收益与阈值，无分组压缩。",
        replay="platform/future_model/scripts/v08_composition_replay.py",
        missing_admission=(*_ADMISSION, "原生来源及设备预算验证"),
    ),
    ResearchCandidate(
        candidate_id="recurring_benefit_threshold", version="1.0.0", title="有限离散计划的最低持续收益",
        evidence="ANALYTIC_SYNTHETIC_CANDIDATE",
        sources=(CandidateSource(
            "research/decision_hub/2026-11-25-recurring-benefit-feasibility-threshold.md",
            "9c27c104e3be8f18eebc18f5ad8a0e10e2940fcf",
        ),),
        applicability="实际期初余额，单一账户，有限离散时段及两个各占一个时段的目标。",
        inputs="现金底线、时段容量、到账滞后、持续收益、费用及期限。",
        outputs="带见证的最低收益、条件可行或无有限阈值。",
        formula="枚举合规执行时点，取各期现金底线导出的收益下界的最大值，再最小化该阈值。",
        failure_example="把预测到账计入初始实际可支配余额会放行原本不可行的路径。",
        baseline="有限整数收益及行动时点枚举。",
        replay="psychohistory.decision_resources.evaluate_recurring_benefit",
        missing_admission=(*_ADMISSION, "实际账本连接及更广时段和任务覆盖"),
    ),
    ResearchCandidate(
        candidate_id="joint_goal_deadline_frontier", version="1.0.0", title="共享资源下的有限联合目标延期前沿",
        evidence="ANALYTIC_SYNTHETIC_CANDIDATE",
        sources=(CandidateSource(
            "research/decision_hub/2026-11-25-joint-goal-deadline-extension-frontier.md",
            "6587769d44804abed17808e7986368178455fbdf",
        ),),
        applicability="已确认资源、联合容量及有限离散时段。限定两个各占一个时段的目标。",
        inputs="实际期初余额、费用、时间容量、明确的硬期限或允许延期的期限。",
        outputs="条件可行的联合完成日期及不可支配延期向量。",
        formula="枚举同时满足现金、时段、硬期限的执行时点，只保留逐目标延期不可支配的向量。",
        failure_example="分别执行两项最早可行任务可能重复占用同一时段或现金。",
        baseline="逐情景双时点枚举及逐对支配比较。",
        replay="psychohistory.decision_resources.evaluate_goal_deadlines",
        missing_admission=(*_ADMISSION, "多时段任务的原生账本覆盖与独立验证"),
    ),
    ResearchCandidate(
        candidate_id="bounded_residual_evaluation", version="1.0.0", title="隔离有界残差校准评价",
        evidence="ANALYTIC_SYNTHETIC_CANDIDATE",
        sources=(CandidateSource(
            "research/decision_hub/2026-11-25-bounded-residual-correction-gate.md",
            "0b4a892b4daf7c1b887dc93ca672797068d3da63",
        ),),
        applicability="固定候选调整、有时间顺序且隔离的合成已观察结果及可比较的预测目标。",
        inputs="固定残差候选和有界预测、时间有序的测试结果及简单基线。",
        outputs="独立候选比较报告，保留误差、低估和回退状态。",
        formula="将固定调整裁剪到指定边界，比较保留样本上候选、生产参考和简单基线的误差。",
        failure_example="只汇报总体误差可能掩盖低估风险，未执行行动的反事实不计入观察。",
        baseline="同组样本上的未调整预测与简单固定参考。",
        replay="psychohistory.decision_feedback.FeedbackLab",
        missing_admission=(*_ADMISSION, "真实观察效果，另行用途授权及独立留出审查"),
    ),
    ResearchCandidate(
        candidate_id="R258", version="1.0.0", title="R258 有限随机反馈控制",
        evidence="HISTORICAL_BOUNDED_E1",
        sources=(CandidateSource(
            "research/R258/R258_SCIENTIFIC_REPORT_2026-10-23.md",
            "eb1d1851c73f6c2d8fc2f7ffdf597faf7679d868",
        ),),
        applicability="原 R258 三时格、三状态、二动作及人工伯努利扰动域。",
        inputs="初始状态、人工转移概率、阶段及终点损失。",
        outputs="历史模型范围内的最小期望损失、反馈动作与开环比较。",
        formula="V_t(x)=min_u[c_t(x,u)+E V_(t+1)(x') ]。",
        failure_example="控制动作若读取尚未实现的噪声，便不属于原合法反馈策略。",
        baseline="原冻结协议下的开环策略。",
        replay="参照 R258 冻结报告和既有程序的有理算术复算。",
        missing_admission=(*_ADMISSION, "独立验证向个人决策用途转移的条件"),
    ),
)


def default_candidate_registry() -> CandidateRegistry:
    registry = CandidateRegistry()
    for candidate in _BUILTINS:
        registry.register(candidate)
    return registry
