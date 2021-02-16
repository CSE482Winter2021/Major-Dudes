import json
from shapely.geometry import shape, GeometryCollection, Point

# Takes in longitude and latitude as coordinates in King County.
# Returns list of tracts that point is in or on the border of.
def xy_to_tract_num(longitude, latitude):
  with open('../data/tracts_2020.geojson', 'r') as f:
      js = json.load(f)

  # LONGITUDE, LATITUTE
  point = Point(longitude, latitude)
  found = False
  tract = []
  for feature in js['features']:
    polygon = shape(feature['geometry'])
    if polygon.contains(point) or polygon.intersection(point):
      tract.append(feature['properties']['NAME20'])
  if len(tract) == 1:
    print('Found coordinate in tract ', tract[0])
  elif len(tract) > 1:
    print('Found coordinate on border of tracts: ', tract)
  else:
    print('Coordinates not in King County')

  return tract
