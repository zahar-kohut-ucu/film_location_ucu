'''Lab #1.2'''
import argparse
import folium
import pandas as pd

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

def main():
    '''Main function.'''
    a = args.year
    map = folium.Map(tiles="Stamen Terrain")
    map.save('test.html')


if __name__ == '__main__':
    main()