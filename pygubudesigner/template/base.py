<%block name="imports" filter="trim">
import os
import tkinter as tk
import tkinter.ttk as ttk
import pygubu
</%block>

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_UI = os.path.join(PROJECT_PATH, "${project_name}")

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