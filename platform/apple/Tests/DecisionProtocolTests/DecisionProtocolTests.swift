import Foundation
import XCTest
@testable import DecisionProtocol

final class DecisionProtocolTests: XCTestCase {
    func testTransportAcceptsLoopbackAndExplicitPrivateHTTPSOnly() throws {
        let loopback = try LocalEngineEndpoint("http://127.0.0.1:8765")
        XCTAssertEqual(loopback.url.absoluteString, "http://127.0.0.1:8765")
        XCTAssertNoThrow(try LocalEngineEndpoint("https://172.20.4.5:8765/"))
        for url in ["http://192.168.0.1:8765", "https://172.32.0.1", "https://example.org",
                    "http://127.1", "http://127.0.0.1@192.168.0.1", "https://10.0.0.1?send=1",
                    "http://127.0.0.1/another/path", "https://192.168.000.1"] {
            XCTAssertThrowsError(try LocalEngineEndpoint(url), url)
        }
    }

    func testMutationBodyKeepsUnicodeAndSendsSnakeCaseIdentity() throws {
        let id = SessionRevision(sessionId: "session-a", sessionInstance: "instance-a", revision: 3)
        let text = "🏡每月最多三千元，含停车费。e\u{301}"
        let data = try DecisionWire.encoder.encode(TurnRequest(session: id, text: text))
        let parsed = try XCTUnwrap(JSONSerialization.jsonObject(with: data) as? [String: Any])
        XCTAssertEqual(parsed["session_id"] as? String, "session-a")
        XCTAssertEqual(parsed["session_instance"] as? String, "instance-a")
        XCTAssertEqual(parsed["revision"] as? Int, 3)
        XCTAssertEqual((parsed["text"] as? String)?.unicodeScalars.map(\.value), text.unicodeScalars.map(\.value))
        XCTAssertEqual(DecisionWire.originalSlice("👩‍💻金额一百", start: 3, end: 5), "金额")
    }

    func testConfirmationEncodesExplicitCorrectionAndSeparateDismissal() throws {
        let id = SessionRevision(sessionId: "session-a", sessionInstance: "instance-a", revision: 3)
        let correction = ClaimCorrection(claimId: "new-cost", supersedes: "old-cost")
        let request = ConfirmationRequest(session: id, claimIds: ["new-cost"], optionIds: ["A"], acceptContext: true,
                                          corrections: [correction], dismissClaimIds: ["misread-unit"])
        let parsed = try XCTUnwrap(JSONSerialization.jsonObject(with: DecisionWire.encoder.encode(request)) as? [String: Any])
        XCTAssertEqual(parsed["corrections"] as? [[String: String]], [["claim_id": "new-cost", "supersedes": "old-cost"]])
        XCTAssertEqual(parsed["dismiss_claim_ids"] as? [String], ["misread-unit"])
    }

    func testResultCannotReuseAnotherIncarnationOrEnlargePartialAuthority() throws {
        let payload = """
        {"session_id":"one","session_instance":"first","revision":1,"cancel_nonce":"abc",
         "phase":"CLARIFY","summary":{"conclusion":"有待核实","differences":[],"unknowns":[]},
         "state":{"confirmed":false,"constraints_confirmed":false},"claims":[],"options":[],
         "result":{"session_id":"one","session_instance":"first","revision":1,"protocol":"0.8.0","authority_generation":3,
                   "layers":{"preparation":{"sha256":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},
                   "partial_calculation":{"parent_sha256":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","status":"DESCRIPTIVE_ONLY","version":"1.0.0"}}},
         "partial_analysis":{"session_id":"one","session_instance":"first","revision":1,"version":"1.0.0",
         "authority":"NONE","status":"DESCRIPTIVE_ONLY","authority_generation":3,"dependency_sha256":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
         "checks":[],"differences":[{"label":"现金","higher_option_label":"甲","lower_option_label":"乙","amount":"2.50","unit":"元","horizon":"每月"}]}}
        """
        func decode(_ contents: String) throws -> ConversationSnapshot {
            try DecisionWire.decoder.decode(ConversationSnapshot.self, from: Data(contents.utf8))
        }
        let snapshot = try decode(payload)
        XCTAssertTrue(snapshot.matches(previous: nil, nonce: "abc"))
        XCTAssertFalse(snapshot.matches(previous: nil, nonce: "different"))
        let prior = SessionRevision(sessionId: "one", sessionInstance: "second", revision: 0)
        XCTAssertFalse(snapshot.matches(previous: prior, nonce: nil))
        XCTAssertEqual(snapshot.currentPartial?.differences.first?.amount, "2.50")
        let expanded = try decode(payload.replacingOccurrences(of: "\"NONE\"", with: "\"SELECT\""))
        XCTAssertNil(expanded.currentPartial)
        let stale = try decode(payload.replacingOccurrences(of: "\"authority\":\"NONE\",\"status\":\"DESCRIPTIVE_ONLY\",\"authority_generation\":3",
                                                               with: "\"authority\":\"NONE\",\"status\":\"DESCRIPTIVE_ONLY\",\"authority_generation\":2"))
        XCTAssertNil(stale.currentPartial)
    }
    func testLocalEngineAgainstActualV08API() async throws {
        let environment = ProcessInfo.processInfo.environment
        guard let url = environment["PH_APPLE_LOOPBACK_TEST_URL"],
              let token = environment["PH_APPLE_LOOPBACK_TEST_TOKEN"] else {
            throw XCTSkip("Set the loopback test URL and token for a disposable v0.8 service.")
        }
        let client = try LocalEngine(endpoint: LocalEngineEndpoint(url), token: token)
        try await client.verifyConnection()
        let nonce = LocalEngine.cancellationNonce()
        let first = try await client.start("预算最多3000元。A：费用4000元。B：费用2000元。我不能确定是否必须搬家。", nonce: nonce)
        XCTAssertNotEqual(first.sessionId, nonce)
        let confirmed = try await client.confirm(session: first.identity,
                                                  claims: first.claims.filter { $0.status == "PROVISIONAL" }.map(\.id),
                                                  options: first.options.map(\.id), context: true)
        XCTAssertEqual(confirmed.identity.revision, 2)
        XCTAssertNil(confirmed.analysis)
        let partial = try XCTUnwrap(confirmed.currentPartial)
        XCTAssertEqual(partial.checks.first?.lower, "4000")
        XCTAssertEqual(partial.differences.first?.amount, "2000")
        do {
            _ = try await client.analyze(session: first.identity)
            XCTFail("A stale revision acquired calculation authority.")
        } catch LocalEngineError.rejected(422) {}
        try await client.discard(first.identity)
        do {
            _ = try await client.analyze(session: confirmed.identity)
            XCTFail("A discarded instance acquired calculation authority.")
        } catch LocalEngineError.rejected(404) {}
    }
}
