import os, sys
import json
import geojson
import copy
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parentdir)
from utils import constants

import pygeohash
from shapely.geometry import shape, Point

from scripts.census_structures import CensusFileParser

NAME = 'p0_census_tracts'

def merge_tracts_supertracts(pop_data, geo_js):
    possible_tracts = {}
    for tract in geo_js['features']:
        num = tract['properties']['TRACTCE20']
        possible_tracts[num] = [0, num]
        supertract = num[0:4] + '00'
        if supertract not in possible_tracts:
            possible_tracts[num[0:4] + '00'] = [0]
        possible_tracts[num[0:4] + '00'].append(num)
    
    for tract in pop_data:
        num = tract[3]
        supertract = num[0:4] + '00'
        if num in possible_tracts:
            possible_tracts[num][0] = 1
        elif supertract in possible_tracts:
            possible_tracts[supertract][0] = 1
            possible_tracts[supertract].append(num)
        else:
            print("Tract", num, "doesn't exist in geojs")

    final_tracts = {}
    for p_tract in possible_tracts:
        if possible_tracts[p_tract][0] == 1:
            if len(possible_tracts[p_tract]) == 2:
                supertract = p_tract[0:4] + '00'
                if possible_tracts[p_tract][1] in possible_tracts[supertract] and possible_tracts[supertract][0] == 1:
                    pass
                else:
                    final_tracts[p_tract] = set(possible_tracts[p_tract][1:])
            else:
                final_tracts[p_tract] = set(possible_tracts[p_tract][1:])
    del final_tracts['990100']
    return final_tracts


def create_merged_geojs(geo_js, final_tracts):
    new_geo_js = copy.deepcopy(geo_js)
    for feature in geo_js['features']:
        if feature['properties']['TRACTCE20'] == '990100':
            new_geo_js['features'].remove(feature)
    for tract in final_tracts:
        sub_tract_features = []
        for feature in geo_js['features']:
            if feature['properties']['TRACTCE20'] in final_tracts[tract]:
                sub_tract_features.append(feature)
        new_feature = sub_tract_features[0]
        for sub in sub_tract_features:
            geom = shape(new_feature['geometry'])
            curr_geom = shape(sub['geometry'])
            merged = geom.union(curr_geom)
            tr_name = str(float(tract)/100)
            if tr_name[-2:] == '.0':
                tr_name = tr_name[:-2]
            new_feature = geojson.Feature(id=tract, properties={'TRACT NUMBER':tr_name}, geometry=merged)
            new_geo_js['features'].remove(sub)
        new_geo_js['features'].append(new_feature)
 
    return new_geo_js


def merge_census_data(data, final_tracts):
    new_data = {}
    for tract in data:
        if tract in final_tracts:
            new_data[tract] = data[tract]
        else:
            supertract = tract[0:4] + '00'
            if supertract == '990100':
                continue
            if tract in final_tracts[supertract]:
                if supertract in new_data:
                    # need to add current and new values
                    for i in range(len(new_data[supertract])):
                        new_data[supertract][i] += data[tract][i]
                else:
                    new_data[supertract] = data[tract]
            else:
                print("Tract", tract, "doesn't exist in final_tracts")
    return new_data


def run_pipeline():
    # Run pipeline
    CENSUS_RT_DATA_DIR = os.path.join(constants.DATA_DIR, 'census_data', 'raw_data')
    CENSUS_RB_DATA_DIR = os.path.join(constants.DATA_DIR, 'census_data', 'raw_data')

    CENSUS_OUTPUT_DATA_DIR = os.path.join(constants.DATA_DIR, 'census_data', 'pipeline_output')

    with open(f'{CENSUS_RT_DATA_DIR}/tracts_2020.geojson', 'r') as f:
        geo_js = json.load(f)

    with open(f'{CENSUS_RT_DATA_DIR}/tract_population.json') as f:
        pop_data = json.load(f)[1:]

    final_tracts = merge_tracts_supertracts(pop_data, geo_js)

    pop_dict = CensusFileParser.tract_population_dict(f'{CENSUS_RT_DATA_DIR}/tract_population.json')
    age_dict = CensusFileParser.tract_age_dict(f'{CENSUS_RT_DATA_DIR}/gender_data.json')
    gender_dict = CensusFileParser.tract_gender_dict(f'{CENSUS_RT_DATA_DIR}/gender_data.json')
    race_dict = CensusFileParser.tract_race_dict(f'{CENSUS_RT_DATA_DIR}/race_data.json')
    income_dict = CensusFileParser.tract_income_dict(f'{CENSUS_RT_DATA_DIR}/income_data.json')
    disability_dict = CensusFileParser.tract_disability_dict(f'{CENSUS_RT_DATA_DIR}/disabilities_data.json')
    merged_pop_dict = merge_census_data(pop_dict, final_tracts)
    merged_age_dict = merge_census_data(age_dict, final_tracts)
    merged_gender_dict = merge_census_data(gender_dict, final_tracts)
    merged_race_dict = merge_census_data(race_dict, final_tracts)
    merged_income_dict = merge_census_data(income_dict, final_tracts)
    merged_disability_dict = merge_census_data(disability_dict, final_tracts)

    tract_dict = {}
    for tract in final_tracts:
        tract_dict[tract] = {}
        tr_name = str(float(tract)/100)
        if tr_name[-2:] == '.0':
            tr_name = tr_name[:-2]
        tract_dict[tract]['name'] = tr_name
        tract_dict[tract]['population'] = merged_pop_dict[tract][0]
        tract_dict[tract]['race'] = merged_race_dict[tract]
        tract_dict[tract]['gender'] = merged_gender_dict[tract]
        tract_dict[tract]['age'] = merged_age_dict[tract]
        tract_dict[tract]['income'] = merged_income_dict[tract]
        tract_dict[tract]['disability'] = merged_disability_dict[tract]

    with open(f'{CENSUS_OUTPUT_DATA_DIR}/tract_to_demographics_v2.json', 'w') as outfile:
        json.dump(tract_dict, outfile)

    new_geo_js = create_merged_geojs(geo_js, final_tracts)

    for feature in new_geo_js['features']:
        tract_info = tract_dict[feature['id']]
        feature['properties']['population'] = tract_info['population']
        feature['properties']['race'] = tract_info['race']
        feature['properties']['gender'] = tract_info['gender']
        feature['properties']['age'] = tract_info['age']
        feature['properties']['income'] = tract_info['income']
        feature['properties']['disability'] = tract_info['disability']

    with open(f'{CENSUS_OUTPUT_DATA_DIR}/tracts_demographics_v2.geojson', 'w') as outfile:
        json.dump(new_geo_js, outfile)


if __name__ == '__main__':
    run_pipeline()
