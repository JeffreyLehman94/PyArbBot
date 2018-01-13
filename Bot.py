import urllib.request
import ccxt

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


kuCoinPrices = getKucoin()
bittrexPrices = getBittrex()

diff = kuCoinPrices[0]-bittrexPrices[1]
print("BUYING ON KUCOIN AND SELLING ON BITTREX WILL YEILD: %s" %(diff))
diff = bittrexPrices[0]-kuCoinPrices[1]
print("BUYING ON KUCOIN AND SELLING ON BITTREX WILL YEILD: %s" %(diff))