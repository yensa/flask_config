flask_config
=============

A quick way to configure flask from the environment variables

```Python
import flask
from flask_config import EnvironConfig, converters as types

config_variables = [
  ("VARIABLE"),
  ("VAR2", 42, types.Integer),
]

app = flask.Flask('My App')

config = EnvironConfig(config_variables)
config.init_app(app)

# OR
EnvironConfig(config_variables, app)
```
