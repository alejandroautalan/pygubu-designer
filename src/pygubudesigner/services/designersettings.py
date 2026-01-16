#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import pygubudesigner.services.designersettingsui as baseui

from pygubu.forms.transformer.tkboolean import BoolTransformer
from pygubudesigner.preferences import preferences, default_config, CfgOption
from pygubudesigner.services.theming import get_ttk_style
from pygubudesigner.i18n import translator
from pygubudesigner.services.image_loader import iconset_loader


class DesignerSettings(baseui.DesignerSettingsUI):
    def __init__(self, master=None):
        super().__init__(
            master, translator=translator, image_loader=iconset_loader
        )

        self.dialog_toplevel = self.mainwindow.toplevel

        # setup theme values
        s = get_ttk_style()
        styles = s.theme_names()
        themelist = []
        for name in styles:
            themelist.append((name, name))
        themelist.sort()
        self.ttk_theme.configure(values=themelist)

        bool_transformer = BoolTransformer()
        form_config = {
            CfgOption.CENTER_PREVIEW: dict(model_transformer=bool_transformer),
            CfgOption.WIDGET_NAMING_USE_UNDERSCORE: dict(
                model_transformer=bool_transformer
            ),
            CfgOption.WIDGET_NAMING_UFLETTER: dict(
                model_transformer=bool_transformer
            ),
        }
        self.frm_settings = self.ffb_settings.get_form(form_config)

    def run(self):
        self.edit_settings()
        self.mainwindow.run()

    def edit_settings(self):
        # set defaults
        defaults = default_config.copy()

        # Load user options
        user_settings = preferences.config.copy()
        self.frm_settings.edit(user_settings, defaults)

    def _deselect_combobox_text(self):
        """
        Deselect all text in all combo boxes.

        If we don't do this, the next time the preference window opens,
        One of the combo boxes may have all its text selected.
        """
        for field in self.frm_settings.fields.values():
            widget = field.widget
            if widget.winfo_class() == "TCombobox":
                widget.select_clear()

    def on_dialog_close(self, event=None):
        self._deselect_combobox_text()
        self.mainwindow.close()

    def btn_cancel_clicked(self):
        self.on_dialog_close()

    def btn_apply_clicked(self):
        form = self.frm_settings
        form.submit()
        valid = form.is_valid()
        if valid:
            preferences.update(form.cleaned_data)
            parent = self.dialog_toplevel.nametowidget(
                self.dialog_toplevel.winfo_parent()
            )
            parent.event_generate("<<PygubuDesignerPreferencesSaved>>")
            self.on_dialog_close()
        else:
            # FIXME
            print(form.errors)


if __name__ == "__main__":
    root = tk.Tk()
    app = DesignerSettings(root)
    app.run()
