from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from firstwindow.advanced_handoff import (
    AGNES_IMAGE_MODEL,
    AGNES_VIDEO_MODEL,
    DIRECT_HERMES_COMMAND,
    HANDOFF_MARKER_FILENAME,
    IMAGE_PLUGIN_KEY,
    STANDALONE_HERMES_PROFILE,
    VIDEO_PLUGIN_KEY,
    ensure_standalone_agnes_hermes,
    install_agnes_media_plugins,
)
from firstwindow.hermes_agnes import AGNES_MODEL


class _Completed:
    def __init__(self, returncode: int = 0, stdout: str = "", stderr: str = ""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class FakeHermes:
    def __init__(self, profile: Path, *, fail_key: str | None = None):
        self.profile = profile
        self.exists = False
        self.fail_key = fail_key
        self.commands: list[list[str]] = []
        self.values: dict[str, object] = {
            "plugins.enabled": ["existing/plugin"],
        }

    def _get(self, key: str):
        if key == "model":
            return {
                "default": self.values.get("model.default"),
                "provider": self.values.get("model.provider"),
                "base_url": self.values.get("model.base_url"),
            }
        if key == "providers.agnes":
            return {
                "api": self.values.get("providers.agnes.api"),
                "key_env": self.values.get("providers.agnes.key_env"),
                "transport": self.values.get("providers.agnes.transport"),
                "default_model": self.values.get("providers.agnes.default_model"),
            }
        return self.values.get(key)

    def __call__(self, command, **kwargs):
        del kwargs
        cmd = list(command)
        self.commands.append(cmd)
        if cmd[:4] == ["hermes", "profile", "show", STANDALONE_HERMES_PROFILE]:
            if not self.exists:
                return _Completed(1, "", "missing")
            return _Completed(0, f"Profile: {STANDALONE_HERMES_PROFILE}\nPath: {self.profile}\n")
        if cmd[:4] == ["hermes", "profile", "create", STANDALONE_HERMES_PROFILE]:
            self.exists = True
            self.profile.mkdir(parents=True, exist_ok=True)
            return _Completed()
        if cmd[:3] == ["hermes", "config", "get"] and "--json" in cmd:
            value = self._get(cmd[3])
            return _Completed(0, json.dumps(value))
        if cmd[:3] == ["hermes", "config", "set"]:
            key, raw = cmd[3], cmd[4]
            if key == self.fail_key:
                return _Completed(1, "", "forced failure")
            if raw.startswith("[") or raw.startswith("{"):
                try:
                    value = json.loads(raw)
                except json.JSONDecodeError:
                    value = raw
            else:
                value = raw
            self.values[key] = value
            return _Completed()
        return _Completed(1, "", "unexpected command")


class AdvancedHandoffTests(unittest.TestCase):
    def test_creates_independent_ready_profile_without_putting_secret_in_commands(self):
        with tempfile.TemporaryDirectory() as tmp:
            profile = Path(tmp) / "agneshermes"
            fake = FakeHermes(profile)
            secret = "agnes-test-secret-123"

            result = ensure_standalone_agnes_hermes(
                secret,
                which=lambda _name: "hermes",
                runner=fake,
            )

            self.assertTrue(result.ready, result.reason)
            self.assertTrue(result.created)
            self.assertEqual(result.direct_command, DIRECT_HERMES_COMMAND)
            self.assertEqual(result.route.model, AGNES_MODEL)
            self.assertTrue(result.route.no_fallbacks)
            self.assertTrue(result.image_plugin_ready)
            self.assertTrue(result.video_plugin_ready)
            self.assertEqual(fake.values["image_gen.model"], AGNES_IMAGE_MODEL)
            self.assertEqual(fake.values["video_gen.model"], AGNES_VIDEO_MODEL)
            self.assertEqual(fake.values["toolsets"], ["hermes-cli", "video_gen"])
            self.assertTrue((profile / HANDOFF_MARKER_FILENAME).is_file())
            self.assertIn("existing/plugin", fake.values["plugins.enabled"])
            self.assertIn(IMAGE_PLUGIN_KEY, fake.values["plugins.enabled"])
            self.assertIn(VIDEO_PLUGIN_KEY, fake.values["plugins.enabled"])

            env_text = (profile / ".env").read_text(encoding="utf-8")
            self.assertIn("AGNES_API_KEY=", env_text)
            self.assertIn(secret, env_text)
            for command in fake.commands:
                self.assertNotIn(secret, " ".join(command))

            self.assertTrue((profile / "plugins" / "image_gen" / "agnes" / "__init__.py").is_file())
            self.assertTrue((profile / "plugins" / "video_gen" / "agnes" / "__init__.py").is_file())

    def test_missing_key_configures_profile_but_does_not_claim_ready(self):
        with tempfile.TemporaryDirectory() as tmp:
            fake = FakeHermes(Path(tmp) / "agneshermes")
            result = ensure_standalone_agnes_hermes(
                None,
                which=lambda _name: "hermes",
                runner=fake,
            )
            self.assertFalse(result.ready)
            self.assertEqual(result.reason, "agnes-key-missing")
            self.assertTrue(result.route.ready)
            self.assertTrue(result.image_plugin_ready)
            self.assertTrue(result.video_plugin_ready)

    def test_existing_unmanaged_profile_is_not_mutated(self):
        with tempfile.TemporaryDirectory() as tmp:
            profile = Path(tmp) / "agneshermes"
            profile.mkdir(parents=True)
            fake = FakeHermes(profile)
            fake.exists = True
            result = ensure_standalone_agnes_hermes(
                "must-not-be-written",
                which=lambda _name: "hermes",
                runner=fake,
            )
            self.assertFalse(result.ready)
            self.assertEqual(result.reason, "profile-name-conflict-unmanaged")
            self.assertFalse((profile / ".env").exists())
            self.assertFalse(any(cmd[:3] == ["hermes", "config", "set"] for cmd in fake.commands))

    def test_repair_preserves_user_added_toolsets(self):
        with tempfile.TemporaryDirectory() as tmp:
            profile = Path(tmp) / "agneshermes"
            fake = FakeHermes(profile)
            first = ensure_standalone_agnes_hermes(
                "valid-secret",
                which=lambda _name: "hermes",
                runner=fake,
            )
            self.assertTrue(first.ready, first.reason)
            fake.values["toolsets"] = ["web", "hermes-cli", "video_gen"]
            repaired = ensure_standalone_agnes_hermes(
                None,
                which=lambda _name: "hermes",
                runner=fake,
            )
            self.assertTrue(repaired.ready, repaired.reason)
            self.assertEqual(fake.values["toolsets"], ["web", "hermes-cli", "video_gen"])

    def test_config_failure_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            fake = FakeHermes(Path(tmp) / "agneshermes", fail_key="video_gen.model")
            result = ensure_standalone_agnes_hermes(
                "valid-secret",
                which=lambda _name: "hermes",
                runner=fake,
            )
            self.assertFalse(result.ready)
            self.assertEqual(result.reason, "config-set-failed:video_gen.model")

    def test_generated_plugins_are_dependency_free_python_and_use_scoped_agnes_env(self):
        with tempfile.TemporaryDirectory() as tmp:
            profile = Path(tmp)
            image_root, video_root = install_agnes_media_plugins(profile)
            for path in (image_root / "__init__.py", video_root / "__init__.py"):
                source = path.read_text(encoding="utf-8")
                compile(source, str(path), "exec")
                self.assertIn("AGNES_API_KEY", source)
                self.assertNotIn("npm", source.lower())
                self.assertNotIn("agnes-ai-cli", source.lower())

            self.assertIn("/v1/images/generations", (image_root / "__init__.py").read_text(encoding="utf-8"))
            video_source = (video_root / "__init__.py").read_text(encoding="utf-8")
            self.assertIn("/v1/videos", video_source)
            self.assertIn("video_id", video_source)
            self.assertIn("remixed_from_video_id", video_source)


if __name__ == "__main__":
    unittest.main()
