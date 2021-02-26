import os
import json

import pygeohash
from shapely.geometry import shape, Point

from utils import constants


CENSUS_DATA_DIR = os.path.join(constants.DATA_DIR, 'census_data')


class CensusReader:

    def __init__(self):

        # GIS Data
        with open(f'{CENSUS_DATA_DIR}/tracts_2020.geojson', 'r') as f:
            geo_js = json.load(f)

        # Holds the geoJson feature and polygon for each tract
        self.shapes = [
            (feature, shape(feature['geometry']))
            for feature in geo_js['features']
        ]

        # Maps seen points to their tract num
        self.seen_points = {}

        # Total population data
        with open(f'{CENSUS_DATA_DIR}/tract_population.json') as f:
            pop_data = json.load(f)

        # Maps tract nums to their population
        self.tract_pops = {}
        for i in range(len(pop_data)):
            if i != 0:
                tr = pop_data[i]
                self.tract_pops[tr[len(tr) - 1]] = int(tr[0])

        # Race data
        with open(f'{CENSUS_DATA_DIR}/race_data.json') as f:
            race_data = json.load(f)

        # Map from tract num to list:
        #   [White Only, Black Only, Native Only, Asian Only,
        #   Pacific Islander Only, Other Only, White-Mix, Black-Mix,
        #   Native-Mix, Asian-Mix, Pacific Islander-Mix, Other-Mix]
        self.tract_race = {}
        for i in range(len(race_data)):
            if i != 0:
                tr = race_data[i]
                tr_race_data = [
                    int(tr[0]), int(tr[1]),
                    int(tr[2]), int(tr[3]),
                    int(tr[4]), int(tr[5]),
                    int(tr[6]) - int(tr[0]),
                    int(tr[7]) - int(tr[1]),
                    int(tr[8]) - int(tr[2]),
                    int(tr[9]) - int(tr[3]),
                    int(tr[10]) - int(tr[4]),
                    int(tr[11]) - int(tr[5])
                ]
                self.tract_race[tr[len(tr) - 1]] = tr_race_data

        # Gender & Age data
        with open(f'{CENSUS_DATA_DIR}/gender_data.json') as f:
            gender_data = json.load(f)

        # Map from tract num to list:
        #   [Male, Female]
        self.tract_gender = {}

        # Map from tract num to list:
        #   [<5, 5-9, 10-14, 15-17, 18-19, 20, 21, 22-24, 25-29, 30-34,
        #    35-39, 40-44, 45-49, 50-54, 55-59, 60-61, 62-64, 65-66,
        #    67-69, 70-74, 75-79, 80-84, 85+]
        self.tract_age = {}
        for i in range(len(gender_data)):
            if i != 0:
                tr = gender_data[i]
                self.tract_gender[tr[len(tr) - 1]] = [int(tr[0]), int(tr[24])]

                tr_age_data = [
                    int(tr[1]) + int(tr[25]), int(tr[2]) + int(tr[26]),
                    int(tr[3]) + int(tr[27]), int(tr[4]) + int(tr[28]),
                    int(tr[5]) + int(tr[29]), int(tr[6]) + int(tr[30]),
                    int(tr[7]) + int(tr[31]), int(tr[8]) + int(tr[32]),
                    int(tr[9]) + int(tr[33]), int(tr[10]) + int(tr[34]),
                    int(tr[11]) + int(tr[35]), int(tr[12]) + int(tr[36]),
                    int(tr[13]) + int(tr[37]), int(tr[14]) + int(tr[38]),
                    int(tr[15]) + int(tr[39]), int(tr[16]) + int(tr[40]),
                    int(tr[17]) + int(tr[41]), int(tr[18]) + int(tr[42]),
                    int(tr[19]) + int(tr[43]), int(tr[20]) + int(tr[44]),
                    int(tr[21]) + int(tr[45]), int(tr[22]) + int(tr[46]),
                    int(tr[23]) + int(tr[47])
                ]
                self.tract_age[tr[len(tr) - 1]] = tr_age_data

        # Income data
        with open(f'{CENSUS_DATA_DIR}/income_data.json') as f:
            income_data = json.load(f)

        # Map from tract num to list:
        #   [<10k, 10000-19999, 20000-34999, 35000-49999, 50000-74999, 75000+]
        self.tract_income = {}
        for i in range(len(income_data)):
            if i != 0:
                tr = income_data[i]
                tr_income_data = [
                    int(tr[0]), int(tr[1]), int(tr[2]),
                    int(tr[3]), int(tr[4]), int(tr[5])
                ]
                self.tract_income[tr[len(tr) - 1]] = tr_income_data

        # Disability data
        with open(f'{CENSUS_DATA_DIR}/disabilities_data.json') as f:
            disability_data = json.load(f)

        # Map from tract num to list:
        #   [disabled < 18, disabled 18-64, disabled 65+]
        self.tract_disability = {}
        for i in range(len(disability_data)):
            if i != 0:
                tr = disability_data[i]
                tr_disability_data = [int(tr[0]) + int(tr[3]) + int(tr[6]), 
                                      int(tr[1]) + int(tr[4]) + int(tr[7])]
                self.tract_disability[tr[len(tr) - 1]] = tr_disability_data

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

        supertract = tract[:len(tract) - 2] + '00'

        if supertract in self.tract_pops:
            return self.tract_pops[supertract]

        return -1

    def get_tract_age_pop(self, tract):
        """
        ARGS:
        tract or subtract number

        Returns an array of populations per age group of the given tract, 
        or the tract containing the given subtract. If not found, returns empty list.
        The list is in the following form:
        [< 5, 5-9, 10-14, 15-17, 18-19, 20, 21, 22-24, 25-29, 30-34, 35-39, 40-44, 
        45-49, 50-54, 55-59, 60-61, 62-64, 65-66, 67-69, 70-74, 75-79, 80-84, 85+]
        """

        if tract in self.tract_age:
            return self.tract_age[tract]

        supertract = tract[:len(tract) - 2] + '00'
        
        if supertract in self.tract_age:
            return self.tract_age[supertract]

        return []
        
    def get_tract_gender_pop(self, tract):
        """
        ARGS:
        tract or subtract number

        Returns a list of populations per gender of the given tract, 
        or the tract containing the given subtract. If not found, returns empty list.
        The list is in the following form:
        [Population Male, Population Female]
        """

        if tract in self.tract_gender:
            return self.tract_gender[tract]

        supertract = tract[:len(tract) - 2] + '00'

        if supertract in self.tract_gender:
            return self.tract_gender[supertract]

        return []

    def get_tract_race_pop(self, tract):
        """
        ARGS:
        tract or subtract number

        Returns a list of populations per race of the given tract, 
        or the tract containing the given subtract. If not found, returns empty list.
        The list is in the following form:
        [ White Only, Black Only, Native Only, Asian Only, Hawaiian/Pacific Islander Only, 
          Other Only, Multiracial White, Multiracial Black, Multiracial Native, 
          Multiracial Asian, Multiracial Hawaiian/Pacific Islander, Multiracial Other ]
        """

        if tract in self.tract_race:
            return self.tract_race[tract]

        supertract = tract[:len(tract) - 2] + '00'

        if supertract in self.tract_race:
            return self.tract_race[supertract]

        return []

    def get_tract_disabled_pop(self, tract):
        """
        ARGS:
        tract or subtract number

        Returns a list of populations with one disability and 2+ disabilities of the given tract, 
        or the tract containing the given subtract. If not found, returns empty list.
        The list is in the following form:
        [1 disability, 2+ disabilities]
        """

        if tract in self.tract_disability:
            return self.tract_disability[tract]

        supertract = tract[:len(tract) - 2] + '00'

        if supertract in self.tract_disability:
            return self.tract_disability[supertract]

        return []

    def get_tract_income_pop(self, tract):
        """
        ARGS:
        tract or subtract number

        Returns a list of populations in different income ranges of the given tract, 
        or the tract containing the given subtract. If not found, returns empty list.
        The list is in the following form:
        [<10k, 10000-19999, 20000-34999, 35000-49999, 50000-74999, 75000+]
        """

        if tract in self.tract_income:
            return self.tract_income[tract]

        supertract = tract[:len(tract) - 2] + '00'

        if supertract in self.tract_income:
            return self.tract_income[supertract]

        return []
