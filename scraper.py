from bs4 import BeautifulSoup
from geopy.geocoders import GoogleV3
import requests
import re
import accommodation
import sqlite3


def construct_rightmove_url(location, bedrooms, price, is_furnished):
    url = "http://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%{LOCATION}&maxBedrooms="\
        "{MAX_BEDROOMS}&minBedrooms={MAX_BEDROOMS}&maxPrice={MAX_PRICE}&includeLetAgreed=false&furnishTypes={IS_FURNISHED}"\
        "&letType=student"

    query_url = url.replace("{LOCATION}", location)  # THIS WILL NEED A HELPER METHOD

    query_url = query_url.replace("{MAX_BEDROOMS}", bedrooms)

    query_url = query_url.replace("{MAX_PRICE}", price)

    if is_furnished is True:
        query_url = query_url.replace("{IS_FURNISHED}", "furnished")
    else:
        query_url = query_url.replace("{IS_FURNISHED}", "unfurnished")

    print(query_url)

    get_rightmove_houses(query_url)


def get_rightmove_houses(url):
    result = requests.get(url)
    page = result.content
    soup = BeautifulSoup(page, "html.parser")

    link_list = create_rightmove_links(soup)

    for link in link_list:
        conn = sqlite3.connect("houses.db")
        c = conn.cursor()

        c.execute('''SELECT * FROM accommodations WHERE url=?''', (link,))

        result = c.fetchone()

        if result is None:

            soup_list = get_rightmove_soups(link_list)

            for item in soup_list:

                house = create_rightmove_house(item)

                add_house_to_db(house)


def create_rightmove_house(item):
    page_url = item.find("meta", property="og:url")
    page_url = page_url["content"]
    price = item.find(id="propertyHeaderPrice")

    if price is not None:
        price = price.text
        price = re.search('£(.*) pcm', price)
        price = price.group(1)
        price = int(price)

    bedrooms = item.find(string=re.compile("bedroom"))
    bedrooms = str(bedrooms.string)
    bedrooms = bedrooms.rsplit("bedroom", 1)[0]
    bedrooms = bedrooms.strip()
    bedrooms = int(bedrooms)

    address = item.find("address", class_="pad-0 fs-16 grid-25")
    address_string = str(address.string)
    geolocator = GoogleV3()
    location = geolocator.geocode(address_string)

    furnished_type = item.find(id="furnishedType")
    furnished_string = str(furnished_type.string)
    is_furnished = 0
    if furnished_string == "Furnished":
        is_furnished = 1

    house = accommodation.Accommodation(price, bedrooms, "UNSURE", is_furnished, page_url)
    house.lat = location.latitude
    house.long = location.longitude
    return house


def get_rightmove_soups(link_list):
    soup_list = []
    for link in link_list:
        result = requests.get(link)
        page = result.content
        soup_list.append(BeautifulSoup(page, "html.parser"))
        print("request")
    return soup_list


def create_rightmove_links(soup):
    link_list = []
    for link in soup.find_all("a", "propertyCard-link"):

        if link.get("href") != "/property-for-sale/property-0.html":
            link_list.append("http://www.rightmove.co.uk" + link.get("href"))
    link_list = set(link_list)
    return link_list


def init_db():
    conn = sqlite3.connect("houses.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS accommodations
                (url text PRIMARY KEY, ppm int, bedrooms int, bills_inc text, lat real, long real, is_furnished int)''')


def add_house_to_db(house):
    conn = sqlite3.connect("houses.db")
    c = conn.cursor()

    # row = [(house.url, house.ppm, house.bedrooms, house.bills_inc, house.lat, house.long, house.is_furnished)]

    c.execute('INSERT INTO accommodations VALUES (?,?,?,?,?,?,?)',
              (house.url, house.ppm, house.bedrooms, house.bills_inc, house.lat, house.long, house.is_furnished))

    conn.commit()


init_db()

construct_rightmove_url("5E219", "4", "400", True)

