import json

from app.control_parsers import DisplayControl, parse_control

rules = [
    {
        "definitionId": "a7b20d23-8a75-46d8-a84a-52cc28f17685",
        "name": 'venue is "Other"',
    },
    {
        "definitionId": "ad907413-ef2c-47d5-8a64-5668f5f431ca",
        "name": 'facilities include "Public transport"',
    },
    {
        "definitionId": "273504d2-0bd3-4b27-9d03-b734db073213",
        "name": 'next steps are "Schedule next lunch"',
    },
]


def should_parse_alert_control():
    json_str = """
    {
        "help": null,
        "readOnly": true,
        "localId": "C10720115-08f7-45b8-90ac-8245688bb86e",
        "alertText": "About this form",
        "visibilityRuleId": null,
        "number": 0,
        "hidden": false,
        "name": "about_text",
        "inputSize": 12,
        "alertType": "INFORMATION",
        "_type": "NewAlertControl",
        "subType": "ALERT",
        "alertBody": "This is a dummy form design."
    }
    """
    jsn = json.loads(json_str)

    item: DisplayControl = parse_control(jsn, rules)

    assert item.label == "About this form\nThis is a dummy form design."
    assert item.type == "Guidance text"
    assert item.details == ""
    assert item.visibility_rule == ""
    assert item.mandatory is None


def should_parse_conditional_text_control():
    json_str = """
    {
        "help": null,
        "readOnly": false,
        "prependLabel": null,
        "localId": "C2c1f6e2e-c550-4f68-a6fb-3adb08c81434",
        "visibilityRuleId": "a7b20d23-8a75-46d8-a84a-52cc28f17685",
        "number": 1,
        "hidden": false,
        "name": "other_venue",
        "inputSize": 12,
        "defaultValue": null,
        "label": {
            "value": "Other venue",
            "width": 12,
            "alignment": "LEFT"
        },
        "groupScope": false,
        "_type": "NewTextControl",
        "validation": {
            "dataType": "TEXT",
            "pattern": null,
            "minLength": null,
            "maxLength": null,
            "minValue": null,
            "maxValue": null,
            "mandatory": "NOT_MANDATORY"
        },
        "numberOfRows": null,
        "subType": "TEXT",
        "appendLabel": null
    }
    """

    jsn = json.loads(json_str)

    item: DisplayControl = parse_control(jsn, rules)

    assert item.type == "Free text"
    assert item.label == "Other venue"
    assert item.details == ""
    assert item.visibility_rule == 'venue is "Other"'
    assert item.mandatory is False
