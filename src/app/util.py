from typing import Iterable

JsonObject = (
    str
    | int
    | float
    | bool
    | None
    | list[Iterable["JsonObject"]]
    | dict[str, Iterable["JsonObject"]]
)


def jsonpath(data: JsonObject, path: str, default=None, path_separator="/"):
    """Extract value from nested dicts and lists parsed from JSON

    :data: presumed to be parsed JSON. Consists of str, int, float, bool, and
    None, within lists and str-keyed dicts
    :path: path within data
    :default: value to return if path not found
    :path_separator:

    Example:
    data = {"pages":[{"title": "Page 1"}, {"title": "Page 2"}]}
    dlpath(data, "pages/1/title") == "Page 2"
    """

    key, _, rem = path.partition(path_separator)

    if key == "":
        return data

    if isinstance(data, list):
        try:
            key = int(key)
        except ValueError as exc:
            raise ValueError(f'Cannot index list with non-integer "{key}"') from exc

        if key < len(data):
            return jsonpath(data[int(key)], rem)

        return default

    if key in data:
        return jsonpath(data[key], rem)

    return default
