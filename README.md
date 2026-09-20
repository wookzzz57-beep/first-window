# FirstWindow

<p align="center">
  <strong>Your first coding agent for Windows.</strong><br>
  Start from one window: get ready → choose a folder → describe the task.
</p>

<p align="center">
  <a href="https://github.com/wookzzz57-beep/first-window/releases/latest"><img alt="Latest release" src="https://img.shields.io/github/v/release/wookzzz57-beep/first-window"></a>
  <a href="https://github.com/wookzzz57-beep/first-window/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/wookzzz57-beep/first-window/actions/workflows/ci.yml/badge.svg?branch=main"></a>
  <a href="https://github.com/wookzzz57-beep/first-window/actions/workflows/windows-build.yml"><img alt="Windows build" src="https://github.com/wookzzz57-beep/first-window/actions/workflows/windows-build.yml/badge.svg?branch=main"></a>
  <a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <img alt="Windows" src="https://img.shields.io/badge/platform-Windows-0078D4">
</p>

<p align="center">
  <a href="https://github.com/wookzzz57-beep/first-window/releases/latest/download/FirstWindow-Windows-x64.exe"><strong>Download for Windows</strong></a>
  ·
  <a href="https://firstwindow-public.vercel.app">Website</a>
  ·
  <a href="docs/BEGINNER.md">Beginner Guide</a>
  ·
  <a href="https://github.com/wookzzz57-beep/first-window/releases/latest">Release Notes</a>
</p>

---

## Coding agents should not require an agent course

FirstWindow is a **beginner-first Windows launcher for coding agents**. It keeps provider setup, route checks, recovery state, and verification behind a small GUI so a new user can focus on the task instead of the plumbing.

### Start in 3 steps

| 1 · Get ready | 2 · Pick a folder | 3 · Describe the task |
| --- | --- | --- |
| Press **Make Me Ready / 一键就绪**. FirstWindow checks the setup and runs a live readiness probe. | Choose the project folder the agent is allowed to work in. | Write what you want in plain language and press **Start / 开始**. |

No terminal is required for the normal Windows flow. If an interrupted task is found, FirstWindow can offer **Continue / 继续** after the exact execution route is verified again.

<p align="center">
  <strong>Simple surface. Guarded execution. Verifiable completion.</strong>
</p>

### Real Windows walkthrough

<p align="center">
  <img src="docs/assets/firstwindow-startup.gif?v=real-v042-20260920" alt="Real FirstWindow v0.4.2 Windows walkthrough" width="880">
</p>

<p align="center"><sub>Captured from the packaged v0.4.2 Windows EXE: switch English / 简体中文, choose a safe demo project, and enter a task. Window-only capture; no generated mock UI.</sub></p>

## What makes FirstWindow different

| Beginner problem | FirstWindow behavior |
| --- | --- |
| “I do not know which provider this will use.” | **Route is explicit.** Hermes Agent is the executor; Agnes API can be the cloud lane, and a validated Hermes Managed Local model can be the local lane. |
| “Could this silently cost money?” | **Fail closed.** Unknown-cost routes are blocked instead of silently falling back. |
| “The agent stopped halfway through.” | **Durable resume.** Task, checkpoint, evidence, and next-action state are stored locally with the project. |
| “The agent said done. Is it actually done?” | **Evidence-based acceptance.** Agent exit success and final task verification are separate gates. |
| “I just want a Windows app.” | **GUI-first.** English / 简体中文 switching, readiness checks, Start, Continue, and status are available in one window. |

## Current release — v0.4.2

The current **v0.4.2 Windows app** is the stable product baseline.

- Packaged **Windows x64 EXE**
- **SHA-256 checksum** published with the release
- Real **Hermes Agent → Agnes API** readiness and task execution verified on Windows
- Strict **no-silent-fallback $0 guard**
- Durable **task + checkpoint + evidence + resume** flow
- Bilingual **English / 简体中文** UI
- Independent acceptance gate: agent exit 0 does **not** automatically mean VERIFIED

