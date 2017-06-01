#!/usr/bin/env python
# In development, it is preferred to run the app via the `flask` command:
# export FLASK_APP=iot_app/__init__.py flask run

from iot_app import app

app.run(host='0.0.0.0', port=5000, debug=True)
