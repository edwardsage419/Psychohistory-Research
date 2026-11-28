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
