from flask import Flask
app = Flask(__name__)

@app.route("/")
def welcome():
	return"<H1>Welcome</H1>"