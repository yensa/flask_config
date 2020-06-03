# -*- coding: utf-8 -*-

import click
from flask import current_app
from flask.cli import with_appcontext
import pprint


@click.command("showconfig", help="Shows the current config of the application")
@click.option("--valid", default=False, type=bool, is_flag=True)
@with_appcontext
def show_config(valid):
    if not valid:
        pprint.pprint(current_app.config)
    else:
        configs = current_app.extensions["CONFIG"].get_valid_configs()
        for key, default, conv in configs:
            if default is not None:
                line = f"{key} [{default}] type: {conv}"
            else:
                line = f"{key} type: {conv}"

            print(line)
