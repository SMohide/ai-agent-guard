from enum import Enum

from pydantic import BaseModel


class Decision(str, Enum):
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"
    ASK_HUMAN = "ASK_HUMAN"


class GuardDecision(BaseModel):
    decision: Decision
    reason: str
    risk_score: int
    action_id: str


def make_decision(
    risk_score: int,
    require_human: bool = False,
) -> tuple[Decision, str]:
    """Translate a computed risk score into a safe approval decision."""

    risk_score = max(0, min(int(risk_score), 100))

    if risk_score >= 80:
        return Decision.BLOCK, "Risk score exceeds the blocking threshold."

    if require_human or risk_score >= 50:
        return (
            Decision.ASK_HUMAN,
            "Human approval is required before this action proceeds.",
        )

    return Decision.ALLOW, "Action is within policy limits and low-risk threshold."