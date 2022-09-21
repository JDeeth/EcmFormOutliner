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
