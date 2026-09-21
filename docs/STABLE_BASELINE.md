# FirstWindow Stable Baseline

The accepted runtime and GitHub public-source baseline is **v0.4.3**.

This baseline deliberately separates **released product truth**, **checked-in public-source truth**, and **external production deployment truth** so an external deployment lag cannot be mistaken for a runtime regression.

## 1. Runtime release truth

Canonical identity:

- release tag: `v0.4.3`
- tag commit: `c5b0b4d864d57998676585efc8505232d6008c2c`
- GitHub Release ID: `392790362`
- Windows EXE SHA-256: `3696420971ad124cd63ed76eb02acce2d338c5a7276b7208fce33905d04865b4`
- release Windows workflow: `35577250346` — success
- release CI workflow: `35577250248` — success

The tag-driven Windows workflow rebuilt the single-file EXE, passed packaged self-test and packaged English/简体中文 UI self-test, generated SHA256SUMS, verified tag/version equality, and created the GitHub Release.

The exact runtime/package source files are pinned by Git blob SHA in `STABLE_BASELINE.json`.

## 2. GitHub public-source truth

Accepted public-surface main SHA:

- `0622d28aea287e063d1f426b0dabc45c9d8d5158`

The README identifies v0.4.3 as the current release and now uses **real packaged v0.4.3 window-only captures**:

- `docs/assets/firstwindow-window-v043.png`
- `docs/assets/firstwindow-startup-v043.gif`

The capture source was the official v0.4.3 Release EXE after verifying SHA-256 `3696420971ad124cd63ed76eb02acce2d338c5a7276b7208fce33905d04865b4`. The application window was captured in isolation; no unrelated desktop/browser content is represented.

The earlier v0.4.2 PNG/GIF remain byte-for-byte preserved as historical provenance assets for the existing historical website block.

All accepted public-source files are pinned by Git blob SHA in `STABLE_BASELINE.json`.

## 3. External production deployment truth

Canonical URL:

- https://firstwindow-public.vercel.app

At the v0.4.3 baseline closure check, the canonical Vercel deployment still served `softwareVersion=0.4.2` and footer `current release v0.4.2`.

This is an **external synchronization blocker**, not evidence that the v0.4.3 GitHub Release failed. Production must not be claimed as v0.4.3 until independently read back and verified.

Verification used DNS-over-HTTPS to obtain a current Vercel A record and `curl --resolve` so the request preserved the correct Host/SNI and TLS validation. TLS verification was not disabled.

## 4. Control truth

While v0.4.3 remains the accepted product baseline:

- `PROJECT_STATE.status == "post-release"`
- `current_release == "v0.4.3"`
- `active_engineering_issue == null`
- `engineering_queue == []`
- `launch_control.product_baseline_frozen == true`
- launch issue remains `#17`

External blockers may remain in post-release state, but they must be explicit and must not be turned into false product claims.

## Mutation rule

A runtime or accepted GitHub public-source file must not drift silently.

To intentionally change one:

1. create a scoped engineering issue with evidence;
2. transition project control into engineering-active state;
3. change and verify the product on an isolated branch;
4. pass CI / Windows / release acceptance;
5. establish the next accepted baseline;
6. only then update `STABLE_BASELINE.json`.

External production deployment state is verified independently from repository source truth.

## Automated checks

`python scripts/check_stable_baseline.py` verifies:

- exact runtime file set and Git blob identities;
- exact GitHub public-source file set and Git blob identities;
- package version;
- frozen project-control state.

CI additionally verifies the pinned GitHub tag and Release asset identities. During a scoped release transition it validates the pinned prior release by ID without incorrectly requiring it to remain GitHub Latest; once frozen, Latest must equal the accepted stable release.
