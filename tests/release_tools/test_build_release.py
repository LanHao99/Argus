from __future__ import annotations

import os

from argus_skill.release_tools import build_release


def test_release_uses_the_platform_npm_launcher() -> None:
    expected = "npm.cmd" if os.name == "nt" else "npm"
    assert build_release.NPM_COMMAND == expected


def test_release_subprocesses_use_current_python_bin(monkeypatch) -> None:
    captured = {}
    monkeypatch.setattr(build_release.sys, "executable", "/opt/argus-venv/bin/python")
    monkeypatch.setenv("PATH", "/usr/bin:/bin")

    def fake_run(argv, **kwargs):
        captured["argv"] = argv
        captured.update(kwargs)

    monkeypatch.setattr(build_release.subprocess, "run", fake_run)

    build_release.run("npm", "run", "build")

    assert captured["argv"] == ("npm", "run", "build")
    assert captured["check"] is True
    assert captured["env"]["PATH"].split(os.pathsep)[0] == "/opt/argus-venv/bin"
    assert captured["env"]["PYTHONPATH"].split(os.pathsep)[0] == str(build_release.ROOT)
