from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/welcome")
def welcome():
	return"<H1>Welcome</H1>"

@app.route("/welcome/home")
def welcomehome():
	return"<H1>Welcome home</H1>"

@app.route("/welcome/back")
def welcomeback():
	return"<H1>Welcome back</H1>"