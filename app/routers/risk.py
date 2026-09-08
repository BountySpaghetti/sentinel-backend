from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ScoreRequest(BaseModel):
    address: str
    recent_tx_count: int
    recent_tx_volume: float


@router.post("/score")
def score_address(req: ScoreRequest):
    """
    Run the LangGraph risk-scoring pipeline on an address.

    TODO(#issue): app/agents/pipeline.py is currently a stub that returns a
    fixed score. It needs a real LangGraph graph with at least: a data-gather
    node, a scoring node, and a decision node that decides whether to call
    flag_anomaly on-chain.
    """
    return {"address": req.address, "score": 0, "flagged": False}
