# Argus Doctor and Repair Pipeline Specification

- **Status:** Approved
- **Date:** 2026-08-14
- **Scope:** Source, editable, wheel, frozen Desktop, CLI, Web, daemon, Windows, macOS, Linux
- **Compatibility:** Preserve `argus --doctor`; accept `argus doctor` and hidden legacy `argus -doctor`

## 1. Context

Argus spans Python, Node, multiple Agent CLIs, a persistent daemon, WebAPI, Ink TUI, and Electron Desktop. Failures often present in one surface while their root cause lives in another: an occupied port, stale PID sidecar, missing Electron binary, stale release artifact, wrong interpreter, unavailable backend, or a process that is alive but making no semantic progress.

Doctor must turn those facts into deterministic findings. Repair must be a separate, typed, auditable phase. Different user machines require different actions, so successful and unsuccessful repair paths must be retained locally and exportable as a sanitized upstream report. No diagnostic text may be executed as a shell command.

## 2. Functional Requirements

- **FR-1 Read-only Doctor:** `argus doctor`, `argus --doctor`, and `argus -doctor` MUST perform no mutation.
- **FR-2 Bootstrap Doctor:** `argus-doctor` MUST run with the Python standard library when Argus Core cannot import.
- **FR-3 Cross-platform inventory:** Doctor MUST report OS, architecture, install mode, checkout, interpreter, venv, Git, Node, frontend assets, configured backend, Web endpoint, daemon identity, lock state, and known Desktop runtime paths.
- **FR-4 Stable findings:** Every finding MUST contain stable code, scope, severity, status, evidence, repair action IDs, and a human-safe recommendation.
- **FR-5 Blockage detection:** Doctor MUST distinguish stopped, starting, healthy, stalled, draining, owned port conflict, unowned port conflict, stale sidecar, missing dependency, and release mismatch.
- **FR-6 Repair plans:** `argus repair --plan` MUST persist a versioned plan with a unique ID, target fingerprint, preconditions, actions, risks, and verification checks.
- **FR-7 Registered actions only:** Repair MUST execute only actions registered in code. It MUST NOT execute arbitrary finding text.
- **FR-8 Authorization tiers:** SAFE actions MAY run under `argus repair --safe`; CONSENT actions require explicit `--apply <plan-id> --yes`; MANUAL actions are never executed.
- **FR-9 Revalidation:** Every action MUST revalidate its preconditions immediately before mutation and MUST skip when the target identity changed.
- **FR-10 Verification:** Repair MUST rerun Doctor and persist before/after findings and action outcomes.
- **FR-11 Path memory:** Repair MUST remember canonical checkout, interpreter, state root, Desktop user-data, Web endpoint, and successful repair provider paths under `ARGUS_SKILL_HOME/repairs/`.
- **FR-12 Audit history:** Plans and outcomes MUST be append-only/auditable and redact credentials and bearer tokens.
- **FR-13 Upstream report:** `argus repair --prepare-pr <plan-id>` MUST create a sanitized Markdown report with reproduction, environment class, findings, actions, verification, and candidate changed paths. It MUST NOT publish.
- **FR-14 Authorized PR submission:** `--submit-pr` MAY invoke GitHub CLI only after explicit confirmation, only from a clean checkout on a non-main branch, and only for tracked source changes produced by a registered repository repair action.
- **FR-15 Existing runtime safety:** Doctor/Repair MUST NOT kill unknown processes, reset/stash/merge Git, change credentials, elevate with sudo/UAC, or spend money automatically.

## 3. Non-functional Requirements

- **NFR-1:** Default Doctor completes within 10 seconds without network probes.
- **NFR-2:** Deep probes are bounded individually to 15 seconds.
- **NFR-3:** JSON output remains valid UTF-8 under Windows CP936/PowerShell 5.1.
- **NFR-4:** Plan application is idempotent; reapplying a completed SAFE plan performs no duplicate mutation.
- **NFR-5:** Secrets, tokens, credential-bearing URLs, and home-directory user names are redacted from export bundles.
- **NFR-6:** A failed repair leaves an explicit failed outcome and does not claim success.

