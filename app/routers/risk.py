from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from app.stellar import score_account

router = APIRouter()


class ScoreRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    address: str = Field(pattern=r"^G[A-Z2-7]{55}$", description="Classic Stellar account public key")


@router.post("/score")
def score_address(req: ScoreRequest):
    """Screen a Stellar account using its recent Horizon operations."""
    return score_account(req.address)
