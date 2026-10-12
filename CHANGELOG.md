# Changelog

## 0.1.0 - 2026-10-12

- Extracted the existing GamerHQ Progression & Achievements implementation into its standalone package.
- Preserved Skill ID `progression`, Runtime API 1, Management API IDs and storage keys.
- Added configurable XP sources, deterministic levels, achievements, rewards, announcements and generic Management UI behavior.
- Added daily XP caps, bounded activity deduplication and revision-safe configuration updates.
- Added declarative `metric_at_least` achievement rules for Progression-owned metrics.
- Added Skill-owned chat cooldown enforcement while keeping raw voice-eligibility observation at the Host boundary.
- Added validated reward grant configuration and explicit role-backed `channel_access` semantics.
- Added independent package metadata, tests, contributor/security documentation and release automation.
- Added Python 3.12 / 3.14 CI and immutable SDK compatibility validation.
