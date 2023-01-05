from flask import Flask, render_template, url_for, request, send_file
import time
import datetime
import requests
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

app = Flask(__name__)


##-------------------------------------------------------------------------------------------
## HOME ROUTE
##-------------------------------------------------------------------------------------------
@app.route("/")
def index():
	return render_template("home.html")
##-------------------------------------------------------------------------------------------




##-------------------------------------------------------------------------------------------
## MAIN API CALL FUNCTION
##-------------------------------------------------------------------------------------------
def get_weather(city_name):
	API_key = "0951ebb00319e01258d421af9baa3d0c"
	url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={API_key}"
	response = requests.get(url)
	code = response.json()["cod"]
	
	if code == 200:
		country = (response.json()['sys']['country'])
		weather = response.json()['weather'][0]['main']
		temperature = round(response.json()['main']['temp'])
		return {"city":city_name,"country":country,"weather":weather,"temperature":temperature,"status":code}
	else:
		return("error")
##-------------------------------------------------------------------------------------------




##-------------------------------------------------------------------------------------------
## ROUTE WEATHER API WITHOUT CHART
##-------------------------------------------------------------------------------------------
@app.route("/weather",methods=["POST","GET"])
def weather():
	if request.method == "GET":
		weather = get_weather("Riga")
		return render_template("weather.html", datetime = str(time.ctime()), city = weather["city"],country=weather["country"],weather=weather["weather"],temperature=weather["temperature"])
	else:
		usrcity = request.form["usrinput"]
		weather = get_weather(usrcity)
		
		if weather != "error":
			return render_template("weather.html", datetime = str(time.ctime()), city = weather["city"],country=weather["country"],weather=weather["weather"],temperature=weather["temperature"])
		else:
			return render_template("weather_error.html")

## Route for weather error
@app.route("/weather/error",methods=["POST","GET"])
def weather_error():
	usrcity = request.form["usrinput"]
	weather = get_weather(usrcity)
	
	if weather != "error":
		return render_template("weather.html", datetime = str(time.ctime()), city = weather["city"],country=weather["country"],weather=weather["weather"],temperature=weather["temperature"])
	else:
		return render_template("weather_error.html")
##-------------------------------------------------------------------------------------------



