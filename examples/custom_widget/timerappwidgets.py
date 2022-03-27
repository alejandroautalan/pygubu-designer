from pygubu import BuilderObject, register_widget
from timewidget import TimeWidget


class TimeWidgetBuilder(BuilderObject):
    class_ = TimeWidget


register_widget('customappwidgets.timewidget', TimeWidgetBuilder,
                'TimeWidget', ('ttk', 'customapp'))

