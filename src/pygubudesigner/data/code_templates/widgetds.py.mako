<%inherit file="base.py.mako"/>

<%block name="imports" filter="trim">
% if not MODULE_IMPORTS:
# <MODULE_IMPORTS>
${parent.imports()}
# </MODULE_IMPORTS>
% else:
${MODULE_IMPORTS}
% endif
</%block>

<%block name="class_definition" filter="trim">
% if not CLASS_DEFINITION:
# <CLASS_DEFINITION>
class ${class_name}(${widget_base_class}):
    """Your widget direct subclass.

    Only simple properties will be configured.
    No commands, no bindings.
    """
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        # </CLASS_DEFINITION>
% else:
${CLASS_DEFINITION}
% endif
        # widget setup
    ${widget_code}\
% if not CLASS_BODY:
    # <CLASS_BODY>  # </CLASS_BODY>
% else:
${CLASS_BODY}
% endif

${callbacks}\
</%block>

<%block name="main">
% if not MODULE_BODY:
# <MODULE_BODY>
if __name__ == "__main__":
    root = tk.Tk()
    widget = ${class_name}(root)
% if not main_widget_is_toplevel:
    widget.pack(expand=True, fill="both")
% endif
    root.mainloop()
# </MODULE_BODY>
% else:
${MODULE_BODY}
% endif
</%block>
