import yaml

try:  # Assume we're a submodule in a package.
    import classes as cs
except ImportError:  # Apparently no higher-level package has been imported, fall back to a local import.
    from . import classes as cs


def get_parsed_yaml(filename: str):
    stream = open(filename, encoding='utf8', mode='r')
    parsed_doc = yaml.safe_load(stream)
    stream.close()
    return parsed_doc
