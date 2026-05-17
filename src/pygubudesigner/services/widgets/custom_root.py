"""A custom tkinter.Tk class.

If ttkbootstrap is loaded, it will use Window as the base class
for the CustomRoot class.
"""

import sys
import tkinter as tk


BaseRoot = tk.Tk

has_ttkbootstrap_window = False
if "ttkbootstrap" in sys.modules:
    # ttkbootstrap is a namespace pkg, so add aditional check:
    try:
        from ttkbootstrap import Window

        has_ttkbootstrap_window = True
    except ImportError:
        pass

has_bootstack_window = False
if "bootstack" in sys.modules:
    from bootstack import Window  # noqa: F811

    has_bootstack_window = True

if has_ttkbootstrap_window or has_bootstack_window:
    # do ttkbootstrap stuff

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
