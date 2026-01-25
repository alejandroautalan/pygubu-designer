
[Leer en Español](Documentation/README/es.md). More translations [here](Documentation/README)

Welcome to Pygubu Designer!
===========================

`Pygubu Designer` is a [RAD tool](https://en.wikipedia.org/wiki/Rapid_application_development) to enable _quick_ and _easy development of user interfaces_ for the Python's `tkinter` module.

The user interfaces designed are saved as [XML](https://en.wikipedia.org/wiki/XML) files, and, by using the _pygubu builder_, these can be loaded by applications dynamically as needed.

Pygubu Designer is inspired by [Glade](https://gitlab.gnome.org/GNOME/glade).

Installation
============

The latest version of pygubu requires Python >= 3.9

You can install pygubu-designer using **pip**:

```
pip install pygubu-designer
```

For other installation methods, please see [this page](https://github.com/alejandroautalan/pygubu-designer/wiki/Installation-&-Related).


Screenshot
==========

<img src="pygubu-designer.png" alt="pygubu-desinger.png">


Usage
=====

Pygubu designer supports two types of workflow. The first and classic method is creating an application that uses the "*.ui" file that defines your user interface.

In the classic mode, pygubu is in charge of creating the widgets and connecting defined bindings. I recommend this mode for apps that have one or a few windows, but you can use it for creating apps of any complexity (Pygubu Designer it self was created with this mode, but now uses the new one). This method uses a class based approach where your code lives in the derived class and the base class is updated by pygubu designer.

The second method is to create an app with a coded version of the *.ui file. Using the same class based approach mentioned above, pygubu designer generates the python code for the base class and you write the app logic in the derived class.

Generating the code for the UI has some benefits:

- The *.ui file is not required at runtime
- Allows you to create pure tkinter apps, if you do not use any pygubu widget (eliminating pygubu dependency).
- Easy creation of custom widgets.

Whichever you choose, you can always modify the user interface using pygubu designer.


Starting Pygubu Designer
------------------------

Type on the terminal one of the following commands depending on your system.

### Unix-like systems

```
pygubu-designer
```

For other platforms see [this page](https://github.com/alejandroautalan/pygubu-designer/wiki/Launch).


Documentation
=============

Visit the [wiki](https://github.com/alejandroautalan/pygubu-designer/wiki) for
more documentation.


The following are some good tkinter (and tk) references:

- [TkDocs](http://www.tkdocs.com)
- [Graphical User Interfaces with Tk](https://docs.python.org/3/library/tk.html)
- [Tkinter 8.5 reference: a GUI for Python](https://tkdocs.com/shipman)
- [An Introduction to Tkinter](http://effbot.org/tkinterbook) [(archive)](http://web.archive.org/web/20200504141939/http://www.effbot.org/tkinterbook)
- [Tcl/Tk 9.0 Manual](https://www.tcl-lang.org/man/tcl9.0/TkCmd/index.html)
- [Tcl/Tk 8.6 Manual](https://www.tcl-lang.org/man/tcl8.6/TkCmd/contents.htm)


You can also see the [examples](examples) directory or watch [this introductory video tutorial](http://youtu.be/wuzV9P8geDg).


History
=======

See the list of changes [here](HISTORY.md).


License
=======

Pygubu Designer: GPL-3.0 license

Pygubu Designer can generate pure python code scripts. For those cases where
a license is required for these scripts, they are licensed under the same
license as the pygubu core: MIT License.
This applies to all standard plugins that come with pygubu core. If you're
using a third-party plugin, check the plugin license.
