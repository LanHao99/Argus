<div align="center">

<img src="docs/assets/argus-mascot.svg" width="140" alt="Argus multi-eye agent mascot">

# Argus

### Persistent, reviewed autonomy for research and engineering

Long-running agent work that can plan, execute, verify, pause, and continue beyond a single model turn.

**Preview v0.1.1 · Official open-source release on the way.**

[![GitHub Stars](https://img.shields.io/github/stars/lbx154/Argus?style=flat-square)](https://github.com/lbx154/Argus/stargazers)
[![License](https://img.shields.io/github/license/lbx154/Argus?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![arXiv](https://img.shields.io/badge/arXiv-2608.05144-b31b1b?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2608.05144)

[Website](https://argusbot.cn) · [Technical Report · arXiv:2608.05144](https://arxiv.org/pdf/2608.05144) · [WeChat Community](#wechat-community) · **English** / [简体中文](README.zh-CN.md)

`Manager` → `Planner` → `Engineer` ⇄ `Reviewer`

</div>

---

## What is Argus?

Most agents are optimized for one conversation or one coding turn. Argus is built for work that lasts: it keeps state, separates execution from judgment, and resumes from verified progress instead of starting over.

| Capability | What it means |
|---|---|
| **Persistent state** | Tasks, checkpoints, decisions, Skills, and evidence survive sessions and runtime upgrades. |
| **Independent review** | Execution and verification stay separate; normal rounds end with a Reviewer judgment. |
| **Four-role runtime** | Manager, Planner, Engineer, and Reviewer have distinct authority and responsibilities. |
| **Real tool use** | Agents work through files, terminals, experiments, APIs, and inspectable artifacts. |
| **Domain extensibility** | Verticals can define custom stages, tools, evidence requirements, and completion standards. |
| **Multiple backends** | Run with GitHub Copilot CLI, Pi, Codex CLI, Claude Code, or OpenCode. |

## Runtime model

| | Authority | Responsibility |
|---:|---|---|
| `01` | **Manager · Control** | Interprets operator intent, selects the workflow, and owns stage transitions. |
| `02` | **Planner · Direction** | Chooses the next high-value task and defines the evidence it must produce. |
| `03` | **Engineer · Execution** | Implements, researches, runs experiments, and creates inspectable artifacts. |
| `04` | **Reviewer · Verification** | Independently checks correctness, evidence, limitations, and completion. |

A project can stop, resume, survive a runtime replacement, and continue from its latest verified position.

**Native backends:** `GitHub Copilot CLI` · `Pi` · `OpenAI Codex CLI` · `Claude Code` · `OpenCode`

## Quick Install

### Requirements

- Python 3.11+
- Node.js 22+
- One supported Agent CLI installed and authenticated through its official login flow

### Install

```bash
git clone https://github.com/lbx154/Argus.git
cd Argus

python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
```

### Connect a backend

```bash
argus --setup --non-interactive \
  --backend copilot \
  --accept-house-rules
```

Use `copilot`, `pi`, `codex`, `claude`, or `opencode` for `--backend`.

### Launch

```bash
argus
```

```bash
argus --doctor   # verify the installation
argus --status   # inspect the current runtime
```

## Interfaces

### Terminal cockpit

```bash
argus
```

Use the terminal cockpit to talk to the Manager, follow live work, inspect state, and resume projects.

### Web UI

Start Argus and open the Web UI in your default browser:

```bash
argus --web
```

Default address: [http://127.0.0.1:8799](http://127.0.0.1:8799)

```bash
argus --web --no-open    # start without opening a browser
argus --web --port 8800  # use another port
```

#### Remote server over SSH

On the server:

```bash
argus --web --no-open
```

On your computer:

```bash
ssh -L 8799:127.0.0.1:8799 user@server
```

Then open [http://127.0.0.1:8799](http://127.0.0.1:8799) locally.

<details>
<summary><strong>Direct LAN access</strong></summary>

Direct LAN access must be protected by a bearer token:

```bash
export ARGUS_SKILL_WEB_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
printf '%s\n' "$ARGUS_SKILL_WEB_TOKEN"
argus --web --host 0.0.0.0 --port 8799 --no-open
```

Open the URL below from another machine, replacing the host and token:

```text
http://SERVER_IP:8799/?token=YOUR_TOKEN
```

Never expose `0.0.0.0` without `ARGUS_SKILL_WEB_TOKEN`.

</details>

## Advanced usage

Argus is designed to be changed, not merely configured.

### Adapt the runtime

If you are an agent enthusiast, deploy Argus locally and make the complete loop fit the way you work. Tune role prompts, workflow boundaries, review policy, tools, and operating conventions; connect your own infrastructure; preserve the behavior you care about with tests.

### Build your own Vertical

A Vertical gives your field its own stages, Skills, datasets, tools, evidence expectations, evaluation methods, and completion criteria. Planning and review can then follow the real standards of your domain instead of a generic process.

### Use another agent as the outer layer

GitHub Copilot, Pi, Codex, Claude Code, OpenCode, OpenClaw, or Hermes can be the environment from which you invoke Argus, inspect its state, operate its local CLI or Web/API surface, and continue improving the deployment.

- **Native Argus backends:** GitHub Copilot CLI, Pi, Codex CLI, Claude Code, OpenCode
- **External agent operators:** OpenClaw, Hermes, or any agent that can use a shell or HTTP API

Useful entry points:

```bash
argus --doctor
argus --status
argus --web --no-open
```

The most capable setup is often an Argus instance deliberately adapted to your own ambitious field and way of working.

## Update

```bash
cd Argus
git pull --ff-only
.venv/bin/python -m pip install -e .
.venv/bin/argus
```

Argus detects stale local WebAPI and daemon processes and replaces them at a controlled task boundary.

## WeChat community

Scan the QR code below to join the Argus community. The expiry date is printed in the image; if it has expired, open an Issue and ask the maintainers for the latest code.

<p align="center">
  <img src="docs/assets/argus-wechat-group.jpg" width="360" alt="Argus WeChat community QR code">
</p>
