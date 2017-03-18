import get_houses

#  Both methods construct a search url based on the input parameters


def construct_rightmove_url(location, bedrooms, price, is_furnished):
    url = "http://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%{LOCATION}&maxBedrooms="\
            "{MAX_BEDROOMS}&minBedrooms={MAX_BEDROOMS}&maxPrice={MAX_PRICE}&includeLetAgreed=false&furnishTypes="\
            "{IS_FURNISHED}&letType=student"

    query_url = url.replace("{LOCATION}", location)  # THIS WILL NEED A HELPER METHOD

    bedrooms = str(bedrooms)

    query_url = query_url.replace("{MAX_BEDROOMS}", bedrooms)

    price = str(price)

    query_url = query_url.replace("{MAX_PRICE}", price)

    if is_furnished == 1:
        query_url = query_url.replace("{IS_FURNISHED}", "furnished")
    else:
        query_url = query_url.replace("{IS_FURNISHED}", "unfurnished")

    print(query_url)

    return get_houses.get_rightmove_houses(query_url)


def construct_afs_url(location, bedrooms, price, is_furnished, bills_inc):
    url = "http://www.accommodationforstudents.com/searchresults.asp?lookingfor=any&city={LOCATION}&numberofbedrooms="\
            "{MAX_BEDROOMS}&cost={MAX_PRICE}&searchtype=city&street=&postcode=&area=&orderby=latest&bills_included="\
            "{BILLS_INC}&x=29&y=24&perpage=200"

    query_url = url.replace("{LOCATION}", location)

    bedrooms = str(bedrooms)

    query_url = query_url.replace("{MAX_BEDROOMS}", bedrooms)

    monthly_price = int(price)

    weekly_price = int((monthly_price * 12) / 52)

    weekly_price = str(weekly_price)

    query_url = query_url.replace("{MAX_PRICE}", weekly_price)

    if bills_inc == 1:
        query_url = query_url.replace("{BILLS_INC}", "1")
    else:
        query_url = query_url.replace("{BILLS_INC}", "0")

    print(query_url)

    return get_houses.get_afs_houses(query_url, bedrooms)