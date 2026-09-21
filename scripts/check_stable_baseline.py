from __future__ import annotations

import hashlib
import json
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "STABLE_BASELINE.json"


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _actual_runtime_paths(root: Path) -> set[str]:
    paths = {"pyproject.toml", "scripts/firstwindow_gui.py"}
    package = root / "src" / "firstwindow"
    paths.update(
        p.relative_to(root).as_posix()
        for p in package.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    )
    return paths


def _actual_public_paths(root: Path) -> set[str]:
    paths = {"README.md", "vercel.json"}
    site = root / "site"
    paths.update(p.relative_to(root).as_posix() for p in site.rglob("*") if p.is_file())
    paths.update(
        {
            "docs/assets/firstwindow-window.png",
            "docs/assets/firstwindow-startup.gif",
        }
    )
    return paths


def _check_files(root: Path, expected: list[dict[str, Any]], actual_paths: set[str], label: str) -> list[str]:
    failures: list[str] = []
    expected_paths = {item["path"] for item in expected}
    if actual_paths != expected_paths:
        added = sorted(actual_paths - expected_paths)
        removed = sorted(expected_paths - actual_paths)
        if added:
            failures.append(f"{label} contains unbaselined files: {', '.join(added)}")
        if removed:
            failures.append(f"{label} is missing baselined files: {', '.join(removed)}")

    for item in expected:
        path = root / item["path"]
        if not path.is_file():
            failures.append(f"missing {label} file: {item['path']}")
            continue
        size = path.stat().st_size
        if size != item["size"]:
            failures.append(f"{label} size drift: {item['path']} expected={item['size']} actual={size}")
        digest = git_blob_sha(path)
        if digest != item["git_blob_sha"]:
            failures.append(
                f"{label} blob drift: {item['path']} expected={item['git_blob_sha']} actual={digest}"
            )
    return failures


def validate_stable_baseline(root: Path = ROOT, manifest_path: Path = MANIFEST) -> list[str]:
    failures: list[str] = []
    baseline = json.loads(manifest_path.read_text(encoding="utf-8"))

    if baseline.get("schema_version") != 1:
        failures.append("stable baseline schema_version must be 1")
    if baseline.get("project") != "FirstWindow":
        failures.append("stable baseline project must be FirstWindow")
    if baseline.get("status") != "stable-frozen":
        failures.append("stable baseline status must be stable-frozen")

    runtime = baseline["runtime_release"]
    project = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))["project"]

    state = json.loads((root / "PROJECT_STATE.json").read_text(encoding="utf-8"))
    contract = baseline["control_contract"]
    if state.get("current_release") != contract["current_release"]:
        failures.append("PROJECT_STATE current_release drift")

    launch_control = state.get("launch_control", {})
    frozen = (
        state.get("status") == contract["status"]
        and state.get("active_engineering_issue") is None
        and state.get("engineering_queue") == []
        and launch_control.get("product_baseline_frozen") is True
    )

    queue = state.get("engineering_queue")
    active = state.get("active_engineering_issue")
    engineering_transition = (
        state.get("status") not in {"post-release", "released"}
        and isinstance(active, int)
        and isinstance(queue, list)
        and bool(queue)
        and queue[0] == active
    )

    if frozen:
        if project["version"] != runtime["version"]:
            failures.append(
                f"package version drift: expected={runtime['version']} actual={project['version']}"
            )
        failures.extend(
            _check_files(root, runtime["files"], _actual_runtime_paths(root), "runtime")
        )
        public = baseline["public_surface"]
        failures.extend(
            _check_files(root, public["files"], _actual_public_paths(root), "public surface")
        )
        if launch_control.get("active_issue") != contract["launch_issue"]:
            failures.append("launch issue drift from stable baseline contract")
    elif engineering_transition:
        # Product drift is allowed only after project control explicitly enters
        # a scoped engineering state. PROJECT_STATE validation owns the rest of
        # the engineering-state invariants.
        pass
    else:
        failures.append(
            "baseline is neither frozen post-release nor an explicit scoped engineering transition"
        )

    return failures


def main() -> int:
    failures = validate_stable_baseline()
    if failures:
        print("stable baseline validation failed:")
        print("\n".join(f"- {failure}" for failure in failures))
        return 1
    baseline = json.loads(MANIFEST.read_text(encoding="utf-8"))
    print(
        "stable baseline ok: "
        f"{baseline['baseline_id']} "
        f"tag={baseline['runtime_release']['tag']} "
        f"runtime_files={len(baseline['runtime_release']['files'])} "
        f"public_files={len(baseline['public_surface']['files'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
