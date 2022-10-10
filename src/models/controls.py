from dataclasses import dataclass
from enum import Enum, auto
from typing import ClassVar, List, Optional


@dataclass
class BaseControl:
    """Attributes shared by all form controls"""

    class Type(Enum):
        """Form control types, not necessarily 1:1 with form design subType"""

        # inputs
        DATE = auto()
        SIGNATURE = auto()
        FREEHAND = auto()
        # IDENTITY = auto() # Not included - no subType, unclear function
        IMAGE_UPLOAD = auto()

        # inputs - text
        TEXT = auto()
        RICH_TEXT = auto()
        HIDDEN = auto()
        NUMBER = auto()

        # select
        LIST_BOX = auto()
        CHECKBOXES = auto()
        RADIO_BUTTONS = auto()

        # static
        ALERT = auto()

        # dynamic

        # calculations

        # fallback
        NOT_SPECIFIED = auto()

    type: ClassVar[Type]
    subtypes: ClassVar[List[str]]

    local_id: str  #  UUID prefixed with "C"
    name: str  #  designer_specified internal name
    help_text: str = ""
    read_only: Optional[bool] = None
    hidden: Optional[bool] = None
    visibility_rule_guid: Optional[str] = None


class InputControl(BaseControl):
    hint_text: str = ""  #  grey placeholder text, not a default answer
    default_answer: str = ""  #  also sometimes defaultValue
    label: str = ""
    label_hidden: bool = False
    group_scope: bool = False
    mandatory_on_save: bool = False


class Date(InputControl):
    """Date input - "Historic dates only" is PAST_DATE subtype"""

    type = BaseControl.Type.DATE
    subtypes = ["DATE", "PAST_DATE"]


class Signature(InputControl):
    """Freehand signature"""

    type = BaseControl.Type.SIGNATURE
    subtypes = ["drawingProperties/subType:SIGNATURE"]


class Freehand(InputControl):
    """Freehand drawing over optional background image"""

    type = BaseControl.Type.FREEHAND
    subtypes = ["drawingProperties/subType:FREEHAND"]
    image_uri: str = ""
    image_alt_text: str = ""


class ImageUpload(InputControl):
    type = BaseControl.Type.IMAGE_UPLOAD
    subtypes = ["mediaProperties/subType:IMAGE"]


# -------------------------------------------------------------------------------


class TextControl(InputControl):
    prepend_label: str = ""
    append_label: str = ""
    validation_pattern: str = ""
    number_of_rows: Optional[int] = None


class Text(TextControl):
    type = BaseControl.Type.TEXT
    number_of_rows = 1


class RichText(TextControl):
    type = BaseControl.Type.RICH_TEXT


class Hidden(TextControl):
    subtypes = ["HIDDEN"]
    type = BaseControl.Type.HIDDEN


class Number(TextControl):
    subtypes = ["validation/dataType:HIDDEN"]
    type = BaseControl.Type.HIDDEN


# -------------------------------------------------------------------------------


class SelectionControl(InputControl):
    @dataclass
    class Choice:
        label: str
        value: str
        selected_by_default: bool = False

    choices: List[Choice]
    minimum_selections: int = 0
    maximum_selections: Optional[int] = None


class ListBox(SelectionControl):
    type: ClassVar[BaseControl.Type] = BaseControl.Type.LIST_BOX
    maximum_selections = 1


class Checkboxes(SelectionControl):
    type: ClassVar[BaseControl.Type] = BaseControl.Type.CHECKBOXES


class RadioButtons(SelectionControl):
    type: ClassVar[BaseControl.Type] = BaseControl.Type.RADIO_BUTTONS
    maximum_selections = 1
    is_horizontal: bool = True


# -------------------------------------------------------------------------------


class Alert(BaseControl):
    """Static text in a coloured box"""

    type = BaseControl.Type.ALERT
    subtypes = ["ALERT"]

    class AlertType(Enum):
        INFORMATION = "INFORMATION"

        NOT_SPECIFIED = "NOT_SPECIFIED"

    alert_type: AlertType = AlertType.NOT_SPECIFIED
    alert_title: str = ""  #  alertText
    alert_body: str = ""  #  body of alert, in markdown
