"""A custom tkinter.Tk class.

If ttkbootstrap is loaded, it will use Window as the base class
for the CustomRoot class.
"""

import sys
import tkinter as tk

BaseRoot = tk.Tk
Window = None  # pylint: disable=invalid-name

if "ttkbootstrap" in sys.modules:
    # ttkbootstrap is a namespace pkg, so add additional check:
    try:
        from ttkbootstrap import Window
    except ImportError:
        Window = None

if Window is None and "bootstack" in sys.modules:
    from bootstack import Window  # noqa: F811 # pylint: disable=import-error

if Window is not None:
    # do ttkbootstrap / bootstack stuff

    class ttkbRoot(Window):  # pylint: disable=too-few-public-methods
        # pylint: disable=invalid-name,too-many-arguments,too-many-positional-arguments
        def __init__(
            self,
            screenName=None,
            baseName=None,
            className="Tk",
            useTk=True,
            sync=False,
            use=None,
        ):
            kw = {
                "screenName": screenName,
                "baseName": baseName,
                "className": className,
                "useTk": useTk,
                "sync": sync,
                "use": use,
            }
            super().__init__(**kw)

    BaseRoot = ttkbRoot


class CustomRoot(BaseRoot):
    pass
