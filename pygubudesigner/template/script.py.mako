<%inherit file="base.py.mako"/>
<%block name="class_definition" filter="trim">
class ${class_name}:
    def __init__(self, master=None):
        # build ui
${widget_code}
        # Main widget
        self.mainwindow = self.${main_widget}
    
${callbacks}
    def run(self):
        self.mainwindow.mainloop()
</%block>
