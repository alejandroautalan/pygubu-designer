<%inherit file="base.py.mako"/>
<%block name="imports" filter="trim">
${import_lines}
</%block>

<%block name="class_definition" filter="trim">
class ${class_name}(${widget_base_class}):
    def __init__(self, master=None, **kw):
        super(${class_name}, self).__init__(master, **kw)
${widget_code}
${callbacks}
</%block>

<%block name="main">
if __name__ == '__main__':
    root = tk.Tk()
    widget = ${class_name}(root)
    widget.pack(expand=True, fill='both')
    root.mainloop()
</%block>
