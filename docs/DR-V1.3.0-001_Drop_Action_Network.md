# DR-V1.3.0-001 — Drop Action Network from Phase 1

**Decision record ID:** DR-V1.3.0-001
**Date:** 2026-05-13
**Status:** ACCEPTED
**Author:** Michael Turon (operator)
**Affected version:** v1.3.0
**Supersedes:** N/A

## Decision

Drop Action Network from v1.3.0. Brevo handles both newsletter subscriber capture AND volunteer signup via two forms on one unified contact list with tag-based segmentation.

## Rationale

Phase 1 mode is pre-endorsement, list-building primary. No campaign event calendar, no canvass shifts to schedule, no distributed-organizing tooling required.

Action Network earns its place when: event RSVPs with shifts, distributed organizing, voter-file integrations (EveryAction/VoteBuilder), bulk SMS to organized volunteers. None of these are Phase 1 needs.

Brevo form builder + tag segmentation captures all volunteer data the campaign needs in Phase 1: name, email, phone, ZIP, availability, skill preferences.

## Consequences

- Two vendors (Brevo + ActBlue) instead of three
- One review cycle saved (Sam Ray + Lauren review Brevo once for both forms)
- Two webhook endpoints in V0.1 instead of three
- Volunteer destination in hugo.toml points to /newsletter/ until Brevo volunteer form is built (v1.3.1)

## Phase 2 re-add trigger

Re-add Action Network if: campaign has recurring events with shift signups OR needs EveryAction/VoteBuilder voter-file sync OR distributed organizing becomes operational.

## Sign-off

| Role | Name | Date |
|---|---|---|
| Operator | Michael Turon | 2026-05-13 |
| Counsel | Sam Ray | pending batched review |
| Treasurer | Lauren Turon | pending walkthrough |
