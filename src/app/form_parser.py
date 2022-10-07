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

        # must calculate rules first, & have available for page/** parsers
        self._rules = self._parse_rules(form_json["rules"])
        self._form = self._parse_form(form_json, self._rules)

    def _parse_form(self, form_json: Dict, rules: List[Form.Rule]) -> Form.Form:
        pages = self._parse_pages(form_json["pages"])
        return Form.Form(
            name=form_json["name"],
            type_guid=form_json["formDefinitionId"],
            rules=rules,
            pages=pages,
            source_json=form_json,
        )

    def _parse_rules(self, rules_json: Dict) -> List[Form.Rule]:
        rules = []
        for rule in rules_json:
            rules.append(
                Form.Rule(
                    name=rule["name"],
                    local_id=rule["definitionId"],
                    description=rule["description"],
                )
            )
            return rules

    def _parse_pages(self, pages_json: Dict) -> List[Form.Page]:
        pages = []
        for page in pages_json:
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

        # gather controls from adjoining rows into PlainRun subsections
        subsections: Dict[int, Form.Subsection] = {}
        for row in section_json["rows"]:
            row_num = row["number"]
            subsections[row_num] = subsections.pop(
                row_num - 1, Form.PlainRun(row_number=row_num, controls=[])
            )
            for column in row["columns"]:
                subsections[row_num].controls.extend(column["controls"])

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
    def form(self) -> Form.Form:
        """The simplified form"""
        return self._form

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
