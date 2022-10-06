from dataclasses import dataclass
from typing import List

from models.form.control import BaseControl


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