## 4. Acceptance Criteria

- **AC-1 (FR-1):** Given a file-system snapshot, when Doctor runs, then no file content, process, port, or Git state changes.
- **AC-2 (FR-2):** Given an unimportable Core, when standalone Doctor runs, then it returns structured bootstrap findings instead of crashing.
- **AC-3 (FR-5):** Given a live daemon with stale semantic progress, Doctor reports `stalled`, not `stopped`.
- **AC-4 (FR-5):** Given an occupied Web port, Doctor identifies whether the listener is owned, compatible, incompatible, or unknown.
- **AC-5 (FR-6/FR-10):** Given repairable findings, `repair --plan` persists a plan; apply records outcomes and post-repair verification.
- **AC-6 (FR-7):** Given a malicious recommendation string, Repair never executes it.
- **AC-7 (FR-8/FR-9):** Given a SAFE stale PID action whose PID becomes live before apply, Repair skips it.
- **AC-8 (FR-11):** Given a successful provider action, its canonical executable/path is available to the next Doctor run.
- **AC-9 (FR-13):** Given a completed plan, prepare-pr emits a credential-free report and does not call GitHub.
- **AC-10 (FR-14):** Given no explicit confirmation, dirty main, or missing `gh` auth, submit-pr refuses safely.
- **AC-11 (NFR-3):** Given a CP936 stream, Doctor and Repair emit valid readable output without `UnicodeEncodeError`.
- **AC-12 (NFR-4):** Given an already applied plan, a second apply is a no-op with `already_applied` status.

## 5. Edge Cases

- **EC-1:** Multiple Argus checkouts exist; report all, never delete or silently choose a dirty checkout.
- **EC-2:** PID is reused; require PID plus boot identity/lock proof.
- **EC-3:** Port listener changes during inspection; mark finding `changed_during_probe`.
- **EC-4:** State root is read-only; downgrade actions to MANUAL.
- **EC-5:** Core imports but optional Desktop/Web dependencies are absent.
- **EC-6:** GitHub Actions or GitHub billing blocks CI; classify as external service, not a test failure.
- **EC-7:** Repair process is interrupted; the next run reconciles `running` actions to `interrupted` before continuing.

## 6. API Contracts

```ts
interface DoctorFinding {
  code: string;
  scope: 'host'|'install'|'cli'|'web'|'desktop'|'backend'|'daemon'|'project'|'update';
  severity: 'info'|'warning'|'error'|'critical';
  ok: boolean;
  status: string;
  detail: string;
  evidence: Record<string, unknown>;
  repair_action_ids: string[];
  recommendation: string;
}

interface RepairAction {
  id: string;
  provider: string;
  risk: 'safe'|'consent'|'manual';
  target: string;
  precondition: Record<string, unknown>;
  verify_codes: string[];
}

interface RepairPlan {
  schema_version: 1;
  plan_id: string;
  created_at: string;
  target_fingerprint: string;
  findings: DoctorFinding[];
  actions: RepairAction[];
  status: 'planned'|'running'|'completed'|'partial'|'failed';
}
```

## 7. Data Models

| Entity | Storage | Constraints |
|---|---|---|
| Repair plan | `repairs/plans/<plan-id>.json` | Immutable identity; atomic updates |
| Repair history | `repairs/history.jsonl` | Append-only; redacted |
| Path memory | `repairs/path-memory.json` | Canonical absolute paths; no secrets |
| PR report | `repairs/reports/<plan-id>.md` | Sanitized; no automatic publication |

## 8. Out of Scope

- Automatic credential creation, migration, deletion, or login.
- Automatic sudo/UAC/root elevation.
- Automatic package-manager installation outside the active Argus environment without consent.
- Automatic termination of unowned processes.
- Automatic Git reset, stash, merge, rebase, force-push, or main-branch commit.
- Fully autonomous PR publication without explicit operator authorization.
