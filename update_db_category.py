
from iot_app.models import Part
import flask_sqlalchemy
from iot_app import db

sku_category = {'BOB': 'controller',\
                'CAB': 'cable',\
                'COM': 'misc',\
                'DEV': 'controller',\
                'GPS': 'sensor',\
                'LCD': 'actuator',\
                'KIT': 'kit',
                'PRT': 'misc',\
                'ROB': 'actuator',\
                'SEN': 'sensor',\
                'TOL': 'tool',\
                'WRL': 'wireless'}

parts = Part.query.all()
for part in parts:
    sku = part.sparkfun_id.split('-')[0]
    if sku == 'LAB':
        print 'ignoring ' + part.name

    else:
        print part.name + ': ' + sku_category[sku]
        part.category = sku_category[sku]
        db.session.commit()
    #sku = 'KIT' or 'LAB', drop from table




# BOB = controller
# CAB = cable
# COM = misc
# DEV = controller
# GPS = sensor
# LCD = actuator
# ROB = actuator
# SEN = sensor
# TOL = tool
# WRL = wireless
# KIT = (drop)
# LAB = (drop)
# PRT = misc
#
