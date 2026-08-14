from __future__ import annotations

import base64
import os

_WINDOWS_RESERVED = frozenset({
    "con",
    "prn",
    "aux",
    "nul",
    *(f"com{i}" for i in range(1, 10)),
    *(f"lpt{i}" for i in range(1, 10)),
})


def portable_filename_component(
    value: str,
    *,
    windows: bool | None = None,
    max_bytes: int = 120,
) -> str:
    """Encode a logical identifier as one bounded, portable path component."""
    text = str(value)
    raw = text.encode("utf-8")
    if len(raw) > max_bytes:
        raise ValueError(f"identifier exceeds {max_bytes} UTF-8 bytes")
    on_windows = os.name == "nt" if windows is None else windows
    stem = text.split(".", 1)[0].casefold()
    unsafe = (
        not text
        or text.startswith("~")
        or any(char in text for char in "/\\\0")
        or (
            on_windows
            and (
                any(ord(char) < 32 or char in '<>:"|?*' for char in text)
                or text.endswith((" ", "."))
                or stem in _WINDOWS_RESERVED
            )
        )
    )
    if not unsafe:
        return text
    encoded = base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")
    return f"~{encoded}"


__all__ = ["portable_filename_component"]
