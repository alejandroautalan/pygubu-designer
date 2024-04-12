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
class ${class_name}(baseui.${class_name}UI):
    def __init__(self, master=None):
        super().__init__(master)

${methods}\

${callbacks}\
</%block>
