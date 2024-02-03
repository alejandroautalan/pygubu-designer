<%inherit file="base.py.mako"/>

<%block name="imports" filter="trim">
${parent.imports()}
from ${module_name}ui import ${class_name}UI
</%block>

<%block name="class_definition" filter="trim">
#
# Manual user code
#

class ${class_name}(${class_name}UI):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
</%block>

<%block name="main">
if __name__ == "__main__":
    root = tk.Tk()
    widget = ${class_name}(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
</%block>
