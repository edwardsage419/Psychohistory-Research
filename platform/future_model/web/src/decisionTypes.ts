export type DecisionVersion = 'v4' | 'v5';
export type PersonalApiVersion = DecisionVersion | 'v6' | 'v7';
export type Api = <T>(path: string, body?: unknown, version?: PersonalApiVersion, signal?: AbortSignal) => Promise<T>;
export const decisionPath = 'decisions';

export class DecisionApiError extends Error {
  constructor(message: string, readonly status: number) { super(message); }
}

export type ValueKind = 'fact' | 'estimate' | 'assumption' | 'synthetic' | 'unknown';
export const kindLabels: Record<ValueKind, string> = {
  fact: '事实', estimate: '估计', assumption: '假设', synthetic: '合成', unknown: '未知',
};
export type Quantity = { lower: number | string | null; upper: number | string | null; unit: string; kind: ValueKind; source: string; horizon?: string | null };
export type Bounds = { lower: number | string; upper: number | string };
export type Objective = { id: string; label: string; unit: string; direction: 'max' | 'min' };
export type Constraint = { id: string; label: string; unit: string; operator: '>=' | '>' | '<=' | '<'; threshold: number | string; source: string; horizon?: string | null };
export type Option = { id: string; label: string; measurements: Record<string, Quantity>; scores: Record<string, Quantity> };
export type Scenario = { id: string; label: string; utilities: Record<string, Quantity>; kind: ValueKind; source: string; probability: null };
export type Numeric = number | string;
export type EvidenceItem = { id: string; label: string; kind: ValueKind; source: string; verification: 'user_supplied' | 'user_confirmed' | 'unverified'; scope: string };
export type SourcedRange = { lower: Numeric | null; upper: Numeric | null; kind: ValueKind; source: string };
export type InformationInput = {
  signals: { id: string; label: string }[];
  prior: Record<string, SourcedRange>;
  likelihoods: Record<string, Record<string, SourcedRange>>;
  cost: Quantity | null;
  actions_by_signal: Record<string, { option_ids: string[]; kind: ValueKind; source: string }>;
  unrestricted_actions: boolean;
  action_source: string;
  parameter_domain: 'unknown' | 'rectangle' | 'constrained';
  parameter_domain_source: string;
  timing_basis: string | null;
  fixed_policy?: Record<string, string>;
  verification_source?: string | null;
};
export type Cutoff = { at: Numeric; inclusive: boolean; kind: ValueKind; source: string };
export type TimingAction = { cutoff: Cutoff | null; switching_cost: SourcedRange | null; delay_losses: Record<string, SourcedRange>; reversibility: { description: string; kind: ValueKind; source: string } | null };
export type Investigation = {
  mode: 'deterministic' | 'joint' | 'conditional'; cost: SourcedRange | null; duration: SourcedRange | null; kind: ValueKind; source: string;
  joint: { scenario_id: string; signal_id: string; duration: Numeric; probability: Numeric }[];
  completion_by_state: Record<string, { duration: Numeric; probability: Numeric }[]>;
};
export type TimingInput = {
  confirmed: boolean; time_unit: string | null; time_origin: string | null; horizon: Cutoff | null; decision_deadline: Cutoff | null; desired_time: SourcedRange | null;
  predicted_completion: SourcedRange | null; wait_duration: SourcedRange | null; actions: Record<string, TimingAction>;
  status_quo_option_id: string | null; fallback_option_id: string | null; investigation: Investigation | null;
};
export type PreferenceSnapshot = { values: { label: string; value: string }[]; applicability: string; provenance: string; adopted_version_id: string | null };
export type PreferenceVersion = { version_id: string; adopted_at: string; decision_id: string; review_index: number; source_kind: string; preferences: PreferenceSnapshot };
export type DecisionState = {
  schema_version: '1.0.0'; decision_id: string; revision: number; question: string; confirmed: boolean;
  deadline: string | null; constraints_confirmed: boolean; objectives: Objective[]; constraints: Constraint[];
  options: Option[]; weights_confirmed: boolean; weights: Record<string, Bounds>; score_basis: string | null;
  score_dependence: string; score_dependence_source: string | null; score_transform: string; shared_offsets: Record<string, Bounds>;
  shared_offset_dependence: string; scenarios: Scenario[]; scenario_basis: string | null;
  scenario_dependence: string; scenario_dependence_source: string | null;
  precision_radius: number | string | null; reference_option_id: string | null;
  workflow_version?: '0.5.0'; intent?: string | null; evidence?: EvidenceItem[]; information?: InformationInput | null; timing?: TimingInput | null;
  intended_option_id?: string | null; plan_note?: string | null; preferences?: PreferenceSnapshot | null;
};
export type Question = { field: string; prompt: string };
export type Understanding = { mode: string; message: string; suggestions: { field: string; value: string; source: string }[] };
export type PlanItem = {
  id: string; category: string; action: string; priority: string; prompt: string; reason: string;
  target: { field: string; [key: string]: unknown }; evidence_status: string;
};
export type WorkflowPlan = { intent?: { description: string | null; hints: { domain: string; prompt: string; evidence_status: string }[] }; steps: { stage: string; status: string }[]; items: PlanItem[]; can_run: { model_id: string; title: string }[] };
export type StartResponse = { state: DecisionState; questions: Question[]; understanding: Understanding; plan?: WorkflowPlan };
export type DecisionTable = { title: string; columns: string[]; rows: unknown[] };
export type DecisionChart = { title: string; unit: string; rows: { label: string; lower: number | string; upper: number | string }[] };
export type DecisionMethod = {
  model_id: string; version: string; title: string; status: string; reasons?: unknown;
  result?: { summary?: unknown; tables?: DecisionTable[]; charts?: DecisionChart[]; [key: string]: unknown } | null;
  [key: string]: unknown;
};
export type Analysis = {
  decision_id: string; revision: number; input_hash: string; hub_version: string; status: string;
  questions: Question[]; feasibility: { option_id: string; label: string; status: string; checks: { constraint_id: string; status: string; reason: string }[] }[];
  methods: DecisionMethod[]; advice: unknown; risks: unknown; gaps: unknown; priority_gap: string | null; plan?: WorkflowPlan; execution?: { available: boolean; authorization: string; action_endpoint: string }; temporal_scope?: Record<string, string>;
};
export type Consent = { authorized: boolean; epoch: string | null };
export type HistoryItem = { decision_id: string; question: string; revision: number };
export type DecisionRecord = {
  decision_id: string;
  snapshots: { decision_id: string; revision: number; state: DecisionState; analysis: Analysis | null; confirmed_at: string }[];
  action: { option_id: string; occurred_at: string; recorded_at: string; revision: number; coverage: unknown } | null;
  reviews: { option_id: string; observation: string; observed_at: string; kind: string; recorded_at: string; hindsight?: { evidence: string | null; process_quality?: string | null; current_preferences: PreferenceSnapshot | null }; adopted_preferences?: PreferenceVersion }[];
};
export type RestoreResponse = { mode: 'preview' | 'restored'; isolated: boolean; eligible?: boolean; decision_count: number; reason?: string };

