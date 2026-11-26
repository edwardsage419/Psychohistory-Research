import type { Analysis, DecisionState } from './decisionTypes';

export type Claim = {
  id: string;
  kind: string;
  evidence_kind: string;
  field: string;
  subject: string;
  value: string;
  unit: string;
  source: string;
  status: string;
  prior_ids: string[];
  supersedes: string | null;
};

export type ConversationOption = { id: string; label: string; status: 'PROVISIONAL' | 'CONFIRMED' };
export type ConversationSummary = {
  conclusion: string;
  differences: string[];
  unknowns: string[];
  question: string | null;
  warning: string | null;
  focus: string | null;
};
export type ConversationView = {
  session_id: string;
  revision: number;
  dialogue: { role: 'user' | 'assistant'; text: string }[];
  summary: ConversationSummary;
  claims: Claim[];
  options: ConversationOption[];
  analysis: Analysis | null;
  state: DecisionState;
  phase: 'CLARIFY' | 'ANALYZED';
  local_model_status: string;
  result: { session_id: string; revision: number; protocol: string; cutoff: string; receipt_sha256: string };
  knowledge: {
    methods: { method: string; title?: string; requirements?: { id: string; description: string }[] }[];
    search: { hits: { card: { title: string; path: string; version: string; applicability_boundary: string | null }; snippet: string }[] };
  } | null;
  resources: {
    state: unknown;
    result: {
      cash: { status: string; balance?: string; currency?: string };
      options: Record<string, { status: string; cash: { margin?: string }; time: { reason?: string } }>;
    };
    reused: boolean;
  } | null;
  semantic: { blocking_obligations: { id: string; source: string }[] };
  selected_option_id: string | null;
  selected_plan: { option_id: string; trigger: string } | null;
  changes: string[];
};
export type ConversationStatus = {
  local_model: { status: string; enabled: boolean };
  purpose_consent: Record<string, { available: boolean; authorized: boolean }>;
};
