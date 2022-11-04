from .predefined import PROPERTY_DEFINITIONS


class PropertiesManager:
    _required = ("class", "id")
    _definitions_cache = {}

    @classmethod
    def iternames(cls):
        yield from cls._required

        for name in sorted(PROPERTY_DEFINITIONS.keys()):
            if name not in cls._required:
                yield name

    @classmethod
    def get_definition_for(cls, pname: str, builder_uid: str):
        _key = (pname, builder_uid)
        if _key in cls._definitions_cache:
            return cls._definitions_cache[_key]
        # Calculate and cache params
        definition = cls.get_definition(pname)
        default_params = (
            dict(definition["params"]) if "params" in definition else {}
        )
        default_mode = default_params.get("mode", None)
        def_cached = {
            "params": default_params,
            "help": definition.get("help", None),
            "default": definition.get("default", None),
        }
        specific = {}
        # Get editor parameters for a specific builder_uid
        # First, search for exact match
        for key in definition:
            if key == builder_uid:
                specific = definition[key]
                break
        if not specific:
            # Search for partial match
            for key in definition:
                if key.endswith(".*"):
                    needle = key[:-2]
                    if needle in builder_uid:
                        specific = definition[key]
                        break
        def_cached.update(**specific)
        final_params = def_cached["params"]
        if "mode" not in final_params:
            final_params["mode"] = default_mode
        cls._definitions_cache[_key] = def_cached
        return def_cached

    @classmethod
    def get_definition(cls, pname):
        return PROPERTY_DEFINITIONS[pname]
