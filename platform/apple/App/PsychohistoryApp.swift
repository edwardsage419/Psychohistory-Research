import DecisionProtocol
import SwiftUI

@main
struct PsychohistoryApp: App {
    var body: some Scene {
        WindowGroup { DecisionScreen() }
    }
}

@MainActor
private struct DecisionScreen: View {
    @Environment(\.scenePhase) private var scenePhase
    @State private var endpoint = DecisionScreen.defaultEndpoint
    @State private var token = ""
    @State private var engine: LocalEngine?
    @State private var snapshot: ConversationSnapshot?
    @State private var pendingNonce: String?
    @State private var request: Task<Void, Never>?
    @State private var generation = 0
    @State private var draft = ""
    @State private var lastInput = ""
    @State private var failure: String?
    @State private var stale = false
    @State private var choice: ConversationSnapshot.Option?
    @State private var trigger = ""

    private static var defaultEndpoint: String {
        #if os(macOS)
        "http://127.0.0.1:8765"
        #else
        ""
        #endif
    }

    var body: some View {
        NavigationStack {
            if scenePhase == .active {
                ScrollView {
                    VStack(alignment: .leading, spacing: 18) {
                        if let engine { conversation(engine) } else { connectForm }
                        if request != nil { ProgressView("正在等待本地服务…") }
                        if let failure { Text(failure).foregroundStyle(.red).accessibilityAddTraits(.updatesFrequently) }
                    }
                    .frame(maxWidth: 680, alignment: .leading)
                    .padding(24)
                    .frame(maxWidth: .infinity)
                }
                .navigationTitle("个人决策")
                .toolbar {
                    if engine != nil {
                        Button("断开连接") { close(disconnect: true) }
                    }
                }
            } else {
                Text("本地决策内容已隐藏")
            }
        }
        .onChange(of: scenePhase) { _, phase in
            if phase == .background { close(disconnect: true) }
        }
        .onDisappear { close(disconnect: true) }
        .confirmationDialog("确认你的选择", isPresented: Binding(
            get: { choice != nil }, set: { if !$0 { choice = nil } }
        ), presenting: choice) { option in
            Button("选择\(option.label)") {
                if let engine, let snapshot, !stale {
                    update { try await engine.select(option.id, session: snapshot.identity) }
                }
            }
        } message: { _ in Text("记录你的选择，实际行动仍由你决定。") }
    }

