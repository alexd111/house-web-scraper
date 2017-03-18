# coding=utf-8

import get_houses
import rightmove_outcodes
from construct_url import construct_rightmove_url, construct_afs_url


# Searches all APIs/websites based on input criteria
def search(location, bedrooms, ppm, is_furnished, bills_inc):
    houses_zoopla = get_houses.get_zoopla_houses(location, bedrooms, ppm, bills_inc)
    houses_afs = construct_afs_url(location, bedrooms, ppm, is_furnished, bills_inc)
    rightmove_locations = rightmove_outcodes.create_dictionary()

    rightmove_code = rightmove_locations[location.casefold()]  # Rightmove uses outcodes for location

    houses_rightmove = construct_rightmove_url(rightmove_code, bedrooms, ppm, is_furnished)

    if houses_afs is None:
        houses_afs = []

    if houses_rightmove is None:
        houses_rightmove = []

    if houses_zoopla is None:
        houses_zoopla = []

    return houses_afs + houses_rightmove + houses_zoopla






