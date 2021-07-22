from flask import Flask,jsonify
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

@app.route("/")
def index():
    URL = "https://www.moneycontrol.com/markets/global-indices/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    # div = soup.find_all("h2",class_=["title_24px", "fn22", "CTR","title_botline"])[0]
    table = soup.find_all("table",class_=["mctable1", "n18_res_table", "tbl_scroll_resp"])[0]


    all_tr = table.tbody.find_all("tr")
    x = []
    for item in all_tr:
        x.append({"name":item.td.a.text.strip()})
        # x["name"] = item.td.a.text.strip()
    return jsonify(x)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)