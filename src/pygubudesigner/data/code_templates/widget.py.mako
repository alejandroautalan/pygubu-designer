<%inherit file="base.py.mako"/>

<%block name="class_definition" filter="trim">
class ${class_name}(${widget_base_class}):
    def __init__(self, master=None, **kw):
        super(${class_name}, self).__init__(master, **kw)
${widget_code}
    %if has_ttk_styles:
        self.setup_ttk_styles()

    def setup_ttk_styles(self):
        # ttk styles configuration
        self.style = style = ttk.Style()
        optiondb = style.master
${ttk_styles}
    %endif
${callbacks}\
</%block>

<%block name="main">
if __name__ == "__main__":
    root = tk.Tk()
    widget = ${class_name}(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
</%block>
