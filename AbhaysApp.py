#Glinghang Associates
import logging
from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
import pandas as pd
from talib import RSI, BBANDS, EMA, SMA, LINEARREG_SLOPE
import time
import os
import random
from datetime import datetime
from Indicators import Indicators

logfilename = os.path.join(os.getcwd(), "logs", datetime.now().strftime("%Y%m%d-%H%M%S"))
logfilename += '.txt'
logging.basicConfig(filename=logfilename,format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)
trd_portfolio = {325121: "AMBUJACEM", 40193: "APOLLOHOSP"}

kws = "";
kite = "";
orderID = 0
"""
make a list of OHLC1min and OHLC5mins
"""
def get_login(api_k, api_s):  # log in to zerodha API panel
    global kws, kite;
    kite = KiteConnect(api_key=api_k)

    print("[*] Generate access Token : ", kite.login_url())
    request_tkn = input("[*] Enter Your Request Token Here : ");

    data = kite.generate_session(request_tkn, api_secret=api_s)
    kite.set_access_token(data["access_token"])
    kws = KiteTicker(api_k, data["access_token"])


api_k = "t379p57sb0374g5l";  # api_key
api_s = "9q2n3xp8mzult6qi7g4w8rt62yinjejn";  # api_secret

get_login(api_k, api_s);  # function that used to get connected with API

ohlc = {};  # python dictionary to store the ohlc data in it
ohlcOneMin = {}
mapOfIndicators = {}

for x in trd_portfolio:
    ohlc[x] = [0, 0, 0, 0, True, 60, 0];  # [o,h,l,c,isThisIsNewCandle,NextTimeToRenewLastCandle,order_id]
    ohlcOneMin[x] = [0, 0, 0, 0, True, 60, 0, True];
    

