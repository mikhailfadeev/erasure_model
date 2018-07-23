# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 15:36:27 2018

@author: mfadeev
"""


import requests
import datetime
import pandas as pd

'''
CREATING A SIMPLE FUNCTION TO DOWNLOAD COINMARKETCAP DATA VIA API
'''

def coinmarketcap_data(ticker, conversion_currency, frequency, data_points):
    if frequency == 'm':
        freq = 'histominute'
    elif frequency == 'h':
        freq = 'histohour'
    elif frequency == 'd':
        freq = 'histoday'
    
    ### Time period to aggregate the data over (for daily it's days, for hourly it's hours and for minute histo it's minutes)
    aggregate = 1
    
    url = 'https://min-api.cryptocompare.com/data/{}?fsym={}&tsym={}&limit={}&aggregate={}'\
    .format(freq, ticker.upper(), conversion_currency.upper(), data_points, aggregate)
    
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df