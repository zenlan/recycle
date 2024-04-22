#! /user/env/bin/python3

import geopandas as gpd
from geoalchemy2 import functions as gfn
import postcodes_io_api
from funcs import *


# These column names mapped to differentiate raw vals from transformed vals later on.
# Ultimately, raw data will all need to be mapped to a standard.
def map_bools():

    return {
        "co_mingled": "src_co_mingled",
        "textiles": "src_textiles",
        "shoes": "src_shoes",
        "books": "src_books",
        "media": "src_media",
        "printer_ca": "src_printer_ca",
        "waste_elec": "src_waste_elec",
        "lightbulbs": "src_lightbulbs",
        "batteries": "src_batteries",
        "carrier_ba": "src_carrier_ba",
        "oil_banks": "src_oil_banks",
    }


# Read Lambeth's raw data and perform necessary transformations.
def get_data(colmap):

    data = gpd.read_file("dat/Recycling_Banks.geojson")
    data.columns = map(str.lower, data.columns)
    # Merge geometry x/y vals to create single lat/lon column.
    # Note that xy vals are reversed, can never guarantee that data conforms to standard.
    data["latlon"] = data["geometry"].apply(lambda p: r"{},{}".format(p.y, p.x))
    data["geometry"] = data["geometry"].apply(
        lambda p: r"POINT({} {})".format(p.y, p.x)
    )
    data["near_postcode"] = None
    data["distance"] = None
    logger.debug(format(data["geometry"]))
    logger.debug(data.columns)
    data.rename(columns=colmap, inplace=True)
    logger.debug(data.columns)
    rows = data.to_dict("records")
    return rows


# Retrieve official UK geolocation and administrative information.
# Optional but potentially useful.
def get_postcodes():
    rows = sq.queryAll()
    latlons = []
    for place in rows:
        ll = place.latlon.split(",")
        x = {"longitude": ll[1], "latitude": ll[0], "radius": 1000, "limit": 1}
        latlons.append(x)
    data = dict()
    data["geolocations"] = latlons
    logger.debug(data)
    api = postcodes_io_api.Api(debug_http=True)
    postcodes = api.get_bulk_reverse_geocode(data)
    logger.debug(postcodes)
    params = []
    if not postcodes["status"] == 200:
        print("POSTCODE QUERY FAILED")
        exit()
    return postcodes["result"]


# Update database with postcode values.
def write_postcodes(postcodes):

    params = []
    for results in postcodes:
        s = r"POINT({} {})".format(
            results["query"]["latitude"], results["query"]["longitude"]
        )
        p = gfn.ST_GeomFromText(s, 4326, "axis-order=lat-long")
        rows = sq.queryFilter(sq._table.geometry.ST_Equals(p))
        for place in rows:
            logger.debug(
                "{} : {} : {}".format(place.objectid, place.latlon, place.location)
            )
            params.append(
                {
                    "oid": place.objectid,
                    "pc": results["result"][0]["postcode"],
                    "d": results["result"][0]["distance"],
                }
            )
    logger.debug(params)
    sq.execUpdatePostcodes(params)


def create_table():
    sq.createTable()


def insert_data():
    rows = get_data(map_bools())
    sq.execInsert(rows)


def insert_postcodes():
    postcodes = get_postcodes()
    write_postcodes(postcodes)


# Optional. Used to create spreadsheet for demo visualisation.
def write_csv():

    df = sq.toDataFrame()
    df.drop(columns=["geometry"], inplace=True)
    df.to_csv("out/{}.csv".format(sq.getTablename()), index=False)


# Post-insert search for data problems.
# E.g. Lambeth has some duplicate lat/lons.
def log_issues():
    results = sq.findIssues()
    for key in results.keys():
        logger.debug("{}: {}".format(key, len(results[key])))
        for place in results[key]:
            logger.debug(
                "{} ~ {} ~ {}".format(place.objectid, place.location, place.latlon)
            )


if __name__ == "__main__":

    logger = logfuncs.init_logger(__file__)

    sq = dbfuncs.sqlConnection()

    while True:
        eval(
            miscfuncs.exec_opt(
                [
                    "create_table()",
                    "insert_data()",
                    "insert_postcodes()",
                    "write_csv()",
                    "log_issues()",
                ]
            )
        )
