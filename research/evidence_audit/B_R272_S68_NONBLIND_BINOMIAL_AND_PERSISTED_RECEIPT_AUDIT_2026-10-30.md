# B audit: R272 S68 paired holdout ranking

Date 2026-10-30 Asia/Singapore. Target (B,R272,S68,nonblind-binomial-15-cell-and-receipt-gate). Frozen R design commit edacaa60498e9a53043db14dd7eb0531d995062b.

## Actual execution
R source JavaScript executed in V8 and enumerated 64 six-bit ordered sources for each of 9 p/pairs. Route R compared two predictions on exactly the same future two bits. It produced 576 comparison-labelled CSV rows and 9 exact JSON summaries.

A separately written Python standard-library program uses Binomial(4,p) times Binomial(2,p) over 15 (K,J) cells per p/pair. It does not import the R enumeration. Native Python --selftest executed with exit 0, 4 grouped controls PASS. The archived Python file Git blob equals the executed local file: e75bd728ecb59975ad071be6211eeec0f2b203e0 (4744 bytes). The Python computation independently matched 9 rows of mean, variance, three directional probabilities and strict wrong-ranking probability, 54 exact comparisons. Internal R route B also agrees with route R on 63 exact metrics, including second moments.

The persisted GitHub JSON and CSV were read back via GitHub connector and compared against a fresh R execution, all 9 JSON result objects and all 576 CSV rows exactly identical. Persisted blobs: JSON 1753b35f867cbf687067fff6ca77e001ab30e8ac; CSV bad6b903605970972c5ebe84d902ee87db7226ce; archived R JavaScript 2e5aca5fd759962661eaadf05440f203bb8e4546. A strict result gate rejected six mutations: missing row, duplicate row, tampered mean, E2 evidence promotion, boolean in integer source count, and altered freeze identity. Positive original receipt passed.

## Scientific limitations
The researcher read the original R272 expected risks before designing S68. This is internal **nonblind** arithmetic and persisted-file verification, not a blinded external-team replication. The Python CLI was executed in selftest mode; its --receipt and --csv options against the *actual remote persisted files* remain NOT_RUN in a native Python runtime. Remote source replay was completed by the connected V8 route, not by the archived Python CLI. No CI run was launched. No E2 or E3 evidence and no empirical calibration, independent real-data test or cluster bootstrap.

Scientific status: INTERNAL_EXACT_RECHECK_PASS; NATIVE_REMOTE_RECEIPT_CLI_PARTIAL; EXTERNAL_REPLICATION_NOT_RUN. R272 original bounded acceptance unchanged; R073/PESEN frozen. No paid services.
