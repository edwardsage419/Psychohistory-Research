"""Exercise all four earlier browser workflows with disposable data roots."""
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

from browser_v04 import PROJECT, loopback_service


def main():
    cases = ("browser_check.py", "browser_v02.py", "browser_v03.py", "browser_v04.py")
    with TemporaryDirectory(prefix="ph-legacy-v05-") as temporary:
        root = Path(temporary).resolve()
        for index, case in enumerate(cases, 1):
            output = root / f"v0{index}.json"
            data = root / f"v0{index}"
            env = {**os.environ, "PH_TEST_DATA": str(data), "PH_BROWSER_REPORT": str(output)}
            command = [sys.executable, str(PROJECT / "scripts" / case)]
            if index == 4:
                subprocess.run(command, env=env, check=True, timeout=120)
            else:
                with loopback_service(data) as (url, _):
                    subprocess.run(command, env={**env, "PH_TEST_URL": url}, check=True, timeout=120)
            result = json.loads(output.read_text(encoding="utf-8"))
            if result.get("status") != "PASS":
                raise ValueError(f"Earlier browser v0.{index} acceptance did not pass")
            print(f"Legacy browser v0.{index}: PASS", flush=True)


if __name__ == "__main__":
    main()
