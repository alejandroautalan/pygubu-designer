# file: tkcalendarwidgets.py

from tkcalendar import DateEntry
from pygubu import BuilderObject, register_widget


class DateEntryBuilder(BuilderObject):
    class_ = DateEntry
    
    OPTIONS_STANDARD = ('cursor', 'font', 'borderwidth', 'state',
                        'foreground', 'background', 'selectbackground',
                        'selectforeground')
    OPTIONS_SPECIFIC = ('disabledbackground', 'disabledforeground')
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC


register_widget('tkcalendarwidgets.dateentry', DateEntryBuilder,
                'DateEntry', ('ttk', 'My Tkcalendar widgets')) 
