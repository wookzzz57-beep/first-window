# FirstWindow Beginner Guide

**English** · [简体中文](BEGINNER.zh-CN.md)

> **Goal:** finish your first task without learning coding-agent infrastructure first.

For the normal Windows path, you do **not** need a terminal. FirstWindow keeps the provider setup, route checks, resume state, and verification behind the app.

## 5-minute quick start

<!-- QUICKSTART:START -->

1. **Download FirstWindow**  
   Get [FirstWindow-Windows-x64.exe](https://github.com/wookzzz57-beep/first-window/releases/latest/download/FirstWindow-Windows-x64.exe). If Windows SmartScreen appears, choose **More info → Run anyway** after confirming you downloaded it from this repository.

2. **Open it and choose your language**  
   Pick **English** or **简体中文**. You can switch languages at any time; FirstWindow remembers the choice.

3. **Press Make Me Ready**  
   FirstWindow checks the computer and prepares a safe $0 route. If something needs your permission, it asks instead of guessing:
   - if Hermes is missing, approve the official installer once;
   - if the Agnes cloud route needs an API key, paste your own key when asked;
   - confirm that the current account/key route is $0 for **your** account.

   Agnes currently advertises a **Free API** on its official site: [agnes-ai.com](https://agnes-ai.com/). Account billing can vary, so FirstWindow still asks you to confirm the route before it runs.

4. **Pick your project folder**  
   Choose the folder FirstWindow is allowed to work in. If you only want to try it, use **Try a demo**.

5. **Describe the task and press Start**  
   Write what you want in normal language, for example:

   > Build a simple personal website and check that it runs.

   If a task was interrupted, choose the same project folder and use **Continue** instead of starting over.

<!-- QUICKSTART:END -->

That is the normal beginner flow.

## What “Make Me Ready” does

You do not need to understand these details to use the app. The button orchestrates them for you:

- checks whether Hermes is available;
- prepares FirstWindow's isolated Agnes route when needed;
- blocks unknown-cost fallback;
- runs a real readiness check before **Start** unlocks;
- keeps the selected project folder pinned for agent work.

FirstWindow may still ask for an install approval, your own API key, or your $0 confirmation. Those are deliberate security/cost boundaries and are not silently automated.

## If FirstWindow asks for an Agnes API key

1. Open [agnes-ai.com](https://agnes-ai.com/).
2. Choose the site's **Free API** / **Access API** entry and sign in if required.
3. Create or copy your API key from the Agnes account/API area.
4. Return to FirstWindow and paste it into the masked prompt.
5. Confirm the route is $0 for your account, then let FirstWindow run its readiness check.

FirstWindow stores the key only in its isolated Hermes profile for FirstWindow. It does not copy provider keys from your normal Hermes profile, store the key in task state, print it to logs, or pass it as a command-line argument.

## If Windows shows SmartScreen

The current community EXE is unsigned, so Windows may show an unknown-publisher warning.

For additional verification, download [SHA256SUMS.txt](https://github.com/wookzzz57-beep/first-window/releases/latest/download/SHA256SUMS.txt) from the same release and compare it with:

```powershell
Get-FileHash .\FirstWindow-Windows-x64.exe -Algorithm SHA256
Get-Content .\SHA256SUMS.txt
```

The SHA-256 values must match.

## If Make Me Ready cannot finish

Use the message FirstWindow shows as the next step. Common cases:

- **Hermes is missing** — approve the official installer, then FirstWindow continues.
- **Agnes API key is missing** — paste your key into the masked prompt.
- **The account/key is not confirmed as $0** — confirm only if it is actually free for your account.
- **A local model is not ready** — advanced users can set up a validated Hermes Managed Local model.
- **The readiness check fails** — no task starts on that route. Fix the shown problem and press **Make Me Ready** again.

FirstWindow fails closed: if it cannot verify a safe route, it stops instead of silently switching to an unknown-cost provider.

## Language switching

The Windows app supports:

- **English**
- **简体中文**

The language can be changed from the top-right selector while the app is open. The preference is saved and reused on the next launch.

Chinese guide: **[简体中文新手教程](BEGINNER.zh-CN.md)**

## What happens under the hood

This section is optional.

```text
FirstWindow
  └─ Hermes Agent
       ├─ Agnes API         ← cloud lane
       └─ Managed Local     ← optional local lane
```

FirstWindow is the control surface. Hermes Agent executes the work. Agnes API can be the cloud provider lane. Direct Agnes CLI is not required for the beginner path.

### Credential boundary

The Agnes key entered in FirstWindow is written only to the isolated `firstwindowzero` Hermes profile.

FirstWindow does **not**:

- copy the default Hermes `.env`;
- import unrelated provider keys;
- store credentials in `.firstwindow/tasks/`;
- print the Agnes key to logs;
- pass the key as a command-line argument;
- silently select another provider if Agnes authentication fails.

Deleting the isolated profile deletes FirstWindow's stored copy of that key.

### Project-directory safety

FirstWindow pins agent work to the selected project using multiple compatible safeguards, including the subprocess working directory, Hermes project selection, cwd-restore disabling, and `TERMINAL_CWD`.

### Durable Resume

Every task stores local recovery state under:

```text
.firstwindow/tasks/<task_id>/
```

That state contains the task objective, checkpoint, next action, evidence, and execution attestation. **Continue** resumes the same durable task instead of relying on hidden chat history.

### “Done” is not proof

FirstWindow separates agent execution from final outcome verification:

- **AC-001** — the agent process completed through the verified execution route.
- **AC-002** — the requested outcome was independently checked.

A successful agent exit can cover AC-001. It does not automatically cover AC-002.

```text
Agent finished
    ↓
execution covered
    ↓
independent outcome check
    ↓
VERIFIED
```

## Advanced CLI

The normal Windows flow does not require this section.

```bash
firstwindow tasks --project .
firstwindow resume <task_id> --project .
firstwindow verify <task_id>
```

For source installation and more CLI examples, see the main [README](../README.md).
