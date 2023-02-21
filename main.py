'''Lab #1.2'''
import argparse
import folium
import pandas as pd
from geopy.exc import GeocoderUnavailable
from geopy.geocoders import Nominatim
from geopy.distance import geodesic as GD

parser = argparse.ArgumentParser()

parser.add_argument(
    'year',
    help = 'Year of film'
)
parser.add_argument(
    'latitude',
    help = 'Your latitude'
)
parser.add_argument(
    'longitude',
    help = 'Your longitude'
)
parser.add_argument(
    'path',
    help = 'Path to database'
)
parser.add_argument(
    'mydatapath',
    help = 'Path to database'
)

args = parser.parse_args()

def main(year, latitude, longitude, path, mydatapath):
    '''
    Creates map which that shows the closest to given point
    places where movies in a given year where shooted.
    '''
    _map = folium.Map(location=[float(latitude), float(longitude)], zoom_start=5)
    default_layer = folium.FeatureGroup(name='Default')
    movies_layer = folium.FeatureGroup(name='Movies')
    my_layer = folium.FeatureGroup(name='Help for Ukraine')

    data = pd.read_csv(path, sep=';')
    data = data.reset_index()

    mydata = pd.read_csv(mydatapath, sep=';')
    mydata = mydata.reset_index()

    geolocator = Nominatim(user_agent="Kohut_Map")
    locations = set()

    for index, row1 in data.iterrows():
        _a = index
        if row1.year == int(year):
            try:
                location = geolocator.geocode(row1.address)
            except GeocoderUnavailable:
                continue
            if location:
                if GD((location.latitude, location.longitude), \
                (float(latitude), float(longitude))).km < 1999:
                    locations.add((row1.movie, (location.latitude, location.longitude)))
            if len(locations) > 9:
                break
    for name, coords in locations:
        movies_layer.add_child(folium.Marker(location=[coords[0], coords[1]],
                                             popup=name,
                                             icon=folium.Icon()))

    for index, row2 in mydata.iterrows():
        country_c = geolocator.geocode(row2.country)
        my_layer.add_child(folium.Marker(location=[country_c.latitude, country_c.longitude],
                                        popup=row2.country + ':' + row2.money + 'B dollars',
                                        icon=folium.Icon(color = "green")))

    default_layer.add_child(folium.Marker(location=[float(latitude), float(longitude)],
                                          popup='Your location.',
                                          icon=folium.Icon(color = "red")))
    default_layer.add_to(map)
    movies_layer.add_to(map)
    my_layer.add_to(map)
    folium.LayerControl(collapsed=False).add_to(map)
    _map.save('test.html')
    if not locations:
        print('No movies which suit your data.')

if __name__ == '__main__':
    main(args.year, args.latitude, args.longitude, args.path, args.mydatapath)
