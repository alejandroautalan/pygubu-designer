from .predefined import PROPERTY_DEFINITIONS


class PropertiesManager:
    @staticmethod
    def iternames():
        yield from PROPERTY_DEFINITIONS.keys()

    @staticmethod
    def get_definition(pname):
        return PROPERTY_DEFINITIONS[pname]
