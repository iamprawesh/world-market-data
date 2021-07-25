from flask import Flask,jsonify,render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def index():
    # for world
    URL = "https://www.moneycontrol.com/markets/global-indices/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    # nifty_sensex = soup.find_all("div",class_=["txtmacmb","slick-slide", "slick-current", "slick-active"])
    # print(nifty_sensex.ul)
    # y =  soup.find("li", {"id": "ind_glb1"})
    results = soup.findAll("div", class_="market_radar_autoload")

    print(results)
    print("results")

    # div = soup.find_all("h2",class_=["title_24px", "fn22", "CTR","title_botline"])[0]
    table = soup.find_all("table",class_=["mctable1", "n18_res_table", "tbl_scroll_resp"])[0]



    all_tr = table.tbody.find_all("tr")
    x = []
    for item in all_tr:
        print()
        all_td = item.find_all("td")
        # print((all_td[0].a.text.strip()))
        # print(all_td[1].text.strip())
        # print(all_td[2].text.strip())
        if all_td[1].text.strip() != "":
            replace_date = item.td.a.text.strip().split("(")[0]
            x.append({
                "name":replace_date.strip(),
                "point":all_td[1].text.strip(),
                "change":all_td[2].text.strip().split('\n')[0]
            })
            # arr.append({"change":all_td[2].text.strip()})
            # x.append(arr)

        # print((all_td[1].a.text.strip()))

        # print(len((all_td)))  
        # x["name"] = item.td.a.text.strip()


    # for nepse
    # pull-left banner-green banner-item
    URL = "http://www.nepalstock.com/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    nepse_div = soup.find_all("div",class_=["pull-left", "banner-green", "banner-item"])[0]
    point_div = nepse_div.find_all("div",class_=["current-index"])[0]
    point_change = nepse_div.find_all("div",class_=["point-change"])[0]

    x.append({
            "name":"nepse",
            "point":point_div.text.strip(),
            "change":point_change.text.strip()
            })
    return jsonify(x)



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
 
    x.insert(1,{
            "name":"NEPSE",
            "point":point_div.text.strip(),
            "change":point_change.text.strip()
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
            x.insert(2,
            {
                    "name":"NASDAQ",
                    "point":market_point,
                    "change":market_change
                }
             )  
        if 'dow' in market_name.lower():
            x.insert(3,
            {
                    "name":"DJI",
                    "point":market_point,
                    "change":market_change
                }
             )
        if 'ftse 100' in market_name.lower():
            x.insert(4,
            {
                    "name":"FTSE 100",
                    "point":market_point,
                    "change":market_change
                }
             )  
        if 'dax' in market_name.lower():
            x.insert(5,
            {
                    "name":"DAX",
                    "point":market_point,
                    "change":market_change
                }
             )  
        if 'cac' in market_name.lower():
            x.insert(6,
            {
                    "name":"CAC 40",
                    "point":market_point,
                    "change":market_change
                }
             )  
        if 'nikkei' in market_name.lower():
            x.insert(7,
            {
                    "name":"NIKKEI 225",
                    "point":market_point,
                    "change":market_change
                }
             )  

        if 'hang seng' in market_name.lower():
            x.insert(8,
            {
                    "name":" HANG SENG",
                    "point":market_point,
                    "change":market_change
                }
             )  
        # if 'sensex' in market_name.lower():
        #     x.insert(8,
        #     {
        #             "name":"SENSEX",
        #             "point":market_point,
        #             "change":market_change
        #         }
        #      ) 
        if 'sensex' in market_name.lower():
            x.insert(9,
            {
                    "name":"SENSEX",
                    "point":market_point,
                    "change":market_change
                }
             )  

        if 'nifty' in market_name.lower():
            x.insert(10,
            {
                    "name":"NIFTY FIFTY",
                    "point":market_point,
                    "change":market_change
                }
             )  

    return jsonify(x)








@app.route("/test")
def Test():
    return render_template('my-form.html')

@app.route('/test', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    print(processed_text)
    return processed_text

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)