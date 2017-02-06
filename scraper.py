from bs4 import BeautifulSoup
from geopy.geocoders import GoogleV3
import requests
import re

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
    link_list = []

    for link in soup.find_all("a", "propertyCard-link"):

        if link.get("href") != "/property-for-sale/property-0.html":

            link_list.append("http://www.rightmove.co.uk/" + link.get("href"))

    link_list = set(link_list)



    soup_list = []

    for link in link_list:
        result = requests.get(link)
        page = result.content
        soup_list.append(BeautifulSoup(page, "html.parser"))
        print("request")

    for item in soup_list:
        price = item.find(id="propertyHeaderPrice")

        if price is not None:
            price = price.text
            price = re.search('£(.*) pcm', price)
            price = price.group(1)
            print(price)

        bedrooms = item.find(string=re.compile("bedroom"))
        bedrooms = str(bedrooms.string)

        bedrooms = bedrooms.rsplit("bedroom", 1)[0]
        bedrooms = bedrooms.strip()
        print(bedrooms)

        address = item.find("address", class_="pad-0 fs-16 grid-25")
        address_string = str(address.string)
        geolocator = GoogleV3()

        location = geolocator.geocode(address_string)
        print(location.address)
        print(location.latitude)
        print(location.longitude)

        furnished_type = item.find(id="furnishedType")

        furnished_string = str(furnished_type.string)

        is_furnished = False

        if furnished_string == "Furnished":
            is_furnished = True;

construct_rightmove_url("5E219", "4", "400", True)
