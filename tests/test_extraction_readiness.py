from __future__ import annotations

from copy import deepcopy
from importlib import metadata
from pathlib import Path
from types import SimpleNamespace
import tomllib
import unittest

from skill_runtime.devtools import require_clean_skill_source, validate_skill_factory
from gamerhq_skill_xp_progression.progression import (
    CONFIG_KEY, MEMBER_KEY_PREFIX, PROGRESSION_CAPABILITIES,
    PROGRESSION_MANAGEMENT_APIS, RUNTIME_API_VERSION, SKILL_ID,
    SKILL_VERSION, DEFAULT_CONFIG, create_skill,
)

ROOT = Path(__file__).resolve().parents[1]

class FakeStorage:
    def __init__(self, values=None):
        self.data = deepcopy(values or {})
        self.writes = 0
        self.deletes = 0
    async def get(self, key):
        return deepcopy(self.data.get(key))
    async def set(self, key, value):
        self.writes += 1
        self.data[key] = deepcopy(value)
    async def delete(self, key):
        self.deletes += 1
        self.data.pop(key, None)

class StandaloneReadinessTests(unittest.IsolatedAsyncioTestCase):
    def test_source_passes_sdk_source_audit(self):
        report = require_clean_skill_source([ROOT / "gamerhq_skill_xp_progression" / "progression.py"])
        self.assertEqual(report.findings, ())

    def test_factory_and_lifecycle_conform(self):
        report = validate_skill_factory(create_skill, expected_skill_id=SKILL_ID)
        self.assertEqual(report.skill_id, "progression")
        self.assertEqual(report.version, SKILL_VERSION)
        self.assertEqual(report.runtime_api_version, RUNTIME_API_VERSION)

    def test_identity_management_and_storage_are_frozen(self):
        skill = create_skill()
        self.assertEqual(skill.manifest.id, "progression")
        self.assertEqual(skill.manifest.version, "0.1.0")
        self.assertEqual(skill.manifest.runtime_api_version, "1")
        self.assertEqual(PROGRESSION_MANAGEMENT_APIS, (
            "progression.status.v1", "progression.get-config.v1",
            "progression.update-config.v1", "progression.preview-level.v1",
            "progression.record-activity.v1", "progression.member-status.v1",
        ))
        self.assertEqual(tuple(c.id for c in skill.manifest.management_apis.exposes), PROGRESSION_MANAGEMENT_APIS)
        self.assertEqual(CONFIG_KEY, "config.v1")
        self.assertEqual(MEMBER_KEY_PREFIX, "member.v1:")

    def test_static_metadata_matches_manifest(self):
        static = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        gamerhq = static["tool"]["gamerhq"]
        skill = create_skill()
        self.assertEqual(gamerhq["skill-id"], skill.manifest.id)
        self.assertEqual(gamerhq["runtime-api"], skill.manifest.runtime_api_version)
        self.assertEqual(tuple(gamerhq["capabilities"]), tuple(skill.manifest.permissions))
        self.assertEqual(tuple(skill.manifest.permissions), PROGRESSION_CAPABILITIES)

    def test_entry_point_matches_manifest(self):
        eps = [ep for ep in metadata.entry_points(group="gamerhq.skills") if ep.name == "progression"]
        self.assertEqual(len(eps), 1)
        factory = eps[0].load()
        self.assertEqual(factory().manifest.id, "progression")

    async def test_partial_member_reads_without_rewrite(self):
        storage = FakeStorage({CONFIG_KEY: DEFAULT_CONFIG, MEMBER_KEY_PREFIX + "7": {"totalXp": 25}})
        status = await create_skill().member_status(SimpleNamespace(storage=storage), {"memberId": 7})
        self.assertEqual(status["totalXp"], 25)
        self.assertEqual(status["sourceXp"], {})
        self.assertEqual(status["dailyXp"], {})
        self.assertEqual(status["metrics"], {})
        self.assertEqual(status["achievements"], ())
        self.assertEqual(status["badges"], ())
        self.assertEqual(status["titles"], ())
        self.assertEqual(status["claimedRewards"], ())
        self.assertEqual(status["ownedRoleGrants"], ())
        self.assertEqual(storage.writes, 0)
        self.assertEqual(storage.deletes, 0)

    async def test_disable_and_health_are_non_destructive(self):
        storage = FakeStorage({CONFIG_KEY: DEFAULT_CONFIG, MEMBER_KEY_PREFIX + "7": {"totalXp": 25}})
        before = deepcopy(storage.data)
        skill = create_skill()
        ctx = SimpleNamespace(storage=storage)
        health = await skill.health_check(ctx)
        await skill.disable(ctx)
        self.assertEqual(health.state, "PASS")
        self.assertEqual(storage.data, before)
        self.assertEqual(storage.writes, 0)
        self.assertEqual(storage.deletes, 0)

if __name__ == "__main__":
    unittest.main()
