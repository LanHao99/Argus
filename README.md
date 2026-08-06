<div align="center">

# ARGUS

### Persistent intelligence for autonomous research and engineering

Turn an open-ended goal into a durable workflow that can plan, build, verify, pause, and resume.

**Official open-source release: on the way · Current version: Preview v0.1.1**

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

## ◆ Advanced usage guide

> Argus is not only something you run. It is a runtime you can reshape.

If you are an agent enthusiast, we recommend deploying Argus locally and making it your own. Adapt the role prompts, workflow, review boundaries, tools, and operating conventions until the full loop fits the way you work.

### Build your own vertical

A vertical gives Argus domain-specific stages, Skills, evidence expectations, and completion criteria. You can add one for your own field so that planning, execution, and review reflect the standards of the domain you care about—not a generic workflow.

Good extensions include:

- a workflow tailored to your research or engineering process;
- domain Skills, tools, datasets, and evaluation methods;
- custom stage and review criteria;
- integrations with your existing infrastructure;
- tests that preserve your preferred operating contract.

### Operate Argus through another agent

Using another agent environment as the outer control layer can also be a powerful workflow. GitHub Copilot, Pi, Codex, Claude Code, OpenCode, OpenClaw, or Hermes can invoke the Argus CLI, inspect its state, operate its local Web/API surface, and help evolve your deployment.

GitHub Copilot CLI, Pi, Codex CLI, Claude Code, and OpenCode can be configured as native Argus backends. OpenClaw and Hermes are best used as external agents that operate a local Argus deployment through its CLI or Web/API interface.

Useful entry points for an outer agent:

```bash
argus --doctor
argus --status
argus --web --no-open
```

The most capable setup is often not a stock installation, but an Argus instance that has been deliberately adapted to your own ambitious field and way of working.

---

## ↻ Update

```bash
cd Argus
git pull --ff-only
.venv/bin/python -m pip install -e .
.venv/bin/argus
```

The launcher detects stale local WebAPI and daemon processes and replaces them at a controlled task boundary.
