from abc import ABC, abstractmethod
from tkinter import ttk
from typing import ClassVar

_STYLE = None

has_sv_ttk = False
has_ttkthemes = False
has_ttkbootstrap = False
has_pygubu_bootstrap = False


class ThemeModule(ABC):
    @abstractmethod
    def theme_names(self) -> list: ...

    @abstractmethod
    def theme_use(self, name): ...

    def can_handle(self, _name) -> bool:
        return False


class SunValleyModule(ThemeModule):
    sv_themes = {"sun-valley-dark": "dark", "sun-valley-light": "light"}

    def __init__(self):
        sv_ttk.get_theme()

    def theme_names(self) -> list:
        return []

    def theme_use(self, name):
        sv_ttk.set_theme(self.sv_themes[name])

    def can_handle(self, name) -> bool:
        return name in self.sv_themes


class TtkthemesModule(ThemeModule):
    def __init__(self):
        self.style = ThemedStyle()
        self.definitions = list(self.style.theme_names())

    def theme_names(self) -> list:
        return self.definitions

    def theme_use(self, name):
        self.style.theme_use(name)

    def can_handle(self, name):
        return name in self.definitions


class TtkbModule(ThemeModule):
    def __init__(self):
        self.style = ttkb.Style()
        theme_list = []
        if hasattr(self.style, "list_themes"):
            theme_list = [td["name"] for td in self.style.list_themes()]
        else:
            theme_list = list(self.style.theme_names())
        self.definitions = theme_list

    def theme_names(self) -> list:
        return self.definitions

    def theme_use(self, name):
        self.style.theme_use(name)

    def can_handle(self, name):
        return name in self.definitions


class PygubuBootstrapModule(ThemeModule):
    def __init__(self):
        self.style = pbs_style.Style()
        self.definitions = list(self.style.theme_names())

    def theme_names(self) -> list:
        return self.definitions

    def theme_use(self, name):
        self.style.theme_use(name)

    def can_handle(self, name):
        return name in self.definitions


class MultipleThemeModuleManager(ttk.Style):
    modules: ClassVar[list] = []
    theme_list: ClassVar[list | None] = None

    def theme_names(self):
        if self.theme_list is None:
            new_list: list[str] = list(super().theme_names())
            for m in self.modules:
                themes = m.theme_names()
                for t in themes:
                    if t not in new_list:
                        new_list.append(t)
            MultipleThemeModuleManager.theme_list = new_list
        return self.theme_list

    def theme_use(self, themename=None):
        if themename is None:
            return super().theme_use()

        theme_set = False
        for m in self.modules:
            if m.can_handle(themename):
                m.theme_use(themename)
                theme_set = True
                break
        if not theme_set:
            return super().theme_use(themename)
        return None


try:
    import ttkbootstrap as ttkb

    # Make shure style management is installed
    import ttkbootstrap.window  # pylint: disable=unused-import

    has_ttkbootstrap = True
except ImportError:
    pass

try:
    import sv_ttk

    has_sv_ttk = True
except ImportError:
    pass
try:
    from ttkthemes.themed_style import ThemedStyle

    has_ttkthemes = True
except ImportError:
    pass

try:
    import pygubu.theming.bootstrap.style as pbs_style

    has_pygubu_bootstrap = True
except ImportError:
    pass


def get_ttk_style():
    """Use themes from multiple modules if they are installed."""
    global _STYLE  # pylint: disable=global-statement
    if _STYLE is None:
        manager = MultipleThemeModuleManager()
        if has_pygubu_bootstrap:
            manager.modules.append(PygubuBootstrapModule())
        if has_ttkthemes:
            manager.modules.append(TtkthemesModule())
        if has_sv_ttk:
            manager.modules.append(SunValleyModule())
        if has_ttkbootstrap:
            manager.modules.append(TtkbModule())

        _STYLE = manager

    return _STYLE


class ThemeChangedMonitor:  # pylint: disable=too-few-public-methods
    """A class to monitor theme change and execute a callback when that happens.
    The callback is executed once in each theme.
    """

    def __init__(self, widget, callback):
        self._w = widget
        self._cb = callback
        self._changed = [
            ttk.Style(widget).theme_use(),
        ]
        widget.bind("<<ThemeChanged>>", self._theme_changed)

    def _theme_changed(self, event):
        w = event.widget
        s = ttk.Style(w)
        theme = s.theme_use()
        if theme not in self._changed:
            self._cb()
            self._changed.append(theme)
