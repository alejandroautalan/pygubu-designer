"""Manage pygubu form widgets in WidgetTreeEditor"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygubu.builder import CLASS_MAP
from pygubu.forms.builder import FormBuilder
from pygubu.forms.widget import FieldWidget

if TYPE_CHECKING:
    from pygubudesigner.uitreeeditor import WidgetTreeEditor


class PygubuFormsManager:
    def __init__(self, wteditor: WidgetTreeEditor):
        self.wteditor = wteditor

    def is_subclass(self, classname: str, classobj: type):
        builder = CLASS_MAP[classname].builder
        if builder.class_ is not None:
            return issubclass(builder.class_, classobj)
        return False

    def is_fbuilder_class(self, classname: str):
        return self.is_subclass(classname, FormBuilder)

    def is_field_class(self, classname: str):
        return self.is_subclass(classname, FieldWidget)

    def get_parent_fbuilder(self, itemid):
        fbitem = None
        fbdata = None
        for parentid, wdata in self.wteditor.iter_parents(itemid):
            if self.is_fbuilder_class(wdata.classname):
                fbitem = parentid
                fbdata = wdata
                break
        return fbitem, fbdata

    def is_field_defined(self, fbitem, fieldname: str) -> bool:
        """Check if field is defined in fbitem scope."""

        is_defined = False
        for item, data in self.wteditor.iter_tree_data():
            if self.is_field_class(data.classname):
                fbparent, _fbdata = self.get_parent_fbuilder(item)
                if fbitem == fbparent:
                    fname = data.widget_property("field_name")
                    if not fname:
                        fname = data.identifier
                    if fname == fieldname:
                        is_defined = True
                        break
        return is_defined

    def get_fieldname_list(self, fbitem):
        flist = []
        for item, data in self.wteditor.iter_tree_data():
            if self.is_field_class(data.classname):
                fbparent, _fbdata = self.get_parent_fbuilder(item)
                if fbitem == fbparent:
                    fname = data.widget_property("field_name")
                    if not fname:
                        fname = data.identifier
                    flist.append(fname)
        return flist
