import sqlite3


def init_db():
    conn = sqlite3.connect("houses.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS accommodations
                (url text PRIMARY KEY, ppm int, bedrooms int, bills_inc text, lat real, long real, address text, is_furnished int)''')


def add_house_to_db(house):
    conn = sqlite3.connect("houses.db")
    c = conn.cursor()

    c.execute('INSERT INTO accommodations VALUES (?,?,?,?,?,?,?,?)',
              (house.url, house.ppm, house.bedrooms, house.bills_inc, house.lat, house.long, house.address, house.is_furnished))

    conn.commit()