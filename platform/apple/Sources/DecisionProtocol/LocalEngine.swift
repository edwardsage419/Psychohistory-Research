import Foundation
#if canImport(FoundationNetworking)
import FoundationNetworking
#endif

public enum LocalEngineError: LocalizedError {
    case endpoint, credential, connection, version, receipt
    case rejected(Int)

    public var errorDescription: String? {
        switch self {
        case .endpoint: return "请输入环回服务地址或已由你控制的专用 HTTPS 服务地址。"
        case .credential: return "请核对本地访问令牌。"
        case .connection: return "无法连接本地服务。请核对服务是否正在运行以及其连接设置。"
        case .version: return "此客户端需要 v0.8 决策协议。"
        case .receipt: return "返回内容与当前会话不一致，请重新开启决策。"
        case .rejected(let status):
            switch status {
            case 401, 403: return "请求未获授权。请重新连接并核对权限。"
            case 404, 409, 410, 422: return "当前版本或条件无法完成此操作，请核对并重新开启决策。"
            default: return "本地服务未完成操作（\(status)）。"
            }
        }
    }
}

public struct LocalEngineEndpoint {
    public let url: URL

    public init(_ text: String) throws {
        guard let components = URLComponents(string: text.trimmingCharacters(in: .whitespacesAndNewlines)),
              let host = components.host, let scheme = components.scheme?.lowercased(),
              components.user == nil, components.password == nil,
              components.query == nil, components.fragment == nil,
              components.percentEncodedPath.isEmpty || components.percentEncodedPath == "/",
              components.port.map({ (1...65535).contains($0) }) ?? true,
              let url = components.url
        else { throw LocalEngineError.endpoint }
        let octets = host.split(separator: ".", omittingEmptySubsequences: false).compactMap { piece -> UInt8? in
            guard let value = UInt8(piece), String(value) == String(piece) else { return nil }
            return value
        }
        let isCanonicalIPv4 = octets.count == 4 && octets.map(String.init).joined(separator: ".") == host
        guard isCanonicalIPv4 else { throw LocalEngineError.endpoint }
        let loopback = host == "127.0.0.1"
        let privateNetwork = octets[0] == 10 || (octets[0] == 172 && (16...31).contains(octets[1]))
            || (octets[0] == 192 && octets[1] == 168)
        guard (loopback && (scheme == "http" || scheme == "https")) || (privateNetwork && scheme == "https")
        else { throw LocalEngineError.endpoint }
        self.url = url
    }
}

private final class NoRedirects: NSObject, URLSessionTaskDelegate {
    func urlSession(_ session: URLSession, task: URLSessionTask,
                    willPerformHTTPRedirection response: HTTPURLResponse, newRequest request: URLRequest,
                    completionHandler: @escaping (URLRequest?) -> Void) {
        completionHandler(nil)
    }
}

public final class LocalEngine {
    private struct Status: Decodable { let conversationVersion: String }
    private struct Empty: Codable {}

    private let endpoint: LocalEngineEndpoint
    private let token: String
    private let network: URLSession

    public init(endpoint: LocalEngineEndpoint, token: String) throws {
        let credential = token.trimmingCharacters(in: .whitespacesAndNewlines)
        guard credential.range(of: "^[A-Za-z0-9_-]{1,128}$", options: .regularExpression) != nil
        else { throw LocalEngineError.credential }
        self.endpoint = endpoint
        self.token = credential
        let configuration = URLSessionConfiguration.ephemeral
        configuration.urlCache = nil
        configuration.httpCookieStorage = nil
        configuration.urlCredentialStorage = nil
        configuration.httpShouldSetCookies = false
        configuration.requestCachePolicy = .reloadIgnoringLocalCacheData
        configuration.timeoutIntervalForResource = 30
        self.network = URLSession(configuration: configuration, delegate: NoRedirects(), delegateQueue: nil)
    }

    deinit { network.invalidateAndCancel() }

    public static func cancellationNonce() -> String {
        UUID().uuidString.lowercased().replacingOccurrences(of: "-", with: "")
    }

    public func verifyConnection() async throws {
        let status: Status = try await send("status", body: Optional<Empty>.none)
        guard status.conversationVersion == DecisionWire.version else { throw LocalEngineError.version }
    }

    public func start(_ question: String, nonce: String) async throws -> ConversationSnapshot {
        try await update("start", body: StartRequest(question: question, cancelNonce: nonce), previous: nil, nonce: nonce)
    }

    public func turn(_ text: String, session: SessionRevision) async throws -> ConversationSnapshot {
        try await update("turn", body: TurnRequest(session: session, text: text), previous: session)
    }

    public func confirm(session: SessionRevision, claims: [String], options: [String], context: Bool,
                        corrections: [ClaimCorrection] = [], dismissals: [String] = []) async throws -> ConversationSnapshot {
        let body = ConfirmationRequest(session: session, claimIds: claims, optionIds: options, acceptContext: context,
                                       corrections: corrections, dismissClaimIds: dismissals)
        return try await update("confirm", body: body, previous: session)
    }

    public func analyze(session: SessionRevision) async throws -> ConversationSnapshot {
        try await update("analyze", body: session, previous: session)
    }

    public func select(_ optionId: String, session: SessionRevision) async throws -> ConversationSnapshot {
        try await update("select", body: SelectionRequest(session: session, optionId: optionId), previous: session)
    }

    public func plan(_ trigger: String, optionId: String, session: SessionRevision) async throws -> ConversationSnapshot {
        try await update("plan", body: SelectionRequest(session: session, optionId: optionId, trigger: trigger), previous: session)
    }

    public func end(_ session: SessionRevision) async throws {
        let _: Empty = try await send("end", body: session)
    }

    public func discard(_ session: SessionRevision) async throws {
        let _: Empty = try await send("discard", body: session)
    }

    public func cancelStart(_ nonce: String) async throws {
        let _: Empty = try await send("cancel-start", body: CancelRequest(cancelNonce: nonce))
    }

    private func update<Body: Encodable>(_ operation: String, body: Body, previous: SessionRevision?, nonce: String? = nil) async throws -> ConversationSnapshot {
        let next: ConversationSnapshot = try await send(operation, body: body)
        guard next.matches(previous: previous, nonce: nonce) else { throw LocalEngineError.receipt }
        return next
    }

    private func send<Body: Encodable, Response: Decodable>(_ operation: String, body: Body?) async throws -> Response {
        let url = ["api", "v8", "decisions", operation].reduce(endpoint.url) { $0.appendingPathComponent($1) }
        var request = URLRequest(url: url)
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Accept")
        if let body {
            request.httpMethod = "POST"
            request.setValue("application/json", forHTTPHeaderField: "Content-Type")
            request.httpBody = try DecisionWire.encoder.encode(body)
        }
        let data: Data
        let response: URLResponse
        do {
            (data, response) = try await network.data(for: request)
        } catch {
            try Task.checkCancellation()
            throw LocalEngineError.connection
        }
        try Task.checkCancellation()
        guard let http = response as? HTTPURLResponse else { throw LocalEngineError.connection }
        guard (200..<300).contains(http.statusCode) else { throw LocalEngineError.rejected(http.statusCode) }
        guard data.count <= 4 * 1024 * 1024 else { throw LocalEngineError.receipt }
        do {
            return try DecisionWire.decoder.decode(Response.self, from: data)
        } catch {
            throw LocalEngineError.receipt
        }
    }
}
