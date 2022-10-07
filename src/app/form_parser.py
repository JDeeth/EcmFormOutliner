"""
FormParser

Converts JSON from Form Designer into a flattened outline
"""

import json
from typing import Dict, List

import models.form_elements as Form


class FormParser:
    """Converts JSON from Form Designer into a flattened outline"""

    def __init__(self, form_json: Dict):
        """Parse form design from JSON"""
        self._json = form_json
        self._rules = self._parse_rule(form_json)
        self._pages = self._parse_pages(form_json)

    def _parse_rule(self, form_json: Dict) -> List[Form.Rule]:
        rules = []
        for rule in form_json["rules"]:
            rules.append(
                Form.Rule(
                    name=rule["name"],
                    local_id=rule["definitionId"],
                    description=rule["description"],
                )
            )
            return rules

    def _parse_pages(self, form_json: Dict) -> List[Form.Page]:
        pages = []
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

    def _parse_sections(self, page_json: Dict) -> List[Form.Section]:
        sections = []
        for section in page_json["sections"]:
            sections.append(
                Form.Section(
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

    def _parse_subsections(self, section_json: Dict) -> List[Form.Subsection]:
        """Resolves section into tables, repeating groups, and plain runs of controls"""

        # gather controls from each row
        subsections = {}
        for row in section_json["rows"]:
            row_num = row["number"]
            subsections[row_num] = subsections.pop(row_num - 1, [])
            for column in row["columns"]:
                subsections[row_num].extend(column["controls"])

        # convert lists of controls into PlainRun objects for easier parsing later
        for row_num, controls in subsections.items():
            subsections[row_num] = Form.PlainRun(row_number=row_num, controls=controls)

        # gather groups and tables
        for group in section_json["groups"]:
            row_num = group["number"]
            subsections[row_num] = self._parse_group(group)

        # sort by row number (sequence in form)
        return [subsection for _, subsection in sorted(subsections.items())]

    def _parse_group(self, group_json):
        """placeholder"""
        return Form.RepeatableGroup(row_number=group_json["number"], controls=[])

    @classmethod
    def load(cls, filename: str):
        """Load form JSON from a file"""
        with open(filename, "r", encoding="utf-8") as file:
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
