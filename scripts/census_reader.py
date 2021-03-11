import os
import json

import pygeohash
from shapely.geometry import shape, Point

from utils import constants


CENSUS_DATA_DIR = os.path.join(constants.DATA_DIR, 'census_data', 'pipeline_output')


class TractCensusReader:
    def __init__(self):
        # GIS Data
        with open(f'{CENSUS_DATA_DIR}/tracts_demographics.geojson', 'r') as f:
            geo_js = json.load(f)

        # Holds the geoJson feature and polygon for each tract
        self.shapes = [
            (feature, shape(feature['geometry']))
            for feature in geo_js['features']
        ]

        # Maps seen points to their tract num
        self.seen_points = {}

        with open(f'{CENSUS_DATA_DIR}/tract_to_demographics.json', 'r') as f:
            self.demographics_info = json.load(f)
        
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
                tract = feature['id']

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
        if tract in self.demographics_info:
            return self.demographics_info[tract]['population']
        else: 
            return -1

    def get_tract_age_pop(self, tract):
        """
        ARGS:
        tract or subtract number

        Returns an array of populations per age group of the given tract,
        or the tract containing the given subtract. If not found, returns empty
        list.
        The list is in the following form:
        [< 5, 5-9, 10-14, 15-17, 18-19, 20, 21, 22-24, 25-29, 30-34, 35-39,
        40-44, 45-49, 50-54, 55-59, 60-61, 62-64, 65-66, 67-69, 70-74, 75-79,
        80-84, 85+]
        """
        if tract in self.demographics_info:
            return self.demographics_info[tract]['age']
        else: 
            return []

    def get_tract_gender_pop(self, tract):
        """
        ARGS:
        tract or subtract number

        Returns a list of populations per gender of the given tract,
        or the tract containing the given subtract. If not found, returns empty
        list.
        The list is in the following form:
        [Population Male, Population Female]
        """
        if tract in self.demographics_info:
            return self.demographics_info[tract]['gender']
        else: 
            return []

    def get_tract_race_pop(self, tract):
        """
        ARGS:
        tract or subtract number

        Returns a list of populations per race of the given tract,
        or the tract containing the given subtract. If not found, returns empty
        list.
        The list is in the following form:
        [ White Only, Black Only, Native Only, Asian Only,
        Hawaiian/Pacific Islander Only, Other Only, Multiracial White,
        Multiracial Black, Multiracial Native, Multiracial Asian,
        Multiracial Hawaiian/Pacific Islander, Multiracial Other ]
        """
        if tract in self.demographics_info:
            return self.demographics_info[tract]['race']
        else: 
            return []

    def get_tract_disabled_pop(self, tract):
        """
        ARGS:
        tract or subtract number

        Returns a list of populations with one disability and 2+ disabilities of
        the given tract, or the tract containing the given subtract. If not
        found, returns empty list. The list is in the following form:
        [1 disability, 2+ disabilities]
        """
        if tract in self.demographics_info:
            return self.demographics_info[tract]['disability']
        else: 
            return []

    def get_tract_income_pop(self, tract):
        """
        ARGS:
        tract or subtract number

        Returns a list of populations in different income ranges of the given
        tract, or the tract containing the given subtract. If not found, return
        empty list.
        The list is in the following form:
        [<10k, 10000-19999, 20000-34999, 35000-49999, 50000-74999, 75000+]
        """
        if tract in self.demographics_info:
            return self.demographics_info[tract]['income']
        else: 
            return []

    def get_all_tracts(self):
        all_tracts = set()
        for tract in self.demographics_info:
            all_tracts.add(tract)
        return all_tracts


class BlockCensusReader:
    def __init__(self):
        # GIS Data
        data_dir = os.path.join(constants.DATA_DIR, 'census_data', 'raw_block_data')
        with open(f'{data_dir}/blocks_2010.geojson', 'r') as f:
            geo_js = json.load(f)

        # Holds the geoJson feature and polygon for each tract
        self.shapes = [
            (feature, shape(feature['geometry']))
            for feature in geo_js['features']
        ]

        # Maps seen points to their tract num
        self.seen_points = {}

        with open(f'{CENSUS_DATA_DIR}/block_to_demographics.json', 'r') as f:
            self.demographics_info = json.load(f)
        
    def xy_to_block_num(self, longitude, latitude):
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
                block = feature['properties']['GEOID10']

                self.seen_points[h] = block
                return block

        self.seen_points[h] = -1
        return -1

    def get_tract_pop(self, block):
        """
        ARGS:
        block number

        Returns the population of the given block. If not found, returns -1.
        """
        tract = block[5:11]
        block_no = block[11:]
        if tract in self.demographics_info and block in self.demographics_info[tract]:
            return self.demographics_info[tract][block]['population']
        else:
            return -1
    
    def get_all_blocks():
        all_blocks = set()
        for tract in self.demographics_info:
            for block in self.demographics_info[tract]:
                all_blocks.add('53033' + tract + block)
        return all_blocks
