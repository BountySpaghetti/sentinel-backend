from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_risk_score_returns_breakdown_and_does_not_claim_chain_action():
    response = client.post(
        "/risk/score",
        json={"address": "GTEST", "recent_tx_count": 100, "recent_tx_volume": 250_000},
    )

    assert response.status_code == 200
    assert response.json() == {
        "address": "GTEST",
        "score": 70,
        "risk_level": "high",
        "threshold": 70,
        "threshold_exceeded": True,
        "score_breakdown": {"transaction_activity": 60, "transaction_volume": 10},
        "window": "caller-supplied recent activity; duration is not currently enforced",
        "on_chain_action": "none",
    }


def test_risk_score_rejects_negative_metrics():
    response = client.post(
        "/risk/score",
        json={"address": "GTEST", "recent_tx_count": -1, "recent_tx_volume": 0},
    )

    assert response.status_code == 422


def test_risk_score_rejects_negative_volume():
    response = client.post(
        "/risk/score",
        json={"address": "GTEST", "recent_tx_count": 1, "recent_tx_volume": -0.1},
    )

    assert response.status_code == 422
