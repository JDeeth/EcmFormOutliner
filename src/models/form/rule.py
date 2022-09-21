# pylint: disable=C0111
from dataclasses import dataclass


@dataclass
class Rule:
    """ Form rule """

    name: str
    local_id: str
    description: str = ""

    @property
    def type(self):
        return "rule"