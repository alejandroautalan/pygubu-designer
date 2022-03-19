<%block name="imports" filter="trim">
<%block name="pathlib_import" filter="trim">
% if use_pathlib:
import pathlib
% else:
import os
% endif
</%block>
import tkinter as tk
import tkinter.ttk as ttk
import pygubu
</%block>

<%block name="project_paths" filter="trim">
% if use_pathlib:
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "${project_name}"
% else:
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_UI = os.path.join(PROJECT_PATH, "${project_name}")
% endif
</%block>


<%block name="class_definition"/>

<%block name="main">
if __name__ == '__main__':
% if main_widget_is_toplevel:
    app = ${class_name}()
    app.run()
% else:
    root = tk.Tk()
    app = ${class_name}(root)
    app.run()
% endif
</%block>
