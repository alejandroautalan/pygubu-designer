from .predefined import PROPERTY_DEFINITIONS


class PropertiesManager:
    _required = ("class", "id")

    @classmethod
    def iternames(cls):
        yield from cls._required

        for name in sorted(PROPERTY_DEFINITIONS.keys()):
            if name not in cls._required:
                yield name

    @staticmethod
    def get_definition(pname):
        return PROPERTY_DEFINITIONS[pname]
