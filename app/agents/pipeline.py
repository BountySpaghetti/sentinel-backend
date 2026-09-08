"""
Risk-scoring agent pipeline.

Intended shape (not yet implemented):
    gather_data -> score_risk -> decide_action

TODO(#issue): build this as a langgraph.graph.StateGraph with the three
nodes above. gather_data should pull recent on-chain activity for the
address; score_risk should combine heuristics (tx velocity, volume,
counterparty diversity) into a 0-100 score; decide_action should decide
whether the score crosses the contract's risk threshold and, if so,
call the backend's on-chain flagging client (not yet built either).
"""


def run_pipeline(address: str) -> dict:
    return {"address": address, "score": 0, "flagged": False}
