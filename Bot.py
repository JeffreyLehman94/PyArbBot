import ccxt
import time
import datetime
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np

SYMBOL = 'DGB/ETH'


def getKucoin():
    book = ccxt.kucoin().fetch_order_book(SYMBOL, {'depth': 10})

    # This array will return the bid in [0] and ask in [1]
    prices = [-1, -1]
    prices[0] = book['bids'][0][0]
    prices[1] = book['asks'][0][0]
    print(prices)
    return prices


def getBittrex():
    book1 = ccxt.bittrex().fetch_order_book(SYMBOL, {'depth': 10})

    # This array will return the bid in [0] and ask in [1]
    prices = [-1, -1]
    prices[0] = book1['bids'][0][0]
    prices[1] = book1['asks'][0][0]
    print(prices)
    return prices


def createDataFrame():
    kuCoinPrices = getKucoin()
    bittrexPrices = getBittrex()
    diff = kuCoinPrices[0] - bittrexPrices[1]
    print("BUYING ON KUCOIN AND SELLING ON BITTREX WILL YEILD: %s" % (diff))
    diff1 = bittrexPrices[0] - kuCoinPrices[1]
    print("BUYING ON KUCOIN AND SELLING ON BITTREX WILL YEILD: %s" % (diff1))
    print(time.ctime())
    frame = pd.DataFrame({'Time': [time.ctime()],
                       'Buying Kucoin': [diff],
                       'Buying Bittrex': [diff1]
                       })
    return frame


df = createDataFrame()
print(df)
writer = ExcelWriter('Pandas-Example2.xlsx')
df.to_excel(writer, 'Sheet1', index=False)
writer.save()
writer.close()
while True:
    try:
        df2 = createDataFrame()
        df = df.append(df2)
        print(df)
        df.to_excel(writer, 'Sheet1', index=False)
        writer.save()
        writer.close()
        time.sleep(60*5)
    except:
        continue