def calculate_ohlc_one_minute(company_data):
    try:
        logging.debug("One min Candle data :: " + trd_portfolio[company_data['instrument_token']] + "  : " + str(
            ohlcOneMin[company_data['instrument_token']][0]) +
                     " : " + str(ohlcOneMin[company_data['instrument_token']][1]) + " : " + str(
            ohlcOneMin[company_data['instrument_token']][2]) +
                     " : " + str(ohlcOneMin[company_data['instrument_token']][3]))
        logging.info(str(company_data['exchange_timestamp'].second) + " " + str(ohlcOneMin[company_data['instrument_token']][7]))
        if company_data['exchange_timestamp'].second == 0 and ohlcOneMin[company_data['instrument_token']][7] :
            """print(trd_portfolio[company_data['instrument_token']], " : ", ohlcOneMin[company_data['instrument_token']][0],
                  " : ", ohlcOneMin[company_data['instrument_token']][1], " : ", ohlcOneMin[company_data['instrument_token']][2],
                  " : ", ohlcOneMin[company_data['instrument_token']][3])  # printing last candle"""
            ohlcOneMin[company_data['instrument_token']][7] = False
            #print("Printing last 1 min candle\n")
            #logging.info(("Printing last one min candle"))
            logging.info(("Printing last One min candle"))
            logging.info("One min Candle data :: " + trd_portfolio[company_data['instrument_token']] + "  : " + str(ohlcOneMin[company_data['instrument_token']][0]) +
                  " : " + str(ohlcOneMin[company_data['instrument_token']][1]) + " : " + str(ohlcOneMin[company_data['instrument_token']][2]) +
                  " : " + str(ohlcOneMin[company_data['instrument_token']][3]))
            #print("------------------------------------------------------------------\n")

            """ind1 = Indicators(x, trd_portfolio[x], 1)
                ind5 = Indicators(x, trd_portfolio[x], 5)
                indList = {}
                indList[1] = ind1
                indList[2] = ind5
                mapOfIndicators[x] = indList"""
            indList = mapOfIndicators[company_data['instrument_token']]
            indList[1].append(ohlc[company_data['instrument_token']][3])
            logging.info(str(indList[2].startCal))
            logging.info(str(indList[1]))
            logging.info(str(indList[2]))
            if(indList[2].startCal == True):
                logging.info(str(indList[1]))
                logging.info(str(indList[2]))
                #xoxo
                if(indList[2].prevRSI == 0):
                    return
                if(indList[2].slope > indList[2].buy_threshold):
                    if(indList[2].prevEMA<indList[2].prevSMA and indList[2].EMA>indList[2].SMA and indList[2].RSI>50):
                    #do rest calculations
                        if(indList[1].prevEMA<indList[1].prevSMA and indList[1].EMA>indList[1].SMA and indList[1].RSI>50):
                            logging.info("Placing buy order")
                            sl=prevOhlc5Low
                            sizeofSL=abs(sl-curr1Close)
                            tp=curr1Close+sizeOfSl	
                            entryPrice=curr1Close
                            #placeOrder(entryPrice,sizeOfSl,tp,sl)
                            #buy=True
                            ohlc[company_data['instrument_token']][6] = kite.place_order(tradingsymbol=trd_portfolio[company_data['instrument_token']],price=company_data['last_price'],variety=kite.VARIETY_BO,exchange=kite.EXCHANGE_NSE,transaction_type=kite.TRANSACTION_TYPE_BUY,quantity=10,squareoff=4, stoploss=2,order_type=kite.ORDER_TYPE_LIMIT,product=kite.PRODUCT_BO) #order placement with sl tp
                if(indList[2].slope < indList[2].sell_threshold):
                    if(indList[2].prevEMA>indList[2].prevSMA and indList[2].EMA<indList[2].SMA and indList[2].RSI<50):
                    #do rest calculations
                        if(indList[1].prevEMA>indList[1].prevSMA and indList[1].EMA<indList[1].SMA and indList[1].RSI<50):
                            logging.info("Placing sell order")
                            sl=prevOhlc5Low
                            sizeofSL=abs(sl-curr1Close)
                            tp=curr1Close+sizeOfSl	
                            entryPrice=curr1Close
                            ohlc[company_data['instrument_token']][6] = kite.place_order(tradingsymbol=trd_portfolio[company_data['instrument_token']],price=company_data['last_price'],variety=kite.VARIETY_BO,exchange=kite.EXCHANGE_NSE,transaction_type=kite.TRANSACTION_TYPE_SELL,quantity=10,squareoff=4, stoploss=2,order_type=kite.ORDER_TYPE_LIMIT,product=kite.PRODUCT_BO) #order placement with sl tp
                            #placeOrder(entryPrice,sizeOfSl,tp,sl)
                            #sold=True
                if(indList[2].slope < indList[2].buy_threshold  and indList[2].slope > indList[2].buy_threshold):
                    if(indList[1].prevEMA>indList[1].prevSMA and indList[1].EMA<indList[1].SMA and indList[1].RSI<50 and indList[1].slope>indList[1].buy_threshold and indList[1].slope<indList[1].sell_threshold):
                            logging.info("Placing sell order")
                            sl=prevOhlc5Low
                            sizeofSL=abs(sl-curr1Close)
                            tp=curr1Close+sizeOfSl	
                            entryPrice=curr1Close
                            ohlc[company_data['instrument_token']][6] = kite.place_order(tradingsymbol=trd_portfolio[company_data['instrument_token']],price=company_data['last_price'],variety=kite.VARIETY_BO,exchange=kite.EXCHANGE_NSE,transaction_type=kite.TRANSACTION_TYPE_SELL,quantity=10,squareoff=4, stoploss=2,order_type=kite.ORDER_TYPE_LIMIT,product=kite.PRODUCT_BO) #order placement with sl tp
                            #placeOrder(entryPrice,sizeOfSl,tp,sl)
                            #sold=True
                    
            # making ohlc for new candle
            ohlcOneMin[company_data['instrument_token']][0] = company_data['last_price'];  # open
            ohlcOneMin[company_data['instrument_token']][1] = company_data['last_price'];  # high
            ohlcOneMin[company_data['instrument_token']][2] = company_data['last_price'];  # low
            ohlcOneMin[company_data['instrument_token']][3] = company_data['last_price'];  # close
            
            
        if company_data['exchange_timestamp'].second > 0:
            ohlcOneMin[company_data['instrument_token']][7] = True
        
        if ohlcOneMin[company_data['instrument_token']][1] < company_data['last_price']:  # calculating high
            ohlcOneMin[company_data['instrument_token']][1] = company_data['last_price']

        if ohlcOneMin[company_data['instrument_token']][2] > company_data['last_price'] or \
                ohlcOneMin[company_data['instrument_token']][2] == 0:  # calculating low
            ohlcOneMin[company_data['instrument_token']][2] = company_data['last_price']

        ohlcOneMin[company_data['instrument_token']][3] = company_data['last_price']  # closing price
        ohlcOneMin[company_data['instrument_token']][5] = company_data['exchange_timestamp'].second;

    except Exception as e:
        print(e);


