from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)
api = Api(app)

# Database setup
def init_db():
    conn = sqlite3.connect('restaurants.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS restaurants
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  address TEXT NOT NULL,
                  borough TEXT NOT NULL,
                  city TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

class Restaurant(Resource):
    def get(self, restaurant_id=None):
        conn = sqlite3.connect('restaurants.db')
        c = conn.cursor()
        
        if restaurant_id:
            c.execute("SELECT * FROM restaurants WHERE id=?", (restaurant_id,))
            restaurant = c.fetchone()
            conn.close()
            
            if restaurant:
                return {
                    'id': restaurant[0],
                    'name': restaurant[1],
                    'address': restaurant[2],
                    'borough': restaurant[3],
                    'city': restaurant[4]
                }
            return {'message': 'Restaurant not found'}
        else:
            c.execute("SELECT * FROM restaurants")  # Removed LIMIT 20
            restaurants = c.fetchall()
            conn.close()
            
            return [{
                'id': r[0],
                'name': r[1],
                'address': r[2],
                'borough': r[3],
                'city': r[4]
            } for r in restaurants]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('address', type=str, required=True)
        parser.add_argument('borough', type=str, required=True)
        parser.add_argument('city', type=str, required=True)
        args = parser.parse_args()

        conn = sqlite3.connect('restaurants.db')
        c = conn.cursor()
        c.execute("INSERT INTO restaurants (name, address, borough, city) VALUES (?, ?, ?, ?)",
                  (args['name'], args['address'], args['borough'], args['city']))
        conn.commit()
        new_id = c.lastrowid
        conn.close()

        return {'id': new_id, 'message': 'Restaurant added successfully'}

api.add_resource(Restaurant, '/restaurants', '/restaurants/<int:restaurant_id>')

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
