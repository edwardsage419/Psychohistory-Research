import { useState } from 'react';
import type { PlanItem, WorkflowPlan } from './decisionTypes';

const stageLabels: Record<string, string> = { UNDERSTAND: '理解问题', FEASIBILITY: '核对底线', COMPARE: '比较选择', TIMING: '判断时机', REVIEW: '记录与回访' };
const stageStatus: Record<string, string> = { READY: '可进行', NEEDS_INPUT: '待补信息', PENDING: '待开始', COMPLETE: '已完成', NOT_APPLICABLE: '本次无须' };
const priorities = { HIGH: '优先核实', MEDIUM: '影响比较', LOW: '可选补充', DEFERRED: '可暂缓' };
const evidenceLabels: Record<string, string> = { UNKNOWN: '证据待补', CONDITIONAL: '有条件', LOGICAL_INVARIANT: '仅在当前条件下可暂缓', PROVISIONAL_HINT: '待核对提示' };

export function DecisionPlan({ plan, navigate }: { plan: WorkflowPlan; navigate: (item: PlanItem) => void }) {
  const [showDeferred, setShowDeferred] = useState(false);
  const deferred = plan.items.filter(item => item.priority === 'DEFERRED');
  const items = showDeferred ? plan.items : plan.items.filter(item => item.priority !== 'DEFERRED');
  return <section className="decision-plan" aria-label="下一步计划">
    <h3>下一步计划</h3>
    <ol className="decision-stage-list">{plan.steps.map(step => <li key={step.stage} data-stage={step.stage} data-status={step.status}><strong>{stageLabels[step.stage] ?? step.stage}</strong><span>{stageStatus[step.status] ?? step.status}</span></li>)}</ol>
    {!!plan.intent?.hints?.length && <details className="decision-disclosure"><summary>查看待核对的领域提示</summary><ul className="decision-values">{plan.intent.hints.map(hint => <li key={hint.domain}>{hint.prompt}</li>)}</ul></details>}
    {items.length > 0 && <ol className="decision-plan-items">{items.map(item => <li key={item.id} data-plan-item={item.id} data-priority={item.priority} data-evidence-status={item.evidence_status}>
      <div className="decision-plan-item-copy"><span className="decision-priority">{priorities[item.priority as keyof typeof priorities] ?? item.priority}</span><strong>{item.prompt}</strong><p>{item.reason}</p><small>{evidenceLabels[item.evidence_status] ?? item.evidence_status}</small></div>
      <button className="text-button" type="button" onClick={() => navigate(item)}>{item.target.field === 'methods' ? '查看方法审计' : '前往填写'}</button>
    </li>)}</ol>}
    {deferred.length > 0 && <button type="button" className="quiet" aria-expanded={showDeferred} onClick={() => setShowDeferred(value => !value)}>{showDeferred ? '收起暂缓事项' : `查看暂缓事项（${deferred.length}）`}</button>}
    {plan.can_run.length > 0 && <p className="muted">当前输入支持的方法：{plan.can_run.map(method => method.title).join('、')}</p>}
  </section>;
}
