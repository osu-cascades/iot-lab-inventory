Utility scripts for scraping images and files from Sparkfun,
saving them locally and storing their representations in the
web application's database.

Before running, ensure that the application database exists. See the README
in the repo root.

Due to the way Python handles package imports, you must run this from
the root directory of the repository. (If you are trying to run scrape_data.py
from same directory as this README, then you are doing it wrong.)

`python -m util.scrape_data util/all_parts.csv`

This will save all downloaded assets to _util/part\_resources_.

Currently, you must also run another script that updates the
category names based on Sparkfun SKUs.

`python -m util.update_db_category`

This will update the category field of part records.
