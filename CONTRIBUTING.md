# Contributing to sorosentinel-backend

## Setup
```
python -m venv .venv
.venv\Scripts\activate      # PowerShell
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload
```

## Before opening a PR
- Run pytest and make sure it passes.
- Keep the PR scoped to one issue; reference it with `Closes #N`.
- Update README.md if you changed a route's behavior.

## Related repos
- sorosentinel-contract — the Soroban contract this service calls
- sorosentinel-frontend — dashboard consuming this service's /events endpoint
