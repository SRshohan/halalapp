from flask import Flask, jsonify, request
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS
from random import randint
from urllib.parse import quote_plus

app = Flask(__name__)
CORS(app)

username = quote_plus("sohanrahman182")
password = quote_plus("Shohan@2019")
app.config["MONGO_URI"] = f"mongodb+srv://{username}:{password}@cluster0.jxwkvmy.mongodb.net/sample_restaurants?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app=app)

@app.route('/restaurants')
def get_restaurants():
    restaurants = mongo.db.restaurants.find().limit(20)
    results = []
    for restaurant in restaurants:
        restaurant['_id'] = str(restaurant['_id'])  # Convert ObjectId to string
        results.append(restaurant)
    return jsonify(results)
@app.route('/restaurant/random')
def get_random_restaurant():
    try:
        # Fetch a single random restaurant
        random_restaurant = mongo.db.restaurants.aggregate([{"$sample": {"size": 1}}]).next()
        random_restaurant['_id'] = str(random_restaurant['_id'])  # Convert ObjectId to string for JSON serialization
        return jsonify(random_restaurant)
    except StopIteration:
        return jsonify({"error": "No restaurants found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
