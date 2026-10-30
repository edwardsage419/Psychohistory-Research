# B R293 S89 remote archived V8 replay and original baseline addendum

Date 2026-10-30 UTC. Track B. Internal nonblind E1 only.

After the initial audit, the exact GitHub persisted R source blob 244812353cf5721113fdca46b7b0b6dd7a2df2c8 was fetched and executed in a V8 JavaScript environment with a minimal CommonJS-compatible assert shim (shebang removed for evaluation). Its exported check() completed successfully. It generated exactly 2112 source rows; the re-generated CSV was re-blobbed through the GitHub connector and its Git blob identity equaled the persisted 61e7c480fca45972760e37c72ed3e8e148603b13. The re-generated JSON string exactly matched the fetched persisted JSON blob 33fadc22d56f2fbb85cc34401c79668b31808a51. This is actual remote archived source replay in V8, not native Node CLI.

Separately fetched original R293 result blob dba2c5c425f6815abc9bcb8e150950653215cb33 and new S89 result blob 33fadc22d56f2fbb85cc34401c79668b31808a51. Directly compared all 400 centered covariance entries across four S89 worlds to the matching original R293 latent-world centered matrices. All 400 exactly matched. This supplements the previously executed Python independent linear-covariance oracle, which checked all 800 S89 raw/centered entries, 2112 full sources and eight rejected mutations. Python local script blob matches the persisted GitHub audit script 691b93b2835477b140cbcea7258547b8c89ad736.

Status: V8_ARCHIVED_SOURCE_REPLAY=PASS; EXACT_CSV_BLOB_PARITY=PASS; EXACT_JSON_TEXT_PARITY=PASS; ORIGINAL_R293_CENTERED_400_PARITY=PASS; PYTHON_LOCAL_NATIVE_TEST=PASS; ARCHIVED_NODE_NATIVE_CLI=NOT_RUN; REMOTE_CHECKOUT_PYTHON_CLI=NOT_RUN; EXTERNAL_TEAM_REPLICATION=NOT_RUN; SCIENTIFIC_ACCEPTANCE=PARTIAL. No CI or billed runner. E2=0, E3=0, R073/PESEN frozen.
