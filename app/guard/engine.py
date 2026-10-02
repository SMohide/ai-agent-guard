import uuid
from typing import Any, Dict

from app.guard.identity import identify_agent
from app.guard.permissions import check_permission
from app.guard.policy import (
    load_agent_policies,
    load_risk_rules,
)
from app.guard.risk import calculate_risk
from app.guard.decision import make_decision
from app.guard.injection import detect_prompt_injection
from app.models.action import AgentActionRequest
from app.models.decision import GuardDecision, Decision


def run_guard(action_request: AgentActionRequest) -> GuardDecision:

    action_id = f"act_{uuid.uuid4().hex[:12]}"

    # --------------------------------------------------
    # 1. IDENTITY
    # --------------------------------------------------

    identity = identify_agent(
        action_request.agent_id,
        action_request.user_id,
    )

    if not identity.authenticated:
        return GuardDecision(
            decision=Decision.BLOCK,
            reason="Agent or user identity is invalid.",
            risk_score=100,
            action_id=action_id,
        )

    # --------------------------------------------------
    # 2. LOAD POLICIES
    # --------------------------------------------------

    agent_policies = load_agent_policies()
    risk_rules = load_risk_rules()

    # --------------------------------------------------
    # 3. PERMISSION CHECK
    # --------------------------------------------------

    permission_ok, permission_reason = check_permission(
        agent_id=action_request.agent_id,
        tool=action_request.tool,
        action=action_request.action,
        agent_policies=agent_policies,
    )

    if not permission_ok:
        return GuardDecision(
            decision=Decision.BLOCK,
            reason=permission_reason,
            risk_score=95,
            action_id=action_id,
        )

    # --------------------------------------------------
    # 4. PROMPT INJECTION CHECK
    # --------------------------------------------------

    text_to_scan = str(action_request.parameters)

    injection_found, matched_pattern = detect_prompt_injection(
        text_to_scan
    )

    if injection_found:
        return GuardDecision(
            decision=Decision.BLOCK,
            reason=f"Possible prompt injection detected: {matched_pattern}",
            risk_score=100,
            action_id=action_id,
        )

    # --------------------------------------------------
    # 5. RISK CALCULATION
    # --------------------------------------------------

    risk_score = calculate_risk(
        action=action_request.action,
        parameters=action_request.parameters,
        risk_rules=risk_rules,
    )

    # --------------------------------------------------
    # 6. HUMAN APPROVAL RULE
    # --------------------------------------------------

    agent = agent_policies.get("agents", {}).get(
        action_request.agent_id,
        {},
    )

    require_human = False

    human_threshold = agent.get("require_human_above")

    amount = action_request.parameters.get("amount")

    if (
        human_threshold is not None
        and isinstance(amount, (int, float))
        and amount > human_threshold
    ):
        require_human = True

    # --------------------------------------------------
    # 7. FINAL DECISION
    # --------------------------------------------------

    decision, reason = make_decision(
        risk_score=risk_score,
        require_human=require_human,
    )

    return GuardDecision(
        decision=decision,
        reason=reason,
        risk_score=risk_score,
        action_id=action_id,
    )