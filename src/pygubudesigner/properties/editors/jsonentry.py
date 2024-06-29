import json
from collections.abc import Iterable
from .propertyeditor import (
    TextPropertyEditor,
    register_editor,
)


class JsonEntry(TextPropertyEditor):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.json_type = None
        self.json_item_type = None

    def parameters(self, **kw):
        self.json_type = kw.pop("json_type", None)
        self.json_item_type = kw.pop("json_item_type", None)
        super().parameters(**kw)

    def _validate(self):
        is_valid = True
        value = self._get_value()
        if len(value) > 0:
            json_value = None
            try:
                json_value = json.loads(value)
            except json.JSONDecodeError:
                is_valid = False
            if is_valid and self.json_type is not None:
                if not isinstance(json_value, self.json_type):
                    is_valid = False
            if (
                is_valid
                and self.json_item_type is not None
                and isinstance(json_value, Iterable)
            ):
                for item in json_value:
                    if not isinstance(item, self.json_item_type):
                        is_valid = False
                        break
        self.show_invalid(not is_valid)
        return is_valid


register_editor("json_entry", JsonEntry)
