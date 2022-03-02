import re


def remove_invalid_characters(xml_data):
    return re.sub(r'^.*?<', '<', xml_data)


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def normalize_keys(data):
    new_data = dict((camel_to_snake(key), value)
                    for (key, value) in data.items())
    return new_data


def normalize_nested_dict_keys(data):
    data = normalize_keys(data)
    for k, v in data.items():
        if isinstance(v, dict):     # For DICT
            data[k] = normalize_nested_dict_keys(v)
        elif isinstance(v, list):   # For LIST
            data[k] = [normalize_nested_dict_keys(i) for i in v]
    return data
