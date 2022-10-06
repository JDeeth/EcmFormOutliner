"""Tests parsing function end to end"""
from json import JSONDecodeError
import pytest

from app.form_parser import FormParser
from models import Form
from models.form.subsection import PlainRun, RepeatableGroup

# pylint: disable=invalid-name,missing-function-docstring


def should_throw_filenotfound_if_infile_missing():
    filename = "tests/non-existant file.json"

    with pytest.raises(FileNotFoundError):
        FormParser.load(filename)


def should_throw_jsondecodeerror_if_infile_not_json():
    filename = f"tests/{__name__}.py"

    with pytest.raises(JSONDecodeError):
        FormParser.load(filename)


@pytest.fixture(name="lunch_form")
def fixture_lunch_form():
    filename = "tests/Lunch planning_1.json"
    return FormParser.load(filename)


def should_parse_form_design_json(lunch_form: FormParser):
    assert lunch_form.json != {}
    assert lunch_form.name == "Lunch planning"


def should_extract_rules_from_form_design(lunch_form: FormParser):
    rule_venue_other = Form.Rule(
        name='venue is "Other"',
        description="",
        local_id="a7b20d23-8a75-46d8-a84a-52cc28f17685",
    )
    assert rule_venue_other in lunch_form.rules


def should_extract_pages_from_form_design(lunch_form: FormParser):
    expected_page_titles = ["Venue", "Invitees", "Follow-up"]
    page_titles = [page.title for page in lunch_form.pages]

    assert page_titles == expected_page_titles

    page1 = lunch_form.pages[0]

    assert page1.title == "Venue"
    assert page1.name == "venue_page"
    assert page1.number == 0
    assert page1.local_id == "Pc69a62ec-4581-4c60-9ad4-a736830938bb"
    assert page1.visibility_rule_name == ""
    assert len(page1.sections) == 3


def should_find_one_subsection_with_five_controls_in_p1s2():
    lunch_form = FormParser.load("tests/Lunch planning_1.json")
    venue_details_section = lunch_form.pages[0].sections[1]

    assert venue_details_section.title == "Venue details"
    assert len(venue_details_section.subsections) == 1
    first_subsection = venue_details_section.subsections[0]
    assert len(first_subsection.controls) == 5


def should_find_run_group_run_in_p3s2():
    lunch_form = FormParser.load("tests/Lunch planning_1.json")
    p3s2 = lunch_form.pages[2].sections[1]

    for a, b in zip(p3s2.subsections, [PlainRun, RepeatableGroup, PlainRun]):
        assert isinstance(a, b)
