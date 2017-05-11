how to start app:
UNIX> python run.py

NOTE: before first launch, create db:
UNIX> python
>>> from iot_app import db
>>> db.create_all()
>>> exit()

TODO:
- setup Flask-SQLAlchemy migration scripts
- test, test, test login / logout w/ Google auth
- populate parts database
- add User roles (e.g., admin vs. student)
- add "cart" feature
- add "checkout" cart