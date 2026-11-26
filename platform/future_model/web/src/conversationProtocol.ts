export type ConversationApiVersion = 'v7' | 'v8';
export type SessionRevision = { session_id: string; revision: number; session_instance?: string };
export type PendingConversation = { cancel_nonce: string };
export type ConversationHandle = PendingConversation | SessionRevision;
type ConditionalCheck = {
  option_label: string; constraint_label: string; status: string;
  lower: string; upper: string; operator: string; threshold: string; unit: string; horizon: string | null;
};
type PointDifference = {
  label: string; higher_option_label: string; lower_option_label: string;
  amount: string; unit: string; horizon: string | null;
};
export type PartialAnalysis = SessionRevision & {
  version: string; authority: string; status: string; dependency_sha256: string; authority_generation: number;
  checks: ConditionalCheck[]; differences: PointDifference[];
};

export type RevisionReceipt = SessionRevision & {
  protocol: string;
  authority_generation?: number;
  layers?: {
    preparation: { sha256: string };
    partial_calculation?: { status: string; parent_sha256: string; version: string };
  };
};
type VerifiedView = SessionRevision & {
  cancel_nonce?: string;
  result: RevisionReceipt;
  partial_analysis?: PartialAnalysis | null;
};

export function mutationIdentity({ session_id, revision, session_instance }: SessionRevision, version: ConversationApiVersion) {
  if (version === 'v7') return { session_id, revision };
  if (!session_instance) throw new Error('此会话已失效，请重新开启。');
  return { session_id, session_instance, revision };
}

export function closingRequest(handle: ConversationHandle, version: ConversationApiVersion, discard = false) {
  if ('cancel_nonce' in handle) {
    return version === 'v8'
      ? { operation: 'cancel-start', body: { cancel_nonce: handle.cancel_nonce } }
      : { operation: 'end', body: { session_id: handle.cancel_nonce } };
  }
  return version === 'v8'
    ? { operation: discard ? 'discard' : 'end', body: mutationIdentity(handle, version) }
    : { operation: 'end', body: { session_id: handle.session_id } };
}

export function acceptConversationView(next: VerifiedView, current: SessionRevision | null, nonce: string | null, version: ConversationApiVersion) {
  if (!next.session_id || next.revision !== (current?.revision ?? 0) + 1
      || next.result.session_id !== next.session_id || next.result.revision !== next.revision
      || next.result.protocol !== (version === 'v8' ? '0.8.0' : '0.7.0')) return false;
  if (current && next.session_id !== current.session_id) return false;
  if (version === 'v7') return true;
  const generation = next.result.authority_generation;
  return !!next.session_instance && next.result.session_instance === next.session_instance
    && typeof generation === 'number' && Number.isSafeInteger(generation) && generation >= 0
    && (current ? next.session_instance === current.session_instance : !!nonce && next.cancel_nonce === nonce);
}

export function partialObservations(view: VerifiedView): string[] {
  const partial = view.partial_analysis;
  const layer = view.result.layers?.partial_calculation;
  if (!partial || partial.authority !== 'NONE' || partial.status !== 'DESCRIPTIVE_ONLY'
      || partial.version !== '1.0.0' || !/^[a-f0-9]{64}$/.test(partial.dependency_sha256)
      || !Number.isSafeInteger(partial.authority_generation) || partial.authority_generation < 0
      || partial.authority_generation !== view.result.authority_generation
      || partial.dependency_sha256 !== view.result.layers?.preparation?.sha256
      || layer?.parent_sha256 !== partial.dependency_sha256
      || layer.status !== partial.status || layer.version !== partial.version
      || view.result.protocol !== '0.8.0' || view.result.session_id !== view.session_id
      || view.result.session_instance !== view.session_instance || view.result.revision !== view.revision
      || partial.session_id !== view.session_id || !partial.session_instance
      || partial.session_instance !== view.session_instance || partial.revision !== view.revision
      || !Array.isArray(partial.checks) || !Array.isArray(partial.differences)) return [];
  const horizon = (value: string | null) => value ? `（${value}）` : '';
  return [
    ...partial.checks.filter(check => check.status === 'CONDITIONAL_VIOLATION').map(check => {
      const measure = check.lower === check.upper ? check.lower : `${check.lower}–${check.upper}`;
      return `${check.option_label}在已知条件下与「${check.constraint_label}」冲突。观测范围 ${measure} ${check.unit}，条件为 ${check.operator} ${check.threshold} ${check.unit}${horizon(check.horizon)}。`;
    }),
    ...partial.differences.map(item =>
      `${item.label}相差 ${item.amount} ${item.unit}。${item.higher_option_label}的数值高于${item.lower_option_label}${horizon(item.horizon)}。`),
  ];
}
