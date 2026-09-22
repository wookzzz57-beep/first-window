from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import shutil
import subprocess
from typing import Any, Callable, Mapping, Sequence

from .hermes_agnes import (
    AGNES_KEY_ENV,
    AGNES_MODEL,
    AGNES_PROVIDER,
    HermesAgnesRoute,
    agnes_api_key_present,
    parse_profile_path,
    read_hermes_agnes_route,
    save_agnes_api_key,
    scoped_env,
)

STANDALONE_HERMES_PROFILE = "agneshermes"
AGNES_IMAGE_MODEL = "agnes-image-2.1-flash"
AGNES_VIDEO_MODEL = "agnes-video-v2.0"
AGNES_API_ROOT = "https://apihub.agnes-ai.com"
AGNES_CHAT_BASE_URL = f"{AGNES_API_ROOT}/v1"
IMAGE_PLUGIN_KEY = "image_gen/agnes"
VIDEO_PLUGIN_KEY = "video_gen/agnes"
DIRECT_HERMES_COMMAND = f"hermes -p {STANDALONE_HERMES_PROFILE} chat"


@dataclass(frozen=True)
class StandaloneHandoffResult:
    ready: bool
    created: bool
    profile_home: str | None
    route: HermesAgnesRoute
    image_plugin_ready: bool
    video_plugin_ready: bool
    direct_command: str
    reason: str


def _run(
    command: Sequence[str],
    *,
    env: Mapping[str, str] | None = None,
    runner: Callable[..., Any] = subprocess.run,
    timeout: int = 30,
):
    return runner(
        list(command),
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=None if env is None else dict(env),
        timeout=timeout,
    )


def _json_value(
    key: str,
    *,
    env: Mapping[str, str],
    runner: Callable[..., Any] = subprocess.run,
) -> Any:
    try:
        completed = _run(["hermes", "config", "get", key, "--json"], env=env, runner=runner, timeout=12)
    except (OSError, subprocess.SubprocessError):
        return None
    if int(getattr(completed, "returncode", 1)) != 0:
        return None
    try:
        return json.loads(str(getattr(completed, "stdout", "") or "").strip())
    except (TypeError, json.JSONDecodeError):
        return None


