from flask import Flask, render_template, url_for
import time
from fuelscrape import circle_miles95, circle_milesPLUS98, circle_milesD, circle_milesPLUSD, circle_autogaze


app = Flask(__name__)

@app.route("/")
def index():
	return render_template("home.html")

@app.route("/weather")
def weather():
	return render_template("weather.html", datetime = str(time.ctime()))

@app.route("/fuel")
def fuel():
	
	return render_template("fuel.html", datetime = str(time.ctime()),c95 = circle_miles95,c98 = circle_milesPLUS98,cmilesD = circle_milesD,cplusD = circle_milesPLUSD, cgaze = circle_autogaze)