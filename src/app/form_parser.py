"""
FormParser

Converts JSON from Form Designer into a flattened outline
"""

import json

from models import Form


class FormParser:
    """ Converts JSON from Form Designer into a flattened outline """

    def __init__(self, form_json: str):
        """ Parse form design from JSON """
        self._json = form_json

        self._rules = list()
        for rule in form_json["rules"]:
            self._rules.append(
                Form.Rule(
                    name=rule["name"],
                    local_id=rule["definitionId"],
                    description=rule["description"],
                )
            )

        self._pages = list()
        for page in form_json["pages"]:
            self._pages.append(
                Form.Page(
                    name=page["name"],
                    title=page["title"],
                    number=page["number"],
                    local_id=page["localId"],
                    visibility_rule_name=self._identify_rule(
                        page["visibilityRuleId"]
                    ),
                    sections=list(),
                )
            )

    @classmethod
    def load(cls, filename: str):
        """ Load form JSON from a file """
        with open(filename, "r") as file:
            return cls(json.load(file))

    @property
    def json(self):
        """ Returns the original JSON """
        return self._json

    @property
    def name(self):
        """ The form's name """
        return self._json["name"]

    @property
    def rules(self):
        """ The form's rules """
        return self._rules

    @property
    def pages(self):
        """ The form's pages """
        return self._pages


    def _identify_rule(self, rule_id):
        """ Look up name of page/section/collection/field visibility rule """
        if not rule_id:
            # no visibility rule applies
            return ""

        for rule in self._rules:
            if rule.local_id == rule_id:
                # form visibility rule identified
                return rule.name

        # otherwise the form is using an external rule - this is rare, however
        return f"(external rule {rule_id[:8]})"