def find_standalone_profile(*, runner: Callable[..., Any] = subprocess.run) -> str | None:
    try:
        completed = _run(
            ["hermes", "profile", "show", STANDALONE_HERMES_PROFILE],
            runner=runner,
            timeout=12,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if int(getattr(completed, "returncode", 1)) != 0:
        return None
    return parse_profile_path(str(getattr(completed, "stdout", "") or ""))


def _set_config(
    key: str,
    value: str,
    *,
    env: Mapping[str, str],
    runner: Callable[..., Any],
) -> bool:
    try:
        completed = _run(
            ["hermes", "config", "set", key, value, "--force"],
            env=env,
            runner=runner,
            timeout=20,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return int(getattr(completed, "returncode", 1)) == 0


def _write_plugin(profile_home: str | Path, category: str, source: str, manifest: str) -> Path:
    root = Path(profile_home) / "plugins" / category / "agnes"
    root.mkdir(parents=True, exist_ok=True)
    (root / "__init__.py").write_text(source.rstrip() + "\n", encoding="utf-8")
    (root / "plugin.yaml").write_text(manifest.rstrip() + "\n", encoding="utf-8")
    return root


def install_agnes_media_plugins(profile_home: str | Path) -> tuple[Path, Path]:
    image_root = _write_plugin(profile_home, "image_gen", _IMAGE_PLUGIN_SOURCE, _IMAGE_PLUGIN_MANIFEST)
    video_root = _write_plugin(profile_home, "video_gen", _VIDEO_PLUGIN_SOURCE, _VIDEO_PLUGIN_MANIFEST)
    return image_root, video_root


def _plugin_config_ready(
    profile_home: str | Path,
    *,
    runner: Callable[..., Any] = subprocess.run,
) -> tuple[bool, bool]:
    env = scoped_env(profile_home)
    enabled = _json_value("plugins.enabled", env=env, runner=runner)
    image_provider = _json_value("image_gen.provider", env=env, runner=runner)
    image_model = _json_value("image_gen.model", env=env, runner=runner)
    video_provider = _json_value("video_gen.provider", env=env, runner=runner)
    video_model = _json_value("video_gen.model", env=env, runner=runner)
    toolsets = _json_value("toolsets", env=env, runner=runner)

    enabled_set = {str(item) for item in enabled} if isinstance(enabled, list) else set()
    toolset_set = {str(item) for item in toolsets} if isinstance(toolsets, list) else set()
    root = Path(profile_home) / "plugins"
    image_files = all((root / "image_gen" / "agnes" / name).is_file() for name in ("__init__.py", "plugin.yaml"))
    video_files = all((root / "video_gen" / "agnes" / name).is_file() for name in ("__init__.py", "plugin.yaml"))

    image_ready = bool(
        image_files
        and IMAGE_PLUGIN_KEY in enabled_set
        and str(image_provider or "") == "agnes"
        and str(image_model or "") == AGNES_IMAGE_MODEL
        and "hermes-cli" in toolset_set
    )
    video_ready = bool(
        video_files
        and VIDEO_PLUGIN_KEY in enabled_set
        and str(video_provider or "") == "agnes"
        and str(video_model or "") == AGNES_VIDEO_MODEL
        and "video_gen" in toolset_set
    )
    return image_ready, video_ready


def read_standalone_handoff(
    *,
    which: Callable[[str], str | None] = shutil.which,
    runner: Callable[..., Any] = subprocess.run,
) -> StandaloneHandoffResult:
    profile_home = find_standalone_profile(runner=runner) if which("hermes") else None
    route = read_hermes_agnes_route(profile_home, which=which, runner=runner)
    if not profile_home:
        return StandaloneHandoffResult(
            False, False, None, route, False, False, DIRECT_HERMES_COMMAND,
            "standalone-profile-missing" if route.hermes_installed else "hermes-not-installed",
        )
    image_ready, video_ready = _plugin_config_ready(profile_home, runner=runner)
    credential_ready = agnes_api_key_present(profile_home)
    ready = bool(route.ready and credential_ready and image_ready and video_ready)
    if ready:
        reason = "standalone-agnes-hermes-ready"
    elif not credential_ready:
        reason = "agnes-key-missing"
    elif not route.ready:
        reason = route.reason
    elif not image_ready:
        reason = "image-plugin-not-ready"
    else:
        reason = "video-plugin-not-ready"
    return StandaloneHandoffResult(
        ready, False, profile_home, route, image_ready, video_ready, DIRECT_HERMES_COMMAND, reason
    )


def ensure_standalone_agnes_hermes(
    api_key: str | None = None,
    *,
    which: Callable[[str], str | None] = shutil.which,
    runner: Callable[..., Any] = subprocess.run,
) -> StandaloneHandoffResult:
    if which("hermes") is None:
        route = read_hermes_agnes_route(None, which=which, runner=runner)
        return StandaloneHandoffResult(
            False, False, None, route, False, False, DIRECT_HERMES_COMMAND, "hermes-not-installed"
        )

    profile_home = find_standalone_profile(runner=runner)
    created = False
    if not profile_home:
        try:
            completed = _run(
                [
                    "hermes", "profile", "create", STANDALONE_HERMES_PROFILE,
                    "--description",
                    "Standalone Agnes + Hermes advanced profile prepared by FirstWindow. "
                    "Text/vision plus Agnes image/video generation; no fallback providers.",
                ],
                runner=runner,
                timeout=120,
            )
        except (OSError, subprocess.SubprocessError):
            completed = None
        if completed is None or int(getattr(completed, "returncode", 1)) != 0:
            route = read_hermes_agnes_route(None, which=which, runner=runner)
            return StandaloneHandoffResult(
                False, False, None, route, False, False, DIRECT_HERMES_COMMAND, "profile-create-failed"
            )
        created = True
        profile_home = find_standalone_profile(runner=runner)

    if not profile_home:
        route = read_hermes_agnes_route(None, which=which, runner=runner)
        return StandaloneHandoffResult(
            False, created, None, route, False, False, DIRECT_HERMES_COMMAND, "profile-path-unavailable"
        )

    if api_key is not None:
        save_agnes_api_key(profile_home, api_key)

    install_agnes_media_plugins(profile_home)
    env = scoped_env(profile_home)

    current_enabled = _json_value("plugins.enabled", env=env, runner=runner)
    enabled = [str(item) for item in current_enabled] if isinstance(current_enabled, list) else []
    for key in (IMAGE_PLUGIN_KEY, VIDEO_PLUGIN_KEY):
        if key not in enabled:
            enabled.append(key)

    settings = (
        ("model.default", AGNES_MODEL),
        ("model.provider", AGNES_PROVIDER),
        ("model.base_url", AGNES_CHAT_BASE_URL),
        ("providers.agnes.api", AGNES_CHAT_BASE_URL),
        ("providers.agnes.key_env", AGNES_KEY_ENV),
        ("providers.agnes.transport", "chat_completions"),
        ("providers.agnes.default_model", AGNES_MODEL),
        ("fallback_providers", "[]"),
        ("plugins.enabled", json.dumps(enabled, separators=(",", ":"))),
        ("image_gen.provider", "agnes"),
        ("image_gen.model", AGNES_IMAGE_MODEL),
        ("video_gen.provider", "agnes"),
        ("video_gen.model", AGNES_VIDEO_MODEL),
        ("toolsets", '["hermes-cli","video_gen"]'),
    )
    for key, value in settings:
        if not _set_config(key, value, env=env, runner=runner):
            route = read_hermes_agnes_route(profile_home, which=which, runner=runner)
            image_ready, video_ready = _plugin_config_ready(profile_home, runner=runner)
            return StandaloneHandoffResult(
                False, created, profile_home, route, image_ready, video_ready,
                DIRECT_HERMES_COMMAND, f"config-set-failed:{key}",
            )

    route = read_hermes_agnes_route(profile_home, which=which, runner=runner)
    image_ready, video_ready = _plugin_config_ready(profile_home, runner=runner)
    credential_ready = agnes_api_key_present(profile_home)
    ready = bool(route.ready and credential_ready and image_ready and video_ready)
    if ready:
        reason = "standalone-agnes-hermes-ready"
    elif not credential_ready:
        reason = "agnes-key-missing"
    elif not route.ready:
        reason = route.reason
    elif not image_ready:
        reason = "image-plugin-not-ready"
    else:
        reason = "video-plugin-not-ready"
    return StandaloneHandoffResult(
        ready, created, profile_home, route, image_ready, video_ready, DIRECT_HERMES_COMMAND, reason
    )


_IMAGE_PLUGIN_MANIFEST = """\
name: agnes
version: 1.0.0
description: Agnes image generation backend prepared by FirstWindow
author: FirstWindow
kind: backend
requires_env:
  - AGNES_API_KEY
"""


_IMAGE_PLUGIN_SOURCE = r'''\
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from agent.image_gen_provider import (
    DEFAULT_ASPECT_RATIO,
    ImageGenProvider,
    error_response,
    normalize_reference_images,
    resolve_aspect_ratio,
    save_b64_image,
    success_response,
)

_PROVIDER = "agnes"
_DEFAULT_MODEL = "agnes-image-2.1-flash"
_DEFAULT_ROOT = "https://apihub.agnes-ai.com"
_SIZE_BY_RATIO = {"landscape": "1024x768", "square": "1024x1024", "portrait": "768x1024"}


def _key() -> str:
    return os.environ.get("AGNES_API_KEY", "").strip()


def _root() -> str:
    return os.environ.get("AGNES_API_ROOT", _DEFAULT_ROOT).strip().rstrip("/")


def _post(path: str, payload: Dict[str, Any], timeout: float = 180.0) -> Dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    req = Request(
        _root() + path,
        data=body,
        headers={"Authorization": "Bearer " + _key(), "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:1000]
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(str(exc.reason)) from exc


class AgnesImageGenProvider(ImageGenProvider):
    @property
    def name(self) -> str:
        return _PROVIDER

    @property
    def display_name(self) -> str:
        return "Agnes Image"

    def is_available(self) -> bool:
        return bool(_key())

    def list_models(self) -> List[Dict[str, Any]]:
        return [{"id": _DEFAULT_MODEL, "display": "Agnes Image 2.1 Flash", "strengths": "Text-to-image and image editing"}]

    def default_model(self) -> Optional[str]:
        return os.environ.get("AGNES_IMAGE_MODEL", "").strip() or _DEFAULT_MODEL

    def get_setup_schema(self) -> Dict[str, Any]:
        return {
            "name": "Agnes Image",
            "badge": "account-dependent",
            "tag": "Agnes image generation; availability and billing follow your Agnes account",
            "env_vars": [{"key": "AGNES_API_KEY", "prompt": "Agnes API key", "url": "https://agnes-ai.com/"}],
        }

    def capabilities(self) -> Dict[str, Any]:
        return {"modalities": ["text", "image"], "max_reference_images": 4}

    def generate(
        self,
        prompt: str,
        aspect_ratio: str = DEFAULT_ASPECT_RATIO,
        *,
        image_url: Optional[str] = None,
        reference_image_urls: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        prompt = (prompt or "").strip()
        ratio = resolve_aspect_ratio(aspect_ratio)
        model = str(kwargs.get("model") or self.default_model() or _DEFAULT_MODEL)
        if not prompt:
            return error_response(error="Prompt is required", error_type="invalid_input", provider=self.name, model=model, aspect_ratio=ratio)
        if not _key():
            return error_response(error="AGNES_API_KEY is not set", error_type="missing_credentials", provider=self.name, model=model, prompt=prompt, aspect_ratio=ratio)

        sources: List[str] = []
        if image_url:
            sources.append(image_url)
        sources.extend(normalize_reference_images(reference_image_urls) or [])
        payload: Dict[str, Any] = {"model": model, "prompt": prompt, "size": _SIZE_BY_RATIO[ratio]}
        if sources:
            payload["extra_body"] = {"image": sources[:4], "response_format": "url"}

        try:
            data = _post("/v1/images/generations", payload)
            rows = data.get("data") if isinstance(data, dict) else None
            first = rows[0] if isinstance(rows, list) and rows else {}
            if not isinstance(first, dict):
                first = {}
            image = str(first.get("url") or "").strip()
            if not image:
                b64_value = str(first.get("b64_json") or "").strip()
                if b64_value:
                    image = str(save_b64_image(b64_value, prefix="agnes"))
            if not image:
                raise RuntimeError("Agnes image response did not contain a URL or base64 image")
            return success_response(
                image=image,
                model=model,
                prompt=prompt,
                aspect_ratio=ratio,
                provider=self.name,
                modality="image" if sources else "text",
            )
        except Exception as exc:
            return error_response(
                error=str(exc), error_type=type(exc).__name__, provider=self.name,
                model=model, prompt=prompt, aspect_ratio=ratio,
            )


def register(ctx) -> None:
    ctx.register_image_gen_provider(AgnesImageGenProvider())
'''


_VIDEO_PLUGIN_MANIFEST = """\
name: agnes
version: 1.0.0
description: Agnes video generation backend prepared by FirstWindow
author: FirstWindow
kind: backend
requires_env:
  - AGNES_API_KEY
"""


_VIDEO_PLUGIN_SOURCE = r'''\
from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from agent.video_gen_provider import VideoGenProvider, error_response, success_response

_PROVIDER = "agnes"
_DEFAULT_MODEL = "agnes-video-v2.0"
_DEFAULT_ROOT = "https://apihub.agnes-ai.com"
_DIMENSIONS = {
    "16:9": (1152, 648), "9:16": (648, 1152), "1:1": (768, 768),
    "4:3": (1024, 768), "3:4": (768, 1024), "3:2": (1152, 768), "2:3": (768, 1152),
}


def _key() -> str:
    return os.environ.get("AGNES_API_KEY", "").strip()


def _root() -> str:
    return os.environ.get("AGNES_API_ROOT", _DEFAULT_ROOT).strip().rstrip("/")


def _request(method: str, path: str, payload: Optional[Dict[str, Any]] = None, timeout: float = 180.0) -> Dict[str, Any]:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    req = Request(
        _root() + path,
        data=body,
        headers={"Authorization": "Bearer " + _key(), "Content-Type": "application/json"},
        method=method,
    )
    try:
        with urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:1000]
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(str(exc.reason)) from exc


def _frames(duration: Optional[int]) -> Tuple[int, int]:
    seconds = max(3, min(18, int(duration or 5)))
    fps = 24
    n = max(1, min(55, round((seconds * fps - 1) / 8)))
    return 8 * n + 1, fps


def _video_url(data: Dict[str, Any]) -> str:
    for key in ("url", "video_url", "remixed_from_video_id"):
        value = data.get(key)
        if isinstance(value, str) and value.startswith(("http://", "https://")):
            return value
    metadata = data.get("metadata")
    if isinstance(metadata, dict):
        value = metadata.get("url")
        if isinstance(value, str) and value.startswith(("http://", "https://")):
            return value
    return ""


class AgnesVideoGenProvider(VideoGenProvider):
    @property
    def name(self) -> str:
        return _PROVIDER

    @property
    def display_name(self) -> str:
        return "Agnes Video"

    def is_available(self) -> bool:
        return bool(_key())

    def list_models(self) -> List[Dict[str, Any]]:
        return [{"id": _DEFAULT_MODEL, "display": "Agnes Video v2.0", "strengths": "Text-to-video and image-to-video", "modalities": ["text", "image"]}]

    def default_model(self) -> Optional[str]:
        return os.environ.get("AGNES_VIDEO_MODEL", "").strip() or _DEFAULT_MODEL

    def get_setup_schema(self) -> Dict[str, Any]:
        return {
            "name": "Agnes Video",
            "badge": "account-dependent",
            "tag": "Agnes async video generation; availability and billing follow your Agnes account",
            "env_vars": [{"key": "AGNES_API_KEY", "prompt": "Agnes API key", "url": "https://agnes-ai.com/"}],
        }

    def capabilities(self) -> Dict[str, Any]:
        return {
            "modalities": ["text", "image"],
            "aspect_ratios": list(_DIMENSIONS),
            "resolutions": ["720p", "1080p"],
            "min_duration": 3,
            "max_duration": 18,
            "supports_audio": False,
            "supports_negative_prompt": True,
            "supports_seed": True,
            "supports_upscale": False,
            "max_reference_images": 4,
        }

    def generate(
        self,
        prompt: str,
        *,
        model: Optional[str] = None,
        image_url: Optional[str] = None,
        reference_image_urls: Optional[List[str]] = None,
        duration: Optional[int] = None,
        aspect_ratio: str = "16:9",
        resolution: str = "720p",
        negative_prompt: Optional[str] = None,
        audio: Optional[bool] = None,
        seed: Optional[int] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        del audio, kwargs
        prompt = (prompt or "").strip()
        model_id = model or self.default_model() or _DEFAULT_MODEL
        ratio = aspect_ratio if aspect_ratio in _DIMENSIONS else "16:9"
        if not prompt:
            return error_response(error="Prompt is required", error_type="invalid_input", provider=self.name, model=model_id, aspect_ratio=ratio)
        if not _key():
            return error_response(error="AGNES_API_KEY is not set", error_type="missing_credentials", provider=self.name, model=model_id, prompt=prompt, aspect_ratio=ratio)

        width, height = _DIMENSIONS[ratio]
        if str(resolution).lower() == "1080p":
            scale = 1080 / min(width, height)
            width, height = int(width * scale), int(height * scale)
        frames, fps = _frames(duration)
        payload: Dict[str, Any] = {
            "model": model_id,
            "prompt": prompt,
            "width": width,
            "height": height,
            "num_frames": frames,
            "frame_rate": fps,
        }
        if image_url:
            payload["image"] = image_url
        refs = [str(x).strip() for x in (reference_image_urls or []) if str(x).strip()]
        if refs:
            payload["extra_body"] = {"image": refs[:4]}
        if negative_prompt:
            payload["negative_prompt"] = negative_prompt
        if seed is not None:
            payload["seed"] = int(seed)

        try:
            created = _request("POST", "/v1/videos", payload)
            video_id = str(created.get("video_id") or "").strip()
            task_id = str(created.get("task_id") or created.get("id") or "").strip()
            if not video_id and not task_id:
                raise RuntimeError("Agnes video response did not contain video_id or task_id")

            deadline = time.monotonic() + 900.0
            current = created
            while True:
                status = str(current.get("status") or "").strip().lower()
                if status == "completed":
                    url = _video_url(current)
                    if not url:
                        raise RuntimeError("Agnes video job completed without a video URL")
                    return success_response(
                        video=url, model=model_id, prompt=prompt,
                        modality="image" if image_url else "text", aspect_ratio=ratio,
                        duration=int(duration or 5), provider=self.name,
                    )
                if status in {"failed", "error", "cancelled", "canceled"}:
                    raise RuntimeError(str(current.get("error") or f"video job ended with status={status}"))
                if time.monotonic() >= deadline:
                    raise TimeoutError("Agnes video job did not complete within 900 seconds")
                time.sleep(10)
                if video_id:
                    current = _request("GET", "/agnesapi?" + urlencode({"video_id": video_id}), timeout=60.0)
                else:
                    current = _request("GET", "/v1/videos/" + task_id, timeout=60.0)
        except Exception as exc:
            return error_response(
                error=str(exc), error_type=type(exc).__name__, provider=self.name,
                model=model_id, prompt=prompt, aspect_ratio=ratio,
            )


def register(ctx) -> None:
    ctx.register_video_gen_provider(AgnesVideoGenProvider())
'''
