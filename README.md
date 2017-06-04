# OSU Cascades IoT Lab Inventory

Before you run the application for the first time, ensure that the database
exists:

```
python
>>> from iot_lab_inventory import db
>>> db.create_all()
>>> exit()
```

You can scrape SparkFun to populate the database and download images and documents:

`python -m util.scrape_data util/all_parts.csv`

Start the app via `python -m flask run`.

## Environment Variables

FLask and the application itself expects certain environment variables to be
set (eg in _$VIRTUAL\_ENV/bin/postactivate_):

```
export FLASK_DEBUG=1
export FLASK_APP=iot_lab_inventory
export GOOGLE_LOGIN_CLIENT_ID=???
export GOOGLE_LOGIN_CLIENT_SECRET=???
```

(c) 2017 Marc Rubin, Yong Bakos. All rights reserved.
