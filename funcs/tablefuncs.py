from datetime import datetime
import sqlalchemy as db
from sqlalchemy.orm import *
import sqlalchemy.dialects.mysql as my
from geoalchemy2 import Geometry


class Place(declarative_base()):

    __tablename__ = "geo_recycle_banks"

    objectid = db.Column(db.Integer, primary_key=True, autoincrement=False)
    location = db.Column(
        my.VARCHAR(255, collation="utf8mb4_unicode_ci"), nullable=False, default="None"
    )
    materials = db.Column(
        my.VARCHAR(255, collation="utf8mb4_unicode_ci"), nullable=False, default="None"
    )
    easting = db.Column(db.Integer, primary_key=False, autoincrement=False)
    northing = db.Column(db.Integer, primary_key=False, autoincrement=False)
    geometry = db.Column(Geometry("POINT", srid=4326))
    latlon = db.Column(my.VARCHAR(255), nullable=True)
    postcode = db.Column(my.VARCHAR(255), nullable=True)  # nearest postcode
    distance = db.Column(db.Float, nullable=True)  # metres from nearest postcode
    updated = db.Column(db.DateTime, default=datetime.now())
    created = db.Column(db.DateTime, default=datetime.now())

    src_co_mingled = db.Column(my.VARCHAR(3), nullable=True)
    src_textiles = db.Column(my.VARCHAR(3), nullable=True)
    src_shoes = db.Column(my.VARCHAR(3), nullable=True)
    src_books = db.Column(my.VARCHAR(3), nullable=True)
    src_media = db.Column(my.VARCHAR(3), nullable=True)
    src_printer_ca = db.Column(my.VARCHAR(3), nullable=True)
    src_waste_elec = db.Column(my.VARCHAR(3), nullable=True)
    src_lightbulbs = db.Column(my.VARCHAR(3), nullable=True)
    src_batteries = db.Column(my.VARCHAR(3), nullable=True)
    src_carrier_ba = db.Column(my.VARCHAR(3), nullable=True)
    src_oil_banks = db.Column(my.VARCHAR(3), nullable=True)
