from flask import Flask
from flask_restful import Resource, Api
import scraper

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class AccommodationRequest(Resource):
    def get(self, location, bedrooms, price, is_furnished):
        bedrooms = int(bedrooms)
        price = int(price)
        is_furnished = int(is_furnished)

        houses = scraper.search(location, bedrooms, price, is_furnished)
        house_list = []
        for item in houses:
            house_list.append({
                'no_of_bedrooms': item.bedrooms,
                'ppm': item.ppm,
                'bills_inc': item.bills_inc,
                'latitude': item.lat,
                'longitude': item.long,
                'is_furnished': item.is_furnished,
                'url': item.url
                })
        return house_list

api.add_resource(HelloWorld, '/')
api.add_resource(AccommodationRequest, '/accommodation/<location>/<bedrooms>/<price>/<is_furnished>')

if __name__ == '__main__':
    app.run(debug=True)