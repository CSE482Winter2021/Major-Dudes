import os, sys
import json
import geojson
import copy
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parentdir)
from utils import constants

import pygeohash
from shapely.geometry import shape, Point

CENSUS_DATA_DIR = os.path.join(constants.DATA_DIR, 'census_data')

with open(f'{CENSUS_DATA_DIR}/tracts_2020.geojson', 'r') as f:
    geo_js = json.load(f)

with open(f'{CENSUS_DATA_DIR}/tract_population.json') as f:
    pop_data = json.load(f)

pop_data = pop_data[1:]
tract_pops = {}
super_tract_pops = {}

for i in range(len(pop_data)):
    tr = pop_data[i]
    tract_pops[tr[3]] = int(tr[0])
    if tr[3][0:4] in super_tract_pops:
        super_tract_pops[tr[3][0:4]].append(tr[3])
    else:
        super_tract_pops[tr[3][0:4]] = [tr[3]]

with open(f'{CENSUS_DATA_DIR}/race_data.json') as f:
    race_data = json.load(f)
race_data = race_data[1:]
# Map from tract num to list:
#   [White Only, Black Only, Native Only, Asian Only,
#   Pacific Islander Only, Other Only, White-Mix, Black-Mix,
#   Native-Mix, Asian-Mix, Pacific Islander-Mix, Other-Mix]
tract_race = {}
for i in range(len(race_data)):
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
    tract_race[tr[len(tr) - 1]] = tr_race_data

# Gender & Age data
with open(f'{CENSUS_DATA_DIR}/gender_data.json') as f:
    gender_data = json.load(f)
gender_data = gender_data[1:]
tract_gender = {}
tract_age = {}
for i in range(len(gender_data)):
    tr = gender_data[i]
    tract_gender[tr[len(tr) - 1]] = [int(tr[0]), int(tr[24])]

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
    tract_age[tr[len(tr) - 1]] = tr_age_data

# Income data
with open(f'{CENSUS_DATA_DIR}/income_data.json') as f:
    income_data = json.load(f)
income_data = income_data[1:]
# Map from tract num to list:
#   [<10k, 10000-19999, 20000-34999, 35000-49999, 50000-74999, 75000+]
tract_income = {}
for i in range(len(income_data)):
    tr = income_data[i]
    tr_income_data = [
        int(tr[0]), int(tr[1]), int(tr[2]),
        int(tr[3]), int(tr[4]), int(tr[5])
    ]
    tract_income[tr[len(tr) - 1]] = tr_income_data

# Disability data
with open(f'{CENSUS_DATA_DIR}/disabilities_data.json') as f:
    disability_data = json.load(f)
disability_data = disability_data[1:]

# Map from tract num to list:
#   [disabled < 18, disabled 18-64, disabled 65+]
tract_disability = {}
for i in range(len(disability_data)):
    tr = disability_data[i]
    tr_disability_data = [int(tr[0]) + int(tr[3]) + int(tr[6]),
                          int(tr[1]) + int(tr[4]) + int(tr[7])]
    tract_disability[tr[len(tr) - 1]] = tr_disability_data







# Some sub-tracts in the geography data don't align with the sub-tracts in the 
# demographics data In order to clean this, we map from a list of sub-tracts in 
# each super-tract in the geo data to a list of sub-tracts in that super-tract 
# in the demo data.
s_to_tract = {}
for feature in geo_js['features']:
    tract = feature['properties']['TRACTCE20']
    supertract = tract[0:4]
    if tract in tract_pops or supertract in super_tract_pops:
        if tuple(super_tract_pops[supertract]) not in s_to_tract:
            s_to_tract[tuple(super_tract_pops[supertract])] = []
        s_to_tract[tuple(super_tract_pops[supertract])].append(tract)

