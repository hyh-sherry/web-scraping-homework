from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def home():
    information = mongo.db.collection.find_one()
    return render_template("index.html", mars_info = information)


@app.route("/scrape")
def scrape():
    mars_data = mission_to_mars.scrape_info()
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)


    