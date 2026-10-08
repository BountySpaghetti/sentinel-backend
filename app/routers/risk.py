from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.agents.pipeline import run_pipeline

router = APIRouter()


class ScoreRequest(BaseModel):
    address: str = Field(min_length=1, max_length=128, description="Stellar address or account identifier")
    recent_tx_count: int = Field(ge=0, description="Transaction count in the caller's recent activity window")
    recent_tx_volume: float = Field(ge=0, description="Aggregate transaction volume in XLM for that window")


@router.post("/score")
def score_address(req: ScoreRequest):
    """Score the caller-supplied activity metrics with the prototype heuristic.

    This endpoint does not fetch chain data or submit a contract transaction.
    """
    return run_pipeline(req.address, req.recent_tx_count, req.recent_tx_volume)
