# -*- coding: utf-8 -*-


class Converter:
    def __call__(self, value):
        return self._convert(value)


class Boolean(Converter):
    TRUE = ["1", "y", "yes", "true", "t"]

    def _convert(self, value):
        if isinstance(value, str):
            return value.lower() in Boolean.TRUE
        return bool(value)


class String(Converter):
    def _convert(self, value):
        return str(value)


class Integer(Converter):
    def _convert(self, value):
        return int(value)


class Float(Converter):
    def _convert(self, value):
        return float(value)
