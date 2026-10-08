# GamerHQ XP & Progression Skill

A portable GamerHQ Skill for configurable XP, levels, achievements and rewards.

**Skill ID:** `progression`  
**Package:** `gamerhq-skill-xp-progression`  
**Version:** `0.1.0`  
**Runtime API:** `1`

## Purpose

This repository contains the standalone Progression implementation originally matured inside GamerHQ. The repository name makes the XP purpose obvious, while the stable runtime identity remains `progression` so existing guild storage and Management API routing stay compatible.

## Features

- Configurable XP sources and daily caps.
- Deterministic level curve, max level and level previews.
- Per-member total XP, per-source XP and activity metrics.
- Stable achievement definitions and threshold unlocks.
- Reward triggers for level, achievement and total XP.
- Badge, title, XP bonus, role, channel-access and announcement grants.
- Safe role ownership semantics for pre-existing Discord roles.
- Configurable level-up, achievement and reward announcements.
- Declarative Management UI Schema for generic GamerHQ management surfaces.
- Bounded activity deduplication through `dedupeKey`.

## Architecture boundary

The Skill owns progression rules and Skill state. GamerHQ owns Discord observation and host integration.

The standalone package does **not** import GamerHQ bot internals, Discord.py, cogs, services, database modules, hosts, config, or another Skill implementation. Voice sampling and completed-LFG observation remain in GamerHQ and call the Skill through public Runtime Management contracts.

## Stable storage

Storage identity is intentionally unchanged:

- `config.v1`
- `member.v1:<discord-member-id>`

GamerHQ Skill Storage is already scoped by guild ID and Skill ID. Because the Skill ID remains `progression`, extraction does not require a data migration.

## Public Management APIs

- `progression.status.v1`
- `progression.get-config.v1`
- `progression.update-config.v1`
- `progression.preview-level.v1`
- `progression.record-activity.v1`
- `progression.member-status.v1`

## Capabilities

- `storage.skill`
- `audit.write`
- `discord.messages.send`
- `discord.channels.read`
- `discord.members.read`
- `discord.roles.manage`

The package does not request `scheduler.jobs`.

## Development

Use Python 3.12 or newer and install the compatible GamerHQ Skill SDK/Runtime contracts before running the package tests.

Typical local flow:

```bash
python -m pip install -U pip
# Install a released or reviewed immutable GamerHQ Skill SDK compatible with >=0.1,<0.2.
python -m pip install -e .
python -m pytest -q
```

Do not use a moving GamerHQ `develop` branch as a release dependency. CI pins an immutable public compatibility commit so this repository remains reproducible and autonomous.

CI validates Python 3.12 and 3.14, package build/install, `pip check`, tests, source portability, SDK conformance, static metadata, capability equality and entry-point identity.

## Extraction status

Version `0.1.0` is the extracted baseline of the existing GamerHQ Progression implementation. This repository does not deploy production and does not contain the GamerHQ host adapter.

## Repository ownership

This repository owns and releases the Progression Skill independently. GamerHQ Host, gamerhq-web, other Skills and production infrastructure are separate repositories with separate owners and release lifecycles. If Progression needs a new upstream public contract, this project produces a handoff instead of modifying the upstream repository directly.

## Release status

Version `0.1.0` is the first independently releasable standalone Progression baseline. The package is compatible with Runtime API `1` and SDK `>=0.1,<0.2`. Release publication is independent of any GamerHQ Host deployment.
