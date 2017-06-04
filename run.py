#!/usr/bin/env python
# In development, it is preferred to run the app via the `flask` command:
# FLASK_APP=iot_lab_inventory python -m flask run

from iot_lab_inventory import app

app.run(host='0.0.0.0', port=5000, debug=True)
