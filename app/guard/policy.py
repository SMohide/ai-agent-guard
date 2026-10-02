from pathlib import Path
from typing import Any

import yaml


POLICY_DIR = Path(__file__).resolve().parents[2] / "policies"


def load_yaml(filename: str) -> dict[str, Any]:
    path = POLICY_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"Policy file not found: {path}")

    with open(path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def load_agent_policies() -> dict[str, Any]:
    return load_yaml("agents.yaml")


def load_tool_policies() -> dict[str, Any]:
    return load_yaml("tools.yaml")


def load_risk_rules() -> dict[str, Any]:
    return load_yaml("risk_rules.yaml")