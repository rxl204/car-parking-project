from pyproj import Proj, transform

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def svy21_to_lat_lon(data):
    svy21 = Proj(init='epsg:3414')  # Define SVY21 projection
    wgs84 = Proj(init='epsg:4326')  # Define WGS84 projection (latitude/longitude)
    data['lon'], data['lat'] = transform(svy21, wgs84, data['x_coord'], data['y_coord'])
    return data