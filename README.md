# Argus

> An autonomous research and engineering runtime for work that takes longer than one model turn.

[Website](https://argusbot.cn) · [Demo video](https://www.youtube.com/watch?v=i8Qy9HCboQE) · [Technical report](technical_report/argus-technical-report.pdf) · [简体中文](README.zh-CN.md)

## What is Argus?

Argus turns an open-ended objective into a persistent, reviewable workflow. It keeps project state across sessions and coordinates four independent roles:

| Role | Responsibility |
|---|---|
| **Manager** | Interprets the operator's intent, selects the workflow, and controls stage transitions. |
| **Planner** | Chooses the next high-value task and defines its evidence requirements. |
| **Engineer** | Implements, researches, runs experiments, and produces artifacts. |
| **Reviewer** | Independently checks correctness, evidence, limitations, and completion. |

The runtime persists tasks, checkpoints, decisions, reusable Skills, and review evidence. A project can stop, resume, survive process upgrades, and continue from its last verified state.

Argus supports GitHub Copilot CLI, OpenAI Codex CLI, Claude Code, OpenCode, and Pi.

## Install

### Requirements

- Python 3.11+
- Node.js 22+
- One supported agent CLI, installed and authenticated through its official setup

### 1. Clone and install

```bash
git clone https://github.com/lbx154/Argus.git
cd Argus

python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
```

### 2. Configure a backend

Choose the backend you already use:

```bash
argus --setup --non-interactive \
  --backend copilot \
  --accept-house-rules
```

Replace `copilot` with `codex`, `claude`, `opencode`, or `pi` when appropriate. Run the selected CLI's official login flow before starting Argus.

### 3. Start

```bash
argus
```

Useful checks:

```bash
argus --doctor
argus --status
```

## Update

```bash
cd Argus
git pull --ff-only
.venv/bin/python -m pip install -e .
.venv/bin/argus
```

The launcher detects stale local WebAPI and daemon processes and replaces them at a controlled task boundary.