def calculate_ohlc(company_data, timestamp):
    try:
        logging.debug(str(company_data['exchange_timestamp'].minute) + " " + str(timestamp) + " " + str(ohlc[company_data['instrument_token']][4]))
        if (((company_data['exchange_timestamp'].minute == 0) or (company_data['exchange_timestamp'].minute % timestamp == 0)) and ohlc[company_data['instrument_token']][4]):
        #if ohlc[company_data['instrument_token']][4]:
            logging.info(ohlc[company_data['instrument_token']][4])
            ohlc[company_data['instrument_token']][4] = False;
            #print("Printing last 5 mins candle\n")
            logging.info(("Printing last 5 mins candle"))
            logging.info(str(timestamp) + " " + str(ohlc[company_data['instrument_token']][4]) + " Candle data :: " + trd_portfolio[company_data['instrument_token']] + "  : " + str(ohlc[company_data['instrument_token']][0]) +
                  " : " + str(ohlc[company_data['instrument_token']][1]) + " : " + str(ohlc[company_data['instrument_token']][2]) +
                  " : " + str(ohlc[company_data['instrument_token']][3]))
                        
            reqID = company_data['instrument_token']
            indList = mapOfIndicators[reqID]
            indList[2].append(ohlcOneMin[company_data['instrument_token']][3])
            logging.info(str(indList[2].startCal))
            logging.info(str(indList[1]))
            logging.info(str(indList[2]))
            if(indList[2].startCal == True):
                logging.info(str(indList[1]))
                logging.info(str(indList[2]))
            """print(trd_portfolio[company_data['instrument_token']], " : ", ohlc[company_data['instrument_token']][0],
                  " : ", ohlc[company_data['instrument_token']][1], " : ", ohlc[company_data['instrument_token']][2],
                  " : ", ohlc[company_data['instrument_token']][3])  # printing last candle

            print("------------------------------------------------------------------\n")"""
            
            # making ohlc for new candle
            ohlc[company_data['instrument_token']][0] = company_data['last_price'];  # open
            ohlc[company_data['instrument_token']][1] = company_data['last_price'];  # high
            ohlc[company_data['instrument_token']][2] = company_data['last_price'];  # low
            ohlc[company_data['instrument_token']][3] = company_data['last_price'];  # close

            ohlc[company_data['instrument_token']][5] = company_data['exchange_timestamp'].minute + 1;
            if company_data['exchange_timestamp'].hour == 0:
                ohlc[company_data['instrument_token']][5] = 1
        logging.debug(str(company_data['exchange_timestamp'].minute) + " " + str(ohlc[company_data['instrument_token']][4]))
        if company_data['exchange_timestamp'].minute % ohlc[company_data['instrument_token']][5] == 0:
            ohlc[company_data['instrument_token']][4] = True;
                            
        if ohlc[company_data['instrument_token']][1] < company_data['last_price']:  # calculating high
            ohlc[company_data['instrument_token']][1] = company_data['last_price']

        if ohlc[company_data['instrument_token']][2] > company_data['last_price'] or \
                ohlc[company_data['instrument_token']][2] == 0:  # calculating low
            ohlc[company_data['instrument_token']][2] = company_data['last_price']

        ohlc[company_data['instrument_token']][3] = company_data['last_price']  # closing price

        #logging.info("Exchange timestamp and ohlc[company_data['instrument_token']][5] - " + str(company_data['exchange_timestamp'].minute) + " " + str(ohlc[company_data['instrument_token']][5]))
        


    except Exception as e:
        print(e);


def on_ticks(ws, ticks):  # retrive continius ticks in JSON format
    for company_data in ticks:
        #print(company_data['instrument_token']) #['timestamp'])
        logging.debug(company_data)
        #print(company_data['volume'])  # print tick by tick data for a perticular company

        calculate_ohlc(company_data, 5);  # finding OHLC for `n` minute candle
        #calculate_ohlc(company_data, 1)
        calculate_ohlc_one_minute(company_data); #special function to calculate 1 minute `ohlc`
        """reqID = company_data['instrument_token']
        indList = mapOfIndicators[reqID]
        indList[1].append(ohlc[company_data['instrument_token']][3])
        indList[2].append(ohlcOneMin[company_data['instrument_token']][3])
        if(indList[1].startCal == True):
            logging.info(indList[1])
            logging.info(indList[2])"""
                        
        # ohlc[company_data['instrument_token']][6] = kite.place_order(tradingsymbol=trd_portfolio[company_data['instrument_token']],price=company_data['last_price'],variety=kite.VARIETY_BO,exchange=kite.EXCHANGE_NSE,transaction_type=kite.TRANSACTION_TYPE_SELL,quantity=10,squareoff=4, stoploss=2,order_type=kite.ORDER_TYPE_LIMIT,product=kite.PRODUCT_BO) #order placement with sl tp
        #print("ORDER PLACED FOR ", trd_portfolio[company_data['instrument_token']], " WITH ORDER ID ",
        #      ohlc[company_data['instrument_token']][6])


def on_connect(ws, response):
    ws.subscribe([x for x in trd_portfolio])
    ws.set_mode(ws.MODE_FULL, [x for x in trd_portfolio])
    
    

# Assign the callbacks.
kws.on_ticks = on_ticks
kws.on_connect = on_connect

for x in trd_portfolio:
    ind1 = Indicators(x, trd_portfolio[x], 1)
    ind5 = Indicators(x, trd_portfolio[x], 5)
    indList = {}
    indList[1] = ind1
    indList[2] = ind5
    mapOfIndicators[x] = indList
kws.connect()