import json
import csv
from shapely.geometry import shape, GeometryCollection, Point

population_data = list(csv.reader(
    open('../data/tract_population.csv', "r"), delimiter=","))

with open('../data/tracts_2020.geojson', 'r') as f:
    geo_js = json.load(f)


def xy_to_tract_num(longitude, latitude):
    # ARGS:
    # longitude of coordinate in King County
    # latitude of coordinate in King Count
    #
    # Returns list of tracts that point is in or on the border of

    point = Point(longitude, latitude)
    found = False
    tract = []
    for feature in geo_js['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point) or polygon.intersection(point):
            tract.append(feature['properties']['TRACTCE20'])
    if len(tract) == 1:
        print('Found coordinate in tract ', tract[0])
    elif len(tract) > 1:
        print('Found coordinate on border of tracts: ', tract)
    else:
        print('Coordinates not in King County')

    return tract


def xy_to_tract_population(longitude, latitude):
    # ARGS:
    # longitude of coordinate in King County
    # latitude of coordinate in King Count
    #
    # Returns a dictionary from tract number to population of the tract to which this coordinate belongs

    tract = xy_to_tract_num(longitude, latitude)
    if len(tract) == 0:
        return None
    tract_no = tract[0]
    subtract_no = tract_no.replace(
        tract_no[len(tract_no) - 1], '0').replace(tract_no[len(tract_no) - 2], '0')
    ret = {}

    for tr in population_data:
        print(tr[4])
        if tr[4] == tract_no or tr[4] == subtract_no:
            ret[tr[4]] = tr[0]

    return ret
