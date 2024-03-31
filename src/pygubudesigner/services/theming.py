import tkinter.ttk as ttk


__style = None

has_sv_ttk = False
has_ttkthemes = False
has_ttkbootsrap = False
has_pygubu_bootstrap = False


class ThemeModule:
    def theme_names(self) -> list:
        raise NotImplementedError

    def theme_use(self, name):
        raise NotImplementedError

    def can_handle(self, name) -> bool:
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


class ttkthemesModule(ThemeModule):
    def __init__(self):
        self.style = ThemedStyle()
        self.definitions = list(self.style.theme_names())

    def theme_names(self) -> list:
        return self.definitions

    def theme_use(self, name):
        self.style.theme_use(name)

    def can_handle(self, name):
        return name in self.definitions


class ttkbModule(ThemeModule):
    def __init__(self):
        self.style = ttkb.Style()
        self.definitions = list(self.style.theme_names())

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
    modules = []
    theme_list = None

    def theme_names(self):
        if self.theme_list is None:
            MultipleThemeModuleManager.theme_list = list(super().theme_names())
            for m in self.modules:
                themes = m.theme_names()
                for t in themes:
                    if t not in self.theme_list:
                        self.theme_list.append(t)
        return self.theme_list

    def theme_use(self, name=None):
        if name is None:
            return super().theme_use()

        theme_set = False
        for m in self.modules:
            if m.can_handle(name):
                m.theme_use(name)
                theme_set = True
                break
        if not theme_set:
            super().theme_use(name)


try:
    import ttkbootstrap as ttkb

    has_ttkbootsrap = True
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
    global __style
    if __style is None:
        manager = MultipleThemeModuleManager()
        if has_pygubu_bootstrap:
            manager.modules.append(PygubuBootstrapModule())
        if has_ttkthemes:
            manager.modules.append(ttkthemesModule())
        if has_sv_ttk:
            manager.modules.append(SunValleyModule())
        if has_ttkbootsrap:
            manager.modules.append(ttkbModule())

        __style = manager

    return __style


class ThemeChangedMonitor:
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
