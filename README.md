# sorosentinel-backend

FastAPI + LangGraph service that scores Stellar addresses for risk and
(eventually) calls the SoroSentinel contract's `flag_anomaly` when a
threshold is crossed.

## Status
Early scaffold. `/health`, `/events`, `/risk/score` exist but `/events` and
`/risk/score` return placeholders — see open issues.

## Run
```
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Test
```
pytest
```
