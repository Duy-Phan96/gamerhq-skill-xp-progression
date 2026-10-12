# Security Policy

## Scope

This repository contains a portable Progression Skill that can store member progression state, award XP and achievements, grant configured roles, and send configured announcements.

## Reporting a vulnerability

Do not publish secrets, tokens, private member data, exploit details, or production identifiers in a public Issue. Report security-sensitive findings privately to the repository owner with the affected version/commit, impact, and non-production reproduction steps.

## Security boundaries

The Skill must use only declared public capabilities and Skill-scoped storage; avoid Host database/filesystem access and private Host imports; suppress unsafe Discord mentions; validate reward configuration before execution; never claim ownership of a pre-existing member role; and keep read-only operations non-destructive.

## Secrets

This Skill should not require production secrets. Never commit or paste Discord bot tokens, API keys, private environment files, production database contents, or private member information.

## Member and Discord data

Treat member IDs, progression state, roles, and announcement destinations as operational data. New data collection should document purpose, storage, retention, and capability impact.

## Dependency and capability changes

New Runtime/SDK dependencies or capabilities require explicit review. If a required security primitive belongs to the Host, create a handoff instead of accessing Host internals.