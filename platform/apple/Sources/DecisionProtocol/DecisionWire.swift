import Foundation

public enum DecisionWire {
    public static let version = "0.8.0"

    public static var encoder: JSONEncoder {
        let encoder = JSONEncoder()
        encoder.keyEncodingStrategy = .convertToSnakeCase
        return encoder
    }

    public static var decoder: JSONDecoder {
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        return decoder
    }

    /// Slice the original input using the engine's half-open Unicode scalar offsets.
    public static func originalSlice(_ original: String, start: Int, end: Int) -> String? {
        let scalars = original.unicodeScalars
        guard start >= 0, start < end, end <= scalars.count else { return nil }
        let lower = scalars.index(scalars.startIndex, offsetBy: start)
        let upper = scalars.index(lower, offsetBy: end - start)
        return String(scalars[lower..<upper])
    }
}

public struct SessionRevision: Codable, Equatable {
    public let sessionId: String
    public let sessionInstance: String
    public let revision: Int

    public init(sessionId: String, sessionInstance: String, revision: Int) {
        self.sessionId = sessionId
        self.sessionInstance = sessionInstance
        self.revision = revision
    }
}

public struct ConversationSnapshot: Decodable {
    public struct Summary: Decodable {
        public let conclusion: String
        public let differences: [String]
        public let unknowns: [String]
        public let question: String?
        public let warning: String?
    }

    public struct State: Decodable {
        public let confirmed: Bool
        public let constraintsConfirmed: Bool
    }

    public struct Claim: Decodable, Identifiable {
        public let id: String
        public let status: String
        public let source: String
        public let kind: String
        public let priorIds: [String]
        public let value: String
        public let unit: String
    }

    public struct Option: Decodable, Identifiable {
        public let id: String
        public let label: String
        public let status: String
    }

    public struct Analysis: Decodable {
        public struct Feasibility: Decodable {
            public let optionId: String
            public let status: String
        }

        public let feasibility: [Feasibility]
        public let temporalScope: [String: String]?
    }

    public struct Receipt: Decodable {
        struct Layers: Decodable {
            struct Preparation: Decodable { let sha256: String }
            struct PartialCalculation: Decodable {
                let parentSha256: String
                let status: String
                let version: String
            }
            let preparation: Preparation
            let partialCalculation: PartialCalculation?
        }

        public let protocolVersion: String
        public let authorityGeneration: Int
        let layers: Layers
        public let sessionId: String
        public let sessionInstance: String
        public let revision: Int

        enum CodingKeys: String, CodingKey {
            case protocolVersion = "protocol"
            case sessionId, sessionInstance, revision, authorityGeneration, layers
        }

        var identity: SessionRevision { .init(sessionId: sessionId, sessionInstance: sessionInstance, revision: revision) }
    }

    public struct Partial: Decodable {
        public struct Check: Decodable {
            public let optionLabel: String
            public let constraintLabel: String
            public let status: String
            public let lower: String
            public let upper: String
            public let `operator`: String
            public let threshold: String
            public let unit: String
            public let horizon: String?
        }

        public struct Difference: Decodable {
            public let label: String
            public let higherOptionLabel: String
            public let lowerOptionLabel: String
            public let amount: String
            public let unit: String
            public let horizon: String?
        }

        public let sessionId: String
        public let sessionInstance: String
        public let revision: Int
        public let version: String
        public let authority: String
        public let status: String
        public let dependencySha256: String
        public let authorityGeneration: Int
        public let checks: [Check]
        public let differences: [Difference]

        var identity: SessionRevision { .init(sessionId: sessionId, sessionInstance: sessionInstance, revision: revision) }
    }

    public let sessionId: String
    public let sessionInstance: String
    public let revision: Int
    public let cancelNonce: String?
    public let phase: String
    public let summary: Summary
    public let state: State
    public let claims: [Claim]
    public let options: [Option]
    public let analysis: Analysis?
    public let result: Receipt
    public let selectedOptionId: String?
    public struct Plan: Decodable { public let trigger: String }
    public let selectedPlan: Plan?
    private let partialAnalysis: Partial?

    public var identity: SessionRevision { .init(sessionId: sessionId, sessionInstance: sessionInstance, revision: revision) }

    public func matches(previous: SessionRevision?, nonce: String?) -> Bool {
        guard protocolMatchesReceipt else { return false }
        if let previous {
            return sessionId == previous.sessionId && sessionInstance == previous.sessionInstance
                && revision > previous.revision && revision - previous.revision == 1
        }
        return revision == 1 && nonce != nil && nonce == cancelNonce
    }

    public var currentPartial: Partial? {
        guard let partialAnalysis, let layer = result.layers.partialCalculation,
              protocolMatchesReceipt, partialAnalysis.identity == identity,
              partialAnalysis.authorityGeneration == result.authorityGeneration,
              partialAnalysis.dependencySha256 == result.layers.preparation.sha256,
              partialAnalysis.dependencySha256 == layer.parentSha256,
              partialAnalysis.version == layer.version, partialAnalysis.status == layer.status,
              partialAnalysis.authority == "NONE", partialAnalysis.status == "DESCRIPTIVE_ONLY",
              partialAnalysis.version == "1.0.0",
              partialAnalysis.dependencySha256.range(of: "^[a-f0-9]{64}$", options: .regularExpression) != nil
        else { return nil }
        return partialAnalysis
    }

    private var protocolMatchesReceipt: Bool {
        result.protocolVersion == DecisionWire.version && result.identity == identity
            && !sessionId.isEmpty && !sessionInstance.isEmpty && revision > 0 && result.authorityGeneration >= 0
    }
}

struct StartRequest: Encodable { let question: String; let cancelNonce: String }
struct CancelRequest: Encodable { let cancelNonce: String }

struct TurnRequest: Encodable {
    let sessionId: String
    let sessionInstance: String
    let revision: Int
    let text: String

    init(session: SessionRevision, text: String) {
        sessionId = session.sessionId
        sessionInstance = session.sessionInstance
        revision = session.revision
        self.text = text
    }
}

public struct ClaimCorrection: Encodable {
    public let claimId: String
    public let supersedes: String

    public init(claimId: String, supersedes: String) {
        self.claimId = claimId
        self.supersedes = supersedes
    }
}

struct ConfirmationRequest: Encodable {
    let sessionId: String
    let sessionInstance: String
    let revision: Int
    let claimIds: [String]
    let optionIds: [String]
    let acceptContext: Bool
    let corrections: [ClaimCorrection]
    let dismissClaimIds: [String]

    init(session: SessionRevision, claimIds: [String], optionIds: [String], acceptContext: Bool,
         corrections: [ClaimCorrection], dismissClaimIds: [String]) {
        sessionId = session.sessionId
        sessionInstance = session.sessionInstance
        revision = session.revision
        self.claimIds = claimIds
        self.optionIds = optionIds
        self.acceptContext = acceptContext
        self.corrections = corrections
        self.dismissClaimIds = dismissClaimIds
    }
}

struct SelectionRequest: Encodable {
    let sessionId: String
    let sessionInstance: String
    let revision: Int
    let optionId: String
    let confirmed = true
    let trigger: String?

    init(session: SessionRevision, optionId: String, trigger: String? = nil) {
        sessionId = session.sessionId
        sessionInstance = session.sessionInstance
        revision = session.revision
        self.optionId = optionId
        self.trigger = trigger
    }
}
