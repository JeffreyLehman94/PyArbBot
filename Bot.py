import ccxt
import time
import pandas as pd
from pandas import ExcelWriter

# This is the trading-pair the bot will be searching for
# Changing this will change the overall program for a different pair
SYMBOL = 'XLM/ETH'
SYMBOL2 = 'MIOTA/XLM'
feeMAX = .0025
ethPrice = ccxt.binance().fetch_order_book('ETH/USDT')
ethPrice = ethPrice['asks'][0][0]
print('ETH price in $: %s' % ethPrice)
ethWorking = 50.00/ethPrice
print('50$ worth of ETH = %s' % ethWorking)

# Gets the current bid and ask prices of the trading pair on Kucoin
# Returns an array of the highest bid (index 0) and the lowest ask (index 1)
def getExchange1():
    book = ccxt.binance().fetch_order_book(SYMBOL)
    prices = [-1, -1]
    prices[0] = book['bids'][0][0]
    prices[1] = book['asks'][0][0]
    return prices


# Gets the current bid and ask prices of the trading pair on Bittrex
# Returns an array of the highest bid (index 0) and the lowest ask (index 1)
def getExchange2():
    book1 = ccxt.bittrex().fetch_order_book(SYMBOL)
    prices = [-1, -1]
    prices[0] = book1['bids'][0][0]
    prices[1] = book1['asks'][0][0]
    return prices


# This def gets the prices on two different exchanges, checks if there is an arbitrage opportunity (buy/ask > 1)
# then creates and returns a dataframe with this data
def createDataFrame():
    Exchange1Prices = getExchange1()
    Exchange2Prices = getExchange2()
    ex1buy = ethWorking/Exchange1Prices[1]

    print('Amount of XLM you can buy on exchange 1: %s' % ex1buy)

    diff1 = Exchange2Prices[0] - Exchange1Prices[1]
    print('Buying xlm on exchange 1 then selling it on exchange 2 will yield: %s per coin' % diff1)
    diff = Exchange1Prices[0] - Exchange2Prices[1]
    print('Buying xlm on exchange 2 then selling it on exchange 1 will yield: %s per coin' % diff)

    frame = pd.DataFrame({'ATime': [time.ctime()],
                          'Ex1Bid': [Exchange1Prices[0]],
                          'Ex1Ask': [Exchange1Prices[1]],
                          'Ex1Diff': [diff],
                          'Ex2Bid': [Exchange2Prices[0]],
                          'Ex2Ask': [Exchange2Prices[1]],
                          'Ex2Diff': [diff1],
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
