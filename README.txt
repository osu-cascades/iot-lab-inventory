#create new database schema
UNIX> python
>>> from iot_app import db
>>> db.create_all()

#scrape sparkfun to populate db and download jpgs and pdfs
UNIX> python scrape_data.py all_parts.csv

#how to start app:
UNIX> ./run.py

