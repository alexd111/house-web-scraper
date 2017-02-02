from bs4 import BeautifulSoup
from urllib.request import urlopen, quote
import requests

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
    soup = BeautifulSoup(open(page))


construct_rightmove_url("5E219", "4", "500", True)
