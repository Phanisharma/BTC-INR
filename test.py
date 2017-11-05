import ccxt
import requests

ccyXchange_API = "http://api.fixer.io/latest?base=INR&symbols=USD,JPY"
# min24 = cs.getMin24Hrs(_endpoint="/exchange/min24Hr")
# max24 = cs.getMax24Hrs(_endpoint="/exchange/max24Hr")
# ask_orders = cs.getAskOrders(_endpoint="/exchange/ask/orders", _max=10)
# bid_orders = cs.getBidOrders(_endpoint="/exchange/bid/orders", _max=10)
#
# print(min24)
# print(max24)
# print(ask_orders)
# print(bid_orders)

# ccxt - Market depth
# print(exchange.fetch_l2_order_book('BTC/INR', {'depth': 10}))


# convert to INR
def toINR(Ticker, CCY):
    try:
        r = requests.get(ccyXchange_API)
    except requests.exceptions.ConnectionError:
        print("Connection refused")
        return -404
    data = r.json()
    if(CCY == 'JPY'):
        Ticker[2:] = [x / data["rates"]["JPY"] for x in Ticker[2:]]
    else:
        Ticker[2:] = [x / data["rates"]["USD"] for x in Ticker[2:]]
    return(Ticker)


# ccxt - Market Price
def ExchangeMarketPrice(exchange, Symbol):
    orderbook = exchange.fetch_order_book(Symbol)
    bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
    ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None
    spread = (ask - bid) if(bid and ask) else None
    return[exchange.id, 'market price', bid, ask, spread]


# ccxt - Ticker - all data
# print(exchange.fetch_ticker('BTC/INR'))
coinsecure = ExchangeMarketPrice(ccxt.coinsecure(), 'BTC/INR')  # India
bitfinex = ExchangeMarketPrice(ccxt.bitfinex2(), 'BTC/USD')  # US
bitstamp = ExchangeMarketPrice(ccxt.bitstamp1(), 'BTC/USD')  # US
bitflyer = ExchangeMarketPrice(ccxt.bitflyer(), 'BTC/JPY')

coinsecure[2:] = [x / 100 for x in coinsecure[2:]]
bitfinex_INR = toINR(bitfinex, 'USD')
bitstamp_INR = toINR(bitstamp, 'USD')
bitflyer_INR = toINR(bitflyer, 'JPY')

print(coinsecure)
print(bitfinex_INR)
print(bitstamp_INR)
print(bitflyer_INR)
