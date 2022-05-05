from datetime import date
from datetime import datetime
import datetime
import returncalculator
import trendline_30
import trendline_90
import trendline_180
import trendline_270
import trendline_365
import optimize_30
import optimize_90
import optimize_180
import optimize_270
import optimize_365
import data_coinapi


#assets = ["S&P500","BTC","ETH","USDT", "MATIC"]

assets = ["BTC","ETH","USDT", "MATIC"]


begdate = datetime.datetime(2020, 12, 31, 0, 0)
enddate = datetime.datetime(2021, 12, 31, 0, 0)

##you can change the risk free rate here
risk_free_rate = 0.03


## this calls code that fetches data from CoinAPI which is a crypto data provider. Pleae note that the data is collected
##from 400 days earlier from the "begdate" as you need that data to calculate 365 day returns. 

for i in range(len(assets)):
    try:
        data_coinapi.collect(assets[i], begdate, enddate)
        print('got data for ' + assets[i] )
        
    except:
        print('could not get data for ' + assets[i] )
        

##this calls the return calculator and calculates returns. This might take some time. 
returncalculator.main(assets, begdate, enddate)
print("return calculations done")


##creates trendlines. Charts saved in the chart folder. 
trendline_30.main1(risk_free_rate)
print("30 day trendlines done")

trendline_90.main2(risk_free_rate)
print("90 day trendlines done")

trendline_180.main3(risk_free_rate)
print("180 day trendlines done")

trendline_270.main4(risk_free_rate)
print("270 day trendlines done")

trendline_365.main5(risk_free_rate)
print("365 day trendlines done")


##calculates optimized portfolios and creates charts. Charts saved in the Charts folder. 
optimize_30.opt_port30(risk_free_rate)
print("30 day optimization_done")

optimize_90.opt_port90(risk_free_rate)
print("90 day optimization_done")

optimize_180.opt_port180(risk_free_rate)
print("180 day optimization_done")

optimize_270.opt_port270(risk_free_rate)
print("270 day optimization_done")


optimize_365.opt_port365(risk_free_rate)
print("365 day optimization_done")

