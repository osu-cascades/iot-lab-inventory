# OSU Cascades IoT Lab Inventory

Start the app via `python -m flask run`. But you will want to make sure your
development environment is ready first.

To get your development environment up and running, you'll need an appropriate
configuration, dependencies, a database, and some seed data.

## Python Version

While code should be written to support Python 2.7, you should use Python 3.6.1
or higher.

## Virtualenv and Virtualenv Wrapper

Use them. Create a virtualenv for this application.

## Dependencies

See _requirements.txt_. Select your virtualenv and install dependencies with
`pip install -r requirements.txt`.

## Configuration

Flask and the application itself expects certain environment variables to be
set (eg in _$VIRTUAL\_ENV/bin/postactivate_):

```
export FLASK_DEBUG=1
export FLASK_APP=iot_lab_inventory
export FLASK_SECRET_KEY='\xba\x19...'
export GOOGLE_LOGIN_CLIENT_ID=???
export GOOGLE_LOGIN_CLIENT_SECRET=???
export DATABASE_URL=postgresql://localhost/iot_lab_inventory_dev
```

## Database

Before you run the application for the first time, ensure that the database
exists, and then use the migrations:

`python -m flask db upgrade`

This is a better approach for ongoing development, since Alembic will store
the appropriate metadata in the schema, allowing you to apply future migrations.

If you just want to boostrap the schema, you can:

```
python
>>> from iot_lab_inventory import db
>>> db.create_all()
>>> exit()
```

## Seed Data

You can scrape SparkFun to populate the database and download images and
documents:

`python -m util.scrape_data util/all_parts.csv`


(c) 2017 Marc Rubin, Yong Bakos. All rights reserved.
