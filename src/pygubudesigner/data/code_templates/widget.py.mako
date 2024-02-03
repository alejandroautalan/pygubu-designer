<%inherit file="base.py.mako"/>

<%block name="imports" filter="trim">
${parent.imports()}
</%block>

<%block name="class_definition" filter="trim">
#
# Base class definition
#
class ${class_name}(${widget_base_class}):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
${widget_code}

${callbacks}\
</%block>

<%block name="main">
if __name__ == "__main__":
    root = tk.Tk()
    widget = ${class_name}(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
</%block>
