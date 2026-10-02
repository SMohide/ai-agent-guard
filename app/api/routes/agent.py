from fastapi import APIRouter

from app.guard.engine import run_guard
from app.models.action import AgentActionRequest
from app.models.decision import GuardDecision


router = APIRouter(
    prefix="/agent",
    tags=["Agent"],
)


@router.post(
    "/action",
    response_model=GuardDecision,
)
def evaluate_agent_action(
    request: AgentActionRequest,
):

    return run_guard(request)