# -*- coding: utf-8 -*-
import os

import flask
import pytest
from flask_config import EnvironConfig, __version__, converters


def test_version():
    assert __version__ == "0.1.0"


@pytest.fixture
def app():
    app = flask.Flask("flask_config")
    return app


class TestEnvironConfig:
    config = [
        ("VALUE", "value"),
        ("VALUE2", 42, converters.Integer),
    ]

    def test_init(self, app):
        config = EnvironConfig(self.config)
        config.init_app(app)

        assert app.extensions["CONFIG"] is config

    def test_pull_from_env(self, app):
        os.environ["VALUE"] = "hello"

        EnvironConfig(self.config, app)

        assert "VALUE" in app.config
        assert app.config["VALUE"] == "hello"

        assert app.config["VALUE2"] == 42

    def test_convert_from_env(self, app):
        os.environ["VALUE2"] = "300"

        EnvironConfig(self.config, app)

        assert app.config["VALUE2"] == 300


class TestConverters:
    @pytest.mark.parametrize(
        "value,expected",
        [
            ("1", True),
            ("0", False),
            ("any", False),
            ("y", True),
            ("yes", True),
            ("True", True),
            ("YES", True),
            ("T", True),
            ("t", True),
            ("NO", False),
        ],
    )
    def test_boolean(self, value, expected):
        assert converters.Boolean()(value) == expected

    @pytest.mark.parametrize(
        "value,expected",
        [("42", "42"), ("hello", "hello"), ("Hello World", "Hello World")],
    )
    def test_string(self, value, expected):
        assert converters.String()(value)

    @pytest.mark.parametrize("value,expected", [("42", 42), ("122", 122)])
    def test_integer(self, value, expected):
        assert converters.Integer()(value) == expected

    @pytest.mark.parametrize(
        "value,expected", [("12", 12.0), ("120", 120.0), ("1.9999", 1.9999)]
    )
    def test_float(self, value, expected):
        assert converters.Float()(value) == expected
