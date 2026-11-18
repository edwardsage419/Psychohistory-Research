"""Shared v0.2 registration, protocol approval and comparison operations."""
from . import sources
from .degroot import DeGroot
from .plugins import Registry, registry
from .prediction import protocol_spec
from .v02_execution import RUN_KIND, digest, source_snapshot, validate_result


comparison_registry = Registry()
comparison_registry.register(DeGroot())


def models():
    return [*registry.describe(), *comparison_registry.describe()]


class Workflow:
    def __init__(self, store, repo):
        self.store = store
        self.repo = repo

    def register_source(self, research_id, commit=None):
        try:
            record = sources.capture(self.repo, research_id, commit)
        except sources.SourceError as error:
            self.store.audit({"event": "SOURCE_REGISTRATION_REJECTED", "research_id": research_id,
                              "reason": str(error)})
            raise
        previous = self.store.research_records("sources")
        other_version = any(row["research_id"] == research_id and row["source_id"] != record["source_id"]
                            for row in previous)
        warnings = list(record["warnings"])
        if other_version:
            warnings.append("OTHER_SOURCE_VERSION_REGISTERED")
        if not self.store.register_source(record, warnings):
            warnings.append("DUPLICATE_SOURCE_ID")
        return {**record, "warnings": warnings}


    def source(self, identity):
        record = self.store.research_record("sources", identity)
        if record.get("source_id") != identity:
            raise ValueError("Source record identity does not match its registration key")
        return record

    def verify_source(self, identity):
        try:
            return sources.verify(self.repo, self.source(identity))
        except sources.SourceError as error:
            self.store.audit({"event": "SOURCE_VERIFICATION_REJECTED", "source_id": identity,
                              "reason": str(error)})
            raise

    def create_protocol(self, source_id, seed, model_id, model_version):
        comparison_registry.get(model_id, model_version)
        self._execution_source(source_id)
        body = {"source_id": source_id, "spec": protocol_spec(seed, model_id),
                "code_sha256": digest(source_snapshot())}
        identity = digest(body)
        record = {"protocol_id": identity, "status": "DRAFT", **body}
        self.store.register_research_record("protocols", identity, record)
        return self.protocol(identity)

    def protocol(self, identity):
        record = self.store.research_record("protocols", identity)
        if (record["protocol_id"] != identity or
                self._protocol_digest(record) != identity):
            raise ValueError("Protocol content identity mismatch")
        return record

    def _execution_source(self, identity):
        source = self.source(identity)
        if source["research_id"] != "R123" or source["origin"] != "MAIN":
            raise PermissionError("Only the pinned main R123 reference admits the synthetic comparison")
        return self.verify_source(identity)

    def approve_protocol(self, identity):
        protocol = self.protocol(identity)
        self._execution_source(protocol["source_id"])
        return self.store.approve_protocol(identity, self._verify_protocol)

    @staticmethod
    def _protocol_digest(record):
        return digest({key: record[key] for key in ("source_id", "spec", "code_sha256")})

    def _verify_protocol(self, record):
        if self._protocol_digest(record) != record["protocol_id"]:
            raise ValueError("Protocol content identity mismatch")
        if record["code_sha256"] != digest(source_snapshot()):
            raise ValueError("Protocol code identity changed. Use its recorded version or a new seed.")
        self._execution_source(record["source_id"])
        if record["spec"] != protocol_spec(record["spec"]["seed"], DeGroot.model_id):
            raise ValueError("Unrecognized synthetic protocol profile")

    def verify_config(self, config):
        approved = self.protocol(config["protocol_id"])
        if approved["status"] != "APPROVED":
            raise ValueError("Approve the immutable protocol before execution")
        expected = {key: approved[key] for key in ("protocol_id", "spec", "source_id")}
        if config != expected:
            raise ValueError("Approved protocol configuration changed")
        self._verify_protocol(approved)

    def submit(self, scheduler, protocol_id, retry_of=None):
        protocol = self.protocol(protocol_id)
        config = {key: protocol[key] for key in ("protocol_id", "spec", "source_id")}
        self.verify_config(config)
        spec = protocol["spec"]
        holdout = digest({"dataset": spec["dataset_version"], "seed": spec["seed"]})
        return scheduler.submit_comparison(config, holdout, protocol["code_sha256"], retry_of=retry_of)

    def run(self, identity):
        run = self.store.get_run(identity)
        if run.get("kind") != RUN_KIND:
            raise KeyError("Unknown comparison experiment")
        return run

    def retry(self, scheduler, identity):
        run = self.run(identity)
        return self.submit(scheduler, run["config"]["protocol_id"], retry_of=identity)

    def result(self, identity):
        run = self.run(identity)
        if run["status"] != "COMPLETED":
            raise ValueError("No completed result available")
        artifact = self.store.get(run["result_hash"])
        validate_result(run, artifact)
        return {"artifact_sha256": run["result_hash"], "result": artifact}
