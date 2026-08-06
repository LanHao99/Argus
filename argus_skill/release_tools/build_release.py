#!/usr/bin/env python3
"""Atomically refresh Argus release identity and both production frontends."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run(*argv: str, cwd: Path = ROOT) -> None:
    env = os.environ.copy()
    # npm frontend scripts invoke `python`; pin that name to the interpreter
    # running this release build instead of whichever legacy system Python
    # happens to appear first on PATH.
    python_bin = str(Path(sys.executable).parent)
    env["PATH"] = os.pathsep.join(
        value for value in (python_bin, env.get("PATH", "")) if value
    )
    env["PYTHONPATH"] = os.pathsep.join(
        value for value in (str(ROOT), env.get("PYTHONPATH", "")) if value
    )
    subprocess.run(argv, cwd=cwd, check=True, env=env)


def main() -> int:
    try:
        # Generated protocol source participates in the release digest, so it
        # must be refreshed before computing the manifest. Reversing these two
        # steps makes a schema change require two builds: the first build updates
        # types and then correctly rejects its now-stale manifest.
        run(
            sys.executable,
            "-m",
            "argus_skill.release_tools.generate_event_types",
        )
        run(
            sys.executable,
            "-m",
            "argus_skill.release_tools.generate_manifest",
            "--prepare-build",
        )
        run("npm", "run", "build", cwd=ROOT / "frontend" / "web")
        run("npm", "run", "build", cwd=ROOT / "frontend" / "tui")
        run(
            sys.executable,
            "-m",
            "argus_skill.release_tools.check_artifacts",
        )
    except subprocess.CalledProcessError as exc:
        return int(exc.returncode or 1)
    manifest = json.loads((ROOT / "argus_skill" / "release_manifest.json").read_text())
    print(f"release ready: {manifest['release_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
