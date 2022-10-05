"""
FormParser

Converts JSON from Form Designer into a flattened outline
"""

import json

from models import Form
from models.form.section import Section


class FormParser:
    """Converts JSON from Form Designer into a flattened outline"""

    def __init__(self, form_json: str):
        """Parse form design from JSON"""
        self._json = form_json
        self._rules = self._parse_rule(form_json)
        self._pages = self._parse_pages(form_json)

    def _parse_rule(self, form_json):
        rules = list()
        for rule in form_json["rules"]:
            rules.append(
                Form.Rule(
                    name=rule["name"],
                    local_id=rule["definitionId"],
                    description=rule["description"],
                )
            )
            return rules

    def _parse_pages(self, form_json):
        pages = list()
        for page in form_json["pages"]:
            pages.append(
                Form.Page(
                    name=page["name"],
                    title=page["title"],
                    number=page["number"],
                    local_id=page["localId"],
                    visibility_rule_name=self._identify_rule(page["visibilityRuleId"]),
                    sections=self._parse_sections(page),
                )
            )
        return pages

    def _parse_sections(self, page_json):
        sections = list()
        for section in page_json["sections"]:
            sections.append(
                Section(
                    name=section["name"],
                    title=section["title"],
                    number=section["number"],
                    local_id=section["localId"],
                    visibility_rule_name=self._identify_rule(
                        section["visibilityRuleId"]
                    ),
                    subsections=self._parse_subsections(section),
                )
            )
        return sections

    def _parse_subsections(self, section_json):
        """Resolves section into tables, repeating groups, and plain runs of controls"""
        controls = list()
        for row in section_json["rows"]:
            for column in row["columns"]:
                controls.extend(column["controls"])
        output = list()
        if controls:
            output.extend([controls])
        output.extend([self._parse_group(group) for group in section_json["groups"]])
        return output

    def _parse_group(self, group_json):
        """placeholder"""
        number = group_json["number"]
        return f"group{number}"

    @classmethod
    def load(cls, filename: str):
        """Load form JSON from a file"""
        with open(filename, "r") as file:
            return cls(json.load(file))

    @property
    def json(self):
        """Returns the original JSON"""
        return self._json

    @property
    def name(self):
        """The form's name"""
        return self._json["name"]

    @property
    def rules(self):
        """The form's rules"""
        return self._rules

    @property
    def pages(self):
        """The form's pages"""
        return self._pages

    def _identify_rule(self, rule_id):
        """Look up name of page/section/collection/field visibility rule"""
        if not rule_id:
            # no visibility rule applies
            return ""

        for rule in self._rules:
            if rule.local_id == rule_id:
                # form visibility rule identified
                return rule.name

        # otherwise the form is using an external rule - this is rare, however
        return f"(external rule {rule_id[:8]})"
