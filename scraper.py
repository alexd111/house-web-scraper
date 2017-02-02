from bs4 import BeautifulSoup
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

        link_list.append("http://www.rightmove.co.uk/" + link.get("href"))

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

construct_rightmove_url("5E219", "4", "500", True)
