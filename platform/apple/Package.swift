// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "DecisionProtocol",
    platforms: [.macOS(.v14), .iOS(.v17)],
    products: [.library(name: "DecisionProtocol", targets: ["DecisionProtocol"])],
    targets: [
        .target(name: "DecisionProtocol"),
        .testTarget(name: "DecisionProtocolTests", dependencies: ["DecisionProtocol"]),
    ]
)
