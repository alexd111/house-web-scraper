import requests
import sqlite3
from bs4 import BeautifulSoup
from geopy import GoogleV3

import accommodation
import create_house
import create_link
import web_scraper


def get_zoopla_houses(location, bedrooms, price, bills_inc):
    house_list = []
    monthly_price = int(price)

    weekly_price = int((monthly_price * 12) / 52)

    parameters = {
        'area': location,
        'radius': 5,
        'listing_status': 'rent',
        'maximum_price': weekly_price,
        'minimum_beds': bedrooms,
        'maximum_beds': bedrooms,
        'api_key': 'zwqrekb5d6zawqmxud9bnpte'
    }

    r = requests.get('http://api.zoopla.co.uk/api/v1/property_listings.js', params=parameters)

    result = r.json()

    for item in result['listing']:
        print(item['details_url'])

        conn = sqlite3.connect("houses.db")
        c = conn.cursor()

        house_url = item['details_url']
        house_bedrooms = int(item['num_bedrooms'])
        house_price = item['rental_prices']['per_month']
        house_bills = bills_inc
        house_lat = item['latitude']
        house_long = item['longitude']

        geolocator = GoogleV3()
        house_location = geolocator.geocode(item['displayable_address'])
        if house_location is None:
            house = accommodation.Accommodation(house_price, house_bedrooms, house_bills, item['displayable_address'],
                                                "UNSURE", house_url)
        else:
            house = accommodation.Accommodation(house_price, house_bedrooms, house_bills, house_location.address, "UNSURE", house_url)
        house.lat = house_lat
        house.long = house_long

        c.execute('''SELECT * FROM accommodations WHERE url=?''', (house_url,))

        result = c.fetchone()

        if result is None:  # Check if house is not already in database
            web_scraper.add_house_to_db(house)
            house_list.append(house)
        else:
            house = accommodation.Accommodation(result[1], result[2], result[3], result[6], result[7], result[0])
            house.lat = result[4]
            house.long = result[4]
            house_list.append(house)

        return house_list


def get_afs_houses(url, bedrooms):
    result = requests.get(url)
    page = result.content
    soup = BeautifulSoup(page, "html.parser")

    link_list = create_link.create_afs_links(soup, bedrooms)

    house_list = []

    for link in link_list:
        conn = sqlite3.connect("houses.db")
        c = conn.cursor()

        c.execute('''SELECT * FROM accommodations WHERE url=?''', (link,))

        result = c.fetchone()

        if result is None: # Check if house is not already in database

            data_list = web_scraper.get_soups(link_list)

            for i in range(len(data_list)):
                house = create_house.create_afs_house(data_list[i], link_list[i], bedrooms)

                web_scraper.add_house_to_db(house)

                house_list.append(house)

        else:

            house = accommodation.Accommodation(result[1], result[2], result[3], result[6], result[7], result[0])
            house.lat = result[4]
            house.long = result[4]
            house_list.append(house)

    return house_list


def get_rightmove_houses(url):

    result = requests.get(url)
    page = result.content
    soup = BeautifulSoup(page, "html.parser")

    link_list = create_link.create_rightmove_links(soup)
    house_list = []

    for link in link_list:
        conn = sqlite3.connect("houses.db")
        c = conn.cursor()

        c.execute('''SELECT * FROM accommodations WHERE url=?''', (link,))

        result = c.fetchone()

        if result is None: # Check if house is not already in database

            soup_list = web_scraper.get_soups(link_list)

            for item in soup_list:

                house = create_house.create_rightmove_house(item)

                web_scraper.add_house_to_db(house)

                house_list.append(house)
        else:

            house = accommodation.Accommodation(result[1], result[2], result[3], result[6], result[7], result[0])
            house.lat = result[4]
            house.long = result[4]
            house_list.append(house)

    return house_list