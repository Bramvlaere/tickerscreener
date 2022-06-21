from bs4 import BeautifulSoup
import requests
import os
import json
import datetime
import sys,os
from bs4 import BeautifulSoup
import requests
import pandas as pd
import tabulate
from sqlalchemy.orm import sessionmaker
import Database_implementation as decl
import sqlalchemy as db
import pytz, holidays
import shutil
import zipfile


class db_holder:
    def __init__(self):
        pass
    
    
    def create_session(self):
        ''''
        shortcut to create session to the database
        :PARAM None
        :RETURN session object

        ''' 
        filename = os.path.abspath(__file__)
        dbdir = filename.rstrip('classmodule.py')
        dbpath = os.path.join(dbdir, "findatabase.db")
        engine = db.create_engine(f'sqlite://///{dbpath}.sqlite3',echo=True) 
        decl.Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        return session
    def query_insert(self,table_name,jsoninsert):
        filename = os.path.abspath(__file__)
        dbdir = filename.rstrip('classmodule.py')
        dbpath = os.path.join(dbdir, "findatabase.db")
        engine = db.create_engine(f'sqlite://///{dbpath}.sqlite3',echo=True) 
        connection = engine.connect()
        metadata = db.MetaData()
        table = db.Table(table_name, metadata, autoload=True, autoload_with=engine)
        connection.execute(table.insert(),jsoninsert)

        
        

class Ticker_logger:   
 
    '''Represent a collection of All the days you called the function'''
 
    def __init__(self):
 
        ''' Initialize Finance_log with an empty list'''
        self.finlogs = []
        
    def checkmarkettime(self):
        tz = pytz.timezone('US/Eastern')
        us_holidays = holidays.US()
        def afterHours(now = None):
                if not now:
                    now = datetime.datetime.now(tz)
                openTime = datetime.time(hour = 9, minute = 30, second = 0)
                closeTime = datetime.time(hour = 16, minute = 0, second = 0)
                # If a holiday
                if now.strftime('%Y-%m-%d') in us_holidays:
                    return True
                # If before 0930 or after 1600
                if (now.time() < openTime) or (now.time() > closeTime):
                    return True
                # If it's a weekend
                if now.date().weekday() > 4:
                    return True

                return False
            
    #def Generate_report(self):
        '''
                for filename in os.listdir():
                if 'generated' in filename:
                shutil.rmtree(filename)
            if filename.endswith(".zip"):
                os.remove(filename)
        '''

        
        #reportzip = zipfile.ZipFile('generated_report.zip'), 'w')
        
        #for folder, subfolders, files in os.walk('/Users/vanlaere/Desktop/FinScraper'):
        
         #   for file in files:
        #        if file.endswith('.pdf'):
        #            reportzip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), '/Users/vanlaere/Desktop/FinScraper'), compress_type = zipfile.ZIP_DEFLATED)
        
        #reportzip.close()                
        
                #return f+'.xlsx'
        
            
            
            
        
        
    def New_Ticker_Finlog(self,url):
        """Goes to the trending ticker tab and collects all the most relevant information while creating a json file and returns it in an organized dictionary format

        Returns:
            dictionary: collection of the most trending tickers with the key as the info and the value as value
        """    
        data_type=url.split('/')
        Data_collection=[]
        popper=['52 Week Range','Intraday High/Low','Day Chart','Market Time','Avg Vol (3 month)','PE Ratio (TTM)']#popout items if they exist
        name_map={'Price_Intraday':'Price (Intraday)','ChangeByPercentage':'% Change','MarketCap':'Market Cap','LastPrice':'Last Price'}
        url_response = BeautifulSoup(requests.get(url).content, 'html.parser').find_all(class_ = 'simpTblRow')    
        for tag in url_response:
            
            collector={row['aria-label']:row.getText() for row in tag.find_all('td')}
            for colum in popper: # this part could be way more efficient would fix it if more time was available
                collector.pop(colum,None)
            for correct_name,incorrect_name in name_map.items():
                collector[correct_name] = collector.pop(incorrect_name,None)
            collector={k: v for k, v in collector.items() if v!=None}    
            collector['Link']=tag.find('a')['href']
            collector['Date']=str(datetime.date.today())
            Data_collection.append(collector)
            
            
            
        #os.mkdir(f'FinData_Collected-{data_type[-1]}') later add functionality to have every record in a seperate folder
        save_path = 'FinData_Collected'
        save_path = os.path.join(os.getcwd(),save_path)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        file_name = f"{data_type[-1]}_Data-{datetime.date.today()}.json"
        completeName = os.path.join(save_path, file_name)
        with open(completeName, 'w+') as fp: #writed data to json
            json.dump(Data_collection, fp,indent=2)
        self.From_Json_dbloader(data_type[-1],save_path)
        return Data_collection
    
    def From_Json_dbloader(self,d_type,pather):
        for filename in os.listdir(pather):
            file_typ=filename.split('_')[0]
            if file_typ==d_type:
                f = os.path.join(pather, filename)
                with open(f, 'r') as openfile:
                        json_object = json.load(openfile)
                        if d_type=='gainers':
                            db_holder().query_insert('GainersOfTheDay',json_object)
                        elif d_type=='most-active':
                            db_holder().query_insert('MostActiveOfTheDay',json_object)
                        else:
                            db_holder().query_insert('TrendingTickerOfTheDay',json_object)
                            
                            

                
  

        

class Menu:
    def __init__(self):
        self.url_finder=['https://finance.yahoo.com/trending-tickers','https://finance.yahoo.com/gainers','https://finance.yahoo.com/most-active']
        self.choices = {"1" : self.add_log,'2':self.Show_Full_Log,"3" : self.quit}
        #not working print('\n==========================================\n','YOUR WEBSERVER WILL START AUTOMATICALLY','\n==========================================\n')
    def auto_logger(self):
        for url in self.url_finder:
            print(url)
            Ticker_logger().New_Ticker_Finlog(self.url_finder[url])
            #add redoing it daily
        print("Your auto logs have been added and scheduled daily") 

    def add_log(self):

        ''' Add a new log in the collected folder ''' 

        memo = int(input(""" 



                Please enter: Option Ticker Menu  


                0# Trending Tickers

                1# Best Performance Tickers

                2# Most Activity Tickers
                

                """))
        new_inquery=Ticker_logger()
        new_inquery.New_Ticker_Finlog(self.url_finder[memo])
        print("Your logs have been added")   

    def Show_Full_Log(self):
        # assign directory
        # iterate over files in that directory
        dir_path = './FinData_Collected'
        #print(os.path.realpath('__main__.py')) might make it more scalable
        dir_path = os.path.join(os.getcwd(),dir_path)
        for filename in os.listdir(dir_path):
            f = os.path.join(dir_path, filename)
            if os.path.isfile(f):
                titler=f[:-5].replace('-',' ').split('/')[-1].upper()
                print('\n','##################','\n','\n',titler,'\n','\n','##################','\n')
                df = pd.read_json(f)
                print(tabulate.tabulate(df, headers = 'keys', tablefmt = 'pretty'))          

    def display_menu(self):

        print(""" 



                Finlogger Menu  



                1. Add Finance Log

                2. Show Full Finance Log

                3. Quit program

                """)

    def run(self):
        
        
        ''' Display menu and respond to user choices '''




        self.display_menu()

        choice = input("Enter an option: " )

        action = self.choices.get(choice)

        if action:

                action()

        else:

            print("{0} is not a valid choice".format(choice))

    def quit(self):

        ''' quit or terminate the program '''



        print("Thank you for using finlogger today")

        sys.exit(0)
        

