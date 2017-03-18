from flask import Flask, request
from flask_restful import Resource, Api, reqparse

import database
import web_scraper

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class AccommodationRequest(Resource):
    def get(self, location, bedrooms, price, is_furnished, bills_inc):
        args = request.args
        bedrooms = int(bedrooms)
        price = int(price)
        is_furnished = int(is_furnished)
        bills_inc = int(bills_inc)

        houses = web_scraper.search(location, bedrooms, price, is_furnished, bills_inc)
        house_list = []
        for item in houses:
            house_list.append({
                'bedrooms': item.bedrooms,
                'ppm': item.ppm,
                'billsInc': item.bills_inc,
                'latitude': item.lat,
                'longitude': item.long,
                'address': item.address,
                'isFurnished': item.is_furnished,
                'url': item.url
                })
        return house_list


class AccommodationRequestArgs(Resource):
    def get(self):
        args = request.args
        location = args['location']
        bedrooms = int(args['bedrooms'])
        price = int(args['price'])
        if args['billsInc'] == 'True':
            bills_inc = 1
        else:
            bills_inc = 0
        if args['isFurnished'] == 'True':
            is_furnished = 1
        else:
            is_furnished = 0

        houses = web_scraper.search(location, bedrooms, price, is_furnished, bills_inc)
        house_list = []
        for item in houses:
            house_list.append({
                'bedrooms': item.bedrooms,
                'ppm': item.ppm,
                'billsInc': item.bills_inc,
                'latitude': item.lat,
                'longitude': item.long,
                'address': item.address,
                'isFurnished': item.is_furnished,
                'url': item.url
                })
        return house_list


class AccommodationTest(Resource):
    def get(self, location, bedrooms, price, is_furnished, bills_inc):
        return {'location': location,
                'bedrooms': bedrooms,
                'price': price,
                'is_furnished': is_furnished,
                'bills_inc': bills_inc}


api.add_resource(AccommodationRequest, '/accommodation/<location>/<bedrooms>/<price>/<is_furnished>/<bills_inc>')

api.add_resource(AccommodationRequestArgs, '/accommodationArgs', endpoint='accommodationArgs')

api.add_resource(AccommodationTest, '/accommodationTest/<location>/<bedrooms>/<price>/<is_furnished>/<bills_inc>')

if __name__ == '__main__':
    database.init_db()
    app.run(debug=True, host='0.0.0.0')
