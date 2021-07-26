from flask import Flask,jsonify,render_template
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
from datetime import datetime,timedelta
import json
app = Flask(__name__)


CORS(app)


# class User(db.Model):
#     _id = db.Column("id",db.Integer, primary_key=True)
#     # username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120))

#     def __repr__(self):
#         return '<User %r>' % self.email

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
                    "order":2

                }
             )  
        if 'dow' in market_name.lower():
            x.append(
            {
                    "name":"DJI",
                    "point":market_point,
                    "change":market_change,
                    "order":3
                }
             )
        if 'ftse 100' in market_name.lower():
            x.append(
            {
                    "name":"FTSE 100",
                    "point":market_point,
                    "change":market_change,
                    "order":4
                }
             )  
        if 'dax' in market_name.lower():
            x.append(
            {
                    "name":"DAX",
                    "point":market_point,
                    "change":market_change,
                    "order":5
                }
             )  
        if 'cac' in market_name.lower():
            x.append(
            {
                    "name":"CAC 40",
                    "point":market_point,
                    "change":market_change,
                    "order":6
                }
             )  
        if 'nikkei' in market_name.lower():
            x.append(
            {
                    "name":"NIKKEI 225",
                    "point":market_point,
                    "change":market_change,
                    "order":7
                }
             )  

        if 'hang seng' in market_name.lower():
            x.append(
            {
                    "name":" HANG SENG",
                    "point":market_point,
                    "change":market_change,
                    "order":8
                }
             )   
        if 'sensex' in market_name.lower():
            x.append(
            {
                    "name":"SENSEX",
                    "point":market_point,
                    "change":market_change,
                    "order":9
                }
             )  

        if 'nifty' in market_name.lower():
            x.append(
            {
                    "name":"NIFTY FIFTY",
                    "point":market_point,
                    "change":market_change,
                    "order":10
                }
             )  
    x = sorted(x ,key=lambda item:item['order'])

    return x

@app.route("/")
def index():
    marketList = []
    try:
        from os import path
        ifexist = path.exists("data.json")
        if ifexist:
            file1 = open("data.json","r+")
            print("exist")
            data = json.load(file1)
            current = datetime.now()
            expires_time = data[0]['expires_in']
            # expires_time = str(datetime.now() -  timedelta(hours=2))
            #  
            expires = datetime.strptime(expires_time, '%Y-%m-%d %H:%M:%S.%f')
            current = datetime.strptime( str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f')
            # print(data[1])
            if current > expires:
                nepse = nepseData()
                marketList.append(nepse)
                world = worldMarket()
                marketList += world 
                storeData(file1,marketList)
            else:
                # load from json file
                marketList = data[1]
                

        else:
            file1 = open("data.json","w+")
            nepse = nepseData()
            marketList.append(nepse)
            world = worldMarket()
            marketList += world 
            storeData(file1,marketList)
            print("not exist")

            return jsonify(marketList)
    except:
        return jsonify([])
    finally:
        file1.close()
        return jsonify(marketList)
  


        
    

    # data = json.load(file1)

    # if(data[0] )
    # print(type(data))
    # plus3 = datetime.now() +  timedelta(hours=2)
    # if (plus3 < datetime.now()):
    #     print("current time is bigger")
    # expires_in = plus3.strftime("%H:%M:%S")
    # # try:
    
    # file1.write(json.dumps([{"expires_in":expires_in},x]))
    # file1.close()
    # # except FileNotFoundError as error:
    #     # print(error)
    #     # print("rrr")

    # return jsonify(x)


def storeData(file1,data):
    expires_in = datetime.now() +  timedelta(hours=2)
    # expires_in = plus3.strftime("%H:%M:%S")
    file1.write(json.dumps([{"expires_in":str(expires_in)},data]))
    file1.close()


@app.route("/new")
def new():
    x = []

    # for nepal
    URL = "http://www.nepalstock.com/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    nepse_div = soup.find_all("div",class_=["pull-left", "banner-green", "banner-item"])[0]
    point_div = nepse_div.find_all("div",class_=["current-index"])[0]
    point_change = nepse_div.find_all("div",class_=["point-change"])[0]
 
    x.append({
            "name":"NEPSE",
            "point":point_div.text.strip(),
            "change":point_change.text.strip(),
            "order":1
            })
    # for world
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
                    "order":2

                }
             )  
        if 'dow' in market_name.lower():
            x.append(
            {
                    "name":"DJI",
                    "point":market_point,
                    "change":market_change,
                    "order":3
                }
             )
        if 'ftse 100' in market_name.lower():
            x.append(
            {
                    "name":"FTSE 100",
                    "point":market_point,
                    "change":market_change,
                    "order":4
                }
             )  
        if 'dax' in market_name.lower():
            x.append(
            {
                    "name":"DAX",
                    "point":market_point,
                    "change":market_change,
                    "order":5
                }
             )  
        if 'cac' in market_name.lower():
            x.append(
            {
                    "name":"CAC 40",
                    "point":market_point,
                    "change":market_change,
                    "order":6
                }
             )  
        if 'nikkei' in market_name.lower():
            x.append(
            {
                    "name":"NIKKEI 225",
                    "point":market_point,
                    "change":market_change,
                    "order":7
                }
             )  

        if 'hang seng' in market_name.lower():
            x.append(
            {
                    "name":" HANG SENG",
                    "point":market_point,
                    "change":market_change,
                    "order":8
                }
             )   
        if 'sensex' in market_name.lower():
            x.append(
            {
                    "name":"SENSEX",
                    "point":market_point,
                    "change":market_change,
                    "order":9
                }
             )  

        if 'nifty' in market_name.lower():
            x.append(
            {
                    "name":"NIFTY FIFTY",
                    "point":market_point,
                    "change":market_change,
                    "order":10
                }
             )  
    x = sorted(x ,key=lambda item:item['order'])
    return jsonify(x)


@app.route("/exp")
def ExpiryTime():
    try:
        file1 = open("data.json","r+")
        data = json.load(file1)
        file1.close()
        return jsonify(data[0])
    except:
        return jsonify(["some eror"])
    

@app.route("/test")
def Test():
    now = datetime.now()
    return render_template('my-form.html')

@app.route('/test', methods=["GET",'POST'])
def my_form_post():
    # email = None

    text = request.form['text']
    processed_text = text.upper()
    print(processed_text)
    return processed_text

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)









