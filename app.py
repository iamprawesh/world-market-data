from flask import Flask,jsonify,render_template
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
from datetime import datetime,timedelta
import json
import logging
app = Flask(__name__)


CORS(app)


def getHTML(url):
    page = requests.get(url)

    raw = BeautifulSoup(page.content, "html.parser")
    return raw
    
def nepseData():
    soup = getHTML("http://www.nepalstock.com/")
    nepse_div = soup.find_all("div",class_=["pull-left", "banner-green", "banner-item"])[0]
    point_div = nepse_div.find_all("div",class_=["current-index"])[0]
    point_change = nepse_div.find_all("div",class_=["point-change"])[0]

    data =  {
                    "name":"NEPSE",
            "point":point_div.text.strip(),
            "change":point_change.text.strip(),
            "order":1
            }
    return data


def worldMarket():
        # for world
    x = []
    URL = "https://www.investing.com/indices/major-indices"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    # nifty_sensex = soup.find_all("div",class_=["txtmacmb","slick-slide", "slick-current", "slick-active"])
    # print(nifty_sensex.ul)
    y =  soup.find_all("tr", {"data-test":"price-row"})
    # soup.find("div", {"class" : "data-sitekey"}))
    # results = soup.find("div", class_="table-browser_table-browser-wrapper__2ynbE")
    # print(y.tbody)
    # print(len(y.tbody.tr))
    for i in y:
        # print(i.td[1].div.a)
        all_td = i.find_all("td")
        # name
        market_name = all_td[1].div.a.text.strip()
        market_point = all_td[2].text.strip(),
        market_change = all_td[5].text.strip(),

        market_change = ''.join(market_change)
        market_point = ''.join(market_point)
        if 'nasdaq' in market_name.lower():
            # print(name)      
            x.append(
            {
                    "name":"NASDAQ",
                    "point":market_point,
                    "change":market_change,
                    "order":10

                }
             )  
        if 'dow' in market_name.lower():
            x.append(
            {
                    "name":"DJI",
                    "point":market_point,
                    "change":market_change,
                    "order":6
                }
             )
        if 'ftse 100' in market_name.lower():
            x.append(
            {
                    "name":"FTSE 100",
                    "point":market_point,
                    "change":market_change,
                    "order":7
                }
             )  
        if 'dax' in market_name.lower():
            x.append(
            {
                    "name":"DAX",
                    "point":market_point,
                    "change":market_change,
                    "order":8
                }
             )  
        if 'cac' in market_name.lower():
            x.append(
            {
                    "name":"CAC 40",
                    "point":market_point,
                    "change":market_change,
                    "order":9
                }
             )  
        if 'nikkei' in market_name.lower():
            x.append(
            {
                    "name":"NIKKEI 225",
                    "point":market_point,
                    "change":market_change,
                    "order":4
                }
             )  

        if 'hang seng' in market_name.lower():
            x.append(
            {
                    "name":"HANG SENG",
                    "point":market_point,
                    "change":market_change,
                    "order":5
                }
             )   
        if 'sensex' in market_name.lower():
            x.append(
            {
                    "name":"SENSEX",
                    "point":market_point,
                    "change":market_change,
                    "order":2
                }
             )  

        if 'nifty' in market_name.lower():
            x.append(
            {
                    "name":"NIFTY FIFTY",
                    "point":market_point,
                    "change":market_change,
                    "order":3
                }
             )  
    x = sorted(x ,key=lambda item:item['order'])

    return x

@app.route("/")
def index():
    marketList = []
    logging.basicConfig(filename="std.log", 
					format='%(asctime)s %(message)s', 
					filemode='a',
                    level=logging.DEBUG
                    ) 

    from os import path
    ifexist = path.exists("data.txt")
    print(ifexist)
    print("ifexist")
    try:
        if ifexist:
            file1 = open("data.txt","r+")
            # print("exist")
            data = json.load(file1)
            # print(data)
            current = datetime.now()
            expires_time = data[0]['expires_in']
            # expires_time = str(datetime.now() -  timedelta(hours=2))
            #  
            expires = datetime.strptime(expires_time, '%Y-%m-%d %H:%M:%S.%f')
            current = datetime.strptime( str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f')
            print(expires)
            print(current)
            
            # print(data[1])
            if current > expires:
                nepse = nepseData()
                marketList.append(nepse)
                fileinwite = open("data.txt","w")
                world = worldMarket()
                print("expired")
                print("refetching")
                marketList += world

                storeData(fileinwite,marketList)
            else:
                print("not expired")
                marketList = data[1]

        else:
            print("file not exist")
            fileinwite = open("data.txt","w")
            nepse = nepseData()
            marketList.append(nepse)
            world = worldMarket()
            marketList += world 
            storeData(fileinwite,marketList)
            print("not exist")
        print("=============================")
        return jsonify(marketList)



    except Exception as e:

        marketList = []
        print(e)
        return jsonify([])


def storeData(file1,data):
    expires_in = datetime.now() +  timedelta(hours=1)
    file1.write(json.dumps([{"expires_in":str(expires_in)},data]))
    file1.close()


@app.route("/new")
def newv2():
    marketList = []
    nepse = nepseData()
    marketList.append(nepse)
    world = worldMarket()
    marketList += world
    return jsonify(marketList)





@app.route("/exp")
def ExpiryTime():
    try:
        file1 = open("data.txt","r+")
        data = json.load(file1)
        file1.close()
        return jsonify(data[0])
    except:
        return jsonify(["some eror"])
    



if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)









