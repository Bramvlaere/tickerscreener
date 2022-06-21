from flask import Flask,redirect,render_template,request
from endpoints.Ticker_endpoint import Tickerendpoint
from sqlalchemy import create_engine, and_, false , or_ ,text
import pandas as pd
import datetime
import requests
import classmodule
from bs4 import BeautifulSoup
import Database_implementation as decl
import time
import os

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(APP_PATH, 'TICKSCREENER/templates')
print(TEMPLATE_PATH)
app = Flask(__name__,template_folder=TEMPLATE_PATH)
app.register_blueprint(Tickerendpoint, url_prefix='')

@app.route('/background_process')
def background_process():
    location=classmodule.Ticker_logger().Generate_report()
    return location


@app.route('/')
def index():
    session=classmodule.db_holder().create_session()
    tick_info = session.query(decl.gainers).from_statement(text(f"SELECT * FROM GainersOfTheDay"))
    biggestgainer=max([float(k.ChangeByPercentage[1:-1]) for k in tick_info])
    lowestgainer=min([float(k.ChangeByPercentage[1:-1]) for k in tick_info])
    gainticker=[i.Symbol for i in session.query(decl.gainers).from_statement(text(f"SELECT * FROM GainersOfTheDay WHERE ChangeByPercentage LIKE '%{biggestgainer}%'"))]
    gainlowtick=[i.Symbol for i in session.query(decl.gainers).from_statement(text(f"SELECT * FROM GainersOfTheDay WHERE ChangeByPercentage LIKE '%{biggestgainer}%'"))]
    earning = datetime.datetime(2022, 6, 30) - datetime.datetime.now()
    lowestgainer=[str(lowestgainer)+'%',gainlowtick[0]]
    biggestgainer=[str(biggestgainer)+'%',gainticker[0]]
    if classmodule.Ticker_logger().checkmarkettime():
        market='Open'
    else: market='Closed'

    return render_template('index.html', tick_info=tick_info,biggestgainer=biggestgainer,earning=earning,lowestgainer=lowestgainer,market=market)



if __name__ == '__main__':
    app.run(debug=True) #have turned debugging on for the sake of allowing to save while running server