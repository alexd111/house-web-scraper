from flask import Flask
from flask_restful import Resource, Api
import scraper

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class AccommodationRequest(Resource):
    def get(self, location, bedrooms, price, is_furnished, bills_inc):
        bedrooms = int(bedrooms)
        price = int(price)
        is_furnished = int(is_furnished)
        bills_inc = int(bills_inc)

        houses = scraper.search(location, bedrooms, price, is_furnished, bills_inc)
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

api.add_resource(HelloWorld, '/')
api.add_resource(AccommodationRequest, '/accommodation/<location>/<bedrooms>/<price>/<is_furnished>/<bills_inc>')

if __name__ == '__main__':
    scraper.init_db()
    app.run(debug=True, host='0.0.0.0')
