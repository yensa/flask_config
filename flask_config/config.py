# -*- coding: utf-8 -*-

import dotenv
import logging
from os import environ

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
        self.store_keys(app)

        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions["CONFIG"] = self

    def get_valid_configs(self):
        return self._config

    def load_dotenv(self, filename=None):
        dotenv.load_dotenv(filename)

    def store_keys(self, app):
        for key, default, conv in self._config:
            value = self.get_config(key, default, conv)

            app.config[key] = value

    def get_config(self, key, default=None, conv=str):
        raise_on_error = default is None

        try:
            value = conv(environ[key])
        except KeyError:
            if raise_on_error:
                raise ConfigError(f"Cannot find a value for key {key}")
            value = default
        except TypeError:
            logger.warn(
                f"Found a value for {key} but could not convert using {conv}"
                f", will fallback to {default}"
            )

        return value
