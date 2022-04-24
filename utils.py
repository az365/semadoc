import yaml
from functools import wraps
from typing import Optional, Iterable, Union

Array = Union[list, tuple]


def get_detected_doctype_by_filename(filename: str, default: Optional[str] = None) -> str:
    extension = filename.split('.')[-1]
    if extension in ('txt', 'yaml'):
        doctype = extension
        return doctype
    elif default:
        return default
    else:
        raise ValueError


def get_parsed_yaml_from_lines(self, lines: Iterable):
    yaml_data = yaml.safe_load(lines)
    for obj in yaml_data:
        assert isinstance(obj, dict)
        self.add_dict_obj(obj)
    return self


def get_canonic_synonym(key, synonyms_list: Iterable[Array], skip_missing: bool = False, class_name=None):
    for t in synonyms_list:
        if key in t:
            return t[0]
    if not skip_missing:
        raise ValueError('key {} is not allowed for {} class'.format(key, class_name or ''))


def is_in_synonyms(key, synonyms_list: Iterable[Array]):
    return get_canonic_synonym(key, synonyms_list=synonyms_list, skip_missing=True) is not None


def get_standardized_dict(obj: dict, keys_synonyms: Union[list, tuple]) -> dict:
    obj_copy = obj.copy()
    standardized_dict = dict()
    for synonyms in keys_synonyms:
        main_key = synonyms[0]
        for key in synonyms:
            cur_value = obj_copy.pop(key, None)
            if cur_value:
                prev_value = standardized_dict.get(main_key)
                if prev_value:
                    if not isinstance(prev_value, list):
                        prev_value = [prev_value]
                    if not isinstance(cur_value, list):
                        cur_value = [cur_value]
                    new_value = prev_value + cur_value
                else:
                    new_value = cur_value
                # is_plural = main_key[-1] == 's'
                is_plural = main_key in list_plural_keys
                if is_plural and not isinstance(new_value, list):
                    new_value = [new_value]
                standardized_dict[key] = new_value
    if obj_copy:
        standardized_dict['err'] = obj_copy
    return standardized_dict


def singleton(cls):
    @wraps(cls)
    def wrapper(*args, **kwargs):
        if not wrapper.instance:
            wrapper.instance = cls(*args, **kwargs)
        return wrapper.instance
    wrapper.instance = None
    return wrapper
