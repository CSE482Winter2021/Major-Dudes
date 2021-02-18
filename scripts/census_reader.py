import json
import csv

import pygeohash
from shapely.geometry import shape, Point

from utils import constants


class CensusReader:

    def __init__(self):

        pop_data = list(csv.reader(
            open(f'{constants.DATA_DIR}/tract_population.csv', "r"),
            delimiter=","
        ))

        # Maps tract nums to their population
        self.tract_pops = {tr[4]: tr[0] for tr in pop_data}

        with open(f'{constants.DATA_DIR}/tracts_2020.geojson', 'r') as f:
            geo_js = json.load(f)

        # Holds the geoJson feature and polygon for each tract
        self.shapes = [
            (feature, shape(feature['geometry']))
            for feature in geo_js['features']
        ]

        # Maps seen points to their tract num
        self.seen_points = dict()

    def xy_to_tract_num(self, longitude, latitude):
        """
        ARGS:
        longitude of coordinate in King County
        latitude of coordinate in King County

        Returns the tract number corresponding to the given coordinates. If the
        coordinates are outside king county, returns -1.
        """

        h = pygeohash.encode(latitude, longitude)  # Flipped for geohash
        if h in self.seen_points:
            return self.seen_points[h]

        point = Point(longitude, latitude)
        for feature, polygon in self.shapes:
            if polygon.contains(point):
                tract = feature['properties']['TRACTCE20']

                self.seen_points[h] = tract
                return tract

        self.seen_points[h] = -1
        return -1

    def get_tract_pop(self, tract):
        """
        ARGS:
        tract or subtract number

        Returns the population of the given tract, or the tract containing the
        given subtract. If not found, returns -1.
        """

        if tract in self.tract_pops:
            return self.tract_pops[tract]

        supertract = tract\
            .replace(tract[len(tract) - 1], '0')\
            .replace(tract[len(tract) - 2], '0')

        if supertract in self.tract_pops:
            return self.tract_pops[supertract]

        return -1
