from dataclasses import dataclass, field
from typing import List

from models.controls import BaseControl

# pylint: disable=duplicate-code


@dataclass
class Subsection:
    """Base class for components of a section"""

    row_number: int
    controls: List[BaseControl]


@dataclass
class PlainRun(Subsection):
    """A continguous set of ordinary form controls"""


@dataclass
class RepeatableGroup(Subsection):
    """A repeatable set of form controls"""


@dataclass
class Table(Subsection):
    """A repeatable set of form controls, structured as a table"""


@dataclass
class Section:
    """Form section, composed of subsections and metadata

    Can contain zero subsections, which would be strange
    """

    name: str
    title: str
    number: int
    local_id: str
    visibility_rule_name: str = ""
    subsections: List[Subsection] = field(default_factory=list)


@dataclass
class Page:
    """Form page"""

    name: str
    title: str
    number: int
    local_id: str
    visibility_rule_name: str = ""

    sections: List[Section] = field(default_factory=list)


@dataclass
class Rule:
    """Form rule"""

    name: str
    local_id: str
    description: str = ""
