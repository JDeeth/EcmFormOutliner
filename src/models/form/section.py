from dataclasses import dataclass, field
from typing import List


from models.form.subsection import Subsection

# pylint: disable=duplicate-code


@dataclass
class Section:
    """Form section

    A section contains subsections.

    A subsection is:
    - a run of one or more controls,
    - a table, or
    - a repeatable group

    It is possible for a section to have no subsections, i.e. be completely
    empty, but this would be a bit nonsensical.
    """

    name: str
    title: str
    number: int
    local_id: str
    visibility_rule_name: str = ""
    subsections: List[Subsection] = field(default_factory=list)
