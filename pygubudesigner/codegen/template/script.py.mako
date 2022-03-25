<%inherit file="base.py.mako"/>

<%block name="class_definition" filter="trim">
class ${class_name}:
    def __init__(self, master=None):
        # build ui
${widget_code}
        # Main widget
        self.mainwindow = self.${main_widget}
        %if has_ttk_styles:
        
        self.setup_ttk_styles()
        %endif
    
    def run(self):
        self.mainwindow.mainloop()
    %if has_ttk_styles:
    
    def setup_ttk_styles(self):
        # ttk styles configuration
        self.style = style = ttk.Style()
        optiondb = style.master
${ttk_styles}
    %endif

${callbacks}\
</%block>
