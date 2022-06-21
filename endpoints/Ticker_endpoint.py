import Database_implementation as decl
from sqlalchemy import create_engine, and_, false , or_ ,text
from flask import jsonify,Blueprint,redirect,render_template,request
import datetime
import classmodule


session=classmodule.db_holder().create_session()
Tickerendpoint = Blueprint('tick', __name__) #might need to add template folder and static folder
#test purposes

@Tickerendpoint.route('lookup/<ticker>',methods=['GET'])
def ticker_finder(ticker):
    tick_info = session.query(decl.gainers).from_statement(text(f"SELECT * FROM GainersOfTheDay WHERE Symbol LIKE '%{ticker}%'"))
    tickinfo=[i.Symbol for i in list(tick_info)]
    print(tickinfo[0])
    return render_template('index_ticker.html',tick_info=tickinfo[0])


