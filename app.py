import flask
from flask import Flask, request, url_for, render_template, redirect, make_response
import pymongo
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def home():
    
    mars_data = mongo.db.collection.find_one()
    return render_template('index.html', mars_data=mars_data)



@app.route("/scrape")
def scrape():

    mars_data = scrape_mars.scrape_info()
    mongo.db.collection.replace_one({}, mars_data, upsert=True)
    
    data = mongo.db.collection.find_one()
    return render_template('main.html', mars_data=data)

    
if __name__ == "__main__":
    app.run(debug=True)
