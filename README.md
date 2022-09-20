# ECM Form Outliner

---

This is (/will become) an app for parsing OLM ECLIPSE Case Management form
designs into a simplified outline, presented in a Word document.

For example, an outline like this:

| Question                             | Type                    |
| ------------------------------------ | ----------------------- |
| __Date of order *__                  | Date                    |
| __Sandwich type__                    | Ploughman / BLT / Other |
| _(if Other)_ __Other sandwich type__ | Free text               |

represents a section of a form where the user can record a date and pick one
of three options. If the selection is "Other" then a free text box is shown
where the user can record the details.

## Status

Non-functional. At this point all that exists is the package framework.

## Installation

On a PC with Python installed:

```bash
pip install ecm_form_outliner
```

Then to launch:

```bash
ecm_form_outliner
```

## Development

```bash
git clone https://github.com/JDeeth/EcmFormOutliner
cd EcmFormOutliner
python3 -m venv venv
. venv/bin/activate
python3 -m pip install .[dev]
```

To run tests:

```bash
python3 -m pytest .
```