# Neutral template — Procedure / Protocol

**Type:** Local Kristal  
**Workspace:** `kristal.local-workspace/3.2.0`  
**State architecture:** `kristal.state/9.0`

## Local checks and builds

```bash
python tools/kristal.py check .
python tools/kristal.py build-v9 .
```

Building a state does not activate an AI layer by default.

## Optional AI reader outputs

```bash
python tools/kristal.py build-ai .
python tools/kristal.py check-ai .
python tools/kristal.py pack-ai . --output portable-ai.zip
```

## Hosting and publication

Kristal Manager can synchronize a hosted reading surface. Kristal GitHub Setup / Bootstrap handles qualification, publication, and optional activation as separate authorized steps. A synchronized reader view is not a new semantic state or automatic publication.
