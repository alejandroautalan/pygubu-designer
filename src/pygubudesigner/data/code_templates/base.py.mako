#!/usr/bin/python3
<%block name="imports" filter="trim">
${import_lines}
</%block>
<%block name="project_paths"/>
<%block name="class_definition"/>

<%block name="main" filter="trim">
if __name__ == "__main__":
% if main_widget_is_toplevel:
    app = ${class_name}()
    app.run()
% else:
    root = tk.Tk()
    app = ${class_name}(root)
    app.run()
% endif
</%block>
