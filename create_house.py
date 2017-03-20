import re
from geopy import GoogleV3

import accommodation

# All methods scan webpage objects for data needed for creating Accommodation objects

def create_afs_house(soup, url, bedrooms):
    price = soup.find("div", class_="style12x")
    price = price.text
    price = re.search('£(.*)pw', price)  # Find price per week
    price = price.group(1)
    price = int(price)
    price = int((price * 52) / 12)
    print(price)

    pattern = re.compile('[A-Z]{1,2}[0-9][0-9A-Z]?\s?[0-9][A-Z]{2}')  # Find postcode

    location_string = soup.find(text=pattern)
    location_string = str(location_string.string)
    location_string = re.sub(r'\([^)]*\)', '', location_string)  # Remove whitespace

    geolocator = GoogleV3()
    location = geolocator.geocode(location_string)
    print(location.latitude)
    print(location.longitude)

    furnished = soup.find(text=re.compile("Furnished"))

    house = accommodation.Accommodation(price, bedrooms, "UNSURE", location.address, 1, url)
    house.lat = location.latitude
    house.long = location.longitude

    return house


def create_rightmove_house(item):
    page_url = item.find("meta", property="og:url")
    page_url = page_url["content"]
    price = item.find(id="propertyHeaderPrice")

    if price is not None:
        price = price.text
        price = re.search('£(.*) pcm', price)  # Get price per month
        price = price.group(1)
        price = int(price)

    bedrooms = item.find(string=re.compile("bedroom"))
    bedrooms = str(bedrooms.string)
    print(page_url)
    print(bedrooms)
    bedrooms = bedrooms.rsplit("bedroom", 1)[0]
    bedrooms = bedrooms.strip()
    bedrooms = int(bedrooms)

    address = item.find("address", class_="pad-0 fs-16 grid-25")
    address_string = str(address.string)
    geolocator = GoogleV3()
    location = geolocator.geocode(address_string)

    if location is None:
        location = ""

    furnished_type = item.find(id="furnishedType")
    furnished_string = str(furnished_type.string)
    is_furnished = 0
    if furnished_string == "Furnished":
        is_furnished = 1

    house = accommodation.Accommodation(price, bedrooms, "UNSURE", location.address, is_furnished, page_url)
    house.lat = location.latitude
    house.long = location.longitude
    return house
