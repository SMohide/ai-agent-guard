from dataclasses import dataclass


@dataclass
class AgentIdentity:
    agent_id: str
    user_id: str
    authenticated: bool = True


def identify_agent(agent_id: str, user_id: str) -> AgentIdentity:
    """
    Resolve the identity of the agent and the human user behind it.

    V1 uses a simple trusted identity.
    Real authentication will be added later.
    """

    if not agent_id or not user_id:
        return AgentIdentity(
            agent_id=agent_id,
            user_id=user_id,
            authenticated=False,
        )

    return AgentIdentity(
        agent_id=agent_id,
        user_id=user_id,
        authenticated=True,
    )