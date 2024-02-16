import keyword

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
