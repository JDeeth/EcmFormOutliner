import pytest
from app.util import jsonpath


def test_returns_plain_obj_with_no_path():
    assert jsonpath("hello", "") == "hello"


def test_returns_none_with_missing_dict_key():
    assert jsonpath({1: 1}, "2") is None


def test_returns_none_with_out_of_index_list():
    assert jsonpath([1, 2], "2") is None


def test_throws_valueerror_if_navigating_list_with_non_int():
    with pytest.raises(ValueError):
        jsonpath([1, 2], "not_a_number")


def test_returns_given_default_with_missing_key():
    assert jsonpath({1: 1}, "2", "steve") == "steve"


def test_returns_dict_val_with_simple_key():
    assert jsonpath({"a": 1}, "a") == 1


def test_returns_list_val_with_with_digit_key():
    assert jsonpath([2, 4, 8, 10], "3") == 10


def test_dlpath_example_code():
    data = {"pages": [{"title": "Page 1"}, {"title": "Page 2"}]}
    assert jsonpath(data, "pages/1/title") == "Page 2"
