__author__ = 'Jacob'
from peewee import *
import sqlite3
import os

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree


# Peewee Database set up and creation of tables
database = SqliteDatabase('exoplanets.db', threadlocals=True)
database.connect()


class BaseModel(Model):
    class Meta:
        database = database


class Systems(BaseModel):
    name = CharField()
    rightAscension = DoubleField()
    declination = DoubleField()
    distance = DoubleField()
    epoch = TextField()


class Stars(BaseModel):
    system_name = CharField()
    is_binary = BooleanField()
    name = CharField()
    mass = DoubleField()
    radius = DoubleField()
    magV = DoubleField()
    magB = DoubleField()
    magJ = DoubleField()
    magH = DoubleField()
    magK = DoubleField()
    meetallicity = DoubleField()
    spectral_type = TextField()
    temperature = DoubleField()


class Planets(BaseModel):
    name = CharField()
    list = CharField()
    mass = DoubleField()
    radius = DoubleField()
    temperature = DoubleField()
    period = DoubleField()
    semi_major_axis = DoubleField()
    eccentricity = DoubleField()
    inclination = DoubleField()
    periastron = DoubleField()
    ascending_node = DoubleField()
    longitude = DoubleField()
    description = TextField()
    age = DoubleField()
    discovery_method = CharField()
    is_transiting = BooleanField()
    transit_time = TimeField()
    last_update = DateField()
    discovery_year = IntegerField()
    image = TextField()
    image_description = TextField()
    spin_orbital_alignment = DoubleField()


def create_tables():
    Systems.create_table(True)
    Stars.create_table(True)
    Planets.create_table(True)

#End of table creation and schema of database


#Start of XML parser
for file in os.listdir("C:\Development\Resources\Github\open_exoplanet_catalogue\systems") or os.listdir("C:\Development\Resources\Github\open_exoplanet_catalogue\kepler"):
    count = 0
    if file.endswith(".xml"):
        print(file)
        #Gets all files that end with .xml in directory and parse them
        tree = etree.parse("C:\Development\Resources\Github\open_exoplanet_catalogue\systems" + "\\" + file)
        root = tree.getroot()
        for system in root:
            print(system)
            for star in system:
                print(star)
                for planet in star:
                    print(planet)