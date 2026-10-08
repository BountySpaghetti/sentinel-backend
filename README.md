# Stellar Sentinel Backend

[![CI](https://github.com/Stellar-Sentinel/sentinel-backend/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Stellar-Sentinel/sentinel-backend/actions/workflows/ci.yml)

Read-only FastAPI service for screening Stellar accounts and displaying flags emitted by the Stellar Sentinel Soroban contract. It uses Horizon for account and operation data and Stellar RPC for Soroban events. Risk scores are transparent screening heuristics, not proof of fraud, financial advice, or an on-chain action.

## API

| Endpoint | Behavior |
| --- | --- |
| `GET /health` | Liveness check. |
| `GET /network/status` | Soroban RPC health and its current latest/oldest retained ledger plus `ledger_retention_window`. |
| `POST /risk/score` | Fetches account balances and recent operations from Horizon; returns bounded score, signals, and metrics. |
| `GET /events?limit=20&cursor=...` | Reads `flagged` events for `CONTRACT_ID` via Soroban RPC. |

### Screen an account

```bash
curl -X POST http://localhost:8000/risk/score \
  -H 'Content-Type: application/json' \
  -d '{"address":"G...55-character Stellar account public key..."}'
```

The response includes `score` (0–100), `risk_level`, `threshold_exceeded`, the individual `signals`, `metrics`, source endpoint/network, and observation time. The current baseline adds bounded points for high recent operation count, native XLM transfer volume, and counterparty spread. A low account sequence adds only a weak review signal. Threshold is 70. These simple rules need calibration and should not be treated as a trained model. `threshold_exceeded` means only that the off-chain score reached the configured baseline threshold; it does not submit a transaction or create a contract flag.

Horizon operations are fetched newest-first, up to `OPERATION_SCAN_LIMIT` (maximum 200). The screening window is `ACTIVITY_WINDOW_DAYS` (default 7). This is a bounded sample: accounts with more activity than the scan limit may have older operations in the window omitted. Transfer volume includes native XLM amounts only; issued assets are excluded rather than combined as if denominated in XLM. Horizon availability and retention are controlled by the configured service.

### Read on-chain events

`GET /events` returns only events for the configured contract. First-page queries start within `EVENTS_LOOKBACK_LEDGERS` (default 50,000) of the latest RPC ledger, clamped forward to the RPC's reported `oldestLedger`. Further pages use the returned opaque `next_cursor` as `cursor`. Stellar RPC retains only a bounded recent history (reported as `ledger_retention_window`; provider-configured and commonly around seven days), so this endpoint is not a complete historical archive. Missing `CONTRACT_ID` returns HTTP 503. RPC/Horizon failures are surfaced as service errors; no placeholder events are returned.

## Stellar integration

The contract authorizes monitoring agents and emits a `flagged` event when an authorized agent calls `flag_anomaly` with a score meeting the contract threshold. This backend currently reads that event stream but deliberately has no signing key and does not submit transactions. Account scoring queries the public Horizon API; event retrieval and network status use the public Soroban RPC API. Configure endpoints for the same Stellar network as the deployed contract.

## Run locally

Requires Python 3.11 or newer.

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open [http://localhost:8000/docs](http://localhost:8000/docs).

## Configuration

Copy `.env.example` to `.env` and adjust values as needed, or set them directly as environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `HORIZON_URL` | `https://horizon-testnet.stellar.org` | Horizon API base URL. |
| `SOROBAN_RPC_URL` | `https://soroban-testnet.stellar.org` | Soroban RPC endpoint. |
| `NETWORK_PASSPHRASE` | Stellar Testnet passphrase | Network label/passphrase returned by the API. |
| `CONTRACT_ID` | empty | Deployed Sentinel contract ID; required for `/events`. |
| `REQUEST_TIMEOUT_SECONDS` | `8` | Outbound HTTP timeout. |
| `OPERATION_SCAN_LIMIT` | `200` | Maximum operations examined, capped by Horizon at 200. |
| `ACTIVITY_WINDOW_DAYS` | `7` | Recent operation window. |
| `EVENTS_LOOKBACK_LEDGERS` | `50000` | First-page Soroban event search window. |
| `CORS_ORIGINS` | `http://localhost:3000` | Comma-separated allowed browser origins. |

Never place account secrets, signing keys, or tokens in source control. The service is read-only and needs no secrets for the current capabilities.

## Development

```bash
python -m pytest
```

Tests mock external Horizon/RPC responses. See [CONTRIBUTING.md](CONTRIBUTING.md). Licensed under MIT.
