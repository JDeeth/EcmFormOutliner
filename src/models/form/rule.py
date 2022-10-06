from dataclasses import dataclass


@dataclass
class Rule:
    """Form rule"""

    name: str
    local_id: str
    description: str = ""
