import csv
import sys
import requests
from bs4 import BeautifulSoup
import urllib2
import os

NAME = 4
NUM = 1
URL = 2

f = open(sys.argv[1], 'r')
reader = csv.reader(f)
headers = reader.next()

for row in reader:
    name = row[NAME]
    num = row[NUM]
    url = row[URL]

    print 'grabbing data for "' + name + '"'

    #get the part's page
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    #create a directory based on the part's name
    dirname = name.replace(' ', '_')
    try:
        os.mkdir(dirname)
    except Exception as e:
        pass

    #get part name (from page)
    #TODO: add name to db
    divs = soup.find_all('div', class_='product-title')
    for d in divs:
        h1 = d.find('h1')
        if h1 is not None:
            print h1.text

    #get part description
    #TODO: add description to db
    divs = soup.find_all('div', class_="description")
    for d in divs:
        p = d.find('p')
        if p is not None and 'Description' in p.text:
            print p.text

    #grab all jpg images, store in file system
    #TODO: add image filename(s) to db
    images = soup.find_all('img')
    i = 1
    for image in images:
        src = image.get('src')
        alt = image.get('alt')
        if '.jpg' in src and alt==name:
            #store image in part_name/1.jpg, 2.jpg, ...
            image_data = urllib2.urlopen(src).read()
            with open(dirname + '/' + str(i) + ".jpg", "wb") as image_file:
                image_file.write(image_data)
            i += 1

    #grab all pdf documentation, store in file system
    #TODO: add pdf filename(s) to db
    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        if href is not None \
                and '.pdf' in href \
                and 'http' in href \
                and 'micrel' not in href:
            pdf_name = href.split('/')[-1]
            pdf_data = urllib2.urlopen(href).read()
            with open(dirname + '/' + pdf_name, 'wb') as pdf_file:
                pdf_file.write(pdf_data)


    #TODO: grab full webpage for "Hookup Guide"
    # use UNIX> wkhtmltopdf on HookupGuide URL

    #TODO: grab data for kits
    #if name has word "Kit" in it
        # follow all <a> href urls with "sparkfun.com" and "products" in url
        # go to page, extract name, description, images, datasheets
        # store in subdirectory of kit

f.close()
