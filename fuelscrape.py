import requests
from bs4 import BeautifulSoup

#url_neste = requests.get("https://www.neste.lv/lv/content/degvielas-cenas")
#url_virsi = requests.get("https://www.virsi.lv/lv/privatpersonam/degviela/degvielas-un-elektrouzlades-cenas")
#url_viada = requests.get("https://www.viada.lv/zemakas-degvielas-cenas/")
#url_kool = requests.get("https://koolbusiness.lv/degvielas-cenu-vesture/")
#url_gotika = requests.get("https://www.gotikaauto.lv")

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




