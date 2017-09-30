#!/usr/bin/env python
# TODO: description of this script

import os
import sys
import csv
import requests
if sys.version_info[0] < 3:
    import urllib2                   # Python 2
else:
    import urllib.request as urllib2 # Python 3
from bs4 import BeautifulSoup
import flask_sqlalchemy
from iot_lab_inventory import db
from iot_lab_inventory.models import InventoryItem, Part, Image, Document


# Column number in csv file
SKU = 0
NUM = 1
URL = 2
NAME = 4

if len(sys.argv) != 2:
    print("usage: ./scrape_data.py all_parts.csv")
    exit(1)

f = open(sys.argv[1], 'r')
reader = csv.reader(f)
if sys.version_info[0] < 3:
    headers = reader.next() # Python 2
else:
    next(reader)            # Python 3

for row in reader:
    part = Part()
    name = row[NAME].strip(' ')
    sku = row[SKU]
    sku_num = sku.split('-')[1]
    part.name = name
    part.category = 'misc'
    part.sparkfun_id = sku

    num = row[NUM]
    url = row[URL]

    inventoryItem = InventoryItem()
    inventoryItem.quantity = num
    part.inventory_item = inventoryItem

    print('grabbing data for "' + name + '"')

    # Get the part's page
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Create a directory based on the part's name
    dirname = os.path.dirname(__file__) + '/part_resources/'
    try:
        os.mkdir(dirname)
    except Exception as e:
        pass

    # Get part description
    divs = soup.find_all('div', class_="description")
    for d in divs:
        p = d.find('p')
        if p is not None:
            part.description = p.text

    # Grab all jpg images, store in file system
    divs = soup.find_all('div', class_="carousel-inner")
    for div in divs:
        images = div.find_all('img')
        i = 1
        for image in images:
            src = image.get('src')
            if '.jpg' in src and sku_num in src:
                # Store image in part_name_1.jpg, 2.jpg, ...
                filename = name.replace(' ', '_').replace('/','_') + '_' + str(i) + '.jpg'
                imageObj = Image(filename=filename)
                imageObj.part = part

                image_data = urllib2.urlopen(src).read()
                with open(dirname + filename, "wb") as image_file:
                    image_file.write(image_data)

                i += 1

    #grab all documentation:
    docs_div = soup.find_all('div', {'id':'documents-tab'})
    for div in docs_div:
        links = div.find_all('a')
        for link in links:
            if 'Hookup Guide' in link.string or 'Datasheet' in link.string or 'Tutorial' in link.string:
                href = link.get('href')
                filename = name.replace(' ', '_') + '_' + link.string.replace(' ', '_')
                if '.pdf' in href:
                    filename += '.pdf'
                elif '.zip' in href:
                    filename += '.zip'
                else:
                    filename += '.html'
                cmd = 'wget %s -O %s' % (href, dirname + filename)
                document = Document(filename=filename)
                document.part = part
                os.system(cmd)

    # Put part into database
    db.session.add(part)
    db.session.commit()

f.close()
