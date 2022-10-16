from typing import Optional
from app.util import jsonpath


class DisplayControl:
    """Seam between json-wrangling and output formatting"""

    def __init__(self, json_: dict, rules: dict):
        """Save defaults - return None if details not in JSON"""
        self._json = json_
        self._label = jsonpath(json_, "label/value")
        self._type = self._json.get("subType")
        self._details = ""
        self._vis_rule = visibility_rule(json_.get("visibilityRuleId"), rules)
        on_save = jsonpath(json_, "validation/mandatory")
        self._mandatory = None if on_save is None else on_save == "MANDATORY_ON_SAVE"

    @property
    def label(self) -> str:
        """Unadorned, untrimmed label or guidance text"""
        return self._label

    @property
    def type(self) -> str:
        """Control subType typically"""
        return self._type

    @property
    def details(self) -> str:
        """Any relevant details e.g. max rows

        Perhaps should be a dict"""
        return self._details

    @property
    def visibility_rule(self) -> str:
        """Name of applicable visibility rule, otherwise empty string"""
        return self._vis_rule

    @property
    def mandatory(self) -> Optional[bool]:
        """
        MANDATORY_ON_SAVE: True
        NOT_MANDATORY: False
        otherwise: None
        """
        return self._mandatory


class Alert(DisplayControl):
    def __init__(self, json_, rules):
        super().__init__(json_, rules)
        self._type = "Guidance text"
        self._label = "\n".join(
            [self._json["alertText"], self._json["alertBody"]],
        )


class TextLine(DisplayControl):
    def __init__(self, json_, rules):
        super().__init__(json_, rules)
        self._type = "Free text"


def visibility_rule(vis_rule_id: str, rules: list) -> str:
    """Returns rule name given rule ID"""
    rules = {rule["definitionId"]: rule["name"] for rule in rules}
    rules[None] = ""

    result = rules.get(vis_rule_id)
    if vis_rule_id and not result:
        result = f"(external rule {vis_rule_id[:8]}"
    return result


def parse_control(jsn: dict, rules: list) -> DisplayControl:
    """Create relevant DisplayControl"""
    types = {
        "alert": Alert,
        "text": TextLine,
    }
    subtype = jsn.get("subType", "").lower()
    type_ = types.get(subtype, DisplayControl)
    return type_(jsn, rules)
