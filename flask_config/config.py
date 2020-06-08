# -*- coding: utf-8 -*-

import logging
from os import environ

import dotenv
from flask_config import converters
from flask_config.exc import ConfigError

logger = logging.getLogger(__name__)


class EnvironConfig:
    """
    This class intent is to provide configuration using the environment variables
    """

    def __init__(self, config, app=None):
        self._config = config

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self._store_keys(app)

        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions["CONFIG"] = self

    def get_valid_configs(self):
        return self._config

    def load_dotenv(self, filename=None):
        dotenv.load_dotenv(filename)

    def _store_keys(self, app):
        for config in self._config:
            key = config[0]
            value = self.get_config(*config)

            app.config[key] = value

    def get_config(self, key, default=None, conv=converters.String):
        raise_on_error = default is None

        value = default

        try:
            value = conv()(environ[key])
        except KeyError:
            if raise_on_error:
                raise ConfigError(f"Cannot find a value for key {key}")
        except TypeError:
            logger.warn(
                f"Found a value for {key} but could not convert using {conv}"
                f", will fallback to {default}"
            )

        return value
