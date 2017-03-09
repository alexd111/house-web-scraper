import re

# Both methods parse the websites' search results page and return a list of links to propery listings

def create_afs_links(soup, bedrooms):
    link_list = []
    for item in soup.find_all("span", class_="style13y"):
        no_of_bedrooms = str(item.contents[0].string)
        no_of_bedrooms = no_of_bedrooms.rsplit("bed", 1)[0]
        no_of_bedrooms = no_of_bedrooms.strip()
        if no_of_bedrooms == bedrooms:
            link_list.append("http://www.accommodationforstudents.com" + item.parent.attrs["href"])
    return link_list


def create_rightmove_links(soup):
    link_list = []
    for link in soup.find_all("a", "propertyCard-link"):

        if link.get("href") != "/property-for-sale/property-0.html":
            url = link.get("href")
            url_number = re.findall(r'\d+', url)
            link_list.append("http://www.rightmove.co.uk/property-to-rent/property-" + url_number[0] + ".html")
    link_list = set(link_list)
    return link_list
