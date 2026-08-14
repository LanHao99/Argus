from __future__ import annotations

from argus_skill.core.portable_filename import portable_filename_component


def test_windows_reserved_and_unsafe_names_are_encoded() -> None:
    assert portable_filename_component("CON", windows=True).startswith("~")
    assert portable_filename_component("team::task", windows=True).startswith("~")


def test_encoded_looking_logical_id_cannot_alias_an_unsafe_id() -> None:
    unsafe = portable_filename_component("team::task", windows=True)

    assert portable_filename_component(unsafe, windows=True) != unsafe


def test_oversized_identifier_is_rejected() -> None:
    try:
        portable_filename_component("x" * 121, windows=True)
    except ValueError as exc:
        assert "120" in str(exc)
    else:
        raise AssertionError("oversized identifier must not reach the filesystem")
