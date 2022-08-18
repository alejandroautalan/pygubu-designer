# file: tkcalendarwidgets.py

from tkcalendar import DateEntry
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)


class DateEntryBuilder(BuilderObject):
    class_ = DateEntry

    OPTIONS_STANDARD = (
        "cursor",
        "font",
        "borderwidth",
        "state",
        "foreground",
        "background",
        "selectbackground",
        "selectforeground",
    )
    OPTIONS_SPECIFIC = ("disabledbackground", "disabledforeground")
    OPTIONS_CUSTOM = (
        "year",
        "month",
        "day",
        "date_pattern",
        "headersbackground",
        "headersforeground",
    )
    ro_properties = ("year", "month", "day")
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    virtual_events = ("<<DateEntrySelected>>",)

    def _process_property_value(self, pname, value):
        if pname in ("year", "month", "day"):
            return int(value)
        return super()._process_property_value(pname, value)


# Set a builder unique id
_builder_id = "tkcalendarwidgets.dateentry"

# Register the builder
register_widget(
    _builder_id,
    DateEntryBuilder,
    "DateEntry",
    ("ttk", "My Tkcalendar widgets"),
)

# Register custom property
# Params:
# Builder id
# Property name
# Editor name and options. Using a choice here to input only allowed values.
# Tooltip help
register_custom_property(
    _builder_id,
    "date_pattern",
    "choice",
    values=("", "MM/dd/yy", "MM/dd/yyyy", "dd/MM/yyyy"),
    state="readonly",
    help="Date pattern",
)
register_custom_property(
    _builder_id,
    "year",
    "naturalnumber",
)
register_custom_property(
    _builder_id,
    "month",
    "naturalnumber",
)
register_custom_property(
    _builder_id,
    "day",
    "naturalnumber",
)
register_custom_property(
    _builder_id,
    "headersbackground",
    "colorentry",
)
register_custom_property(
    _builder_id,
    "headersforeground",
    "colorentry",
)
