"""Executable text for the isolated v2 worker. No checkout import paths."""
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import types


MODULES = ("contracts", "state", "degroot", "prediction")
TRAJECTORY_MODULES = ("contracts", "state", "degroot", "replicator", "trajectories")


def main():
    destination = Path(sys.argv[1])
    limits = {"memory": "NOT_ENFORCED", "cpu": "NOT_ENFORCED",
              "parent_death": "NOT_ENFORCED", "isolated_python": bool(sys.flags.isolated),
              "optimization": sys.flags.optimize}
    try:
        envelope = json.load(sys.stdin)
        files = envelope["files"]
        expected = sys.argv[3]
        identity = hashlib.sha256(json.dumps(
            files, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode()).hexdigest()
        if identity != expected or not sys.flags.isolated or not sys.flags.no_site:
            raise ValueError("Isolated worker source identity mismatch")
        lifecycle = types.ModuleType("sealed_worker_lifecycle")
        exec(compile(bytes.fromhex(files["worker_lifecycle.py"]),
                     "<sealed:worker_lifecycle.py>", "exec"), lifecycle.__dict__)
        limits.update(lifecycle.configure_worker(int(sys.argv[2])))
        kind = envelope.get("kind", "prediction-comparison-v1")
        if kind not in {"prediction-comparison-v1", "mechanism-trajectory-v1"}:
            raise ValueError("Unsupported sealed worker kind")
        modules = TRAJECTORY_MODULES if kind == "mechanism-trajectory-v1" else MODULES
        package = types.ModuleType("psychohistory")
        package.__path__ = []
        sys.modules[package.__name__] = package
        for name in modules:
            qualified = f"psychohistory.{name}"
            module = types.ModuleType(qualified)
            module.__file__ = f"<sealed:{name}.py>"
            module.__package__ = package.__name__
            sys.modules[qualified] = module
            setattr(package, name, module)
            exec(compile(bytes.fromhex(files[f"{name}.py"]), module.__file__, "exec"), module.__dict__)
        configuration = envelope["config"]
        if kind == "mechanism-trajectory-v1":
            result = package.trajectories.compute(configuration)
            result.update(input=configuration, code_sha256=identity)
        else:
            result = package.prediction.run_comparison(configuration["spec"])
            result.update(protocol_id=configuration["protocol_id"], source_id=configuration["source_id"],
                          input=configuration, code_sha256=identity)
        payload = {"ok": True, "result": result}
    except Exception as error:
        payload = {"ok": False, "error": f"{type(error).__name__}: {str(error)[:500]}"}
    payload.update(worker_pid=os.getpid(), limits=limits)
    raw = json.dumps(payload, sort_keys=True, allow_nan=False, ensure_ascii=False).encode()
    if len(raw) > 32 * 1024**2:
        raise ValueError("Worker output exceeds artifact budget")
    if os.getppid() != int(sys.argv[2]):
        return
    with destination.open("xb") as output:
        output.write(raw)


if __name__ == "__main__":
    main()
