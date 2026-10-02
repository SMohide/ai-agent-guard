from typing import Dict, Any


def check_permission(
    agent_id: str,
    tool: str,
    action: str,
    agent_policies: Dict[str, Any],
) -> tuple[bool, str]:
    """
    Check whether an agent is allowed to use a specific tool/action.
    """

    agent = agent_policies.get("agents", {}).get(agent_id)

    if not agent:
        return False, f"Unknown agent: {agent_id}"

    allowed_tools = agent.get("allowed_tools", [])

    if tool not in allowed_tools:
        return (
            False,
            f"Agent '{agent_id}' is not allowed to use tool '{tool}'",
        )

    blocked_tools = agent.get("blocked_tools", [])

    if tool in blocked_tools:
        return (
            False,
            f"Tool '{tool}' is explicitly blocked for agent '{agent_id}'",
        )

    allowed_actions = agent.get("allowed_actions", {})

    if allowed_actions:
        tool_actions = allowed_actions.get(tool, [])

        if action not in tool_actions:
            return (
                False,
                f"Action '{action}' is not allowed for tool '{tool}'",
            )

    return True, "Permission granted"