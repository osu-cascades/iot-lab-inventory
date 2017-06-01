#!/usr/bin/env python

import csv
import sys
import requests
from bs4 import BeautifulSoup
import urllib2
import os
from iot_app.models import InventoryItem, Part, Image, Document
import flask_sqlalchemy
from iot_app import db

# Column number in csv file
SKU = 0
NUM = 1
NAME = 4
URL = 2

if len(sys.argv) != 2:
    print("usage: ./scrape_data.py all_parts.csv")
    exit(1)

f = open(sys.argv[1], 'r')
reader = csv.reader(f)
headers = reader.next()

for row in reader:
    part = Part()
    name = row[NAME]
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
    dirname = 'part_resources/'
    try:
        os.mkdir(dirname)
    except Exception as e:
        pass

    # Get part description
    divs = soup.find_all('div', class_="description")
    for d in divs:
        p = d.find('p')
        if p is not None and 'Description' in p.text:
            part.description = p.text

    # Grab all jpg images, store in file system
    images = soup.find_all('img')
    i = 1
    for image in images:
        src = image.get('src')
        if '.jpg' in src and sku_num in src:
            # Store image in part_name_1.jpg, 2.jpg, ...
            image_data = urllib2.urlopen(src).read()
            filename = name.replace(' ', '_').replace('/','_') + '_' + str(i) + '.jpg'
            with open(dirname + filename, "wb") as image_file:
                image_file.write(image_data)
            imageObj = Image(filename=filename)
            imageObj.part = part
            i += 1

    # Grab all pdf documentation, store in file system
    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        if href is not None \
                and '.pdf' in href \
                and 'http' in href:
                # and 'micrel' not in href\
                # and 'interlinkelectronics' not in href:
            pdf_name = href.split('/')[-1]
            pdf_name = pdf_name.replace('%','_')
            try:
                pdf_data = urllib2.urlopen(href).read()
                filename = name.replace(' ', '_').replace('/','_') + '_' + pdf_name
                with open(dirname + filename, 'wb') as pdf_file:
                    pdf_file.write(pdf_data)

                document = Document(filename=filename)
                document.part = part
            except Exception as e:
                pass

        if link.string == 'Hookup Guide':
            if href is not None and 'learn' in href:
                filename = name.replace(' ','_').replace('/','_') + '_hookup_guide.pdf'
                cmd = "wkhtmltopdf '" + href + "' " + '"' + dirname + filename + '"'
                document = Document(filename=filename)
                document.part=part
                os.system(cmd)

    # Put part into database
    db.session.add(part)
    db.session.commit()

f.close()
