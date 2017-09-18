#!/usr/bin/python3
import time
import sys
import json
import os
import lib
import fake

currency = 'BTC_STRAT'

if len(sys.argv) > 1:
    currency = 'BTC_{}'.format(sys.argv[1].upper())

pList = lib.returnTicker(forceUpdate = True)
rate = float(pList[currency]['lowestAsk'])

fee = 0.0025

def find_next(data):
    sortlist = sorted(data, key = lambda x: x['rate'])
    buyList = list(filter(lambda x: x['type'] == 'buy', sortlist))
    sellList = list(filter(lambda x: x['type'] == 'sell', sortlist))

    # total amount of the currency sold
    ttl_sell_currency = sum([x['amount'] for x in sellList])
    ttl_sell_btc = sum([x['total'] for x in sellList])

    ttl_buy_currency = 0
    ttl_buy_btc = 0
    for x in buyList:
        if ttl_buy_currency >= ttl_sell_currency:
            return x['rate']
            break
        ttl_buy_currency += x['amount']
        ttl_buy_btc += x['total'] 

lib.bprint("{} @ {:.8f}".format(currency, rate))
data = lib.trade_history(currency, forceUpdate = True)

next_price = []
for i in range(0,10):
    strike = find_next(data)
    if strike:
        next_price.append(find_next(data))
    fake.sell(data, 0.0005 / rate, rate)

marker = {True: '*', False: ' '}
for p_int in range(100,120,2):
    p = float(p_int)/ 100
    lib.bprint ("{:.2f} {}".format(p, "\t".join(["{} {:.8f}".format(marker[rate > i * p], i * p) for i in next_price])))

data = lib.trade_history(currency)
buyList = list(filter(lambda x: x['type'] == 'buy', data))
sellList = list(filter(lambda x: x['type'] == 'sell', data))

print("Last buy")
lib.bprint("\n".join([" {} {:.8f} {:.8f}".format(i['date'], i['rate'], i['btc']) for i in reversed(buyList[-5:])]))
print("Last sell")
lib.bprint("\n".join([" {} {:.8f} {:.8f}".format(i['date'], i['rate'], i['btc']) for i in reversed(sellList[-5:])]))
