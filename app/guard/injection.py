from __future__ import annotations


def detect_prompt_injection(text: str) -> tuple[bool, str]:
    """Detect common prompt-injection phrases that try to override instructions.

    Returns a tuple of (was_injection_detected, matched_pattern).
    """

    if not text:
        return False, ""

    normalized = str(text).lower()

    suspicious_patterns = [
        "ignore previous instructions",
        "ignore all previous instructions",
        "override system prompt",
        "override developer instructions",
        "disregard the above",
        "forget the above",
        "you are now",
        "new instructions",
        "system prompt",
        "developer prompt",
        "bypass policy",
        "bypass the rules",
        "act as if",
        "ignore the developer",
        "ignore the system",
    ]

    for pattern in suspicious_patterns:
        if pattern in normalized:
            return True, pattern

    return False, ""