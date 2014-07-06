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
    is_system = BooleanField()
    rightAscension = DoubleField()
    declination = DoubleField()
    distance = DoubleField()
    epoch = TextField()


class Stars(BaseModel):
    system_name = CharField()
    is_star = BooleanField()
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
    system_name = CharField()
    is_planet = BooleanField()
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
            current_system_dict = {}
            if system.tag == "name":
                if "name" in current_system_dict is True and current_system_dict["name"] == '':
                    current_system_dict[system.tag] = system.text
                    current_system_dict["is_system"] = True
                elif "name" in current_system_dict is True and current_system_dict["name"] != '':
                    current_system_dict["name"] = current_system_dict["name"].append(" " + system.text)
            else:
                current_system_dict[system.tag] = system.text

            for star in system:
                current_star_dict = {}
                if system.tag == "name":
                    if "name" in current_star_dict is True and current_star_dict["name"] == '':
                        current_star_dict["system_name"] = system.text
                        current_star_dict["is_star"] = True
                    elif "name" in current_star_dict is True and current_star_dict["name"] != '':
                        current_star_dict["name"] = current_star_dict["name"].append(" " + system.text)
                else:
                    current_star_dict[star.tag] = star.text

                for planet in star:
                    current_planet_dict = {}
                    if system.tag == "name":
                        if "name" in current_planet_dict is True and current_planet_dict["name"] == '':
                            current_planet_dict["system_name"] = system.text
                            current_planet_dict["is_planet"] = True
                        elif "name" in current_planet_dict is True and current_planet_dict["name"] != '':
                            current_planet_dict["name"] = current_planet_dict["name"].append(" " + system.text)
                    else:
                        current_planet_dict[planet.tag] = planet.text