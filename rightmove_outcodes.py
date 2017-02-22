import csv
from geopy.geocoders import ArcGIS


def create_dictionary():
    outcodes = {
        'aberdeen': '5E4',
        'aberystwyth': '5E11',
        'aldershot': '5E22',
        'alfreton': '5E26',
        'ayr': '5E74',
        'bangor': '5E98',
        'barnsley': '5E108',
        'basildon': '5E114',
        'bath': '5E116',
        'bedford': '5E129',
        'belfast': '5E133',
        'bristol': '5E219'
                            }
    return outcodes


def read_in_csv():
    file = open('outcode.csv')
    csv_file = csv.reader(file)
    geolocator = ArcGIS()

    for row in csv_file:
        coordinate_string = row[1] + ", " + row[2]
        location = geolocator.reverse(coordinate_string)
        print(location.raw['City'])

# read_in_csv()
