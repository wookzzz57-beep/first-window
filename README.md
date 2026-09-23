# FirstWindow

<p align="center">
  <strong>Your first coding agent for Windows — powered by Hermes Agent + Agnes AI.</strong><br>
  Free-first, beginner-first: one window to start, and a clear path to native Hermes when you are ready.<br>
  面向 Windows 新手的免费优先 AI Agent 入口：一键就绪，学会后可进阶原生 Hermes。
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
  <a href="https://github.com/wookzzz57-beep/first-window/actions/workflows/windows-build.yml?query=branch%3Amain">Latest development build (ZIP)</a>
  ·
  <a href="https://firstwindow-public.vercel.app">Website</a>
  ·
  <a href="docs/ADVANCED_AGNES_HERMES.md">Advanced handoff (source only)</a>
  ·
  <a href="docs/BEGINNER.md">Beginner Guide</a>
  ·
  <a href="docs/BEGINNER.zh-CN.md">简体中文教程</a>
  ·
  <a href="https://github.com/wookzzz57-beep/first-window/releases/latest">Release Notes</a>
</p>

---

## Coding agents should not require an agent course

FirstWindow is a **beginner-first, free-first Windows desktop launcher** built on [Hermes Agent](https://github.com/NousResearch/hermes-agent) and [Agnes AI](https://github.com/AgnesAI-Labs/AgnesAI-Models). It brings setup, guarded model routing, resumable execution, and evidence-based verification into one small GUI. **It does not train a new model or replace Hermes.**

**中文简介：** FirstWindow 站在 Agnes + Hermes 的肩膀上，把安装配置、免费优先路由、断点恢复和验收放进一个 Windows 窗口，让第一次接触 Agent 的用户也能开始完成真实任务。它不是第三套 Agent 引擎，也不会锁定高级用户。

### Built on Agnes + Hermes

| Foundation | What it contributes |
| --- | --- |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | The actual agent runtime: reasoning loop, task execution, tools, coding workflows, and native profiles. |
| [Agnes AI](https://github.com/AgnesAI-Labs/AgnesAI-Models) | The optional cloud model/API route. Its API family covers text and image understanding, with separate image and video generation endpoints. |
| **FirstWindow** | Beginner onboarding, explicit route/cost checks, project-scoped tasks, checkpoints, resume, evidence, and independent acceptance. |

### Choose your path

| New to agents — **available in v0.4.3** | Growing beyond the GUI — **advanced handoff in source, not yet released** |
| --- | --- |
| Download the Windows app, select a project folder, describe the task, and use **Start / Continue**. | The [advanced setup](docs/ADVANCED_AGNES_HERMES.md) in the current source prepares a separate `agneshermes` Hermes profile with Agnes text/vision and independent image/video backends. After configuration, you can close FirstWindow and use `hermes -p agneshermes chat`. |
| FirstWindow retains its guarded `$0` confirmation, recovery, and evidence gates. | Direct native Hermes use is outside FirstWindow’s runtime `$0` guard. API availability and media-generation costs depend on your Agnes account. |

> **Release status:** The downloadable **v0.4.3 EXE does not include the advanced handoff button**. Advanced setup is available from the current source (`pip install -e .` followed by `firstwindow-gui`); see the [English](docs/ADVANCED_AGNES_HERMES.md) or [中文](docs/ADVANCED_AGNES_HERMES.zh-CN.md) guide. Local configuration checks do **not** prove that live Agnes image/video calls work or are free for every account.

### What “$0” means

FirstWindow is **free and open source (MIT)**. Its beginner `$0` mode requires explicit confirmation of an eligible free route and **fails closed** rather than silently switching to an unknown-cost provider. **Agnes API access, free quotas, rate limits, and image/video billing are account-dependent**; FirstWindow does not make a paid API free. Direct Hermes use after the advanced handoff does not inherit FirstWindow’s runtime cost guard.

### Start in 3 steps

| 1 · Get ready | 2 · Pick a folder | 3 · Describe the task |
| --- | --- | --- |
| Press **Make Me Ready / 一键就绪**. FirstWindow checks the setup and runs a live readiness probe. | Choose the project folder the agent is allowed to work in. | Write what you want in plain language and press **Start / 开始**. |

No terminal is required for the normal Windows flow. On a first run, **Make Me Ready / 一键就绪** handles the setup sequence and only stops for things that require your decision, such as approving the official Hermes installer, pasting your own Agnes API key, or confirming that the current route is $0 for your account. If a task is interrupted, use **Continue / 继续** instead of starting over.

**First time?** Use the [5-minute English guide](docs/BEGINNER.md) or [5 分钟简体中文教程](docs/BEGINNER.zh-CN.md). The advanced routing/security details are there when you need them, not before your first task.

<p align="center">
  <strong>Simple surface. Guarded execution. Verifiable completion.</strong>
</p>

### Real v0.4.3 Windows walkthrough

<p align="center">
  <img src="docs/assets/firstwindow-startup-v043.gif?v=real-v043-20260921" alt="Real FirstWindow v0.4.3 packaged Windows walkthrough in English and Simplified Chinese" width="880">
</p>

<p align="center"><sub>Captured from the official packaged v0.4.3 Windows EXE after verifying the release SHA-256. The GIF contains only the FirstWindow application window and shows the real single-path workspace in English and 简体中文; no generated mock UI or unrelated desktop content.</sub></p>

<p align="center">
  <img src="docs/assets/firstwindow-window-v043.png?v=real-v043-20260921" alt="Real FirstWindow v0.4.3 Windows application window" width="880">
</p>

## What makes FirstWindow different

| Beginner problem | FirstWindow behavior |
| --- | --- |
| “I do not know which provider this will use.” | **Route is explicit.** Hermes Agent is the executor; Agnes API can be the cloud lane, and a validated Hermes Managed Local model can be the local lane. |
| “Could this silently cost money?” | **Fail closed.** Unknown-cost routes are blocked instead of silently falling back. |
| “The agent stopped halfway through.” | **Durable resume.** Task, checkpoint, evidence, and next-action state are stored locally with the project. |
| “The agent said done. Is it actually done?” | **Evidence-based acceptance.** Agent exit success and final task verification are separate gates. |
| “I just want a Windows app.” | **GUI-first.** English / 简体中文 switching, readiness checks, Start, Continue, and status are available in one window. |

## Current release — v0.4.3

The current **v0.4.3 Windows app** is the latest released product.

- Packaged **Windows x64 EXE**
- **SHA-256 checksum** published with the release
- Real **Hermes Agent → Agnes API** readiness and task execution verified on Windows
- Strict **no-silent-fallback $0 guard**
- Durable **task + checkpoint + evidence + resume** flow
- Bilingual **English / 简体中文** UI
- Independent acceptance gate: agent exit 0 does **not** automatically mean VERIFIED

> The community EXE is currently **unsigned**, so Windows SmartScreen may show an unknown-publisher warning. Verify the download against [SHA256SUMS.txt](https://github.com/wookzzz57-beep/first-window/releases/latest/download/SHA256SUMS.txt).

> **Development build (NOT an official release):** The [Windows App workflow](https://github.com/wookzzz57-beep/first-window/actions/workflows/windows-build.yml?query=branch%3Amain) packages the current `main` source on successful runs. Open the latest successful **main / push** run and download `FirstWindow-Windows-x64` under **Artifacts** (GitHub sign-in may be required). The ZIP contains `FirstWindow-Windows-x64.exe` and its matching `SHA256SUMS.txt`; verify the EXE before running it. Current development builds include opt-in standalone Agnes + Hermes advanced setup, but **target-Windows native Hermes and live Agnes image/video acceptance remain outstanding**. They are test candidates, not the verified v0.4.3 Release, even while the embedded package version still reads `0.4.3`. For new users, use the official stable download above.

## Under the simple surface

FirstWindow owns onboarding, routing, durable state, and acceptance. **Hermes Agent** owns execution.

For the Agnes route, FirstWindow uses an isolated Hermes profile, disables silent provider fallback, requires explicit free-route confirmation, runs a live readiness probe, and validates provider/model usage evidence.

Direct Agnes CLI is not required for the beginner path. Native Hermes is a separate advanced option: [follow the standalone Agnes + Hermes handoff guide](docs/ADVANCED_AGNES_HERMES.md). The opt-in feature is available in source, not the published v0.4.3 binary. It creates an independent profile rather than modifying the beginner profile.


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

Start with the **[5-minute English guide](docs/BEGINNER.md)** or **[5 分钟简体中文教程](docs/BEGINNER.zh-CN.md)**. Technical credential, routing, and verification details are kept below the quick-start path.

## Feedback and community

FirstWindow is still early. The most useful feedback is concrete: where onboarding was confusing, what failed on a real Windows machine, and which check prevented or missed a bad outcome.

- **Bug or setup problem:** [Open an issue](https://github.com/wookzzz57-beep/first-window/issues/new)
- **Questions / ideas:** [GitHub Discussions](https://github.com/wookzzz57-beep/first-window/discussions)
- **Latest binary:** [GitHub Releases](https://github.com/wookzzz57-beep/first-window/releases/latest)

If FirstWindow is useful to you—or you want to follow the experiment—**star the repository**. It helps other beginner agent users discover the project.

## License

MIT.
