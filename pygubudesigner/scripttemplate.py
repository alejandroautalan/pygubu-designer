TPL_APPINIT_WITH_TKROOT = \
'''if __name__ == '__main__':
    import tkinter as tk
    root = tk.Tk()
    app = {class_name}(root)
    app.run()
'''

TPL_APPINIT = \
'''if __name__ == '__main__':
    app = {class_name}()
    app.run()
'''

TPL_APPLICATION = \
"""import os
import pygubu


PROJECT_PATH = os.path.dirname(__file__)
PROJECT_UI = os.path.join(PROJECT_PATH, "{project_name}")


class {class_name}:
    def __init__(self):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('{main_widget}')
        builder.connect_callbacks(self)
    
{callbacks}
    def run(self):
        self.mainwindow.mainloop()

{app_init}"""

TPL_CODESCRIPT = \
"""{import_lines}


class {class_name}:
    def __init__(self, master=None):
        # build ui
{widget_code}
        # Main widget
        self.mainwindow = self.{main_widget}

{callbacks}
    def run(self):
        self.mainwindow.mainloop()

{app_init}"""

TPL_WIDGET = \
"""{import_lines}


class {class_name}({widget_base_class}):
    def __init__(self, master=None, **kw):
        {widget_base_class}.__init__(self, master, **kw)
{widget_code}
{callbacks}

if __name__ == '__main__':
    root = tk.Tk()
    widget = {class_name}(root)
    widget.pack(expand=True, fill='both')
    root.mainloop()
"""
