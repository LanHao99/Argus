from __future__ import annotations

import re
from pathlib import Path

from argus_skill.core import runtime_identity as runtime_identity_module
from argus_skill.release import (
    MANIFEST_SCHEMA_VERSION,
    compute_source_digest,
    release_identity,
    release_manifest,
)


def test_release_manifest_matches_current_shipped_source() -> None:
    root = Path(__file__).parents[2]
    manifest = release_manifest()
    assert manifest["schema_version"] == MANIFEST_SCHEMA_VERSION
    assert manifest["source_digest"] == compute_source_digest(root)
    assert manifest["release_id"] == (
        f"{manifest['package_version']}+{manifest['source_digest'][:16]}"
    )
    identity = release_identity(root)
    assert identity["release_matches_source"] is True
    assert identity["runtime_source_digest"] == manifest["source_digest"]


def test_checked_in_frontend_contract_matches_current_release() -> None:
    root = Path(__file__).parents[2]
    manifest = release_manifest()
    generated = (root / "frontend/core/src/release.generated.ts").read_text()
    assert manifest["release_id"] in generated
    assert manifest["source_digest"] in generated

    tui = (root / "frontend/tui/bundle/argus.mjs").read_text()
    assert manifest["release_id"] in tui

    web_root = root / "frontend/web/dist"
    index = (web_root / "index.html").read_text()
    assets = [
        web_root / ref.lstrip("/")
        for ref in re.findall(r'(?:src|href)="([^"]+\.js)"', index)
    ]
    assert assets
    assert any(manifest["release_id"] in path.read_text() for path in assets)


def test_untracked_runtime_skill_does_not_change_release_identity() -> None:
    root = Path(__file__).parents[2]
    generated = root / "argus_skill" / "builtin_skills" / "_release-test-untracked.md"
    before = compute_source_digest(root)
    try:
        generated.write_text("# Runtime-generated skill\n", encoding="utf-8")
        assert compute_source_digest(root) == before
    finally:
        generated.unlink(missing_ok=True)


def test_untracked_new_source_participates_before_first_commit() -> None:
    root = Path(__file__).parents[2]
    source = root / "argus_skill" / "_release_test_untracked_source.py"
    before = compute_source_digest(root)
    try:
        source.write_text("VALUE = 1\n", encoding="utf-8")
        assert compute_source_digest(root) != before
    finally:
        source.unlink(missing_ok=True)


def test_strict_release_preflight_rejects_manifest_source_mismatch(
    monkeypatch,
) -> None:
    monkeypatch.setenv("ARGUS_SKILL_REQUIRE_RELEASE_MATCH", "1")
    monkeypatch.setattr(
        runtime_identity_module,
        "runtime_identity",
        lambda: {"release_matches_source": False},
    )

    error = runtime_identity_module.release_match_preflight_error()

    assert "does not match" in error
    assert "pip install -e ." in error


def test_release_preflight_is_permissive_unless_enabled(monkeypatch) -> None:
    monkeypatch.delenv("ARGUS_SKILL_REQUIRE_RELEASE_MATCH", raising=False)
    monkeypatch.setattr(
        runtime_identity_module,
        "runtime_identity",
        lambda: {"release_matches_source": False},
    )

    assert runtime_identity_module.release_match_preflight_error() == ""
