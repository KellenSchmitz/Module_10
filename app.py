# use Flask to render a template, redirecting to another url, and creating a URL.
from flask import Flask, render_template, redirect, url_for

# use PyMongo to interact with our Mongo database.
from flask_pymongo import PyMongo

# use the scraping code, that we wrote in Jupyter and exported/cleaned in a Python file (scraping.py)
# Both the scraping file and app.py file (this file) needs to be saved in the same folder
import scraping

# Set up flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# Define route for the HTML page
    # index.html is the default HTML file we'll use to display the content we've scraped
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)



# The next lines allow us to access the database, scrape new data using our scraping.py script


@app.route("/scrape")                           # line 1
def scrape():                                   # line 2
   mars = mongo.db.mars                         # line 3
   mars_data = scraping.scrape_all()            # line 4
   mars.update({}, mars_data, upsert=True)      # line 5
   return redirect('/', code=302)               # line 6

   # Line 1 @app.route(“/scrape”) defines the route that Flask will be using and will run the function that we create just beneath it.
   # Line 2 define the function to run the scrape
   # Line 3 assign new variable that points to Mongo database
   # Line 4 create a variable to hold the newly scraped data and the function "scrape_all" that we created in the scraping.py file we wrote
   # Line 5 now update the database.
        #   .update(query_parameter. data, options)
        #   we are inserting data so first we add an empty JSON object with {}
        #   next add the data we stored in variable mars_data
        #   then upsert=True to tell Mongodb to create a new doc if one doesn't exist yet
   # Line 6 this navigates back to / where the newly updated content is displayed

# Tell flask to run
if __name__ == "__main__":
   app.run()