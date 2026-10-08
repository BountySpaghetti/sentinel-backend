from fastapi import FastAPI
from app.config import get_settings
from app.routers import health, events, risk

settings = get_settings()

app = FastAPI(
    title="Stellar Sentinel API",
    description="AI-agent risk monitoring layer for Soroban smart contracts.",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(events.router, prefix="/events", tags=["events"])
app.include_router(risk.router, prefix="/risk", tags=["risk"])

# TODO(#issue): no request logging middleware yet — every request should be
# logged as structured JSON (method, path, status, latency_ms).
# TODO(#issue): no auth/rate-limiting middleware yet — all routes are open.
