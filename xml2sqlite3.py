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
    is_binary = BooleanField()
    rightAscension = TextField()
    declination = TextField()
    distance = DoubleField()
    epoch = TextField()


class Stars(BaseModel):
    system_name = CharField()
    is_star = BooleanField()
    name = CharField()
    mass = DoubleField()
    radius = DoubleField()
    magV = DoubleField()
    magB = DoubleField()
    magI = DoubleField()
    magR = DoubleField()
    magJ = DoubleField()
    magH = DoubleField()
    magK = DoubleField()
    metallicity = DoubleField()
    spectral_type = TextField()
    temperature = DoubleField()


class Planets(BaseModel):
    system_name = CharField()
    star_name = CharField()
    name = CharField()
    list_type = CharField()
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

create_tables()


def parse_system(system_dict):
    print("Parse_system Called")
    current_system = Systems()
    for entry in system_dict:
        if entry == "name":
            current_system.name = system_dict[entry]
        elif entry == "rightascension":
            current_system.rightAscension = system_dict[entry]
        elif entry == "declination":
            current_system.declination = system_dict[entry]
        elif entry == "distance":
            current_system.distance = system_dict[entry]
        elif entry == "epoch":
            current_system.epoch = system_dict[entry]
        elif entry == "is_system":
            current_system.is_system = system_dict[entry]
        elif entry == "is_binary":
            current_system.is_binary = system_dict[entry]
    print("Current_System Saved")
    current_system.save()


def parse_star(star_dict):
    print("Parse_Star called")
    current_star = Stars()
    for entry in star_dict:
        if entry == "name":
            current_star.name = star_dict[entry]
        elif entry == "is_star":
            current_star.is_star = star_dict[entry]
        elif entry == "mass":
            current_star.mass = star_dict[entry]
        elif entry == "radius":
            current_star.radius = star_dict[entry]
        elif entry == "metallicity":
            current_star.metallicity = star_dict[entry]
        elif entry == "spectraltype":
            current_star.spectral_type = star_dict[entry]
        elif entry == "temperature":
            current_star.temperature = star_dict[entry]
        elif entry == "magVBRIGHK":
            current_star.magB = star_dict[entry]
        elif entry == "magV":
            current_star.magV = star_dict[entry]
        elif entry == "magR":
            current_star.magR = star_dict[entry]
        elif entry == "magI":
            current_star.magI = star_dict[entry]
        elif entry == "magG":
            current_star.magG = star_dict[entry]
        elif entry == "magH":
            current_star.magH = star_dict[entry]
        elif entry == "magK":
            current_star.magK = star_dict[entry]
    print("Current_Star Saved")
    current_star.save()


#Start of XML parser
for file in os.listdir("C:\Development\Resources\Github\open_exoplanet_catalogue\systems") or os.listdir("C:\Development\Resources\Github\open_exoplanet_catalogue\kepler"):
    if file.endswith(".xml"):
        print(file)
        #Gets all files that end with .xml in directory and parse them
        tree = etree.parse("C:\Development\Resources\Github\open_exoplanet_catalogue\systems" + "\\" + file)
        root = tree.getroot()
        #Creates a dictionary for each file that starts over with each new file
        current_system_dict = {}
        for system in root:
            #current_system_dict = {}
            if system.tag == "star":
                current_system_dict["is_system"] = True
                current_system_dict["is_binary"] = False
            elif system.tag == "binary":
                current_system_dict["is_system"] = True
                current_system_dict["is_binary"] = True
            else:
                current_system_dict[system.tag] = system.text
            #print(current_system_dict.items())
            if system.tag == "star":
                current_star_dict = {}
                for star in system:
                    #current_star_dict = {}
                    if star.tag == "planet":
                        current_star_dict["is_star"] = True
                    else:
                        current_star_dict[star.tag] = star.text
                    current_planet_dict = {}
                    parse_system(current_system_dict)
                    print(current_star_dict.items())
                    for planet in star:
                        current_planet_dict[planet.tag] = planet.text
                    else:
                        if current_planet_dict is not False:
                            print(current_planet_dict.items())

            #print(current_system_dict.items())
            #print(current_star_dict.items())
            #print(current_planet_dict.items())