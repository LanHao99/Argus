"""Pairing a phone with a LAN-exposed web UI.

The API binds ``127.0.0.1`` by default, which is right for the machine running
the daemon and useless from a phone. Exposing it is a one-flag change
(``--web-host 0.0.0.0``) and the token that protects it was, until now, purely
advisory: the help text said to set ``ARGUS_SKILL_WEB_TOKEN``, and nothing
happened if you didn't. The result was an unauthenticated control surface for
an agent with shell access, one flag away.

This module closes that and makes the secure path the easy one:

* A non-loopback bind **always** ends up authenticated. If no token is
  configured, one is minted for the run rather than serving in the clear.
  ``ARGUS_SKILL_WEB_ALLOW_INSECURE=1`` is the explicit opt-out, for operators
  who front the API with their own auth.
* The reachable URL — token included — is printed with a QR code, so pairing a
  phone is a scan instead of typing a 32-character secret on a touch keyboard.
  The web client stores the token on arrival, so the installed PWA stays
  authenticated afterwards.

Rendering the QR needs the optional ``argus-skill[qr]`` extra; without it the
URL is still printed in full.
"""
from __future__ import annotations

import io
import os
import secrets
import socket
from dataclasses import dataclass

__all__ = [
    "PairingPlan",
    "insecure_bind_allowed",
    "is_loopback_host",
    "pairing_plan",
    "primary_lan_address",
    "render_qr",
]

_LOOPBACK_HOSTS = {"127.0.0.1", "::1", "localhost", ""}
_WILDCARD_HOSTS = {"0.0.0.0", "::"}


def is_loopback_host(host: str) -> bool:
    """Whether *host* keeps the API reachable only from this machine."""
    return str(host or "").strip().lower() in _LOOPBACK_HOSTS


def insecure_bind_allowed() -> bool:
    """Whether the operator explicitly accepted an unauthenticated LAN bind."""
    return (os.environ.get("ARGUS_SKILL_WEB_ALLOW_INSECURE") or "").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def primary_lan_address() -> str:
    """Best-effort address other devices on this network can reach.

    Opening a UDP socket toward a public address makes the OS pick the
    outbound interface without sending a packet — more reliable than
    ``gethostbyname(gethostname())``, which often answers ``127.0.1.1``.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        return str(sock.getsockname()[0])
    except OSError:
        return ""
    finally:
        sock.close()


def render_qr(text: str) -> str:
    """Render *text* as a terminal QR code, or return ``""`` if unavailable.

    Inverted so the light modules use the terminal foreground: the common case
    is a dark terminal, where printing dark modules as blocks would give a
    scanner reversed contrast.
    """
    try:
        import qrcode
    except ImportError:
        return ""
    try:
        code = qrcode.QRCode(border=2)
        code.add_data(text)
        code.make(fit=True)
        buffer = io.StringIO()
        code.print_ascii(out=buffer, invert=True)
        return buffer.getvalue().rstrip("\n")
    except Exception:  # noqa: BLE001 - a missing QR must never block serving
        return ""


@dataclass(frozen=True)
class PairingPlan:
    """What to serve with, and what to tell the operator."""

    token: str
    url: str
    qr: str
    banner: str
    error: str = ""
    minted: bool = False

    @property
    def ok(self) -> bool:
        return not self.error


def pairing_plan(
    host: str,
    port: int,
    *,
    token: str | None = None,
    lan_address: str | None = None,
) -> PairingPlan:
    """Decide the token and pairing message for a ``--web`` run.

    ``token`` defaults to ``ARGUS_SKILL_WEB_TOKEN``. ``lan_address`` is
    injectable so the decision is testable without touching the network.
    """
    configured = (token if token is not None else os.environ.get("ARGUS_SKILL_WEB_TOKEN", "")) or ""
    configured = configured.strip()

    if is_loopback_host(host):
        # Only reachable from this machine; a token stays optional.
        url = f"http://127.0.0.1:{port}/"
        return PairingPlan(
            token=configured,
            url=url,
            qr="",
            banner=f"argus web ui: {url}",
        )

    if not configured and not insecure_bind_allowed():
        minted = secrets.token_urlsafe(24)
    else:
        minted = ""
    effective = configured or minted

    display_host = host
    if host in _WILDCARD_HOSTS:
        display_host = (
            lan_address if lan_address is not None else primary_lan_address()
        ) or "127.0.0.1"
    if ":" in display_host and not display_host.startswith("["):
        display_host = f"[{display_host}]"

    url = f"http://{display_host}:{port}/"
    if effective:
        url = f"{url}?token={effective}"

    lines = [
        "",
        f"  Argus web UI  →  {url}",
    ]
    if minted:
        lines += [
            "",
            "  No ARGUS_SKILL_WEB_TOKEN was set, so a token was generated for this run.",
            "  It changes on every restart; export ARGUS_SKILL_WEB_TOKEN to keep one.",
        ]
    elif not effective:
        lines += [
            "",
            "  WARNING: serving without a token because ARGUS_SKILL_WEB_ALLOW_INSECURE",
            "  is set. Anyone who can reach this port controls the daemon.",
        ]

    qr = render_qr(url)
    if qr:
        lines += ["", "  Scan to open on your phone:", "", qr]
    elif effective:
        lines += [
            "",
            "  (`pip install 'argus-skill[qr]'` prints a scannable QR code here.)",
        ]
    lines.append("")

    return PairingPlan(
        token=effective,
        url=url,
        qr=qr,
        banner="\n".join(lines),
        minted=bool(minted),
    )
