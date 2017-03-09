# coding=utf-8
import requests
import sqlite3
from bs4 import BeautifulSoup

import rightmove_outcodes
from construct_url import construct_rightmove_url, construct_afs_url
from get_houses import get_zoopla_houses


# Searches all APIs/websites based on input criteria
def search(location, bedrooms, ppm, is_furnished, bills_inc):
    houses_zoopla = get_zoopla_houses(location, bedrooms, ppm, bills_inc)
    houses_afs = construct_afs_url(location, bedrooms, ppm, is_furnished, bills_inc)
    rightmove_locations = rightmove_outcodes.create_dictionary()

    rightmove_code = rightmove_locations[location.casefold()]  # Rightmove uses outcodes for location

    houses_rightmove = construct_rightmove_url(rightmove_code, bedrooms, ppm, is_furnished)

    return houses_afs + houses_rightmove + houses_zoopla

# Returns parsable objects of webpages
def get_soups(link_list):
    soup_list = []
    for link in link_list:
        result = requests.get(link)
        page = result.content
        soup_list.append(BeautifulSoup(page, "html.parser"))
        print("request")
    return soup_list


# Initiate database if needed
def init_db():
    conn = sqlite3.connect("houses.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS accommodations
                (url text PRIMARY KEY, ppm int, bedrooms int, bills_inc text, lat real, long real, address text, is_furnished int)''')


def add_house_to_db(house):
    conn = sqlite3.connect("houses.db")
    c = conn.cursor()

    print(house.url)
    c.execute('INSERT INTO accommodations VALUES (?,?,?,?,?,?,?,?)',
              (house.url, house.ppm, house.bedrooms, house.bills_inc, house.lat, house.long, house.address, house.is_furnished))

    conn.commit()


# init_db()
#
# construct_afs_url("bristol", "4", "500", False)
#
# construct_rightmove_url("5E219", "4", "500", False)

