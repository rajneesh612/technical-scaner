import os
import csv
import pandas as pd
import yfinance as yf
import numpy
import talib
from datetime import datetime
from flask import Flask, render_template, request, app
from patterns import candlestick_patterns

from sys import argv

from flask import Flask
application = Flask(__name__)

@application.route('/')
def home():
    pattern= request.args.get('patterns',None)
    stock_dict ={"company":[],"Pattern":[] , "type":[]};
    stocks = {}
    stock_name=[]
    stock_patter=[]
    stock_trend=[]
    row = 0
    if pattern:
        datafile =os.listdir('data/daily')
        for filename in datafile:
            df=pd.read_csv('data/daily/{}'.format(filename))
            pattern_function= getattr(talib,pattern)
            #print(pattern_function)
            try:
                result= pattern_function(df['Open'],df['High'],df['Low'],df['Close'])
                #print(result)
                last=   result.tail().values[0]
                print(last)

                if last>0:
                    print("{} triggered {}".format(filename,pattern))
                    stock_dict["company"].append(filename)
                    stock_dict["Pattern"].append(pattern)
                    stock_dict["type"].append("Bullish")
                    #stocks[row] = {'company': filename}
                    #row =row +1
                    stock_name.append(filename)
                    stock_patter.append(pattern)
                    stock_trend.append("bullish")
                if last<0:
                    print("{} triggered {}".format(filename,pattern))
                    stock_dict["company"].append(filename)
                    stock_dict["Pattern"].append(pattern)
                    stock_dict["type"].append("Bearish")
                    #stocks[row] = {'company': filename}
                    #row = row + 1
                    stock_name.append(filename)
                    stock_patter.append(pattern)
                    stock_trend.append("bearish")
            except:
                pass
            #print(df)
        print(stocks)
        #print(pattern)

    return render_template('home.html', candlestick_patterns=candlestick_patterns, req_list=zip(stock_name,stock_patter,stock_trend) )


@application.route('/snapshot')
def snapshot():
    f = open("data/data.csv", "r")
    companies = csv.reader(f)
    print(companies)
    db = []
    for line in csv.reader(f):
        db.append(line)
    #print(db)
    # companies= f.read()

    d1 = datetime.today().strftime('%Y-%m-%d')
    for company in db:
        symbol = company[0]
        print(symbol)
        data = yf.download(symbol, start="2020-10-01", end= d1)
        data.to_csv('data/daily/{}.csv'.format(symbol))
    return {

        'code': 'sucess'
    }
