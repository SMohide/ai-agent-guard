from typing import Any, Dict


DEFAULT_RISK = {
    "read": 10,
    "search": 10,
    "get_balance": 20,
    "send_internal_email": 35,
    "send_external_email": 60,
    "update_customer": 55,
    "delete_customer": 75,
    "transfer_money": 85,
    "refund_money": 80,
    "change_permissions": 95,
}


def calculate_risk(
    action: str,
    parameters: Dict[str, Any],
    risk_rules: dict,
) -> int:

    action_scores = risk_rules.get("action_scores", DEFAULT_RISK)

    score = action_scores.get(action, 50)

    # Financial amount modifier
    amount = parameters.get("amount")

    if isinstance(amount, (int, float)):
        if amount > 100000:
            score += 15
        elif amount > 50000:
            score += 10
        elif amount > 10000:
            score += 5

    # External destination
    if parameters.get("external") is True:
        score += 10

    return min(score, 100)