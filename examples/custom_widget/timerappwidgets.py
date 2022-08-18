from pygubu.api.v1 import BuilderObject, register_widget
from timewidget import TimeWidget


class TimeWidgetBuilder(BuilderObject):
    class_ = TimeWidget


register_widget(
    "timerappwidgets.timewidget",
    TimeWidgetBuilder,
    "TimeWidget",
    ("ttk", "Timer App Widgets"),
)
