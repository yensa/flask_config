# -*- coding: utf-8 -*-

TRUE_VALUES = ["1", "y", "yes", "true", "t"]


def to_bool(value):
    if isinstance(value, str):
        return value.lower() in TRUE_VALUES
    return bool(value)
