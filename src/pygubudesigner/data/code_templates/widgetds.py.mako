<%inherit file="base.py.mako"/>

<%block name="imports" filter="trim">
${parent.imports()}
</%block>

<%block name="class_definition" filter="trim">
class ${class_name}(${widget_base_class}):
    """Your widget direct subclass.

    Only simple properties will be configured.
    No commands, no bindings.
    """
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

${widget_code}

${callbacks}\
</%block>

<%block name="main">
if __name__ == "__main__":
    root = tk.Tk()
    widget = ${class_name}(root)
% if not main_widget_is_toplevel:
    widget.pack(expand=True, fill="both")
% endif
    root.mainloop()
</%block>
