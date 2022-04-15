# file: tkcalendarwidgets.py

from tkcalendar import DateEntry
from pygubu import BuilderObject, register_widget


class DateEntryBuilder(BuilderObject):
    class_ = DateEntry


register_widget('tkcalendarwidgets.dateentry', DateEntryBuilder,
                'DateEntry', ('ttk', 'My Tkcalendar widgets')) 
