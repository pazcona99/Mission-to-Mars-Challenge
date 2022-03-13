#Import the dependencies

from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

#Set up flask
app = Flask(__name__)

#Connect to mongo using PyMongo
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#Define route for the HTML page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index2.html", mars=mars)

#Set up the scraping route. This will be the 'button' of the web application.
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

if __name__ == "__main__":
   app.run()