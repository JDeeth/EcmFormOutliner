# pylint: disable=C0111
from dataclasses import dataclass


@dataclass
class Section:
    """ Form section """

    name: str
    title: str
    number: int
    local_id: str
    visibility_rule_name: str = ""
