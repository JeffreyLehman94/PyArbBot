import ccxt
import time
import pandas as pd
from pandas import ExcelWriter










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
    return prices


def createDataFrame():
    kuCoinPrices = getKucoin()
    bittrexPrices = getBittrex()
    diff = kuCoinPrices[0] - bittrexPrices[1]
    diff1 = bittrexPrices[0] - kuCoinPrices[1]
    frame = pd.DataFrame({'ATime': [time.ctime()],
                          'KucoinBid': [kuCoinPrices[0]],
                          'KucoinAsk': [kuCoinPrices[1]],
                          'KucoinDiff': [diff],
                          'BittrexBid': [bittrexPrices[0]],
                          'BittrexAsk': [bittrexPrices[1]],
                          'BittrexDiff': [diff1],
                          })
    return frame


SYMBOL = 'DGB/ETH'
df = createDataFrame()
writer = ExcelWriter('Pandas-Example2.xlsx')
df.to_excel(writer, 'Sheet1', index=False)
writer.save()
writer.close()
while True:
    try:
        time.sleep(60 * 5)
        df2 = createDataFrame()
        df = df.append(df2)
        df.to_excel(writer, 'Sheet1', index=False)
        writer.save()
        writer.close()

    except:
        continue
