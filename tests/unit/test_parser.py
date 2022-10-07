"""Testing internal components of FormParser"""
import pytest
from app.form_parser import FormParser
from models.form_elements import PlainRun

# pylint: disable=missing-class-docstring,missing-function-docstring,protected-access


class TestParseSequences:
    @pytest.fixture(name="parser")
    def fixture_parser(self):
        return FormParser(
            {
                "name": "blank",
                "formDefinitionId": "",
                "pages": [],
                "rules": [],
            }
        )

    @pytest.fixture(name="parse_subsections")
    def fixture_parse_subsections(self, parser: FormParser):
        return parser._parse_subsections

    @pytest.fixture(name="parse_group")
    def fixture_parse_group(self, parser: FormParser):
        return parser._parse_group

    def should_give_empty_list_for_empty_section(self, parse_subsections):
        section_json = {
            "rows": [],
            "groups": [],
        }
        assert parse_subsections(section_json) == []

    def should_return_list_with_one_plainrun_if_section_has_one_control(
        self, parse_subsections
    ):
        section_json = {
            "rows": [
                {
                    "number": 0,
                    "columns": [
                        {"controls": ["blahaj"]},
                    ],
                },
            ],
            "groups": [],
        }
        plain_run = PlainRun(row_number=0, controls=["blahaj"])
        assert parse_subsections(section_json) == [plain_run]

    def should_return_list_with_one_plainrun_if_section_has_two_controls(
        self, parse_subsections
    ):
        section_json = {
            "rows": [
                {
                    "number": 0,
                    "columns": [
                        {"controls": ["blahaj", "kallax"]},
                    ],
                },
            ],
            "groups": [],
        }
        plain_run = PlainRun(row_number=0, controls=["blahaj", "kallax"])
        assert parse_subsections(section_json) == [plain_run]

    def should_group_controls_in_adjoining_rows(self, parse_subsections):
        section_json = {
            "rows": [
                {
                    "number": 0,
                    "columns": [
                        {"controls": ["blahaj", "kallax"]},
                        {"controls": ["billy"]},
                    ],
                },
                {
                    "number": 1,
                    "columns": [
                        {"controls": ["poang"]},
                    ],
                },
                {
                    "number": 9,
                    "columns": [
                        {"controls": ["lack"]},
                    ],
                },
            ],
            "groups": [],
        }
        plain_run_1 = PlainRun(
            row_number=0, controls=["blahaj", "kallax", "billy", "poang"]
        )
        plain_run_2 = PlainRun(row_number=9, controls=["lack"])
        assert parse_subsections(section_json) == [plain_run_1, plain_run_2]

    def should_return_group_or_table_as_sole_content(
        self, parse_subsections, parse_group
    ):
        group_1 = {"number": 0, "name": "blahaj"}
        section_json = {
            "rows": [],
            "groups": [group_1],
        }

        assert parse_subsections(section_json) == [parse_group(group_1)]

    def should_return_mixed_subsections_in_right_order(
        self, parse_subsections, parse_group
    ):
        # Representation of section with group/table followed by regular controls
        group_0 = {"number": 0, "name": "poång"}
        section_json = {
            "rows": [
                {
                    "number": 1,
                    "columns": [
                        {"controls": ["blahaj", "kallax"]},
                    ],
                },
            ],
            "groups": [group_0],
        }
        plain_run = PlainRun(row_number=1, controls=["blahaj", "kallax"])
        assert parse_subsections(section_json) == [
            parse_group(group_0),
            plain_run,
        ]
