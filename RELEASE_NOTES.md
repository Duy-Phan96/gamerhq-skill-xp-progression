# Release Notes — v0.1.0

## Summary

First standalone release of the GamerHQ-compatible XP & Progression Skill.

## Public identity

- Distribution: `gamerhq-skill-xp-progression`
- Skill ID: `progression`
- Version: `0.1.0`
- Runtime API: `1`
- SDK compatibility: `>=0.1,<0.2`

## Features

- configurable XP sources and daily caps
- deterministic level calculation and previews
- member XP and activity metrics
- achievements
- level / achievement / total-XP rewards
- badge, title, XP bonus, role, channel-access and announcement rewards
- announcement configuration
- generic Management UI Schema
- bounded activity deduplication

## Public Management APIs

- `progression.status.v1`
- `progression.get-config.v1`
- `progression.update-config.v1`
- `progression.preview-level.v1`
- `progression.record-activity.v1`
- `progression.member-status.v1`

## Storage compatibility

- `config.v1`
- `member.v1:<discord-member-id>`

The standalone extraction preserves Skill ID and storage identity. No release-specific data migration is required.

## Capabilities

- `storage.skill`
- `audit.write`
- `discord.messages.send`
- `discord.channels.read`
- `discord.members.read`
- `discord.roles.manage`

The Skill does not request `scheduler.jobs`.

## Architecture

Host-specific Discord observation remains outside this package. The package consumes only public Runtime/SDK contracts and does not import Discord.py or GamerHQ Host internals.

## Release boundary

This repository releases independently. A Host may choose to install or pin this release later; Host production deployment is not part of this release.
