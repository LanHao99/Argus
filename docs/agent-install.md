# Argus installation instructions for coding agents

You are responsible for completing the installation, not merely describing
commands. Keep changes scoped to Argus and follow these rules:

- Argus does not require a separate Argus account. The selected backend must
  be installed and authenticated through its official login flow.
- Inspect before changing the machine.
- Prefer the Agent CLI that is already running and authenticated.
- Ask before using `sudo`, installing system packages, changing shell startup
  files, or changing global Git or backend configuration.
- Never request secrets in chat, print secrets, or write credentials into the
  Argus repository. Use the backend's official interactive login flow.
- Do not overwrite an existing Argus checkout or discard local modifications.
- Stop and explain the exact blocker if a required action cannot be completed.

### 1. Inspect the environment

Determine the operating system and check:

```bash
git --version
python3 --version
node --version
```

Requirements:

- Python 3.11 or newer
- Node.js 22 or newer
- Git
- One supported Agent CLI

Check which supported backends are available:

```bash
command -v copilot || true
command -v codex || true
command -v claude || true
command -v pi || true
command -v opencode || true
command -v grok || true
command -v qodercli || true
command -v dsh || true
```

Select the CLI hosting the current conversation when possible. Otherwise,
prefer an already installed and authenticated backend. Supported Argus backend
values are:

| Agent CLI | Argus backend |
|---|---|
| GitHub Copilot CLI | `copilot` |
| OpenAI Codex CLI | `codex` |
| Claude Code | `claude` |
| Pi | `pi` |
| OpenCode | `opencode` |
| xAI Grok Build | `grok` |
| Qoder CLI | `qoder` |
| DeepSeek Harness | `dsh` |

If prerequisites are missing, explain the proposed installation command and
obtain approval before using a system package manager, `sudo`, or making a
global installation. Follow the prerequisite project's official installation
instructions rather than inventing an unofficial download source.

### 2. Confirm backend authentication

Use a read-only status or version check first. If the selected CLI is not
authenticated, start its official interactive login flow and let the user
complete browser/device authorization directly. Do not ask the user to send
credentials through chat.

If the current Agent CLI is clearly working through its normal authenticated
session, do not force an unnecessary re-login.

### 3. Install Argus

Choose a persistent installation directory with the user. If they have no
preference, use `$HOME/Argus`.

For a new installation:

```bash
git clone https://github.com/lbx154/Argus.git "$HOME/Argus"
cd "$HOME/Argus"
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

If `$HOME/Argus` already exists:

1. Verify that it is the Argus repository.
2. Inspect `git status`.
3. Never remove or overwrite local changes.
4. If it is clean, update it with `git pull --ff-only`.
5. Re-run `.venv/bin/python -m pip install -e .`.

On Windows, use the platform-appropriate virtual-environment executable and
activation command. Do not assume a POSIX shell.

### 4. Configure the selected backend

From the Argus checkout, run:

```bash
.venv/bin/argus --setup --non-interactive \
  --backend <copilot|codex|claude|pi|opencode|grok|qoder|dsh>
```

Windows PowerShell:

```powershell
.\.venv\Scripts\argus.exe --setup --non-interactive `
  --backend <copilot|codex|claude|pi|opencode>
```

For an OpenAI-compatible endpoint, no backend flag is needed. Setup installs Pi
when it is missing:

```bash
ARGUS_SETUP_API_KEY=... .venv/bin/argus --setup --non-interactive \
  --api-url https://api.example.com/v1 --api-model model-id
```

```powershell
$env:ARGUS_SETUP_API_KEY = "..."
.\.venv\Scripts\argus.exe --setup --non-interactive `
  --api-url https://api.example.com/v1 --api-model model-id
```

Use the backend selected in steps 1-2. Do not silently switch to another
provider after a failed readiness check. Diagnose the reported failure first,
then either fix it or ask the user to choose another installed backend.

### 5. Confirm the model selector

Argus sends a model id to the backend CLI, and its shared default belongs to
the OpenAI catalog. Setup adopts a backend-appropriate model where Argus knows
one, but for any backend it does not, an unset model resolves to an id that CLI
cannot serve — every call then fails, and the Manager reports it only as
`[not dispatched] Manager could not classify this message`.

`argus --setup` reports a `model selector` failure when it can prove the id is
wrong, so a clean setup already covers most cases. Confirm what each role will
actually send:

```bash
.venv/bin/argus --config-help
```

The `[models]` section prints every model knob with its resolved value and
where that value came from (`env`, `persisted`, or `default`). A value marked
`(default)` was chosen by nobody — check that it belongs to the selected
backend's catalog.

If it does not, list the ids the account really holds. The listing command is
backend-specific:

```bash
pi --list-models
opencode auth list
qodercli --list-models
```

Set the chosen id in the environment Argus launches from:

```bash
export ARGUS_SKILL_MODEL=<model-id>
```

`ARGUS_SKILL_MODEL` is the shared default; per-role knobs
(`ARGUS_SKILL_MANAGER_MODEL`, `ARGUS_SKILL_ENGINEER_MODEL`,
`ARGUS_SKILL_REVIEWER_MODEL`, `ARGUS_SKILL_PLAN_MODEL`) override it. Ask before
writing the export into a shell startup file. Inside the running cockpit the
operator can also say "switch the model to <model-id>", which persists the
choice for future sessions.

### 6. Verify the installation

Run:

```bash
.venv/bin/argus --doctor
.venv/bin/argus --status
```

The task is complete only when `argus --doctor` reports that the installation
and selected backend are ready. Do not claim success based only on a successful
package installation.

If the user wants `argus` available outside the checkout, offer a safe PATH or
launcher option appropriate for their operating system. Do not edit shell
startup files without approval.

### 7. Report the result

Tell the user:

- the Argus installation directory;
- the selected backend;
- the model id each role will use;
- whether `argus --doctor` passed;
- the exact command to start Argus;
- any remaining manual action.

Typical launch commands:

```bash
cd "$HOME/Argus"
.venv/bin/argus
```

Web UI:

```bash
cd "$HOME/Argus"
.venv/bin/argus --web
```
