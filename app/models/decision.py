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