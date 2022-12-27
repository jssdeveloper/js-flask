from flask import Flask, render_template, url_for, request
import time
import requests

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("home.html")

@app.route("/weather",methods=["POST","GET"])
def weather():
	def get_weather(city_name = "Nome"):
		API_key = "60aa068482d6ddc251ae5f53570ac5fb"
		url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={API_key}"
		response = requests.get(url)
		code = response.json()["cod"]
		
		if code == 200:
			country = (response.json()['sys']['country'])
			weather = response.json()['weather'][0]['main']
			temperature = round(response.json()['main']['temp'])
			return {"city":city_name,"country":country,"weather":weather,"temperature":temperature}
		else:
			return("City not found")
	weather = get_weather()

	return render_template("weather.html", datetime = str(time.ctime()), temperature = weather["temperature"], weather = weather["weather"], country = weather["country"], city_name = weather["city"])

@app.route("/fuel")
def fuel():
	from bs4 import BeautifulSoup
	
	## GET CIRCLE K ##
	url_circle = requests.get("https://www.circlek.lv/privātpersonām/degvielas-cenas")
	circle = BeautifulSoup(url_circle.content,"html.parser")
	circle = circle.find_all("table",{"class":"ck-striped-table uk-table uk-table-striped"})
	circlestr = ""

	for p in circle:
		circlestr += p.text

	circlestr = circlestr.replace("Degviela","").replace("Cena EUR","").replace("Uzpildes stacijas adrese","").replace("Visos Rīgas DUS degvielas cenas ir vienādas.","")
	circlelist = circlestr.split()
	print(circlelist)

	circle_miles95 = circlelist[2].strip()
	circle_milesPLUS98 = circlelist[9].strip()
	circle_milesD = circlelist[16].strip()
	circle_milesPLUSD = circlelist[23].strip()
	circle_autogaze = circlelist[29].strip()

	return render_template("fuel.html", datetime = str(time.ctime()),c95 = circle_miles95,c98 = circle_milesPLUS98,cmilesD = circle_milesD,cplusD = circle_milesPLUSD, cgaze = circle_autogaze)