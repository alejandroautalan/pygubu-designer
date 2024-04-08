<%inherit file="base.py.mako"/>

<%block name="imports" filter="trim">
${parent.imports()}
</%block>

<%block name="class_definition" filter="trim">
%if with_i18n_support:
# Begin i18n - Setup translator in derived class file
def i18n_noop(value): return value
i18n_translator = i18n_noop
# End i18n

%endif
#
# Base class definition
#
class ${class_name}(${widget_base_class}):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        %if with_i18n_support:
        _ = i18n_translator  # i18n string marker.
        %endif
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
