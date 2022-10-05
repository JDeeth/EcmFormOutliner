from dataclasses import dataclass, field
from typing import List

from models.form.section import Section


@dataclass
class Page:
    """Form page"""

    name: str
    title: str
    number: int
    local_id: str
    visibility_rule_name: str = ""

    sections: List[Section] = field(default_factory=list)