> The community EXE is currently **unsigned**, so Windows SmartScreen may show an unknown-publisher warning. Verify the download against [SHA256SUMS.txt](https://github.com/wookzzz57-beep/first-window/releases/latest/download/SHA256SUMS.txt).

## Under the simple surface

FirstWindow owns onboarding, routing, durable state, and acceptance. **Hermes Agent** owns execution.

For the Agnes route, FirstWindow uses an isolated Hermes profile, disables silent provider fallback, requires explicit free-route confirmation, runs a live readiness probe, and validates provider/model usage evidence.

Direct Agnes CLI is not required for the beginner path; it remains an advanced/manual option.


## Execution architecture

```text
                    ┌─────────────────────────────┐
                    │         FirstWindow         │
                    │ onboarding · routing ·      │
                    │ checkpoints · evidence      │
                    └──────────────┬──────────────┘
                                   │
                            Hermes Agent
                          ┌────────┴────────┐
                          │                 │
                     Agnes API       Managed Local
                    cloud lane       local lane
                          │                 │
                          └────────┬────────┘
                                   │
                         checkpoint + evidence
                                   │
                              VERIFIED?
```

FirstWindow owns the control surface and acceptance state. Hermes owns agent execution.

For the Agnes route, FirstWindow creates an isolated Hermes profile named `firstwindowzero`, disables fallback providers, requires explicit free-route confirmation, runs a live readiness probe, and validates usage evidence against the expected provider/model.

Changing or removing the Agnes credential invalidates the old route proof.

## “Done” is not proof

Each task stores repository-local durable state under `.firstwindow/tasks/<task_id>/`, including:

- objective and acceptance criteria
- checkpoint and next action
- append-only evidence
- execution/provider attestation
- resume context

The default beginner task separates:

- **AC-001** — the agent process completed through the verified execution route
- **AC-002** — the requested task outcome was independently verified

A successful agent run can cover AC-001. It cannot cover AC-002 just by saying “done”.

```text
Agent finished
    ↓
AC-001 covered
    ↓
Independent check required
    ↓
AC-002 covered
    ↓
VERIFIED
```

## Core features

- Windows GUI-first workflow
- English / 简体中文 live switching
- Diagnose
- Make Me Ready / 一键就绪
- Hermes Agent → Agnes API cloud lane
- Hermes Managed Local lane when a validated model is ready
- strict no-silent-fallback $0 guard
- isolated FirstWindow Hermes profile
- real readiness probe + usage attestation
- project-directory pinning
- durable checkpoints and Resume
- evidence ledger and acceptance coverage
- packaged Windows x64 EXE + SHA-256 checksum

<details>
<summary><strong>Install from source</strong></summary>

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -e .
firstwindow doctor
firstwindow-gui
```

</details>

<details>
<summary><strong>Advanced CLI examples</strong></summary>

```bash
firstwindow setup
firstwindow setup --install hermes --yes
firstwindow demo

firstwindow run "Add a /health endpoint and test it" \
  --accept "tests pass" \
  --accept "GET /health returns 200"

firstwindow tasks --project .
firstwindow resume <task_id> --project .
firstwindow evidence <task_id> --criterion AC-001 --kind test --detail "tests passed"
firstwindow evidence <task_id> --criterion AC-002 --kind probe --detail "GET /health -> 200"
firstwindow verify <task_id>
```

</details>

## Security and cost boundaries

FirstWindow intentionally does **not**:

- silently choose an unknown-cost provider
- clone a user's general Hermes provider credentials into its isolated profile
- treat configuration as proof of readiness
- treat agent exit 0 as proof of task completion
- silently switch providers after Agnes authentication fails
- claim Managed Local inference was verified when a validated local model was not available

See **[docs/BEGINNER.md](docs/BEGINNER.md)** for the full credential, route, and verification flow.

## Feedback and community

FirstWindow is still early. The most useful feedback is concrete: where onboarding was confusing, what failed on a real Windows machine, and which check prevented or missed a bad outcome.

- **Bug or setup problem:** [Open an issue](https://github.com/wookzzz57-beep/first-window/issues/new)
- **Questions / ideas:** [GitHub Discussions](https://github.com/wookzzz57-beep/first-window/discussions)
- **Latest binary:** [GitHub Releases](https://github.com/wookzzz57-beep/first-window/releases/latest)

If FirstWindow is useful to you—or you want to follow the experiment—**star the repository**. It helps other beginner agent users discover the project.

## License

MIT.