##-------------------------------------------------------------------------------------------
## WEATHER HISTORY ROUTE
##-------------------------------------------------------------------------------------------
@app.route("/weather_history",methods = ["GET","POST"])
def weather_history():

	if request.method == "GET":
		return render_template("weather_history_get.html",coordinates="")

	else:

		city_name = request.form["cdinput"]

		## GET COORDINATES -------------------------------------------------------------------
		def get_weather(city_name):
			API_key = "0951ebb00319e01258d421af9baa3d0c"
			url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={API_key}"
			response = requests.get(url)
			code = response.json()["cod"]

			return {
				"city" : city_name,
				"lon" : (response.json()["coord"]["lon"]),
				"lat" : (response.json()["coord"]["lat"])
			}
		
		try:
			coordinates = get_weather(city_name)
		except:
			error_msg = "Invalid City name"
			return render_template("weather_history.html",coordinates="",error_msg = error_msg)
		else:

			## HISTORY PART ------------------------------------------------------------------
			## Connect to API with coordinates in payload
			history_key = "8a66acc84emsh6448231a3a489fap1ad41cjsn971b51d14b87"
			def get_closest_station(coordinates):
				querystring = {"lat":coordinates["lat"],"lon":coordinates["lon"]}

				headers = {
					"X-RapidAPI-Key": history_key,
					"X-RapidAPI-Host": "meteostat.p.rapidapi.com"
				}

				stations = requests.get("https://meteostat.p.rapidapi.com/stations/nearby", headers=headers, params=querystring)
				closest_station_id = (stations.json()["data"][0]["id"])
				return(closest_station_id)
			closest_station = get_closest_station(coordinates)
			print(closest_station)

			## Get start and end time with epoch
			timenow = time.time()
			current_date = datetime.datetime.utcfromtimestamp(timenow).strftime("%Y-%m-%d")
			past_date = datetime.datetime.utcfromtimestamp(timenow-31536000).strftime("%Y-%m-%d")

			## Get history data
			def get_history(station="26422",current_date=current_date,past_date=past_date):
				url = "https://meteostat.p.rapidapi.com/stations/daily"
				querystring = {"station":station,"end":current_date,"start":past_date}
				
				headers = {
					"X-RapidAPI-Key": history_key,
					"X-RapidAPI-Host": "meteostat.p.rapidapi.com"
				}

				response = requests.get(url,headers=headers,params=querystring)
				return(response.json()["data"])

			history_data = get_history(closest_station)

			daily_temperature = []

			## Removing days when station did not report data
			for month in history_data:
				if month["date"] and month["tmin"] and month["tavg"] and month["tmax"]:
					daily_temperature.append([month["date"],month["tmin"],month["tavg"],month["tmax"]])

			## Convertting data to individual lists
			date_data = list(date[0] for date in daily_temperature)
			temp_min = list(min[1] for min in daily_temperature)
			temp_avg = list(avg[2] for avg in daily_temperature)
			temp_max = list(max[3] for max in daily_temperature)


			## Drawing chart with min, avg, max temperatures
			plt.figure(figsize=(15, 6), dpi=80)
			plt.plot(date_data,temp_min, label = "Temp Min", color="blue")
			plt.plot(date_data,temp_avg, label = "Temp Avg", color="green")
			plt.plot(date_data,temp_max, label = "Temp Max", color="red")

			#plt.plot(temp_max)
			plt.title(f"{city_name} {past_date} - {current_date}")
			plt.xlabel("Date")
			plt.ylabel("Degrees C")
			plt.legend()

			plt.tick_params(axis="x", labelrotation=90)
			plt.tick_params(axis="x",which="major",length=10, width="2.5")
			plt.xticks(fontsize=5,fontweight="bold")
			plt.show()
			plt.savefig("static/plot.jpg")
			plt.savefig("static/plot.pdf")
			plt.figure().clear()

			average_temp = round((sum(temp_avg) / len(temp_avg)),2)
			
			## GET MINIMUM TEMPERATURE
			absolute_minimum = min(temp_min)
			minimum_index = temp_min.index(absolute_minimum)
			minimum_date = date_data[minimum_index]

			## GET MAXIMUM TEMPERATURE
			absolute_maximum = max(temp_max)
			maximum_index = temp_max.index(absolute_maximum)
			print("maximum:", absolute_maximum)
			maximum_date = date_data[maximum_index]


			## GENERATE RAW DATA FILE
			with open("static/weatherdata.csv","w") as rawdatafile:
				rawdatafile.write("Date,Min Temperature,Max Temperature,Avg Temperature\n")
				for data in range(len(temp_min)):
					rawdatafile.write(f"{date_data[data]},{temp_min[data]},{temp_max[data]},{temp_avg[data]}\n")

			error_msg = ""
			return render_template("weather_history.html",date_data =date_data, temp_min = temp_min, temp_avg = temp_avg, temp_max = temp_max,coordinates=coordinates, error_msg=error_msg,average_temp=average_temp,absolute_minimum=absolute_minimum,minimum_date=minimum_date,absolute_maximum=absolute_maximum,maximum_date=maximum_date)


## DOWNLOAD CSV
@app.route("/weather_history/csv")
def download_csv():
	path = "static/weatherdata.csv"
	return send_file(path,as_attachment=True)

## DOWNLOAD PDF
@app.route("/weather_history/pdf")
def download_pdf():
	path = "static/plot.pdf"
	return send_file(path,as_attachment=True)
	


##-------------------------------------------------------------------------------------------
## NOTIFICATION SIGNL4
##-------------------------------------------------------------------------------------------
@app.route("/notification")
def notifiaction():
	return"notification page"
##-------------------------------------------------------------------------------------------





##-------------------------------------------------------------------------------------------
## FUEL SCRAPE
##-------------------------------------------------------------------------------------------
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
	##-------------------------------------------------------------------------------------------