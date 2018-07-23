# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 13:01:00 2018

@author: mfadeev
"""

import requests
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    
    get_page = requests.get(url)
    raw_data = get_page.json()['Data']
    df = pd.DataFrame(raw_data)
    df['datetime'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df

'''
SMALL FUNCTION TO DRAW GRAPHS
'''

def small_graph_draw(data_file):
    time = [i.strftime('%H:%M') for i in data_file.datetime]

    data_file['close'].plot(color='red')
    plt.ylabel('Price of the cryptocurrency')
    data_file['volumefrom'].plot(kind='bar', secondary_y=True, width = 0.5)
    plt.ylabel('Volume')
    ax = plt.gca()
    ax.set_xticklabels(time)
    return plt

'''
GETTING 3 PAIRS
'''

btc = coinmarketcap_data('BTC', 'USD', 'h', 24)
eth = coinmarketcap_data('ETH', 'USD', 'h', 24)
eos = coinmarketcap_data('EOS', 'USD', 'h', 24)

small_graph_draw(btc).show()
small_graph_draw(eth).show()
small_graph_draw(eos).show()

'''
CREATING A SIMPLE MODEL
'''

### First of all we have to make our time series stationary
btc_returns = np.diff(np.log(btc.close))
eth_returns = np.diff(np.log(eth.close))
eos_returns = np.diff(np.log(eos.close))

### Now let's create simple ARMA models for each TS
from statsmodels.api import tsa

### Small function for ARMA results generation
def simple_arma(returns_file):
    arma = tsa.ARMA(returns_file[:20], (2,1))
    arma_results = arma.fit()
    arma_predictions = arma_results.predict(0, len(returns_file))
    
    plt.plot(returns_file, color='red', label='data')
    plt.plot(arma_predictions, 'b-', label='ARMA prediction')
    plt.ylabel('Returns')
    plt.legend(loc=4)
    returns_next = arma_predictions[-1]
    
    return returns_next

### Fitting three models, getting predicted returns for the next hour
next_returns = {}
next_returns["BTC"] = np.exp(simple_arma(btc_returns))-1
next_returns["ETH"] = np.exp(simple_arma(eth_returns))-1
next_returns["EOS"] = np.exp(simple_arma(eos_returns))-1

print(next_returns)
