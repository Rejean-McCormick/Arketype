# Branch 02 — Arketype designs and an explicitly selected current Kit

**Status:** opted-in local draft.4 source checked; historical templates preserved, **not** canonical semantic authoring qualification.

## Two intentionally separate creation routes

- Default `create` uses historical bundled Kit 3.2.4 as before. The existing 19 archetype models, their metadata and v9 states remain unchanged.
- `--authoring v11` without an external Kit retains the Arketype 1.6.0 bundled **Kit 4.0.0-draft.3** for reproducible past projects. It creates an empty workspace and noncanonical readiness checklist; strict v11 is *not* enabled.
- **New opt-in** `--authoring v11 --external-kit PATH --framework PATH` selects an **independently installed Kit 4.0.0-draft.4** and a **Framework 11.0.0-draft.4** source. The preflight checks Kit version, its own `KIT_VERSION` and all 13 Framework pin digests, then creates the same empty, noncanonical design workspace. No production migration, remote download or publication follows.

```bash
python arketype.py create --type referentiel-semantique --slug example-v11 \
  --title 'Example draft.4' --parent . --authoring v11 \
  --external-kit ../Authoring-Kit --framework ../Framework --dry-run
```

Remove `--dry-run` only after reviewing the selected source roots and destination. `arketype.instance.json` and `design/v11-semantic-readiness.json` disclose the Kit actually used and retain `published=false`, `strict_v11_enabled=false` and `publication_authorized=false`.

## Safety and qualification boundaries

- An archetype name, visual label or content scenario is not a KQ/KP identity. A selected template cannot grant domain security, student/medical rights, or owner authority.
- A v11 readiness checklist is not a populated Framework graph or a passed `check-v11` result; it cannot substitute for authorized Kit registration.
- Future Kit/Framework versions are not silently accepted; the currently qualified local source pair is exact `draft.4`. Older bundled assets remain historical source bytes.
- Existing Arketype full-suite checks require build/v9 receipts and a user-supplied logo absent from the provided SmartDump ZIP; do not replace missing original assets with fabricated ones or mark those checks as passed.

**Next owner gate:** test a real reviewed Arketype→Kit registration workflow on a fresh disposable workspace, with exact identity, lexical catalog and conversion-plan approvals. This branch proves empty-workspace creation only.
