<div align="center">

# ARGUS

### Persistent intelligence for autonomous research and engineering

Turn an open-ended goal into a durable workflow that can plan, build, verify, pause, and resume.

[Website](https://argusbot.cn) · [Demo](https://www.youtube.com/watch?v=i8Qy9HCboQE) · [Technical Report](technical_report/argus-technical-report.pdf) · [简体中文](README.zh-CN.md)

`Manager` → `Planner` → `Engineer` ⇄ `Reviewer`

</div>

---

## ✦ One goal. Four roles. Durable progress.

Argus coordinates four independent, model-driven roles around persistent project state:

| Role | Owns |
|---|---|
| 🧭 **Manager** | Operator intent, workflow selection, and stage transitions |
| 🗺️ **Planner** | The next high-value task and its evidence requirements |
| 🛠️ **Engineer** | Implementation, research, experiments, and artifacts |
| 🔎 **Reviewer** | Independent checks of correctness, evidence, limits, and completion |

```text
operator intent
      │
      ▼
  Manager ──► Planner ──► Engineer ──► Reviewer
      ▲                         │           │
      └──── durable state ◄────┴───────────┘
```

Tasks, checkpoints, decisions, reusable Skills, and review evidence survive across sessions. A project can stop, resume, survive process upgrades, and continue from its latest verified state.

**Supported agent CLIs:** GitHub Copilot CLI · OpenAI Codex CLI · Claude Code · OpenCode · Pi

---

## ⚡ Quick start

### Requirements

- Python 3.11+
- Node.js 22+
- One supported agent CLI installed and authenticated through its official login flow

### 1. Install

```bash
git clone https://github.com/lbx154/Argus.git
cd Argus

python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
```

### 2. Connect your backend

```bash
argus --setup --non-interactive \
  --backend copilot \
  --accept-house-rules
```

Replace `copilot` with `codex`, `claude`, `opencode`, or `pi` as needed.

### 3. Launch the terminal cockpit

```bash
argus
```

Useful checks:

```bash
argus --doctor
argus --status
```

---

## ◉ Web UI

### Local desktop

Start the API and Web UI, then open it in your default browser:

```bash
argus --web
```

The default address is [http://127.0.0.1:8799](http://127.0.0.1:8799).

To start it without opening a browser:

```bash
argus --web --no-open
```

Use a different port when needed:

```bash
argus --web --port 8800
```

### Remote server over SSH — recommended

On the server, keep Argus bound to localhost:

```bash
argus --web --no-open
```

On your computer, forward the port:

```bash
ssh -L 8799:127.0.0.1:8799 user@server
```

Then open [http://127.0.0.1:8799](http://127.0.0.1:8799) locally.

<details>
<summary><strong>Direct LAN access</strong></summary>

Only bind to the LAN with a bearer token configured:

```bash
export ARGUS_SKILL_WEB_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
printf '%s\n' "$ARGUS_SKILL_WEB_TOKEN"
argus --web --host 0.0.0.0 --port 8799 --no-open
```

Open the following URL from another machine, replacing the host and token:

```text
http://SERVER_IP:8799/?token=YOUR_TOKEN
```

Never expose `0.0.0.0` without `ARGUS_SKILL_WEB_TOKEN`.

</details>

---

## ↻ Update

```bash
cd Argus
git pull --ff-only
.venv/bin/python -m pip install -e .
.venv/bin/argus
```

The launcher detects stale local WebAPI and daemon processes and replaces them at a controlled task boundary.
