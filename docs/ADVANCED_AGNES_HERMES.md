# Advanced handoff: standalone Agnes + Hermes

This is the graduation path for users who no longer want FirstWindow to be the day-to-day control surface.

## What it creates

In **Advanced setup**, choose **Configure Agnes + Hermes**. FirstWindow prepares a separate Hermes profile named:

```text
agneshermes
```

This profile is independent from FirstWindow's beginner profile `firstwindowzero`.

It configures:

- Hermes Agent as the executor;
- Agnes `agnes-2.5-flash` for chat, coding, reasoning, tool calling, and image understanding;
- Agnes `agnes-image-2.1-flash` as Hermes' native image-generation backend;
- Agnes `agnes-video-v2.0` as Hermes' native video-generation backend;
- Hermes `hermes-cli` plus `video_gen` toolsets;
- an empty model fallback list.

The Agnes API key is supplied explicitly by the user and stored only in the standalone profile's `.env`. FirstWindow does not copy a credential from another Hermes profile.

## Use Hermes without FirstWindow

After the advanced handoff reports **configured**, FirstWindow can be closed. Start native Hermes with:

```powershell
hermes -p agneshermes chat
```

If Hermes created the profile alias on the current shell/platform, this shorter form may also work:

```powershell
agneshermes chat
```

The explicit `hermes -p agneshermes ...` form is the canonical command.

## What “configured” proves

The handoff verifies locally that:

- the independent Hermes profile exists;
- Agnes is selected as the chat provider;
- the expected Agnes chat model is selected;
- `fallback_providers` is empty;
- the API key is present in that profile;
- the Agnes image/video provider plugin files exist;
- both media plugins are enabled;
- the expected image/video models are selected;
- the required Hermes toolsets are enabled.

This is **configuration verification**, not a claim that a paid or quota-consuming media request was made successfully.

A real image or video generation is separate runtime evidence. API availability, quotas, and billing depend on the Agnes account and API key at the time of use.

## Cost boundary after graduation

FirstWindow's beginner path contains its own $0 confirmation and live-route guard. Once you launch native Hermes directly, **FirstWindow's $0 Guard is no longer in the execution loop**.

The standalone profile still prevents silent model fallback, but it cannot promise that an Agnes image/video request is free. Check the current Agnes account/plan before using media generation.

## Repair or update

Re-open FirstWindow → **Advanced** → **Configure Agnes + Hermes**.

The handoff is designed to repair the dedicated `agneshermes` profile in place without modifying the beginner `firstwindowzero` profile or copying unrelated provider credentials.
