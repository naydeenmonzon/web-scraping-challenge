import flask
from flask import Flask, render_template, redirect
import pymongo
from flask_pymongo import PyMongo

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scraper():
    mars_data = mongo.db.mars_data
    data = scrape_mars.scrape()
    mars_data.update({}, data, upsert=True)

if __name__ == "__main__":
    app.run(debug=True)
