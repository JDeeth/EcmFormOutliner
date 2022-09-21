import pytest
from json import JSONDecodeError

from app.form_parser import FormParser
from models import Form


def test_FormParser_loadsnonexistant_throws():
    filename = "tests/non-existant file.json"

    with pytest.raises(FileNotFoundError):
        FormParser.load(filename)


def test_FormParser_loadsinvalidjson_throws():
    filename = f"tests/{__name__}.py"

    with pytest.raises(JSONDecodeError):
        FormParser.load(filename)


def test_FormParser_loadsvalidjson_successfully():
    filename = "tests/Lunch planning_1.json"

    form = FormParser.load(filename)

    assert form.json != {}
    assert form.name == "Lunch planning"


def test_FormParser_loadsvalidjson_parsesrules():
    filename = "tests/Lunch planning_1.json"
    rule_venue_other = Form.Rule(
        name='venue is "Other"',
        description="",
        local_id="a7b20d23-8a75-46d8-a84a-52cc28f17685",
    )

    lunch_form = FormParser.load(filename)

    assert rule_venue_other in lunch_form.rules


def test_FormParser_loadsvalidjson_parsespages():
    filename = "tests/Lunch planning_1.json"
    expected_page_titles = ["Venue", "Invitees", "Follow-up"]
    lunch_form = FormParser.load(filename)

    page_titles = [page.title for page in lunch_form.pages]

    assert page_titles == expected_page_titles

    page1 = lunch_form.pages[0]

    assert page1.title == "Venue"
    assert page1.name == "venue_page"
    assert page1.number == 0
    assert page1.local_id == "Pc69a62ec-4581-4c60-9ad4-a736830938bb"
    assert page1.visibility_rule_name == ""
