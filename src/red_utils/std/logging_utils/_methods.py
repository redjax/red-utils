from copy import deepcopy


def merge_config_dicts(configdict1: dict = None, configdict2: dict = None):
    merged_config = deepcopy(configdict1)

    def _merge_dicts(d1, d2):
        for key, value in d2.items():
            if key in d1:
                if isinstance(d1[key], dict) and isinstance(value, dict):
                    _merge_dicts(d1[key], value)
                elif isinstance(d1[key], list) and isinstance(value, list):
                    d1[key].extend(value)
                else:
                    # Handle conflict if necessary or just overwrite
                    d1[key] = value
            else:
                d1[key] = value

    _merge_dicts(merged_config, configdict2)
    return merged_config
