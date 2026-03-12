# BruceAI — BRAIN (Neural Memory + Motor)

This repo contains the **BRAIN** blueprint and starter skeleton for BruceAI:
- **BRAINneuralMemory.md** — the full insane-but-doable design doc
- **brain/** — API stubs, memory schema, planner skeletons
- **docs/images/** — diagrams (placeholders included)

Start by reading `BruceAI/BRAINneuralMemory.md`.
 
## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn brain.api.server:app --reload
```
