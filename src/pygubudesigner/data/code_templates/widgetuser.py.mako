<%inherit file="base.py.mako"/>

<%block name="imports" filter="trim">
import tkinter as tk
import tkinter.ttk as ttk
import ${module_name}ui as baseui
</%block>

<%block name="class_definition" filter="trim">
%if with_i18n_support:
# i18n - Setup yout translator function
# baseui.i18n_translator = mytranslator

%endif
#
# Manual user code
#

class ${class_name}(baseui.${class_name}UI):
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
