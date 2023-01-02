import requests
import time
import datetime

city_name = "Berlin"

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
coordinates = get_weather(city_name)

history_key = "8a66acc84emsh6448231a3a489fap1ad41cjsn971b51d14b87"

## HISTORY PART --------------------------------
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

## GET TIME NOW AND 1 YEAR BACK
timenow = time.time()
current_date = datetime.datetime.utcfromtimestamp(timenow).strftime("%Y-%m-%d")
past_date = datetime.datetime.utcfromtimestamp(timenow-31536000).strftime("%Y-%m-%d")

## GET HISTORY DATA
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
#print(history_data)

## THIS IS OUTPUT FOR CSV FILE WITH DAILY TEMPERATURES
daily_temperature = []

for month in history_data:
    if month["date"] and month["tmin"] and month["tavg"] and month["tmax"]:
        daily_temperature.append([month["date"],month["tmin"],month["tavg"],month["tmax"]])

date_data = list(date[0] for date in daily_temperature)
temp_min = list(min[1] for min in daily_temperature)
temp_avg = list(avg[2] for avg in daily_temperature)
temp_max = list(max[2] for max in daily_temperature)

print(date_data)
print(temp_min)
print(temp_avg)
print(temp_max)