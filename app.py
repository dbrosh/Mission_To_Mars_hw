# import dependencies
from flask import Flask, render_template
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

# create flask
app = Flask(__name__)

#Use pymongo to create a mongodb connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def home():
    mars_data = mongo.db.mars_data.find_one()
    return(render_template("index.html", mars=mars_data))

# route to trigger scrape
@app.route("/scrape")
def scrape():
    #run scrape
    mars_scrape_data = scrape_mars.mars()
    #update mongo db with scraped data
    mongo.db.mars_data.update({}, mars_scrape_data, upsert=True)
    #print successful scrape on the pagee
    return ("successful scrape")

    
if __name__=="__main__":
    app.run()