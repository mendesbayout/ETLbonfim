import json

from flask import Flask
from flask_restx import Api, Resource
from pymongo import MongoClient
import json

# Create a Flask app
app = Flask(__name__)

# Initialize the RestX API object
api = Api(app, version='1.0', title='API', description='API for MongoDB database')

# Connect to the MongoDB database


# Define a RestX Resource
@api.route('/compliance')
class Compliance(Resource):
    def get(self):
        client = MongoClient("mongodb+srv://bayout:Ninamendes1%40@cluster0.bo6zstp.mongodb.net/test")
        db = client["complianceRAW"]
        collection = db["compliance"]
        data = []
        for item in collection.find():
            item["_id"] = str(item["_id"])
            data.append({
                "id": item["_id"],
                "link": item["url"],
                "text": item["text"]
            })
        return data


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
