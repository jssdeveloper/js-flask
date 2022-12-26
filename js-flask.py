from flask import Flask, render_template, url_for
import time
app = Flask(__name__)

@app.route("/")
def index():
	return render_template("home.html")

@app.route("/weather")
def weather():
	return render_template("weather.html", datetime = str(time.ctime()))

@app.route("/fuel")
def fuel():
	return render_template("fuel.html", datetime = str(time.ctime()))