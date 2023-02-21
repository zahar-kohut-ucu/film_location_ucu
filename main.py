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

args = parser.parse_args()

def main(year, latitude, longitude, path):
    '''Main function.'''
    map = folium.Map(location=[52.479618,62.185832], zoom_start=10)
    movies_layer = folium.FeatureGroup(name='Movies')
    data = pd.read_csv(path, sep=';')
    data = data.reset_index()
    geolocator = Nominatim(user_agent="Kohut_Map")
    locations = []
    for index, row in data.iterrows():
        if row.year == int(year):
            location = geolocator.geocode(row.address)
            if location:
                if GD((location.latitude, location.longitude), (float(latitude), float(longitude))).km < 3000:
                    locations.append((row.movie, (location.latitude, location.longitude)))
            if len(locations) > 6:
                break
    for name, coords in locations:
        movies_layer.add_child(folium.Marker(location=[coords[0], coords[1]],
                                             popup=name,
                                             icon=folium.Icon()))
    map.add_child(movies_layer)
    map.save('test.html')
    return None

if __name__ == '__main__':
    main(args.year, args.latitude, args.latitude, args.path)