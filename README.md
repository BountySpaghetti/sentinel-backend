# Stellar Sentinel — Backend

[![CI](https://github.com/Stellar-Sentinel/sentinel-backend/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Stellar-Sentinel/sentinel-backend/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Stellar Sentinel's Python API prototype. It provides a deterministic baseline score for caller-supplied account activity and establishes API boundaries for a future Stellar/Soroban monitoring service.

## Current capabilities

| Endpoint | Behavior |
| --- | --- |
| `GET /health` | Returns `{"status":"ok"}`. |
| `GET /events/` | Placeholder response; Soroban RPC event retrieval is not implemented. |
| `POST /risk/score` | Scores the transaction count and XLM volume supplied in the request. It does not fetch chain data or submit a contract transaction. |

FastAPI also exposes interactive API documentation at `/docs` while the service is running.

### Risk score example

```bash
curl -X POST http://localhost:8000/risk/score \
  -H 'Content-Type: application/json' \
  -d '{"address":"G...ACCOUNT","recent_tx_count":40,"recent_tx_volume":250000}'
```

The prototype assigns up to 60 points to transaction count and up to 40 points to volume in XLM:

- Transaction activity saturates at 100 transactions.
- Transaction volume saturates at 1,000,000 XLM.
- Scores below 40 are `low`; scores from 40 to 69 are `elevated`; scores of 70 or higher are `high` and exceed the prototype review threshold.

The response includes the component scores, threshold status, and `on_chain_action: "none"`. The values are demo defaults, not calibrated risk rules. The API trusts the caller's definition of the recent activity window, does not validate that the address exists, and accepts aggregate metrics rather than raw transactions.

## How it fits Stellar and Soroban

The intended system uses Stellar activity as input, computes an explainable off-chain assessment, and can eventually submit threshold-crossing flags to the Soroban contract. The contract authorizes agent addresses and emits flag events. In the current code, these parts are not wired together: `/risk/score` only processes the request body, `/events/` is a placeholder, and no Soroban transaction client exists.

```text
Caller-supplied metrics ──> /risk/score ──> score + explanation
Stellar RPC ──────────────> /events/     (planned; currently placeholder)
Backend signer/agent ────> Soroban flag_anomaly (planned; not connected)
```

The contract source and build instructions are in [sentinel-contract](https://github.com/Stellar-Sentinel/sentinel-contracts). The [frontend](https://github.com/Stellar-Sentinel/sentinel-frontend) currently presents an illustrative landing page and dashboard concept.

## Run locally

Requires Python 3.11 or newer.

```bash
python -m venv .venv
source .venv/bin/activate       # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) to inspect the API.

## Test

```bash
python -m pytest
```

## Configuration

`app/config.py` defines `SOROBAN_RPC_URL`, `NETWORK_PASSPHRASE`, `CONTRACT_ID`, and `ENVIRONMENT` settings, with testnet-oriented defaults. RPC and contract settings are scaffolding and are not used by the current routes. Keep secrets and signing keys out of source control; use environment variables or a local `.env` file for future secrets.

## Roadmap

- Fetch and paginate `flagged` events from Soroban RPC.
- Derive risk inputs from trusted Stellar activity data and define an explicit time window.
- Calibrate and document scoring behavior against reviewed examples.
- Add an authenticated, secure transaction path for authorized Soroban agents.
- Add request logging, rate limits, and integration tests.

## Contributing and license

See [CONTRIBUTING.md](CONTRIBUTING.md). Licensed under the [MIT License](LICENSE).
