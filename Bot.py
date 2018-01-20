import ccxt
import time
import pandas as pd
from pandas import ExcelWriter

# This is the trading-pair the bot will be searching for
# Changing this will change the overall program for a different pair
SYMBOL = 'NEO/ETH'
SYMBOL2 = 'ETH/NEO'
# Gets the current bid and ask prices of the trading pair on Kucoin
# Returns an array of the highest bid (index 0) and the lowest ask (index 1)
def getKucoin():
    book = ccxt.kucoin().fetch_order_book(SYMBOL, {'depth': 10})
    prices = [-1, -1]
    prices[0] = book['bids'][0][0]
    prices[1] = book['asks'][0][0]
    return prices


# Gets the current bid and ask prices of the trading pair on Bittrex
# Returns an array of the highest bid (index 0) and the lowest ask (index 1)
def getBinance():
    book1 = ccxt.binance().fetch_order_book(SYMBOL)
    prices = [-1, -1]
    prices[0] = book1['bids'][0][0]
    prices[1] = book1['asks'][0][0]
    return prices


# This def gets the prices on two different exchanges, checks if there is an arbitrage opportunity (buy/ask > 1)
# then creates and returns a dataframe with this data
def createDataFrame():
    kuCoinPrices = getKucoin()
    bittrexPrices = getBinance()
    diff1 = kuCoinPrices[0] / bittrexPrices[1]
    diff = bittrexPrices[0] / kuCoinPrices[1]
    frame = pd.DataFrame({'ATime': [time.ctime()],
                          'KucoinBid': [kuCoinPrices[0]],
                          'KucoinAsk': [kuCoinPrices[1]],
                          'KucoinDiff': [diff],
                          'BittrexBid': [bittrexPrices[0]],
                          'BittrexAsk': [bittrexPrices[1]],
                          'BittrexDiff': [diff1],
                          })
    return frame


# Main method for starting the program
# Currently creates a dataframe, appends it to the previous one and writes the dataframe to an excel spreadsheet
# This runs every 5 minutes
def main():
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


main()
