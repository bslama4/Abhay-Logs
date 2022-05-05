from kiteconnect import KiteConnect
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
api_key="t379p57sb0374g5l"
api_secret="9q2n3xp8mzult6qi7g4w8rt62yinjejn"
kite = KiteConnect(api_key=api_key)

#If you need access token from idle just comment out the below 2 line then afte place the access token to the 3rd line
####KRT=kite.request_access_token('your_request_token',api_secret)
####print(KRT)
atData = kite.generate_session("sEt5m5kBcpsqfPXU1Z5vWKAW5TST02Dq", api_secret=api_secret)
kite.set_access_token(atData["access_token"])


style.use('fivethirtyeight')

def MA(data,n):
    MA=pd.Series(pd.rolling_mean(data['close'],n),name='MA')
    data=data.join(MA)
    return data

print("placing order")
ORDER= [
{
"exchange":"NSE",
"tradingsymbol": "INFY",
"transaction_type": kite.TRANSACTION_TYPE_SELL,
"quantity": 1,
"order_type": "LIMIT",
"product": kite.PRODUCT_CNC,
"price": 1550
},
{
"exchange":"NSE",
"tradingsymbol": "INFY",
"transaction_type": kite.TRANSACTION_TYPE_SELL,
"quantity": 1,
"order_type": "LIMIT",
"product": kite.PRODUCT_CNC,
"price": 1580
}]
trigger_id = kite.place_gtt(trigger_type=kite.GTT_TYPE_OCO, tradingsymbol='INFY', exchange='NSE', trigger_values=[1550,1600], last_price=1570,orders=ORDER)
print(trigger_id)
"""data=kite.historical_data(instrument_token='325121',from_date='2022-04-27',to_date='2017-04-27',interval='minute')
print("Printing data")
print(data)
data=pd.DataFrame(data)
n=2
SMA=MA(data,n)
MA=SMA['MA']
print(SMA)
SMA.plot()
plt.show()"""