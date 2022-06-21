import sys,os
from bs4 import BeautifulSoup
from flask import Flask
import classmodule as classmodule
from webapp import app
import argparse


#before launching the server use the argeparse below to scrape data
#so comment out the app run and undo the comments from argparse

#my_parser = argparse.ArgumentParser()
#my_parser.version = '1.0'
#my_parser.add_argument('-a', action=classmodule.Menu().run())


##def r(run):
 #   classmodule.Menu().run()


if __name__ == '__main__':
    #classmodule.Menu().run()
    app.run(debug=True)
