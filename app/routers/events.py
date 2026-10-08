from fastapi import APIRouter
from app.config import get_settings

router = APIRouter()
settings = get_settings()


@router.get("/")
def list_events():
    """
    Return recent 'flagged' events emitted by the Stellar Sentinel contract.

    TODO(#issue): this currently returns a hardcoded placeholder. It needs
    to call the Soroban RPC getEvents endpoint, filter by the contract's
    'flagged' topic, and paginate results.
    """
    return {
        "events": [],
        "note": "not yet wired to Soroban RPC — see open issue",
    }
