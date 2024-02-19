import keyword
import pathlib

from pygubu.forms.exceptions import ValidationError


class IdentifierValidator:
    message = "The value is not a valid python identifier."
    code = "identifier"

    def __call__(self, value):
        is_valid = True
        if len(value) > 0:
            if keyword.iskeyword(value):
                is_valid = False
            if is_valid and not str(value).isidentifier():
                is_valid = False
        else:
            # ID must have at least one character
            is_valid = False
        if not is_valid:
            raise ValidationError(self.message, code=self.code)


class PathExistsValidator:
    message = "The path must exist"
    code = "path_exists"

    def __init__(self):
        self.uipath = None

    def __call__(self, value):
        path: pathlib.Path = self.uipath / value
        if not path.exists():
            raise ValidationError(self.message, code=self.code)


class ModulesPathValidator(PathExistsValidator):
    def __call__(self, value):
        super().__call__(value)
