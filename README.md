
[Leer en Español](LEEME.md)

Welcome to Pygubu!
============================================

`Pygubu` is a [RAD tool](https://en.wikipedia.org/wiki/Rapid_application_development) to enable _quick_ and _easy development of user interfaces_ for the Python's `tkinter` module.

The user interfaces designed are saved as [XML](https://en.wikipedia.org/wiki/XML) files, and, by using the _pygubu builder_, these can be loaded by applications dynamically as needed.

Pygubu is inspired by [Glade](https://glade.gnome.org).

Installation
============

The latest version of pygubu requires Python >= 3.6

You can install pygubu-designer using:

### pip

```
pip install pygubu-designer
```
### Arch Linux ([AUR](https://aur.archlinux.org/packages/pygubu-designer))
```
yay pygubu-designer
```

Screenshot
==========

<img src="pygubu-designer.png" alt="pygubu-desinger.png">


Usage
=====

Type on the terminal one of the following commands depending on your system.

### Unix-like systems

```
pygubu-designer
```

### Windows

```
C:\Python3\Scripts\pygubu-designer.exe
```

Where `C:\Python3` is the path to **your** Python installation directory.

Now, you can start creating your tkinter application using the widgets that you
find in the top panel called `Widget Palette`.

After you finished creating your _UI definition_, save it to a `.ui` file by 
going to the top menu `File > Save`.

The following is a UI definition example called 
[helloworld.ui](examples/helloworld/helloworld.ui) created using pygubu:


```xml
<?xml version='1.0' encoding='utf-8'?>
<interface version="1.2">
  <object class="tk.Toplevel" id="mainwindow">
    <property name="height">200</property>
    <property name="resizable">both</property>
    <property name="title" translatable="yes">Hello World App</property>
    <property name="width">200</property>
    <child>
      <object class="ttk.Frame" id="mainframe">
        <property name="height">200</property>
        <property name="padding">20</property>
        <property name="width">200</property>
        <layout manager="pack">
          <property name="expand">true</property>
          <property name="side">top</property>
        </layout>
        <child>
          <object class="ttk.Label" id="label1">
            <property name="anchor">center</property>
            <property name="font">Helvetica 26</property>
            <property name="foreground">#0000b8</property>
            <property name="text" translatable="yes">Hello World !</property>
            <layout manager="pack">
              <property name="side">top</property>
            </layout>
          </object>
        </child>
      </object>
    </child>
  </object>
</interface>
```

Then, you should create your _application script_ as shown below 
([helloworld.py](examples/helloworld/helloworld.py)):

```python
# helloworld.py
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "helloworld.ui"


class HelloworldApp:
    def __init__(self, master=None):
        # 1: Create a builder and setup resources path (if you have images)
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)

        # 2: Load an ui file
        builder.add_from_file(PROJECT_UI)

        # 3: Create the mainwindow
        self.mainwindow = builder.get_object('mainwindow', master)

        # 4: Connect callbacks
        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    app = HelloworldApp()
    app.run()

```

Note that instead of `helloworld.ui` in the following line:

```python
PROJECT_UI = PROJECT_PATH / "helloworld.ui"
```

You should insert the _filename_ (or path) of your just saved UI definition.


Note also that instead of `'mainwindow'` in the following line:

```python
self.mainwindow = builder.get_object('mainwindow', master)
```

You should have the name of your _main widget_ (the parent of all widgets), 
otherwise you will get an error similar to the following:

    Exception: Widget not defined.

See [this](https://github.com/alejandroautalan/pygubu/issues/40) issue for 
more information.


Documentation
=============

Visit the [wiki](https://github.com/alejandroautalan/pygubu-designer/wiki) for 
more documentation.


The following are some good tkinter (and tk) references:

- [TkDocs](http://www.tkdocs.com)
- [Graphical User Interfaces with Tk](https://docs.python.org/3/library/tk.html)
- [Tkinter 8.5 reference: a GUI for Python](https://tkdocs.com/shipman)
- [An Introduction to Tkinter](http://effbot.org/tkinterbook) [(archive)](http://web.archive.org/web/20200504141939/http://www.effbot.org/tkinterbook)
- [Tcl/Tk 8.5 Manual](http://www.tcl.tk/man/tcl8.5/)


You can also see the [examples](examples) directory or watch [this introductory video tutorial](http://youtu.be/wuzV9P8geDg).


History
=======

See the list of changes [here](HISTORY.md).
