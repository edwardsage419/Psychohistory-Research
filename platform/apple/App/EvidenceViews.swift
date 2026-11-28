import DecisionProtocol
import SwiftUI

struct EvidenceReview {
    let claims: [String]
    let options: [String]
    let context: Bool
    let corrections: [ClaimCorrection]
    let dismissals: [String]
}

struct ConfirmEvidence: View {
    private enum ClaimDecision: Hashable { case pending, confirm, dismiss }
    let snapshot: ConversationSnapshot
    let confirm: (EvidenceReview) -> Void
    @State private var decisions: [String: ClaimDecision] = [:]
    @State private var replacements: [String: String] = [:]
    @State private var options: Set<String> = []
    @State private var context = false

    private var pending: [ConversationSnapshot.Claim] { snapshot.claims.filter { $0.status == "PROVISIONAL" } }

    private var incompleteCorrection: Bool {
        pending.contains { claim in
            decisions[claim.id] == .confirm && claim.kind == "revision" && !claim.priorIds.isEmpty
                && replacements[claim.id, default: ""].isEmpty
        }
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("核对与确认").font(.headline)
            ForEach(pending) { claim in claimRow(claim) }
            ForEach(snapshot.options.filter { $0.status == "PROVISIONAL" }) { option in
                Toggle("考虑\(option.label)", isOn: selection(option.id))
            }
            Toggle("我已说明本次目的和硬约束", isOn: $context)
            Button("确认所选内容", action: submit)
                .disabled((!decisions.values.contains(where: { $0 != .pending }) && options.isEmpty && !context)
                          || incompleteCorrection)
        }
    }

    private func claimRow(_ claim: ConversationSnapshot.Claim) -> some View {
        let decision = Binding<ClaimDecision>(get: { decisions[claim.id, default: .pending] }, set: { decisions[claim.id] = $0 })
        let prior = Binding<String>(get: { replacements[claim.id, default: ""] }, set: { replacements[claim.id] = $0 })
        return VStack(alignment: .leading, spacing: 4) {
            Picker(readback(claim), selection: decision) {
                Text("继续核实").tag(ClaimDecision.pending)
                Text("确认").tag(ClaimDecision.confirm)
                Text("略过这项理解").tag(ClaimDecision.dismiss)
            }
            if decision.wrappedValue == .confirm && !claim.priorIds.isEmpty {
                Picker("要替换的此前内容", selection: prior) {
                    Text("暂不替换").tag("")
                    ForEach(claim.priorIds, id: \.self) { id in
                        if let previous = snapshot.claims.first(where: { $0.id == id }) {
                            Text(readback(previous)).tag(id)
                        }
                    }
                }
            }
        }
    }

    private func readback(_ claim: ConversationSnapshot.Claim) -> String {
        claim.source.isEmpty ? "\(claim.value) \(claim.unit)" : claim.source
    }

    private func selection(_ id: String) -> Binding<Bool> {
        Binding(get: { options.contains(id) }, set: { checked in
            if checked { options.insert(id) }
            else { options.remove(id) }
        })
    }

    private func submit() {
        let accepted = pending.filter { decisions[$0.id] == .confirm }
        let corrections = accepted.compactMap { claim -> ClaimCorrection? in
            guard let replaced = replacements[claim.id], !replaced.isEmpty else { return nil }
            return .init(claimId: claim.id, supersedes: replaced)
        }
        confirm(.init(claims: accepted.map(\.id), options: options.sorted(), context: context,
                      corrections: corrections, dismissals: pending.filter { decisions[$0.id] == .dismiss }.map(\.id)))
    }
}

struct PartialResult: View {
    let partial: ConversationSnapshot.Partial

    var body: some View {
        VStack(alignment: .leading, spacing: 7) {
            Text("已核对的局部分析").font(.headline)
            Text("仅适用于已核对的条件。仍需补充信息才能比较完整方案。")
                .foregroundStyle(.secondary)
            ForEach(Array(partial.checks.filter { $0.status == "CONDITIONAL_VIOLATION" }.enumerated()), id: \.offset) { row in
                let check = row.element
                let value = check.lower == check.upper ? check.lower : "\(check.lower)–\(check.upper)"
                Text("\(check.optionLabel)与「\(check.constraintLabel)」冲突。观测范围 \(value) \(check.unit)，条件为 \(check.operator) \(check.threshold) \(check.unit)\(time(check.horizon))。")
            }
            ForEach(Array(partial.differences.enumerated()), id: \.offset) { row in
                let difference = row.element
                Text("\(difference.label)相差 \(difference.amount) \(difference.unit)。\(difference.higherOptionLabel)的数值高于\(difference.lowerOptionLabel)\(time(difference.horizon))。")
            }
        }
        .padding()
        .background(.secondary.opacity(0.1), in: RoundedRectangle(cornerRadius: 12))
    }

    private func time(_ horizon: String?) -> String { horizon.map { "（\($0)）" } ?? "" }
}
