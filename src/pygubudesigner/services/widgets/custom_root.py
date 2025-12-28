"""A custom tkinter.Tk class.

If ttkbootstrap is loaded, it will use Window as the base class
for the CustomRoot class.
"""

import sys
import tkinter as tk


BaseRoot = tk.Tk


if "ttkbootstrap" in sys.modules:
    # do ttkbootstrap stuff
    from ttkbootstrap import Window

    class ttkbRoot(Window):
        def __init__(
            self,
            screenName=None,
            baseName=None,
            className="Tk",
            useTk=True,
            sync=False,
            use=None,
        ):
            kw = dict(
                screenName=screenName,
                baseName=baseName,
                className=className,
                useTk=useTk,
                sync=sync,
                use=use,
            )
            super().__init__(**kw)

    BaseRoot = ttkbRoot


class CustomRoot(BaseRoot):
    pass
