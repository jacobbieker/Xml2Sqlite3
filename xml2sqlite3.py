from peewee import DeleteQuery, SelectQuery

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
    name = CharField(null=True)
    is_system = BooleanField(null=True)
    is_binary = BooleanField(null=True)
    rightAscension = TextField(null=True)
    declination = TextField(null=True)
    distance = DoubleField(null=True)


class Stars(BaseModel):
    system_name = CharField(null=True)
    is_star = BooleanField(null=True)
    name = CharField(null=True)
    mass = DoubleField(null=True)
    radius = DoubleField(null=True)
    magV = DoubleField(null=True)
    magB = DoubleField(null=True)
    magI = DoubleField(null=True)
    magR = DoubleField(null=True)
    magJ = DoubleField(null=True)
    magH = DoubleField(null=True)
    magK = DoubleField(null=True)
    metallicity = DoubleField(null=True)
    spectral_type = TextField(null=True)
    temperature = DoubleField(null=True)


class Planets(BaseModel):
    system_name = CharField(null=True)
    star_name = CharField(null=True)
    name = CharField(null=True)
    list_type = CharField(null=True)
    mass = DoubleField(null=True)
    radius = DoubleField(null=True)
    temperature = DoubleField(null=True)
    period = DoubleField(null=True)
    semi_major_axis = DoubleField(null=True)
    eccentricity = DoubleField(null=True)
    inclination = DoubleField(null=True)
    periastron = DoubleField(null=True)
    ascending_node = DoubleField(null=True)
    longitude = DoubleField(null=True)
    description = TextField(null=True)
    age = DoubleField(null=True)
    discovery_method = CharField(null=True)
    is_transiting = BooleanField(null=True)
    transit_time = TimeField(null=True)
    last_update = DateField(null=True)
    discovery_year = IntegerField(null=True)
    image = TextField(null=True)
    image_description = TextField(null=True)
    spin_orbital_alignment = DoubleField(null=True)


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
        elif entry == "is_system":
            current_system.is_system = system_dict[entry]
        elif entry == "is_binary":
            current_system.is_binary = system_dict[entry]
    print("Trying to Save")
    if current_system.name is not None and current_system.rightAscension is not None and current_system.distance is not None and current_system.is_system is not None and current_system.declination is not None:
        print("Saved")
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
            #parse_system(current_system_dict)
            if system.tag == "star":
                current_star_dict = {}
                for star in system:
                    #current_star_dict = {}
                    if star.tag == "planet":
                        current_star_dict["is_star"] = True
                    else:
                        current_star_dict[star.tag] = star.text
                    current_planet_dict = {}
                    #parse_system(current_system_dict)
                    #print(current_star_dict.items())
                    for planet in star:
                        current_planet_dict[planet.tag] = planet.text
                    else:
                        if current_planet_dict is not False:
                            x = 1
                            #print(current_planet_dict.items())

            print(current_system_dict.items())
            parse_system(current_system_dict)
            #print(current_star_dict.items())
            #print(current_planet_dict.items())


def clean_up_systems():
    sq = SelectQuery(Systems).where(Systems.name).dicts()
    '''Delete the entries that have the same name after the first one'''
    for db_system in sq:
        current_db_system = db_system
        count = 0
        for check in sq:
            print(check.items())

clean_up_systems()