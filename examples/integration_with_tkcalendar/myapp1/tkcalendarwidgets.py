# file: tkcalendarwidgets.py

from pygubu.api.v1 import BuilderObject, register_widget
from tkcalendar import DateEntry


class DateEntryBuilder(BuilderObject):
    class_ = DateEntry


register_widget(
    "tkcalendarwidgets.dateentry",
    DateEntryBuilder,
    "DateEntry",
    ("ttk", "My Tkcalendar widgets"),
)
