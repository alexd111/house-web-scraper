import unittest
import get_houses


class TestGetHouses(unittest.TestCase):
    def setUp(self):
        self.rightmove_list = get_houses.get_rightmove_houses("http://www.rightmove.co.uk/property-to-rent/find.html"
                                                              "?locationIdentifier=REGION%5E219&maxBedrooms=4"
                                                              "&minBedrooms "
                                                              "=4&maxPrice=500&includeLetAgreed=false&furnishTypes"
                                                              "=furnished&letType=student")

    def test_get_rightmove_house(self):
        self.assertTrue(self.rightmove_list)


if __name__ == '__main__':
    unittest.main()