    private var connectForm: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("连接你的本地工作空间").font(.title2.bold())
            #if os(iOS)
            Text("需要已由你配置的专用 HTTPS 决策服务。连接中断时，手机暂时无法计算。")
                .foregroundStyle(.secondary)
            #else
            Text("先启动本地 v0.8 工作台，再输入该工作空间的访问令牌。")
                .foregroundStyle(.secondary)
            #endif
            TextField("本地服务地址", text: $endpoint).textFieldStyle(.roundedBorder)
            SecureField("访问令牌", text: $token).textFieldStyle(.roundedBorder)
            Button("连接") {
                do {
                    let client = try LocalEngine(endpoint: LocalEngineEndpoint(endpoint), token: token)
                    let ticket = generation
                    failure = nil
                    request = Task {
                        do {
                            try await client.verifyConnection()
                            if generation == ticket && !Task.isCancelled {
                                engine = client
                                token = ""
                            }
                        } catch {
                            if generation == ticket && !Task.isCancelled { failure = error.localizedDescription }
                        }
                        if generation == ticket { request = nil }
                    }
                } catch { failure = error.localizedDescription }
            }
            .buttonStyle(.borderedProminent)
            .disabled(request != nil || endpoint.isEmpty || token.isEmpty)
            Text("仅在你点击连接后访问指定地址。令牌和临时对话仅保存在本次应用会话的内存中。")
                .font(.footnote).foregroundStyle(.secondary)
        }
    }

    @ViewBuilder private func conversation(_ client: LocalEngine) -> some View {
        if stale {
            Text("当前结果已失效。开始新决策后可以重新核对条件。").font(.headline)
        } else if let snapshot, request == nil {
            if !lastInput.isEmpty { Text(lastInput).font(.callout).foregroundStyle(.secondary) }
            if let warning = snapshot.summary.warning { Text(warning).foregroundStyle(.secondary) }
            Text(snapshot.summary.conclusion).font(.title3.bold())
            strings(snapshot.summary.differences)
            strings(snapshot.summary.unknowns)
            if let question = snapshot.summary.question { Text(question).font(.headline) }
            if let partial = snapshot.currentPartial { PartialResult(partial: partial) }
            if !snapshot.claims.filter({ $0.status == "PROVISIONAL" }).isEmpty
                || snapshot.options.contains(where: { $0.status == "PROVISIONAL" })
                || !snapshot.state.confirmed || !snapshot.state.constraintsConfirmed {
                ConfirmEvidence(snapshot: snapshot) { review in
                    update {
                        try await client.confirm(session: snapshot.identity, claims: review.claims, options: review.options,
                                                 context: review.context, corrections: review.corrections, dismissals: review.dismissals)
                    }
                }
                .id(snapshot.revision)
            }
            if snapshot.state.confirmed && snapshot.state.constraintsConfirmed {
                Button("计算并比较") { update { try await client.analyze(session: snapshot.identity) } }
            }
            if let analysis = snapshot.analysis {
                Text("方案可行性").font(.headline)
                ForEach(snapshot.options) { option in
                    if let status = analysis.feasibility.first(where: { $0.optionId == option.id })?.status {
                        HStack {
                            Text(option.label)
                            Spacer()
                            Text(feasibilityName(status)).foregroundStyle(.secondary)
                            if snapshot.selectedOptionId == option.id {
                                Text("你已选择")
                            } else if status == "ACCEPT" && (analysis.temporalScope?[option.id] ?? "FEASIBLE") == "FEASIBLE" {
                                Button("选择") { choice = option }
                            }
                        }
                    }
                }
            }
            if let selected = snapshot.selectedOptionId {
                TextField("条件计划，例如达到收入门槛后再行动", text: $trigger, axis: .vertical)
                    .textFieldStyle(.roundedBorder).lineLimit(2...4)
                Button("确认条件计划") {
                    let text = trigger
                    update { try await client.plan(text, optionId: selected, session: snapshot.identity) }
                }
                .disabled(trigger.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty || trigger.unicodeScalars.count > 400)
                if let plan = snapshot.selectedPlan { Text(plan.trigger).font(.callout) }
            }
        }
        if !stale {
            TextField(snapshot == nil ? "你正在考虑什么？" : "补充或修正", text: $draft, axis: .vertical)
                .textFieldStyle(.roundedBorder)
                .lineLimit(3...8)
                .disabled(request != nil)
            Button(snapshot == nil ? "开始对话" : "发送") {
                let text = draft
                if let snapshot { update(input: text) { try await client.turn(text, session: snapshot.identity) } }
                else {
                    let nonce = LocalEngine.cancellationNonce()
                    pendingNonce = nonce
                    update(input: text, start: (client, nonce)) { try await client.start(text, nonce: nonce) }
                }
            }
            .buttonStyle(.borderedProminent)
            .disabled(request != nil || draft.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty || draft.unicodeScalars.count > 6000)
        }
        if snapshot != nil || pendingNonce != nil || stale {
            Button("开始新决策") { close(disconnect: false) }
        }
        Text("此应用使用同一离线决策引擎。历史记录、导出与撤回可在本地 Web 工作台操作。")
            .font(.footnote).foregroundStyle(.secondary)
    }

    @ViewBuilder private func strings(_ values: [String]) -> some View {
        ForEach(Array(values.enumerated()), id: \.offset) { row in Text(row.element) }
    }

    private func feasibilityName(_ status: String) -> String {
        switch status {
        case "ACCEPT": "通过底线"
        case "REJECT": "未通过底线"
        default: "底线待核实"
        }
    }

    private func update(input: String? = nil, start: (LocalEngine, String)? = nil, _ perform: @escaping () async throws -> ConversationSnapshot) {
        let ticket = generation
        failure = nil
        request = Task {
            guard generation == ticket else { return }
            do {
                let next = try await perform()
                if generation == ticket && !Task.isCancelled {
                    snapshot = next
                    pendingNonce = nil
                    if let input {
                        lastInput = input
                        draft = ""
                        trigger = ""
                    }
                } else if let (client, _) = start {
                    try? await client.end(next.identity)
                }
            } catch {
                if let (client, nonce) = start { try? await client.cancelStart(nonce) }
                if generation == ticket && !Task.isCancelled {
                    failure = error.localizedDescription
                    stale = snapshot != nil
                    pendingNonce = nil
                }
            }
            if generation == ticket { request = nil }
        }
    }

    private func close(disconnect: Bool) {
        generation += 1
        let nonce = pendingNonce
        let abandon = disconnect || request != nil || stale
        if nonce == nil { request?.cancel() }
        request = nil
        if let engine {
            if let nonce { Task { try? await engine.cancelStart(nonce) } }
            else if let identity = snapshot?.identity {
                Task {
                    if abandon { try? await engine.discard(identity) }
                    else { try? await engine.end(identity) }
                }
            }
        }
        pendingNonce = nil
        snapshot = nil
        lastInput = ""
        draft = ""
        choice = nil
        trigger = ""
        failure = nil
        stale = false
        if disconnect {
            engine = nil
            token = ""
        }
    }
}
