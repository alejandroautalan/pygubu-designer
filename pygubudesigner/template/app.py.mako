<%inherit file="base.py.mako"/>
<%block name="class_definition" filter="trim">
class ${class_name}:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('${main_widget}', master)
        %if tkvariables:
        
          %for var in tkvariables:
        self.${var} = None
          %endfor
        builder.import_variables(self, ${tkvariables})
        
        %endif
        builder.connect_callbacks(self)
    
${callbacks}
    def run(self):
        self.mainwindow.mainloop()
</%block>
