from bs4 import BeautifulSoup
from geopy.geocoders import GoogleV3
import requests
import re
import accommodation
import sqlite3


def search(location, bedrooms, ppm, is_furnished):
    houses_afs = construct_afs_url(location, bedrooms, ppm, is_furnished)
    if location == "bristol":
        rightmove_location = "5E219"
    houses_rightmove = construct_rightmove_url(rightmove_location, bedrooms, ppm, is_furnished)

    return houses_afs + houses_rightmove


def construct_rightmove_url(location, bedrooms, price, is_furnished):
    url = "http://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%{LOCATION}&maxBedrooms="\
            "{MAX_BEDROOMS}&minBedrooms={MAX_BEDROOMS}&maxPrice={MAX_PRICE}&includeLetAgreed=false&furnishTypes="\
            "{IS_FURNISHED}&letType=student"

    query_url = url.replace("{LOCATION}", location)  # THIS WILL NEED A HELPER METHOD

    bedrooms = str(bedrooms)

    query_url = query_url.replace("{MAX_BEDROOMS}", bedrooms)

    price = str(price)

    query_url = query_url.replace("{MAX_PRICE}", price)

    if is_furnished is True:
        query_url = query_url.replace("{IS_FURNISHED}", "furnished")
    else:
        query_url = query_url.replace("{IS_FURNISHED}", "unfurnished")

    print(query_url)

    return get_rightmove_houses(query_url)


def construct_afs_url(location, bedrooms, price, is_furnished):
    url = "http://www.accommodationforstudents.com/searchresults.asp?lookingfor=any&city={LOCATION}&numberofbedrooms="\
            "{MAX_BEDROOMS}&cost={MAX_PRICE}&searchtype=city&street=&postcode=&area=&orderby=latest&bills_included="\
            "{IS_FURNISHED}&x=29&y=24&perpage=200"

    query_url = url.replace("{LOCATION}", location)

    bedrooms = str(bedrooms)

    query_url = query_url.replace("{MAX_BEDROOMS}", bedrooms)

    monthly_price = int(price)

    weekly_price = int((monthly_price * 12) / 52)

    weekly_price = str(weekly_price)

    query_url = query_url.replace("{MAX_PRICE}", weekly_price)

    if is_furnished is True:
        query_url = query_url.replace("{IS_FURNISHED}", "1")
    else:
        query_url = query_url.replace("{IS_FURNISHED}", "0")

    print(query_url)

    return get_afs_houses(query_url, bedrooms)


def get_afs_houses(url, bedrooms):
    result = requests.get(url)
    page = result.content
    soup = BeautifulSoup(page, "html.parser")

    link_list = create_afs_links(soup, bedrooms)

    house_list = []

    for link in link_list:
        conn = sqlite3.connect("houses.db")
        c = conn.cursor()

        c.execute('''SELECT * FROM accommodations WHERE url=?''', (link,))

        result = c.fetchone()

        if result is None:

            data_list = get_soups(link_list)

            for i in range(len(data_list)):
                house = create_afs_house(data_list[i], link_list[i], bedrooms)

                add_house_to_db(house)

                house_list.append(house)

        else:

            house = accommodation.Accommodation(result[1], result[2], result[3], result[6], result[0])
            house.lat = result[4]
            house.long = result[4]
            house_list.append(house)

    return house_list

# def get_house_from_db(url):


def create_afs_house(soup, url, bedrooms):
    price = soup.find("div", class_="style12x")
    price = price.text
    price = re.search('£(.*)pw', price)
    price = price.group(1)
    price = int(price)
    price = int((price * 52) / 12)
    print(price)

    pattern = re.compile('[A-Z]{1,2}[0-9][0-9A-Z]?\s?[0-9][A-Z]{2}')

    location_string = soup.find(text=pattern)
    location_string = str(location_string.string)
    location_string = re.sub(r'\([^)]*\)', '', location_string)

    geolocator = GoogleV3()
    location = geolocator.geocode(location_string)
    print(location.latitude)
    print(location.longitude)

    furnished = soup.find(text=re.compile("Furnished"))

    house = accommodation.Accommodation(price, bedrooms, "UNSURE", 1, url)
    house.lat = location.latitude
    house.long = location.longitude

    return house


def create_afs_links(soup, bedrooms):
    link_list = []
    for item in soup.find_all("span", class_="style13y"):
        no_of_bedrooms = str(item.contents[0].string)
        no_of_bedrooms = no_of_bedrooms.rsplit("bed", 1)[0]
        no_of_bedrooms = no_of_bedrooms.strip()
        if no_of_bedrooms == bedrooms:
            link_list.append("http://www.accommodationforstudents.com" + item.parent.attrs["href"])
    return link_list


def get_rightmove_houses(url):

    result = requests.get(url)
    page = result.content
    soup = BeautifulSoup(page, "html.parser")

    link_list = create_rightmove_links(soup)
    house_list = []

    for link in link_list:
        conn = sqlite3.connect("houses.db")
        c = conn.cursor()

        c.execute('''SELECT * FROM accommodations WHERE url=?''', (link,))

        result = c.fetchone()

        if result is None:

            soup_list = get_soups(link_list)

            for item in soup_list:

                house = create_rightmove_house(item)

                add_house_to_db(house)

                house_list.append(house)
        else:

            house = accommodation.Accommodation(result[1], result[2], result[3], result[6], result[0])
            house.lat = result[4]
            house.long = result[4]
            house_list.append(house)
    return house_list

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


def get_soups(link_list):
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


# init_db()
#
# construct_afs_url("bristol", "4", "500", False)
#
# construct_rightmove_url("5E219", "4", "500", False)

