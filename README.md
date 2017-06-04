# IoT Lab Inventory

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

Start the app via `./run.py`.
