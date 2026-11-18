"""Executable text for the isolated v2 worker. No checkout import paths."""
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import types


MODULES = ("contracts", "state", "degroot", "prediction")


def main():
    destination = Path(sys.argv[1])
    limits = {"memory": "NOT_ENFORCED", "cpu": "NOT_ENFORCED",
              "parent_death": "NOT_ENFORCED", "isolated_python": bool(sys.flags.isolated),
              "optimization": sys.flags.optimize}
    try:
        if platform.system() == "Linux":
            import ctypes
            import resource
            import signal

            libc = ctypes.CDLL(None, use_errno=True)
            if libc.prctl(1, signal.SIGTERM, 0, 0, 0) != 0:
                raise OSError(ctypes.get_errno(), "Cannot install parent-death guard")
            if os.getppid() != int(sys.argv[2]):
                return
            resource.setrlimit(resource.RLIMIT_AS, (512 * 1024**2,) * 2)
            resource.setrlimit(resource.RLIMIT_CPU, (5, 6))
            limits.update(memory="RLIMIT_AS", cpu="RLIMIT_CPU", parent_death="PR_SET_PDEATHSIG")

        envelope = json.load(sys.stdin)
        files = envelope["files"]
        expected = sys.argv[3]
        identity = hashlib.sha256(json.dumps(
            files, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode()).hexdigest()
        if identity != expected or not sys.flags.isolated or not sys.flags.no_site:
            raise ValueError("Isolated worker source identity mismatch")
        package = types.ModuleType("psychohistory")
        package.__path__ = []
        sys.modules[package.__name__] = package
        for name in MODULES:
            qualified = f"psychohistory.{name}"
            module = types.ModuleType(qualified)
            module.__file__ = f"<sealed:{name}.py>"
            module.__package__ = package.__name__
            sys.modules[qualified] = module
            setattr(package, name, module)
            exec(compile(bytes.fromhex(files[f"{name}.py"]), module.__file__, "exec"), module.__dict__)
        configuration = envelope["config"]
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
    with destination.open("xb") as output:
        output.write(raw)


if __name__ == "__main__":
    main()
