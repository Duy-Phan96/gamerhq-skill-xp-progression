"""Portable Progression & Achievements Skill.

V1 owns progression configuration, deterministic level math, activity awards,
achievement unlocks, reward execution and milestone announcements. Host-specific
Discord observation remains outside this package; the Skill uses only public
Runtime/SDK contracts and host-neutral adapters.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Mapping
from datetime import datetime, timezone

from skill_runtime.contracts.capabilities import SkillCapability
from skill_runtime.contracts.lifecycle import SkillHealth
from skill_runtime.contracts.management import ManagementApiContract, ManagementConflictError
from skill_runtime.contracts.management_ui import ManagementDocumentBinding, ManagementField, ManagementSection, ManagementUiSchema
from skill_runtime.contracts.manifest import SkillManagementApis, SkillManifest


SKILL_ID = "progression"
SKILL_VERSION = "0.2.0"
RUNTIME_API_VERSION = "1"
MAX_REPEAT_AWARDS_PER_CALL = 100

CONFIG_KEY = "config.v1"
MEMBER_KEY_PREFIX = "member.v1:"

STATUS_API = "progression.status.v1"
GET_CONFIG_API = "progression.get-config.v1"
UPDATE_CONFIG_API = "progression.update-config.v1"
PREVIEW_LEVEL_API = "progression.preview-level.v1"
RECORD_ACTIVITY_API = "progression.record-activity.v1"
RECORD_SIGNAL_API = "progression.record-signal.v1"
MEMBER_STATUS_API = "progression.member-status.v1"

PROGRESSION_MANAGEMENT_APIS = (
    STATUS_API,
    GET_CONFIG_API,
    UPDATE_CONFIG_API,
    PREVIEW_LEVEL_API,
    RECORD_ACTIVITY_API,
    RECORD_SIGNAL_API,
    MEMBER_STATUS_API,
)

PROGRESSION_CAPABILITIES = (
    SkillCapability.STORAGE_SKILL.value,
    SkillCapability.AUDIT_WRITE.value,
    SkillCapability.DISCORD_MESSAGES_SEND.value,
    SkillCapability.DISCORD_CHANNELS_READ.value,
    SkillCapability.DISCORD_MEMBERS_READ.value,
    SkillCapability.DISCORD_ROLES_MANAGE.value,
)

PROGRESSION_MANAGEMENT_UI = ManagementUiSchema(
    version="1",
    read_contract=GET_CONFIG_API,
    write_contract=UPDATE_CONFIG_API,
    document=ManagementDocumentBinding(
        read_path="config",
        write_path="config",
        revision_path="revision",
        expected_revision_key="expectedRevision",
    ),
    sections=(
        ManagementSection(
            id="xp-sources",
            title="XP Sources",
            description="Enable activity sources and tune their XP values.",
            fields=(
                ManagementField("voiceEnabled", "Voice XP", "boolean", "xpSources.voice.enabled"),
                ManagementField("voiceXp", "Voice XP per window", "integer", "xpSources.voice.xp", minimum=1),
                ManagementField("voiceWindowMinutes", "Voice window minutes", "integer", "xpSources.voice.windowMinutes", minimum=1),
                ManagementField("voiceDailyCap", "Voice daily XP cap", "integer", "xpSources.voice.dailyCap", minimum=1),
                ManagementField("chatEnabled", "Chat XP", "boolean", "xpSources.chat.enabled"),
                ManagementField("chatXp", "Chat XP per activity window", "integer", "xpSources.chat.xp", minimum=1),
                ManagementField("chatCooldownMinutes", "Chat cooldown minutes", "integer", "xpSources.chat.cooldownMinutes", minimum=1),
                ManagementField("chatDailyCap", "Chat daily XP cap", "integer", "xpSources.chat.dailyCap", minimum=1),
                ManagementField("lfgEnabled", "LFG participation XP", "boolean", "xpSources.lfgParticipation.enabled"),
                ManagementField("lfgXp", "LFG participation XP", "integer", "xpSources.lfgParticipation.xp", minimum=1),
                ManagementField("eventHostEnabled", "Event host XP", "boolean", "xpSources.eventHost.enabled"),
                ManagementField("eventHostXp", "Event host XP", "integer", "xpSources.eventHost.xp", minimum=1),
            ),
        ),
        ManagementSection(
            id="level-curve",
            title="Level Curve",
            description="Control how XP requirements grow over time.",
            fields=(
                ManagementField("baseXp", "Base XP", "integer", "levelCurve.base", minimum=1),
                ManagementField("linearGrowth", "Linear growth", "integer", "levelCurve.linear", minimum=0),
                ManagementField("quadraticGrowth", "Quadratic growth", "integer", "levelCurve.quadratic", minimum=0),
                ManagementField("maxLevel", "Maximum level", "integer", "levelCurve.maxLevel", minimum=1, maximum=1000),
            ),
        ),
        ManagementSection(
            id="achievements",
            title="Achievements",
            description="Achievement definitions and milestone rewards.",
            fields=(
                ManagementField("achievements", "Achievements", "collection", "achievements"),
            ),
        ),
        ManagementSection(
            id="rewards",
            title="Rewards",
            description="Level, XP and achievement-triggered reward bundles.",
            fields=(
                ManagementField("rewards", "Rewards", "collection", "rewards"),
            ),
        ),
        ManagementSection(
            id="announcements",
            title="Announcements",
            description="Choose when and where Progression posts member milestones.",
            fields=(
                ManagementField("announcementsEnabled", "Enable announcements", "boolean", "announcements.enabled"),
                ManagementField("announcementChannel", "Announcement channel", "discord_channel", "announcements.channelId"),
                ManagementField("announceLevelUps", "Post level ups", "boolean", "announcements.levelUp"),
                ManagementField("announceAchievements", "Post achievements", "boolean", "announcements.achievement"),
                ManagementField("announceRewards", "Post rewards", "boolean", "announcements.reward"),
                ManagementField("announcementTemplate", "Message template", "long_text", "announcements.template"),
            ),
        ),
    ),
)


DEFAULT_CONFIG = {
    "revision": 1,
    "levelCurve": {
        "base": 100,
        "linear": 20,
        "quadratic": 2,
        "maxLevel": 100,
    },
    "xpSources": {
        "voice": {
            "enabled": True,
            "xp": 5,
            "windowMinutes": 10,
            "dailyCap": 180,
            "requiresOtherHuman": True,
            "excludeAfk": True,
        },
        "chat": {
            "enabled": True,
            "xp": 3,
            "cooldownMinutes": 5,
            "dailyCap": 120,
        },
        "lfgParticipation": {"enabled": True, "xp": 25},
        "eventHost": {"enabled": True, "xp": 40},
        "communityEvent": {"enabled": True, "xp": 50},
        "tournamentParticipation": {"enabled": True, "xp": 75},
        "tournamentWin": {"enabled": True, "xp": 100},
    },
    "achievements": [
        {
            "id": "server-booster",
            "name": "Server Booster",
            "emoji": "💎",
            "description": "Boost the Discord server.",
            "xp": 250,
            "enabled": True,
            "repeatable": False,
            "condition": {
                "type": "external_signal",
                "provider": "discord",
                "signal": "server_boosted",
            },
        },
        {
            "id": "first-game",
            "name": "First Game",
            "emoji": "🎮",
            "description": "Add your first game to your GamerHQ profile.",
            "xp": 25,
            "enabled": True,
            "repeatable": False,
            "condition": {
                "type": "external_signal",
                "provider": "profile",
                "signal": "first_game_added",
            },
        },
        {
            "id": "first-mate",
            "name": "First Mate",
            "emoji": "🤝",
            "description": "Take part in your first completed LFG event.",
            "xp": 50,
            "enabled": True,
            "repeatable": False,
            "condition": {"type": "metric_at_least", "metric": "lfgParticipations", "threshold": 1},
        },
        {
            "id": "event-regular",
            "name": "Event Regular",
            "emoji": "📅",
            "description": "Attend 10 completed events.",
            "xp": 150,
            "enabled": True,
            "repeatable": False,
            "condition": {"type": "metric_at_least", "metric": "lfgParticipations", "threshold": 10},
        },
        {
            "id": "community-host",
            "name": "Community Host",
            "emoji": "🎤",
            "description": "Host 10 completed events.",
            "xp": 300,
            "enabled": True,
            "repeatable": False,
            "condition": {"type": "metric_at_least", "metric": "eventsHosted", "threshold": 10},
        },
        {
            "id": "voice-rookie",
            "name": "Voice Rookie",
            "emoji": "🎙️",
            "description": "Spend 5 active hours in voice with other members.",
            "xp": 100,
            "enabled": True,
            "repeatable": False,
            "condition": {"type": "metric_at_least", "metric": "voiceMinutes", "threshold": 300},
        },
        {
            "id": "voice-regular",
            "name": "Voice Regular",
            "emoji": "🎙️",
            "description": "Spend 25 active hours in voice with other members.",
            "xp": 250,
            "enabled": True,
            "repeatable": False,
            "condition": {"type": "metric_at_least", "metric": "voiceMinutes", "threshold": 1500},
        },
        {
            "id": "voice-veteran",
            "name": "Voice Veteran",
            "emoji": "🎙️",
            "description": "Spend 100 active hours in voice with other members.",
            "xp": 750,
            "enabled": True,
            "repeatable": False,
            "condition": {"type": "metric_at_least", "metric": "voiceMinutes", "threshold": 6000},
        },
    ],
    "rewards": [],
    "announcements": {
        "enabled": False,
        "channelId": None,
        "levelUp": True,
        "achievement": True,
        "reward": True,
        "template": "🏆 {member} unlocked **{achievement_name}**!\n{achievement_emoji} +{xp} XP · Level {level}",
    },
}


def xp_to_next(level: int, curve: Mapping[str, Any] | None = None) -> int:
    curve = curve or DEFAULT_CONFIG["levelCurve"]
    if level < 1:
        raise ValueError("level must be at least 1")
    base = int(curve["base"])
    linear = int(curve["linear"])
    quadratic = int(curve["quadratic"])
    value = base + linear * level + quadratic * level * level
    return max(1, value)


def cumulative_xp_for_level(level: int, curve: Mapping[str, Any] | None = None) -> int:
    if level < 1:
        raise ValueError("level must be at least 1")
    return sum(xp_to_next(current, curve) for current in range(1, level))


def level_for_xp(total_xp: int, curve: Mapping[str, Any] | None = None) -> tuple[int, int, int]:
    if total_xp < 0:
        raise ValueError("total_xp must be non-negative")
    curve = curve or DEFAULT_CONFIG["levelCurve"]
    max_level = int(curve.get("maxLevel", 100))
    level = 1
    remaining = int(total_xp)
    while level < max_level:
        needed = xp_to_next(level, curve)
        if remaining < needed:
            return level, remaining, needed
        remaining -= needed
        level += 1
    return max_level, remaining, 0


def _positive_int(value: Any, name: str, *, minimum: int = 1, maximum: int = 1_000_000) -> int:
    try:
        value = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if not minimum <= value <= maximum:
        raise ValueError(f"{name} is outside the supported range")
    return value


def _bounded_identifier(value: Any, name: str, *, maximum: int = 80) -> str:
    value = str(value or "").strip().lower()
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789._-")
    if not value or len(value) > maximum or any(char not in allowed for char in value):
        raise ValueError(f"{name} must use 1-{maximum} lowercase identifier characters")
    return value


def validate_config(value: Mapping[str, Any]) -> dict[str, Any]:
    config = deepcopy(dict(value))
    config["revision"] = _positive_int(config.get("revision", 1), "revision")
    curve = dict(config.get("levelCurve") or {})
    curve["base"] = _positive_int(curve.get("base", 100), "levelCurve.base")
    curve["linear"] = _positive_int(curve.get("linear", 20), "levelCurve.linear", minimum=0)
    curve["quadratic"] = _positive_int(curve.get("quadratic", 2), "levelCurve.quadratic", minimum=0)
    curve["maxLevel"] = _positive_int(curve.get("maxLevel", 100), "levelCurve.maxLevel", maximum=1000)
    config["levelCurve"] = curve

    sources = dict(config.get("xpSources") or {})
    for key, source in sources.items():
        if not isinstance(source, Mapping):
            raise ValueError(f"xpSources.{key} must be an object")
        item = dict(source)
        item["enabled"] = bool(item.get("enabled", True))
        item["xp"] = _positive_int(item.get("xp", 1), f"xpSources.{key}.xp")
        if "dailyCap" in item:
            item["dailyCap"] = _positive_int(item["dailyCap"], f"xpSources.{key}.dailyCap")
        if key == "chat" and "cooldownMinutes" in item:
            item["cooldownMinutes"] = _positive_int(
                item["cooldownMinutes"],
                "xpSources.chat.cooldownMinutes",
            )
        if key == "voice":
            if "windowMinutes" in item:
                item["windowMinutes"] = _positive_int(
                    item["windowMinutes"],
                    "xpSources.voice.windowMinutes",
                )
            if "requiresOtherHuman" in item:
                item["requiresOtherHuman"] = bool(item["requiresOtherHuman"])
            if "excludeAfk" in item:
                item["excludeAfk"] = bool(item["excludeAfk"])
        sources[key] = item
    config["xpSources"] = sources

    achievements = []
    seen = set()
    for raw in config.get("achievements", ()):
        if not isinstance(raw, Mapping):
            raise ValueError("achievement must be an object")
        item = dict(raw)
        achievement_id = str(item.get("id", "")).strip().lower()
        if not achievement_id or achievement_id in seen:
            raise ValueError("achievement IDs must be unique and non-empty")
        seen.add(achievement_id)
        item["id"] = achievement_id
        item["name"] = str(item.get("name", "")).strip()[:80]
        if not item["name"]:
            raise ValueError("achievement name is required")
        item["emoji"] = str(item.get("emoji", ""))[:16]
        item["description"] = str(item.get("description", "")).strip()[:300]
        item["xp"] = _positive_int(item.get("xp", 1), f"achievement {achievement_id} xp")
        item["enabled"] = bool(item.get("enabled", True))
        item["repeatable"] = bool(item.get("repeatable", False))
        condition = item.get("condition")
        if condition is None:
            item["condition"] = None
        else:
            if not isinstance(condition, Mapping):
                raise ValueError(f"achievement {achievement_id} condition must be an object")
            condition = dict(condition)
            condition_type = str(condition.get("type", "")).strip()
            if condition_type == "metric_at_least":
                metric = str(condition.get("metric", "")).strip()
                allowed_metrics = {"voiceMinutes", "lfgParticipations", "eventsHosted"}
                if metric not in allowed_metrics:
                    raise ValueError(f"achievement {achievement_id} references an unsupported metric")
                condition["type"] = condition_type
                condition["metric"] = metric
                condition["threshold"] = _positive_int(
                    condition.get("threshold"),
                    f"achievement {achievement_id} threshold",
                )
            elif condition_type == "external_signal":
                condition["type"] = condition_type
                condition["provider"] = _bounded_identifier(
                    condition.get("provider"),
                    f"achievement {achievement_id} provider",
                )
                condition["signal"] = _bounded_identifier(
                    condition.get("signal"),
                    f"achievement {achievement_id} signal",
                )
            else:
                raise ValueError(f"achievement {achievement_id} has an unsupported condition")
            if item["repeatable"]:
                if condition_type == "metric_at_least":
                    condition["repeatEvery"] = _positive_int(
                        condition.get("repeatEvery"),
                        f"achievement {achievement_id} repeatEvery",
                    )
            elif "repeatEvery" in condition:
                raise ValueError(
                    f"achievement {achievement_id} repeatEvery requires repeatable=true"
                )
            item["condition"] = condition
        if item["repeatable"] and not item.get("condition"):
            raise ValueError(
                f"achievement {achievement_id} repeatable achievements need a condition"
            )
        achievements.append(item)
    config["achievements"] = achievements

    rewards = []
    reward_ids = set()
    allowed_types = {"role", "badge", "title", "channel_access", "announcement", "xp_bonus"}
    for raw in config.get("rewards", ()):
        if not isinstance(raw, Mapping):
            raise ValueError("reward must be an object")
        item = dict(raw)
        reward_id = str(item.get("id", "")).strip().lower()
        if not reward_id or reward_id in reward_ids:
            raise ValueError("reward IDs must be unique and non-empty")
        reward_ids.add(reward_id)
        trigger = dict(item.get("trigger") or {})
        trigger_type = str(trigger.get("type", ""))
        if trigger_type not in {"level", "achievement", "xp"}:
            raise ValueError(f"reward {reward_id} has an unsupported trigger")
        if trigger_type == "level":
            trigger["level"] = _positive_int(trigger.get("level"), f"reward {reward_id} level", maximum=curve["maxLevel"])
        elif trigger_type == "xp":
            trigger["xp"] = _positive_int(trigger.get("xp"), f"reward {reward_id} xp")
        else:
            achievement_id = str(trigger.get("achievementId", "")).strip().lower()
            if achievement_id not in seen:
                raise ValueError(f"reward {reward_id} references an unknown achievement")
            trigger["achievementId"] = achievement_id
        item["trigger"] = trigger

        grants = []
        for grant in item.get("grants", ()):
            if not isinstance(grant, Mapping):
                raise ValueError(f"reward {reward_id} grant must be an object")
            grant = dict(grant)
            kind = str(grant.get("type", ""))
            if kind not in allowed_types:
                raise ValueError(f"reward {reward_id} has unsupported grant type")
            grant["type"] = kind
            if kind == "badge":
                badge_id = str(grant.get("badgeId", "")).strip()
                if not badge_id or len(badge_id) > 80:
                    raise ValueError(f"reward {reward_id} badgeId must be 1-80 characters")
                grant["badgeId"] = badge_id
            elif kind == "title":
                title = str(grant.get("title", "")).strip()
                if not title or len(title) > 80:
                    raise ValueError(f"reward {reward_id} title must be 1-80 characters")
                grant["title"] = title
            elif kind == "xp_bonus":
                grant["xp"] = _positive_int(
                    grant.get("xp"),
                    f"reward {reward_id} xp bonus",
                )
            elif kind in {"role", "channel_access"}:
                grant["roleId"] = _positive_int(
                    grant.get("roleId"),
                    f"reward {reward_id} roleId",
                )
            grants.append(grant)
        if not grants:
            raise ValueError(f"reward {reward_id} needs at least one grant")
        item["grants"] = grants
        item["enabled"] = bool(item.get("enabled", True))
        item["name"] = str(item.get("name", reward_id)).strip()[:80]
        rewards.append(item)
    config["rewards"] = rewards

    announcements = dict(config.get("announcements") or {})
    announcements["enabled"] = bool(announcements.get("enabled", False))
    channel_id = announcements.get("channelId")
    if channel_id in (None, "", 0):
        announcements["channelId"] = None
    else:
        announcements["channelId"] = _positive_int(channel_id, "announcements.channelId")
    for key in ("levelUp", "achievement", "reward"):
        announcements[key] = bool(announcements.get(key, True))
    template = str(announcements.get("template", "")).strip()
    if len(template) > 1800:
        raise ValueError("announcement template is too long")
    announcements["template"] = template
    config["announcements"] = announcements
    return config


@dataclass(slots=True)
class ProgressionSkill:
    manifest = SkillManifest(
        id=SKILL_ID,
        name="Progression & Achievements",
        version=SKILL_VERSION,
        runtime_api_version=RUNTIME_API_VERSION,
        description="Configurable XP, levels, achievements and rewards for GamerHQ communities.",
        author="GamerHQ",
        permissions=PROGRESSION_CAPABILITIES,
        management_apis=SkillManagementApis(
            exposes=tuple(
                ManagementApiContract(contract_id)
                for contract_id in PROGRESSION_MANAGEMENT_APIS
            )
        ),
        management_ui=PROGRESSION_MANAGEMENT_UI,
    )

    async def register(self, ctx) -> None:
        ctx.management.expose(STATUS_API, self.status)
        ctx.management.expose(GET_CONFIG_API, self.get_config)
        ctx.management.expose(UPDATE_CONFIG_API, self.update_config)
        ctx.management.expose(PREVIEW_LEVEL_API, self.preview_level)
        ctx.management.expose(RECORD_ACTIVITY_API, self.record_activity)
        ctx.management.expose(RECORD_SIGNAL_API, self.record_signal)
        ctx.management.expose(MEMBER_STATUS_API, self.member_status)

    async def enable(self, ctx) -> None:
        if await ctx.storage.get(CONFIG_KEY) is None:
            await ctx.storage.set(CONFIG_KEY, deepcopy(DEFAULT_CONFIG))

    async def disable(self, ctx) -> None:
        return None

    async def start(self, ctx) -> None:
        return None

    async def stop(self, ctx) -> None:
        return None

    async def health_check(self, ctx) -> SkillHealth:
        try:
            config = await self._config(ctx)
            validate_config(config)
        except Exception:
            return SkillHealth("FAIL", "Progression configuration is invalid.")
        return SkillHealth("PASS", "Progression configuration is valid.")

    async def _config(self, ctx) -> dict[str, Any]:
        stored = await ctx.storage.get(CONFIG_KEY)
        return validate_config(stored if stored is not None else DEFAULT_CONFIG)

    async def status(self, ctx, payload) -> Mapping[str, Any]:
        config = await self._config(ctx)
        return {
            "version": self.manifest.version,
            "maxLevel": config["levelCurve"]["maxLevel"],
            "xpSourceCount": sum(1 for source in config["xpSources"].values() if source.get("enabled")),
            "achievementCount": sum(1 for achievement in config["achievements"] if achievement.get("enabled")),
            "rewardCount": sum(1 for reward in config["rewards"] if reward.get("enabled")),
        }

    async def get_config(self, ctx, payload) -> Mapping[str, Any]:
        return {"config": await self._config(ctx)}

    async def update_config(self, ctx, payload) -> Mapping[str, Any]:
        if "config" not in payload:
            raise ValueError("config is required")
        current = await self._config(ctx)
        expected = payload.get("expectedRevision")
        if expected is not None and int(expected) != int(current["revision"]):
            raise ManagementConflictError(
                "Progression configuration changed. Reopen configuration and review again."
            )
        config = validate_config(payload["config"])
        config["revision"] = int(current["revision"]) + 1
        await ctx.storage.set(CONFIG_KEY, config)
        await ctx.audit.write(action="progression.config.updated", target="progression")
        return {"config": config}

    async def _member_state(self, ctx, member_id: int) -> dict[str, Any]:
        key = MEMBER_KEY_PREFIX + str(member_id)
        state = await ctx.storage.get(key)
        if not isinstance(state, Mapping):
            state = {}
        return {
            "totalXp": int(state.get("totalXp", 0)),
            "sourceXp": dict(state.get("sourceXp") or {}),
            "dailyXp": dict(state.get("dailyXp") or {}),
            "metrics": dict(state.get("metrics") or {}),
            "lastActivity": dict(state.get("lastActivity") or {}),
            "achievements": list(state.get("achievements") or []),
            "achievementCounts": dict(state.get("achievementCounts") or {}),
            "seenActivity": list(state.get("seenActivity") or []),
            "seenSignals": list(state.get("seenSignals") or []),
            "badges": list(state.get("badges") or []),
            "titles": list(state.get("titles") or []),
            "claimedRewards": list(state.get("claimedRewards") or []),
            "ownedRoleGrants": list(state.get("ownedRoleGrants") or []),
        }

    async def member_status(self, ctx, payload) -> Mapping[str, Any]:
        member_id = _positive_int(payload.get("memberId"), "memberId")
        state = await self._member_state(ctx, member_id)
        config = await self._config(ctx)
        level, current, needed = level_for_xp(state["totalXp"], config["levelCurve"])
        return {
            "memberId": member_id,
            "totalXp": state["totalXp"],
            "level": level,
            "currentLevelXp": current,
            "xpToNextLevel": needed,
            "sourceXp": state["sourceXp"],
            "metrics": state["metrics"],
            "achievements": tuple(state["achievements"]),
            "achievementCounts": dict(state["achievementCounts"]),
            "badges": tuple(state["badges"]),
            "titles": tuple(state["titles"]),
            "claimedRewards": tuple(state["claimedRewards"]),
            "ownedRoleGrants": tuple(state["ownedRoleGrants"]),
        }

    async def record_activity(self, ctx, payload) -> Mapping[str, Any]:
        member_id = _positive_int(payload.get("memberId"), "memberId")
        source_id = str(payload.get("source", "")).strip()
        dedupe_key = str(payload.get("dedupeKey", "")).strip()[:160]
        units = _positive_int(payload.get("units", 1), "units", maximum=1000)
        occurred_at = _positive_int(payload.get("occurredAt", 0), "occurredAt", minimum=0, maximum=4_102_444_800)
        if occurred_at == 0:
            occurred_at = int(datetime.now(timezone.utc).timestamp())

        config = await self._config(ctx)
        source = config["xpSources"].get(source_id)
        if not source or not source.get("enabled"):
            return {"memberId": member_id, "source": source_id, "awardedXp": 0, "reason": "disabled"}

        state = await self._member_state(ctx, member_id)
        previous_level = level_for_xp(state["totalXp"], config["levelCurve"])[0]
        if dedupe_key and dedupe_key in state["seenActivity"]:
            level, current, needed = level_for_xp(state["totalXp"], config["levelCurve"])
            return {
                "memberId": member_id,
                "source": source_id,
                "awardedXp": 0,
                "reason": "duplicate",
                "totalXp": state["totalXp"],
                "level": level,
                "currentLevelXp": current,
                "xpToNextLevel": needed,
                "unlockedAchievements": (),
            }
        if source_id == "chat":
            cooldown_seconds = int(source.get("cooldownMinutes", 0)) * 60
            last_chat = int(state["lastActivity"].get("chat", 0))
            if cooldown_seconds and last_chat and occurred_at < last_chat + cooldown_seconds:
                if dedupe_key:
                    state["seenActivity"].append(dedupe_key)
                    state["seenActivity"] = state["seenActivity"][-500:]
                    await ctx.storage.set(MEMBER_KEY_PREFIX + str(member_id), state)
                level, current, needed = level_for_xp(
                    state["totalXp"],
                    config["levelCurve"],
                )
                return {
                    "memberId": member_id,
                    "source": source_id,
                    "awardedXp": 0,
                    "reason": "cooldown",
                    "totalXp": state["totalXp"],
                    "level": level,
                    "currentLevelXp": current,
                    "xpToNextLevel": needed,
                    "unlockedAchievements": (),
                    "rewardEvents": (),
                    "announcementSent": False,
                }

        day = datetime.fromtimestamp(occurred_at, tz=timezone.utc).date().isoformat()
        daily = dict(state["dailyXp"].get(day) or {})
        configured = int(source["xp"]) * units
        cap = int(source.get("dailyCap", configured))
        already = int(daily.get(source_id, 0))
        awarded = max(0, min(configured, cap - already))

        if awarded:
            state["totalXp"] += awarded
            state["sourceXp"][source_id] = int(state["sourceXp"].get(source_id, 0)) + awarded
            daily[source_id] = already + awarded
            state["dailyXp"] = {day: daily}
            if source_id == "chat":
                state["lastActivity"]["chat"] = occurred_at

        if source_id == "voice":
            minutes = int(source.get("windowMinutes", 10)) * units
            state["metrics"]["voiceMinutes"] = int(state["metrics"].get("voiceMinutes", 0)) + minutes
        elif source_id == "lfgParticipation":
            state["metrics"]["lfgParticipations"] = int(state["metrics"].get("lfgParticipations", 0)) + units
        elif source_id == "eventHost":
            state["metrics"]["eventsHosted"] = int(state["metrics"].get("eventsHosted", 0)) + units

        unlocked = []
        owned = set(state["achievements"])
        for achievement in config["achievements"]:
            if not achievement.get("enabled"):
                continue
            achievement_id = achievement["id"]
            condition = achievement.get("condition")
            if not condition or condition["type"] != "metric_at_least":
                continue

            metric_value = int(state["metrics"].get(condition["metric"], 0))
            threshold = int(condition["threshold"])
            if metric_value < threshold:
                continue

            previous_count = int(state["achievementCounts"].get(achievement_id, 0))
            repeatable = bool(achievement.get("repeatable"))
            if repeatable:
                repeat_every = int(condition["repeatEvery"])
                eligible_count = 1 + (metric_value - threshold) // repeat_every
                pending = max(0, eligible_count - previous_count)
                occurrence_count = min(pending, MAX_REPEAT_AWARDS_PER_CALL)
                if occurrence_count <= 0:
                    continue
            else:
                if achievement_id in owned:
                    continue
                occurrence_count = 1

            if achievement_id not in owned:
                owned.add(achievement_id)
                state["achievements"].append(achievement_id)

            new_count = previous_count + occurrence_count
            state["achievementCounts"][achievement_id] = new_count
            bonus = int(achievement["xp"]) * occurrence_count
            state["totalXp"] += bonus
            state["sourceXp"]["achievement"] = int(
                state["sourceXp"].get("achievement", 0)
            ) + bonus
            unlocked.append({
                "id": achievement_id,
                "name": achievement["name"],
                "emoji": achievement.get("emoji", ""),
                "xp": bonus,
                "occurrences": occurrence_count,
                "totalOccurrences": new_count,
            })

        if dedupe_key:
            state["seenActivity"].append(dedupe_key)
            state["seenActivity"] = state["seenActivity"][-500:]

        level_before_rewards = level_for_xp(state["totalXp"], config["levelCurve"])[0]
        reward_events = []
        claimed = set(state["claimedRewards"])
        for reward in config["rewards"]:
            if not reward.get("enabled") or reward["id"] in claimed:
                continue
            trigger = reward["trigger"]
            matched = (
                (trigger["type"] == "level" and level_before_rewards >= int(trigger["level"]))
                or (trigger["type"] == "xp" and state["totalXp"] >= int(trigger["xp"]))
                or (trigger["type"] == "achievement" and trigger["achievementId"] in state["achievements"])
            )
            if not matched:
                continue
            grants_applied = []
            for grant in reward["grants"]:
                kind = grant["type"]
                if kind == "badge":
                    badge_id = str(grant.get("badgeId", "")).strip()
                    if badge_id and badge_id not in state["badges"]:
                        state["badges"].append(badge_id)
                        grants_applied.append({"type": "badge", "value": badge_id})
                elif kind == "title":
                    title = str(grant.get("title", "")).strip()[:80]
                    if title and title not in state["titles"]:
                        state["titles"].append(title)
                        grants_applied.append({"type": "title", "value": title})
                elif kind == "xp_bonus":
                    bonus = _positive_int(grant.get("xp"), f"reward {reward['id']} xp bonus")
                    state["totalXp"] += bonus
                    state["sourceXp"]["reward"] = int(state["sourceXp"].get("reward", 0)) + bonus
                    grants_applied.append({"type": "xp_bonus", "xp": bonus})
                elif kind in {"role", "channel_access"}:
                    role_id = _positive_int(grant.get("roleId"), f"reward {reward['id']} roleId")
                    added = await ctx.discord.grant_role(member_id=member_id, role_id=role_id)
                    if added:
                        ownership = f"{reward['id']}:{role_id}"
                        if ownership not in state["ownedRoleGrants"]:
                            state["ownedRoleGrants"].append(ownership)
                        grants_applied.append({"type": kind, "roleId": role_id, "owned": True})
                    else:
                        # Pre-existing roles are never claimed as Progression-owned.
                        grants_applied.append({"type": kind, "roleId": role_id, "owned": False})
                elif kind == "announcement":
                    grants_applied.append({"type": "announcement"})
            if grants_applied:
                claimed.add(reward["id"])
                state["claimedRewards"].append(reward["id"])
                reward_events.append({"id": reward["id"], "name": reward["name"], "grants": tuple(grants_applied)})

        await ctx.storage.set(MEMBER_KEY_PREFIX + str(member_id), state)
        if awarded:
            await ctx.audit.write(
                action="progression.xp.awarded",
                target=str(member_id),
                metadata={"source": source_id, "xp": awarded},
            )
        for achievement in unlocked:
            await ctx.audit.write(
                action="progression.achievement.unlocked",
                target=str(member_id),
                metadata={"achievement": achievement["id"], "xp": achievement["xp"]},
            )

        level, current, needed = level_for_xp(state["totalXp"], config["levelCurve"])
        announcements = config["announcements"]
        announcement_sent = False
        if announcements.get("enabled") and announcements.get("channelId"):
            primary_achievement = unlocked[0] if unlocked else {}
            primary_reward = reward_events[0] if reward_events else {}
            should_send = (
                (unlocked and announcements.get("achievement"))
                or (reward_events and announcements.get("reward"))
                or (level > previous_level and announcements.get("levelUp"))
            )
            if should_send:
                member = await ctx.discord.get_member(member_id=member_id)
                values = {
                    "member": member.display_name,
                    "member_id": str(member_id),
                    "level": str(level),
                    "xp": str(sum(int(item.get("xp", 0)) for item in unlocked) + awarded),
                    "total_xp": str(state["totalXp"]),
                    "achievement_name": str(primary_achievement.get("name", "")),
                    "achievement_emoji": str(primary_achievement.get("emoji", "")),
                    "reward_name": str(primary_reward.get("name", "")),
                }
                message = announcements.get("template", "")
                for key, value in values.items():
                    message = message.replace("{" + key + "}", value)
                if message.strip():
                    await ctx.discord.send_message(
                        channel_id=int(announcements["channelId"]),
                        content=message[:2000],
                        allowed_mentions={
                            "everyone": False,
                            "users": False,
                            "roles": False,
                            "replied_user": False,
                        },
                    )
                    announcement_sent = True

        return {
            "memberId": member_id,
            "source": source_id,
            "awardedXp": awarded,
            "totalXp": state["totalXp"],
            "level": level,
            "currentLevelXp": current,
            "xpToNextLevel": needed,
            "dailySourceXp": int(daily.get(source_id, 0)),
            "dailyCapReached": bool(source.get("dailyCap") and daily.get(source_id, 0) >= int(source["dailyCap"])),
            "unlockedAchievements": tuple(unlocked),
            "rewardEvents": tuple(reward_events),
            "announcementSent": announcement_sent,
        }

    async def record_signal(self, ctx, payload) -> Mapping[str, Any]:
        member_id = _positive_int(payload.get("memberId"), "memberId")
        provider = _bounded_identifier(payload.get("provider"), "provider")
        signal = _bounded_identifier(payload.get("signal"), "signal")
        dedupe_key = str(payload.get("dedupeKey", "")).strip()
        if not dedupe_key or len(dedupe_key) > 160:
            raise ValueError("dedupeKey is required and must be at most 160 characters")
        occurred_at = _positive_int(
            payload.get("occurredAt", 0),
            "occurredAt",
            minimum=0,
            maximum=4_102_444_800,
        )
        if occurred_at == 0:
            occurred_at = int(datetime.now(timezone.utc).timestamp())

        config = await self._config(ctx)
        state = await self._member_state(ctx, member_id)
        if dedupe_key in state["seenSignals"]:
            level, current, needed = level_for_xp(
                state["totalXp"],
                config["levelCurve"],
            )
            return {
                "memberId": member_id,
                "provider": provider,
                "signal": signal,
                "reason": "duplicate",
                "unlockedAchievements": (),
                "rewardEvents": (),
                "totalXp": state["totalXp"],
                "level": level,
                "currentLevelXp": current,
                "xpToNextLevel": needed,
                "announcementSent": False,
            }

        state["seenSignals"].append(dedupe_key)
        state["seenSignals"] = state["seenSignals"][-500:]
        previous_level = level_for_xp(state["totalXp"], config["levelCurve"])[0]

        unlocked = []
        owned = set(state["achievements"])
        for achievement in config["achievements"]:
            if not achievement.get("enabled"):
                continue
            condition = achievement.get("condition")
            if not condition or condition.get("type") != "external_signal":
                continue
            if condition["provider"] != provider or condition["signal"] != signal:
                continue

            achievement_id = achievement["id"]
            repeatable = bool(achievement.get("repeatable"))
            previous_count = int(state["achievementCounts"].get(achievement_id, 0))
            if not repeatable and achievement_id in owned:
                continue

            if achievement_id not in owned:
                owned.add(achievement_id)
                state["achievements"].append(achievement_id)

            new_count = previous_count + 1
            state["achievementCounts"][achievement_id] = new_count
            bonus = int(achievement["xp"])
            state["totalXp"] += bonus
            state["sourceXp"]["achievement"] = int(
                state["sourceXp"].get("achievement", 0)
            ) + bonus
            unlocked.append({
                "id": achievement_id,
                "name": achievement["name"],
                "emoji": achievement.get("emoji", ""),
                "xp": bonus,
                "occurrences": 1,
                "totalOccurrences": new_count,
            })

        reward_events = []
        claimed = set(state["claimedRewards"])
        level_before_rewards = level_for_xp(
            state["totalXp"],
            config["levelCurve"],
        )[0]
        for reward in config["rewards"]:
            if not reward.get("enabled") or reward["id"] in claimed:
                continue
            trigger = reward["trigger"]
            matched = (
                (trigger["type"] == "level" and level_before_rewards >= int(trigger["level"]))
                or (trigger["type"] == "xp" and state["totalXp"] >= int(trigger["xp"]))
                or (
                    trigger["type"] == "achievement"
                    and trigger["achievementId"] in state["achievements"]
                )
            )
            if not matched:
                continue
            grants_applied = []
            for grant in reward["grants"]:
                kind = grant["type"]
                if kind == "badge":
                    badge_id = grant["badgeId"]
                    if badge_id not in state["badges"]:
                        state["badges"].append(badge_id)
                        grants_applied.append({"type": "badge", "value": badge_id})
                elif kind == "title":
                    title = grant["title"]
                    if title not in state["titles"]:
                        state["titles"].append(title)
                        grants_applied.append({"type": "title", "value": title})
                elif kind == "xp_bonus":
                    bonus = int(grant["xp"])
                    state["totalXp"] += bonus
                    state["sourceXp"]["reward"] = int(
                        state["sourceXp"].get("reward", 0)
                    ) + bonus
                    grants_applied.append({"type": "xp_bonus", "xp": bonus})
                elif kind in {"role", "channel_access"}:
                    role_id = int(grant["roleId"])
                    added = await ctx.discord.grant_role(
                        member_id=member_id,
                        role_id=role_id,
                    )
                    grants_applied.append({
                        "type": kind,
                        "roleId": role_id,
                        "owned": bool(added),
                    })
                    if added:
                        ownership = f"{reward['id']}:{role_id}"
                        if ownership not in state["ownedRoleGrants"]:
                            state["ownedRoleGrants"].append(ownership)
                elif kind == "announcement":
                    grants_applied.append({"type": "announcement"})
            if grants_applied:
                state["claimedRewards"].append(reward["id"])
                claimed.add(reward["id"])
                reward_events.append({
                    "id": reward["id"],
                    "name": reward["name"],
                    "grants": tuple(grants_applied),
                })

        await ctx.storage.set(MEMBER_KEY_PREFIX + str(member_id), state)
        await ctx.audit.write(
            action="progression.signal.recorded",
            target=str(member_id),
            metadata={"provider": provider, "signal": signal},
        )
        for achievement in unlocked:
            await ctx.audit.write(
                action="progression.achievement.unlocked",
                target=str(member_id),
                metadata={
                    "achievement": achievement["id"],
                    "xp": achievement["xp"],
                    "provider": provider,
                    "signal": signal,
                },
            )

        level, current, needed = level_for_xp(
            state["totalXp"],
            config["levelCurve"],
        )
        announcements = config["announcements"]
        announcement_sent = False
        if announcements.get("enabled") and announcements.get("channelId"):
            primary_achievement = unlocked[0] if unlocked else {}
            primary_reward = reward_events[0] if reward_events else {}
            should_send = (
                (unlocked and announcements.get("achievement"))
                or (reward_events and announcements.get("reward"))
                or (level > previous_level and announcements.get("levelUp"))
            )
            if should_send:
                member = await ctx.discord.get_member(member_id=member_id)
                values = {
                    "member": member.display_name,
                    "member_id": str(member_id),
                    "level": str(level),
                    "xp": str(sum(int(item.get("xp", 0)) for item in unlocked)),
                    "total_xp": str(state["totalXp"]),
                    "achievement_name": str(primary_achievement.get("name", "")),
                    "achievement_emoji": str(primary_achievement.get("emoji", "")),
                    "reward_name": str(primary_reward.get("name", "")),
                }
                message = announcements.get("template", "")
                for key, value in values.items():
                    message = message.replace("{" + key + "}", value)
                if message.strip():
                    await ctx.discord.send_message(
                        channel_id=int(announcements["channelId"]),
                        content=message[:2000],
                        allowed_mentions={
                            "everyone": False,
                            "users": False,
                            "roles": False,
                            "replied_user": False,
                        },
                    )
                    announcement_sent = True

        return {
            "memberId": member_id,
            "provider": provider,
            "signal": signal,
            "reason": "handled" if unlocked or reward_events else "unhandled",
            "unlockedAchievements": tuple(unlocked),
            "rewardEvents": tuple(reward_events),
            "totalXp": state["totalXp"],
            "level": level,
            "currentLevelXp": current,
            "xpToNextLevel": needed,
            "announcementSent": announcement_sent,
            "occurredAt": occurred_at,
        }

    async def preview_level(self, ctx, payload) -> Mapping[str, Any]:
        total_xp = _positive_int(payload.get("totalXp", 0), "totalXp", minimum=0)
        config = await self._config(ctx)
        level, current, needed = level_for_xp(total_xp, config["levelCurve"])
        return {
            "totalXp": total_xp,
            "level": level,
            "currentLevelXp": current,
            "xpToNextLevel": needed,
            "progress": 1.0 if needed == 0 else current / needed,
        }


def create_skill():
    return ProgressionSkill()
