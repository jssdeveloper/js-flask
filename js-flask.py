from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
	return"<H1>Janis Stals flask page</H1>"

@app.route("/welcome")
def welcome():
	return"<H1>Welcome</H1>"

@app.route("/welcome/home")
def welcomehome():
	return"<H1>Welcome home</H1>"

@app.route("/welcome/back")
def welcomeback():
	return"<H1>Welcome back</H1>"