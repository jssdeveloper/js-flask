from flask import Flask, render_template, url_for, request
import time
import requests

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("home.html")

@app.route("/weather",methods=["POST","GET"])
def weather():
	def get_weather(city_name):
		API_key = "60aa068482d6ddc251ae5f53570ac5fb"
		url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={API_key}"
		response = requests.get(url)
		code = response.json()["cod"]
		
		if code == 200:
			country = (response.json()['sys']['country'])
			weather = response.json()['weather'][0]['main']
			temperature = round(response.json()['main']['temp'])
			return {"city":city_name,"country":country,"weather":weather,"temperature":temperature,"status":code}
		else:
			return("City not found")

	if request.method == "GET":
		weather = get_weather("Riga")
		return render_template("weather.html", datetime = str(time.ctime()), city = weather["city"],country=weather["country"],weather=weather["weather"],temperature=weather["temperature"])
	else:
		usrcity = request.form["usrinput"]
		weather = get_weather(usrcity)
		
		if weather["status"] == 200:
			return render_template("weather.html", datetime = str(time.ctime()), city = weather["city"],country=weather["country"],weather=weather["weather"],temperature=weather["temperature"])
		else:
			return "error"

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

	## GET NESTE PRICE ##
	url_neste = requests.get("https://www.neste.lv/lv/content/degvielas-cenas")
	nsoup = BeautifulSoup(url_neste.content,"html.parser")
	n = (nsoup.find_all("span"))

	alldata = []
	for i in n:
		if len(i.text) > 0:
			alldata.append(i.text)
	print(alldata)

	n95 = alldata[3]
	n98 = alldata[5]
	nd = alldata[7]
	npd = alldata[9]

	## GET VIRSI PRICE ##
	url_virsi = requests.get("https://www.virsi.lv/lv/privatpersonam/degviela/degvielas-un-elektrouzlades-cenas")
	vsoup = BeautifulSoup(url_virsi.content,"html.parser")

	v = (vsoup.find_all("p",{"class":"price"}))

	nlist = []
	for x in v:
		if len(x.text) > 0:
			nlist.append(repr(x.text))
	nlist2 = []
	for y in nlist:
		nlist2.append(y.replace("\\","").replace("n","").replace("\"","").replace("'",""))
	print(nlist2)
	v95 = nlist2[1][3:]
	v98 = nlist2[2][3:]
	vdd = nlist2[0][2:]
	vlpg = nlist2[4][3:]

	return render_template("fuel.html", datetime = str(time.ctime()),c95 = circle_miles95,c98 = circle_milesPLUS98,cmilesD = circle_milesD,cplusD = circle_milesPLUSD, cgaze = circle_autogaze, n95=n95, n98=n98, nd=nd, npd=npd, v95=v95,v98=v98,vdd=vdd,vlpg=vlpg)

