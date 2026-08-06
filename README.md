<div align="center">
  <h1>ARGUS</h1>
  <p><strong>Autonomous research, engineered to persist.</strong></p>
  <p>A durable runtime for agents that need to plan, build, verify, pause, and continue beyond a single model turn.</p>
  <p>
    <a href="https://argusbot.cn"><strong>Website</strong></a>
    &nbsp;·&nbsp;
    <a href="https://www.youtube.com/watch?v=i8Qy9HCboQE"><strong>Demo</strong></a>
    &nbsp;·&nbsp;
    <a href="technical_report/argus-technical-report.pdf"><strong>Technical Report</strong></a>
    &nbsp;·&nbsp;
    <a href="README.zh-CN.md"><strong>简体中文</strong></a>
  </p>
  <p>
    <code>PREVIEW · v0.1.1</code>
    &nbsp;
    <code>OFFICIAL OPEN-SOURCE RELEASE · ON THE WAY</code>
  </p>
</div>

---

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>Persistent by design</h3>
      Tasks, checkpoints, decisions, Skills, and review evidence survive across sessions and process upgrades.
    </td>
    <td width="50%" valign="top">
      <h3>Reviewed by default</h3>
      Execution and verification stay separate. Every normal round ends with an independent Reviewer judgment.
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>Agent-native</h3>
      Roles work with real files, tools, terminals, experiments, and artifacts instead of a closed workflow editor.
    </td>
    <td width="50%" valign="top">
      <h3>Built to be extended</h3>
      Adapt the runtime to your own field with custom role guidance, tools, stages, evidence rules, and Verticals.
    </td>
  </tr>
</table>

## One runtime. Four authorities.

<table>
  <tr>
    <td width="25%" valign="top">
      <strong>01 · MANAGER</strong><br><sub>CONTROL</sub><br><br>
      Interprets operator intent, selects the workflow, and owns stage transitions.
    </td>
    <td width="25%" valign="top">
      <strong>02 · PLANNER</strong><br><sub>DIRECTION</sub><br><br>
      Chooses the next high-value task and defines what evidence it must produce.
    </td>
    <td width="25%" valign="top">
      <strong>03 · ENGINEER</strong><br><sub>EXECUTION</sub><br><br>
      Implements, researches, runs experiments, and creates inspectable artifacts.
    </td>
    <td width="25%" valign="top">
      <strong>04 · REVIEWER</strong><br><sub>VERIFICATION</sub><br><br>
      Independently checks correctness, evidence, limitations, and completion.
    </td>
  </tr>
</table>

Argus keeps these authorities connected through durable project state. A project can stop, resume, survive a runtime replacement, and continue from its latest verified position.

**Native agent backends** &nbsp; `GitHub Copilot CLI` · `Pi` · `OpenAI Codex CLI` · `Claude Code` · `OpenCode`

---

## Start in three steps

### 1 · Install

**Requirements:** Python 3.11+, Node.js 22+, and one authenticated agent CLI.

```bash
git clone https://github.com/lbx154/Argus.git
cd Argus

python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
```

### 2 · Connect a backend

```bash
argus --setup --non-interactive \
  --backend copilot \
  --accept-house-rules
```

Use `copilot`, `pi`, `codex`, `claude`, or `opencode` for `--backend`.

### 3 · Launch

```bash
argus
```

```bash
argus --doctor   # verify the installation
argus --status   # inspect the current runtime
```

---

## Choose your surface

### Terminal cockpit

```bash
argus
```

The terminal cockpit is the fastest way to talk to the Manager, follow live work, inspect state, and resume projects.

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

#### Remote server over SSH — recommended

On the server:

```bash
argus --web --no-open
```

On your computer:

```bash
ssh -L 8799:127.0.0.1:8799 user@server
```

Open [http://127.0.0.1:8799](http://127.0.0.1:8799) locally.

<details>
<summary><strong>Direct LAN access</strong></summary>

<br>

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

---

## Design your own Argus

Argus is designed to be changed, not merely configured.

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>Shape the runtime</h3>
      Tune role prompts, workflow boundaries, review policy, tools, and operating conventions until the complete loop matches how you work.
    </td>
    <td width="50%" valign="top">
      <h3>Build a Vertical</h3>
      Give your field its own stages, Skills, datasets, tools, evidence requirements, evaluation methods, and completion criteria.
    </td>
  </tr>
</table>

If you are an agent enthusiast, we recommend running Argus locally and evolving it into a runtime for your own ambitious domain. Preserve the behavior you care about with tests, connect the infrastructure you already use, and let planning and review follow the standards of your field rather than a generic process.

### Use another agent as the outer layer

GitHub Copilot, Pi, Codex, Claude Code, OpenCode, OpenClaw, or Hermes can act as the environment from which you invoke Argus, inspect its state, operate its local CLI or Web/API surface, and continue improving the deployment.

- **Native Argus backends:** GitHub Copilot CLI, Pi, Codex CLI, Claude Code, OpenCode
- **External agent operators:** OpenClaw, Hermes, or any agent that can use a shell or HTTP API

Useful entry points:

```bash
argus --doctor
argus --status
argus --web --no-open
```

---

## Update

```bash
cd Argus
git pull --ff-only
.venv/bin/python -m pip install -e .
.venv/bin/argus
```

Argus detects stale local WebAPI and daemon processes and replaces them at a controlled task boundary.
