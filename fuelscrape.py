import requests
from bs4 import BeautifulSoup

url_circle = "https://www.circlek.lv/privātpersonām/degvielas-cenas"
url_neste = "https://www.neste.lv/lv/content/degvielas-cenas"
url_virsi = "https://www.virsi.lv/lv/privatpersonam/degviela/degvielas-un-elektrouzlades-cenas"
url_viada = "https://www.viada.lv/zemakas-degvielas-cenas/"
url_kool = "https://koolbusiness.lv/degvielas-cenu-vesture/"
url_gotika = "https://www.gotikaauto.lv"

print(requests.get(url_virsi).text)