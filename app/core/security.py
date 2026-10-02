def authenticate_agent(agent_id: str) -> bool:
    """
    Temporary authentication mechanism.

    Real JWT/OAuth authentication will be added later.
    """

    return bool(agent_id)