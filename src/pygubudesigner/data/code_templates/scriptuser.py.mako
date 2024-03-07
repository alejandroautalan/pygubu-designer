<%inherit file="base.py.mako"/>

<%block name="class_definition" filter="trim">
class ${class_name}(${class_name}UI):
%if with_i18n_support:
    def __init__(self, master=None, translator=None):
        super().__init__(master, translator)
%else:
    def __init__(self, master=None):
        super().__init__(master)
%endif

${methods}\

${callbacks}\
</%block>
