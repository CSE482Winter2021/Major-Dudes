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

def run_pipeline():
    # Run pipeline
    CENSUS_RT_DATA_DIR = os.path.join(constants.DATA_DIR, 'census_data', 'raw_data')
    CENSUS_RB_DATA_DIR = os.path.join(constants.DATA_DIR, 'census_data', 'raw_block_data')

    CENSUS_OUTPUT_DATA_DIR = os.path.join(constants.DATA_DIR, 'census_data', 'pipeline_output')
    

    with open(f'{CENSUS_RB_DATA_DIR}/blocks_2010.json', 'r') as f:
        geo_js = json.load(f)

    with open(f'{CENSUS_RB_DATA_DIR}/total_b_population.json', 'r') as f:
        pop_data = json.load(f)[1:]

    pop_dict = CensusFileParser.block_population_dict(f'{CENSUS_RB_DATA_DIR}/total_b_population.json')
    age_dict = CensusFileParser.block_age_dict(f'{CENSUS_RB_DATA_DIR}/gender_b_data.json')
    gender_dict = CensusFileParser.block_gender_dict(f'{CENSUS_RB_DATA_DIR}/gender_b_data.json')
    race_dict = CensusFileParser.block_race_dict(f'{CENSUS_RB_DATA_DIR}/race_b_data.json')
    income_dict = CensusFileParser.block_income_dict(f'{CENSUS_RB_DATA_DIR}/income_bg_data.json')

    tract_block_dict = {}
    for tract in pop_dict:
        tract_block_dict[tract] = {}
        for block in pop_dict[tract]:
            if block not in tract_block_dict[tract]:
                tract_block_dict[tract][block] = {}
            tract_block_dict[tract][block]['population'] = pop_dict[tract][block][0]
            if block in race_dict[tract]:
                tract_block_dict[tract][block]['race'] = race_dict[tract][block]
            else: 
                tract_block_dict[tract][block]['race'] = []
            if block in gender_dict[tract]:
                tract_block_dict[tract][block]['gender'] = gender_dict[tract][block]
            else: 
                tract_block_dict[tract][block]['gender'] = []
            if block in age_dict[tract]:
                tract_block_dict[tract][block]['age'] = age_dict[tract][block]
            else: 
                tract_block_dict[tract][block]['age'] = []

    with open(f'{CENSUS_OUTPUT_DATA_DIR}/block_to_demographics.json', 'w') as outfile:
        json.dump(tract_block_dict, outfile)


if __name__ == '__main__':
    run_pipeline()
