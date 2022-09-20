import pytest

from app import form_outliner


def test_form_outliner_hello_add():
    assert form_outliner.add(2, 2) == 4