# If the sub-tracts per super tract in the geo data 
# doesn't align with the sub-tracts per super in the demo data,
# we need to reduce all sub-tracts to a single super tract.
# Combine all sub-tract demographics into one and union geographies to one super
new_geo_js = copy.deepcopy(geo_js)
tract_to_demos = {}
for supertract_list in s_to_tract:
    if tuple(s_to_tract[supertract_list]) != supertract_list:
        supertract = supertract_list[0][0:4] + '00'
        
        # total population
        population = 0
        race = [0,0,0,0,0,0,0,0,0,0,0,0]
        gender = [0,0]
        age = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        income = [0,0,0,0,0,0]
        disabilities = [0,0]
        for sub in supertract_list:
            population += int(tract_pops[sub])
            race = [race[i] + tract_race[sub][i] for i in range(len(race))]
            gender = [gender[i] + tract_gender[sub][i] for i in range(len(gender))]
            age = [age[i] + tract_age[sub][i] for i in range(len(age))]
            income = [income[i] + tract_income[sub][i] for i in range(len(income))]
            disabilities = [disabilities[i] + tract_disability[sub][i] for i in range(len(disabilities))]
        
        sub_tract_features = []
        for feature in geo_js['features']:
            if feature['properties']['TRACTCE20'] in s_to_tract[supertract_list]:
                sub_tract_features.append(feature)
        assert(len(sub_tract_features) > 0)
        new_feature = sub_tract_features[0]
        for feature in sub_tract_features:
            new_geo_js['features'].remove(feature)
            geom = shape(new_feature['geometry'])
            curr_geom = shape(feature['geometry'])
            merged = geom.union(curr_geom)
            new_feature = geojson.Feature(id=supertract, properties={}, geometry=merged)
        new_feature['properties']['TRACT_NAME'] = str(int(supertract[0:4]))
        new_feature['properties']['POPULATION'] = population
        new_feature['properties']['RACE'] = race
        new_feature['properties']['GENDER'] = gender
        new_feature['properties']['AGE'] = age
        new_feature['properties']['INCOME'] = income
        new_feature['properties']['DISABILITY'] = disabilities

        new_geo_js['features'].append(new_feature)
        tract_to_demos[supertract] = {'name': str(int(supertract[0:4])), 'population': population, 'race': race, 'gender': gender, 'age': age, 'income': income, 'disability': disabilities}
    else:
        for feature in geo_js['features']:
            if feature['properties']['TRACTCE20'] in s_to_tract[supertract_list]:
                # print(feature['properties']['TRACTCE20'])
                new_feature = geojson.Feature(id=feature['properties']['TRACTCE20'], properties={}, geometry=shape(feature['geometry']))
                new_feature['properties']['TRACT_NAME'] = feature['properties']['NAME20']
                new_feature['properties']['POPULATION'] = tract_pops[feature['properties']['TRACTCE20']]
                new_feature['properties']['RACE'] = tract_race[feature['properties']['TRACTCE20']]
                new_feature['properties']['GENDER'] = tract_gender[feature['properties']['TRACTCE20']]
                new_feature['properties']['AGE'] = tract_age[feature['properties']['TRACTCE20']]
                new_feature['properties']['INCOME'] = tract_income[feature['properties']['TRACTCE20']]
                new_feature['properties']['DISABILITY'] = tract_disability[feature['properties']['TRACTCE20']]

                new_geo_js['features'].remove(feature)
                new_geo_js['features'].append(new_feature)
                tract_to_demos[feature['properties']['TRACTCE20']] = {'name': feature['properties']['NAME20'], 'population': tract_pops[feature['properties']['TRACTCE20']], 'race': tract_race[feature['properties']['TRACTCE20']], 'gender': tract_gender[feature['properties']['TRACTCE20']], 'age': tract_age[feature['properties']['TRACTCE20']], 'income': tract_income[feature['properties']['TRACTCE20']], 'disability': tract_disability[feature['properties']['TRACTCE20']]}

with open('tracts_demographics.geojson', 'w') as outfile:
    json.dump(new_geo_js, outfile)
outfile.close()

with open('tract_to_demographics.json', 'w') as outfile:
    json.dump(tract_to_demos, outfile)
outfile.close()

# print(super_tract_pops)
# poly1 = shape(geo_js['features'][0]['geometry'])
# poly2 = shape(geo_js['features'][1]['geometry'])

# mergedPolygon = poly1.union(poly2)
# geojson_out = geojson.Feature(geometry=mergedPolygon, properties={})