export const newId = () => crypto.randomUUID();
export const emptyQuantity = (unit: string): Quantity => ({ lower: null, upper: null, unit, kind: 'unknown', source: '' });

export const demoQuestion = '我想在周六的短途火车和长途巴士之间选一个，预算不超过 160 元，比较节省时间和行程舒适度。';
export function demoState(state: DecisionState): DecisionState {
  const source = '虚构周末出行案例 · 示例数据';
  const quantity = (lower: number, upper: number, unit: string): Quantity => ({ lower, upper, unit, kind: 'synthetic', source });
  return {
    ...state,
    deadline: '周五晚订票',
    constraints_confirmed: true,
    constraints: [{ id: 'budget', label: '预算上限', unit: '元', operator: '<=', threshold: 160, source }],
    objectives: [
      { id: 'time', label: '节省时间', unit: '分', direction: 'max' },
      { id: 'comfort', label: '舒适度', unit: '分', direction: 'max' },
    ],
    options: [
      { id: 'train', label: '短途火车', measurements: { budget: quantity(130, 150, '元') }, scores: { time: quantity(0.8, 0.9, '分'), comfort: quantity(0.5, 0.6, '分') } },
      { id: 'bus', label: '长途巴士', measurements: { budget: quantity(80, 95, '元') }, scores: { time: quantity(0.4, 0.5, '分'), comfort: quantity(0.7, 0.8, '分') } },
    ],
    weights_confirmed: true,
    weights: { time: { lower: 0.55, upper: 0.75 }, comfort: { lower: 0.25, upper: 0.45 } },
    score_basis: '虚构案例的共同评分量表，0 分最差，1 分最好。',
    score_dependence: 'rectangle',
    score_dependence_source: '示例假设，独立使用各个评分区间的端点。',
    score_transform: 'identity',
    shared_offsets: {},
    shared_offset_dependence: 'unknown',
    scenarios: [
      { id: 'normal', label: '正常运行', utilities: { train: quantity(0.8, 0.9, '效用'), bus: quantity(0.7, 0.8, '效用') }, kind: 'synthetic', source, probability: null },
      { id: 'delay', label: '火车晚点', utilities: { train: quantity(0.35, 0.5, '效用'), bus: quantity(0.65, 0.75, '效用') }, kind: 'synthetic', source, probability: null },
    ],
    scenario_basis: '示例综合效用，0 最差，1 最好。同一情景使用相同量表。',
    scenario_dependence: 'rectangle',
    scenario_dependence_source: '示例假设，压力情景的区间端点可独立组合。',
    precision_radius: 0.05,
    reference_option_id: 'bus',
  };
}
