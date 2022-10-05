"""Testing internal components of FormParser"""
import pytest
from app.form_parser import FormParser

# pylint: disable=missing-class-docstring,missing-function-docstring,protected-access

class TestParseSequences:
    @pytest.fixture
    def parser(self):
        return FormParser(
            {
                "pages": [],
                "rules": [],
            }
        )

    @pytest.fixture
    def parse_sequences(self, parser: FormParser):
        return parser._parse_subsections

    @pytest.fixture
    def parse_group(self, parser: FormParser):
        return parser._parse_group

    def should_give_empty_list_for_empty_section(self, parse_sequences):
        section_json = {
            "rows": [],
            "groups": [],
        }
        assert parse_sequences(section_json) == []

    def should_return_list_with_list_of_one_control_if_section_has_one_control(
        self, parse_sequences
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
        assert parse_sequences(section_json) == [["blahaj"]]

    def should_return_list_with_list_of_two_controls_if_section_has_two_controls(
        self, parse_sequences
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
        assert parse_sequences(section_json) == [["blahaj", "kallax"]]

    def should_return_group_or_table_as_sole_content(
        self, parse_sequences, parse_group
    ):
        group_1 = {"number": 0, "name": "blahaj"}
        section_json = {
            "rows": [],
            "groups": [group_1],
        }

        assert parse_sequences(section_json) == [parse_group(group_1)]
