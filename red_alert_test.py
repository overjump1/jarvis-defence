# -*- coding: utf-8 -*-
#!/usr/bin/python
import json
import requests

class RedAlert():
    def __init__(self):
        self.cookies = ""
        self.headers = {
           "Host":"www.oref.org.il",
           "Connection":"keep-alive",
           "Content-Type":"application/json",
           "charset":"utf-8",
           "X-Requested-With":"XMLHttpRequest",
           "sec-ch-ua-mobile":"?0",
           "User-Agent":"",
           "sec-ch-ua-platform":"macOS",
           "Accept":"*/*",
           "sec-ch-ua": '".Not/A)Brand"v="99", "Google Chrome";v="103", "Chromium";v="103"',
           "Sec-Fetch-Site":"same-origin",
           "Sec-Fetch-Mode":"cors",
           "Sec-Fetch-Dest":"empty",
           "Referer":"https://www.oref.org.il/12481-he/Pakar.aspx",
           "Accept-Encoding":"gzip, deflate, br",
           "Accept-Language":"en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        }
        self.get_cookies()
        self.cities = json.load(open("cities.json", encoding="UTF-8"))
        self.polygons = json.load(open("polygons.json", encoding="UTF-8"))

    def get_cookies(self):
        HOST = "https://www.oref.org.il/"
        r = requests.get(HOST,headers=self.headers)
        self.cookies = r.cookies

    def count_alerts(self,alerts_data):
        return len(alerts_data)

    def get_red_alerts(self):
        #try:
            """
            HOST = "https://www.oref.org.il/WarningMessages/alert/alerts.json"
            r = requests.get(HOST, headers=self.headers, cookies=self.cookies, timeout=5)
            alerts = r.content.decode("UTF-8").replace("\n","").replace("\r","")
            if len(alerts) <= 1:
                return None
            j = json.loads(r.content)
            """
            f = open('test.json', encoding="UTF-8")
            j = json.load(f)
            if len(j["data"]) == 0:
                return None
            #print(r.content.decode("UTF-8"))
            j["title"] = self.get_category(j["cat"])
            city_names, city_ids = self.get_cities(j["data"])
            j["polygons"] = self.get_polygons(city_ids)
            j["english_cities"] = city_names

            return j
        #except Exception as e:
        #    print(e)
        #    return None
    def get_category(self, category_id:int):
        """returns the category name of a given category id"""
        category_id = int(category_id)
        categories = {
            1 : "rocket and missile fire",
            2 : "general alert",
            3 : "earthquake",
            4 : "radiological event",
            5 : "fear of a tsunami",
            6 : "hostile aircraft intrusion",
            7 : "hazardous materials event",
            10 : "flash update",
            13 : "terrorist infiltration",
            101 : "rocket and missile fire drill",
            102 : "flash drill",
            103 : "earthquake drill",
            104 : "radiologic drill",
            105 : "tsunami drill",
            106 : "hostile aircraft drill",
            107 : "hazardous materials drill",
            110 : "flash drill",
            113 : "terrorist infiltration drill"
        }
        return categories[category_id]

    def get_cities(self, hebrew_cities:list):
        "gets english city name array and thier id array"
        english_cities = []
        city_ids = []
        for city in hebrew_cities:
            search = self.cities[city]
            if search is None:
                english_cities.append(city)
            else:
                english_cities.append(search['en'])
                city_ids.append(search['id'])
        return (english_cities, city_ids)

    def get_polygons(self, ids):
        "gets a list of city ids and returns polygons for map use"
        polygons = []
        for id in ids:
            search = self.polygons[str(id)]
            if search is not None:
                polygons.append(search)
        return polygons

