from typing import Any, Dict

from pydantic import BaseModel, Field


class AgentActionRequest(BaseModel):
    agent_id: str = Field(..., description="Unique AI agent identifier")
    user_id: str = Field(..., description="Human user behind the agent")
    tool: str = Field(..., description="Tool the agent wants to use")
    action: str = Field(..., description="Action the agent wants to perform")
    parameters: Dict[str, Any] = Field(default_factory=dict)