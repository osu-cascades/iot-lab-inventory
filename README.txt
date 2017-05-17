how to start app:
UNIX> python run.py

NOTE: before first launch, create db:
UNIX> python
>>> from iot_app import db
>>> db.create_all()
>>> exit()

TODO: (prioritize on working software)
- populate parts database
- update view to show updated data
- change google login to use oauth2 module

- setup Flask-SQLAlchemy migration scripts
- add User roles (e.g., admin vs. student)
- add "cart" feature
- add "checkout" cart

per Yong:
- clean up virtualenv wrapper (try UNIX> workon) instead of just virtualenv
- look at github issue as using google login => use oauth