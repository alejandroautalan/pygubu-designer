import keyword
import pathlib

from pygubu.forms.validation.base import Constraint, ConstraintValidator


class IsIdentifier(Constraint):
    code = "not_identifier_error"
    message = "This value should be a valid python identifier."

    def __init__(self, *args, message=None, **kw):
        super().__init__(*args, **kw)
        if message is not None:
            self.message = message

    def validated_by(self):
        return IsIdentifierValidator


class IsIdentifierValidator(ConstraintValidator):
    def validate(self, value, constraint):
        if str(value).isidentifier() and not keyword.iskeyword(value):
            return
        self.context.add_violation(
            message=constraint.message,
            constraint=constraint,
            code=constraint.code,
            params=None,
        )


class PathExist(Constraint):
    code = "path_not_exits_error"
    message = "The path must exist."

    def __init__(self, *args, message=None, **kw):
        super().__init__(*args, **kw)
        if message is not None:
            self.message = message

    def validated_by(self):
        return PathExistsValidator


class PathExistsValidator(ConstraintValidator):
    def validate(self, value, constraint):
        path = pathlib.Path(value)
        if path.exists():
            return
        self.context.add_violation(
            message=constraint.message,
            constraint=constraint,
            code=constraint.code,
            params=None,
        )


class RelativePathExists(PathExist):
    def __init__(self, *args, start_path=".", **kw):
        super().__init__(*args, **kw)
        self.start_path = start_path

    def validated_by(self):
        return RelativePathExistsValidator


class RelativePathExistsValidator(PathExistsValidator):
    def validate(self, value, constraint):
        path = pathlib.Path(constraint.start_path) / value
        super().validate(path, constraint)
