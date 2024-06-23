import keyword
from .propertyeditor import (
    EntryPropertyEditor,
    ChoicePropertyEditor,
    register_editor,
)


class FormFieldNameEntry(EntryPropertyEditor):
    def _validate(self):
        is_valid = True
        value = self._get_value()
        if len(value) > 0:
            if keyword.iskeyword(value):
                is_valid = False
            if is_valid and not str(value).isidentifier():
                is_valid = False
            # Check if new id is unique
            if is_valid and value != self._initvalue:
                is_valid = self.is_valid_globally(value)
        self.show_invalid(not is_valid)
        return is_valid


register_editor("fieldname_entry", FormFieldNameEntry)


class FormFieldNameSelector(ChoicePropertyEditor):
    FIELD_NAMES = []

    def parameters(self, **kw):
        kw["values"] = [""] + self.FIELD_NAMES
        kw["state"] = "readonly"
        self._combobox.configure(**kw)


register_editor("fieldname_selector", FormFieldNameSelector)
