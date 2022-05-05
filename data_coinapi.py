import requests
import pandas as pd
from datetime import date
from datetime import datetime
from datetime import timedelta
import datetime
import math

##please get a CoinAPI key 
key = "4A68CA94-BCEA-48D9-A430-D8112C1A330D"

def collect(asset_name, beg_date, end_date):

    asset = asset_name
    begining_date = beg_date.date() - timedelta(days=400)
    ending_date = end_date.date()



    total_period = (ending_date - begining_date).days


    asset_data = pd.DataFrame(columns=['Date','Close'])


    if (total_period<100):
        begining_date_d = str(begining_date)
        ending_date_d = str(ending_date+timedelta(days=1))

        url = "https://rest.coinapi.io/v1/exchangerate/"+asset+"/USD/history?period_id=1DAY&time_start="+begining_date_d+"T00:00:00&time_end="+ending_date_d+"T00:00:00"

        headers = {'X-CoinAPI-Key' : key}
        r = requests.get(url, headers=headers)
        data = r.json()

        data_pd = pd.DataFrame(data)

        data_pd_ref = data_pd[['rate_close','time_period_start']]

        data_pd_ref.columns = ['Close', 'Date']

        data_pd_ref = data_pd_ref[['Date','Close']]

        data_pd_ref['Date'] = data_pd_ref['Date'].astype('datetime64[ns]')

        asset_data = asset_data.append(data_pd_ref, True)
        
        

    else:
        numberof_100_days = total_period/100
        interations = int(math.ceil(numberof_100_days))
        initial_date = begining_date

        for i in range(interations):
            period_beg = initial_date + timedelta(days=(i*100))
            period_end = initial_date + timedelta(days=(i+1)*100)
            url = "https://rest.coinapi.io/v1/exchangerate/"+asset+"/USD/history?period_id=1DAY&time_start="+str(period_beg)+"T00:00:00&time_end="+str(period_end)+"T00:00:00"
            headers = {'X-CoinAPI-Key' : key}
            r = requests.get(url, headers=headers)

            data = r.json()
            ##print(data)
            data_pd = pd.DataFrame(data)

            

            data_pd_ref = data_pd[['rate_close','time_period_start']]

            data_pd_ref.columns = ['Close', 'Date']

            data_pd_ref = data_pd_ref[['Date','Close']]

            data_pd_ref['Date'] = data_pd_ref['Date'].astype('datetime64[ns]')

            asset_data = asset_data.append(data_pd_ref, True)


    asset_data.drop_duplicates(subset=['Date'], keep=False)


    asset_data.to_csv('Data/'+asset+'.csv' ,index=False, encoding='utf-8')
