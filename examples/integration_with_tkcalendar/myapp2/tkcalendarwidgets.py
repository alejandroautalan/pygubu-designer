# file: tkcalendarwidgets.py

from pygubu.api.v1 import BuilderObject, register_widget
from tkcalendar import DateEntry


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
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC


register_widget(
    "tkcalendarwidgets.dateentry",
    DateEntryBuilder,
    "DateEntry",
    ("ttk", "My Tkcalendar widgets"),
)
