# FirstWindow Stable Baseline

The accepted stable product baseline is **v0.4.2**.

This baseline is intentionally split into three kinds of truth so later control-only maintenance cannot be confused with a product release.

## 1. Runtime release truth

Canonical identity:

- release tag: `v0.4.2`
- tag commit: `73454bb09cfaf4c43a3fcc1a77cd3d0e80375148`
- GitHub Release ID: `392384670`
- Windows EXE SHA-256: `953f5f260439976d46db4f6b81dd3a74afca83e006edd0d3daf0c24b538b11b0`

The exact runtime/package source files are pinned by Git blob SHA in `STABLE_BASELINE.json`.

## 2. Public-surface truth

The accepted v0.4.2 public surface includes:

- README and website content
- the real packaged-v0.4.2 PNG and GIF captures
- production deployment `dpl_G7TPV8JNzKspE1aoBjMm6w8jPcaW`
- canonical production URL: https://firstwindow-public.vercel.app
- independent production verification run `35504289632`

Those files are also pinned by Git blob SHA.

## 3. Control truth

While v0.4.2 remains the stable product baseline:

- `PROJECT_STATE.status == "post-release"`
- `current_release == "v0.4.2"`
- `active_engineering_issue == null`
- `engineering_queue == []`
- `launch_control.product_baseline_frozen == true`

The launch track may continue without changing the stable product baseline.

## Mutation rule

A runtime or accepted public-surface file must not drift silently.

To intentionally change one:

1. create a scoped engineering issue with evidence;
2. transition project control into engineering-active state;
3. change and verify the product on an isolated branch;
4. pass CI / Windows / release acceptance;
5. establish the next accepted baseline;
6. only then update `STABLE_BASELINE.json`.

Control-only files may evolve without changing the v0.4.2 runtime/public baseline, provided the frozen-product contract still passes.

## Automated checks

`python scripts/check_stable_baseline.py` verifies:

- exact runtime file set and Git blob identities;
- exact public-surface file set and Git blob identities;
- package version;
- frozen project-control state.

CI additionally verifies the live GitHub tag and Release asset identities.

The branch-protection policy on `main` is the repository-level enforcement layer: pull requests are required, CI and Windows checks are required, and force-push/delete are blocked.
