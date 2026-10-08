# sentinel-backend

FastAPI + LangGraph service that scores Stellar addresses for risk and
(eventually) calls the Stellar Sentinel contract's `flag_anomaly` when a
threshold is crossed.

## Status
Early prototype. `/health` is available; `/events` still returns placeholder
data. `/risk/score` applies a deterministic heuristic to caller-supplied
transaction count and volume. It does not fetch Stellar activity or submit
transactions to the Soroban contract.

### Risk scoring

Send `POST /risk/score` with `address`, `recent_tx_count` (non-negative), and
`recent_tx_volume` (non-negative XLM). The score assigns up to 60 points to
transaction count (saturating at 100) and up to 40 points to volume (saturating
at 1,000,000 XLM). Scores of 70 or more exceed the prototype review threshold.
The response includes the component breakdown and `on_chain_action: "none"`.
These values are uncalibrated demo defaults, and the duration of the caller's
"recent" window is not currently enforced.

## Run
```
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Test
```
pytest
```
