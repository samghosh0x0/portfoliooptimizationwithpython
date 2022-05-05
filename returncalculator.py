import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from datetime import date
from datetime import datetime
import datetime
from dateutil import parser
import numpy as np
import re



def main(assets, beg_date, end_date):

    N = len(assets)


    begdate = beg_date
    enddate = end_date

    analysis_currency = "USD"



    #for converting removing dollar signs from price values
    non_decimal = re.compile(r'[^\d.]+')


    for asset in range(len(assets)):
        
        data_r = pd.read_csv ('Data/'+assets[asset]+'.csv')
        count= len(data_r)

        for j in range(count):
            
            dtobj = parser.parse(data_r['Date'][j])
            data_r['Date'][j] = dtobj
            
        data = data_r.sort_values(by=['Date'], ascending=True)
        data = data.reset_index(drop=True)

        data['Close'] = data['Close'].astype(str)
        
        for j1 in range(count):
            data['Close'][j1] = non_decimal.sub('', data['Close'][j1])
            
        data['Close'] = data['Close'].astype(float)

        #very very small prices
        ##data['Close'] = data['Close']*1000
        
        mask = (data['Date'] > begdate) & (data['Date'] <= enddate)
        data1 = data.loc[mask]
        
        data1['Date'] = pd.to_datetime(data1['Date']).apply(lambda date: date.toordinal())

        g = sns.lmplot(data=data1, x="Date", y='Close', truncate=False, scatter_kws={"s": 1}, lowess=True, height=5, aspect=1.5)

        g.fig.subplots_adjust(top=.9)
        
        
        # iterate through the axes of the figure-level plot
        for ax in g.axes.flat:
            labels = ax.get_xticks() # get x labels
            new_labels = [date.fromordinal(int(label)) for label in labels] # convert ordinal back to datetime
            new_labels1 = [item.strftime("%B %d, %Y") for item in new_labels]
            ax.set_xticks(labels)
            ax.set_xticklabels(new_labels1, rotation=30, fontsize=8) # set new labels

            fmt = '${x:,.1f}'
            tick = mtick.StrMethodFormatter(fmt)
            ax.yaxis.set_major_formatter(tick) 
            plt.xticks(rotation=25)

     
        plt.title(assets[asset]+":Price Trend")
        plt.ylabel("Price in "+analysis_currency)
        plt.grid()
        ##plt.show()
        plt.savefig('Charts/price/'+assets[asset]+'price_trend.png', bbox_inches='tight')
        plt.close()



    def return_calc(asset_name):
        
        data_r = pd.read_csv ('Data/'+asset_name+'.csv')
        
        count= len(data_r)

        for j in range(count):
            
            dtobj = parser.parse(data_r['Date'][j])
            data_r['Date'][j] = dtobj
            
        data = data_r.sort_values(by=['Date'], ascending=True)
        data = data.reset_index(drop=True)

        ##print(data)

        data['Close'] = data['Close'].astype(str)
        
        for j1 in range(count):
            data['Close'][j1] = non_decimal.sub('', data['Close'][j1])
            
        data['Close'] = data['Close'].astype(float)

        #Rolling 30 day return.;
        cutoff =  data['Date'][0]+ datetime.timedelta(days=30)
        ##print(cutoff)
        beg30 = (data[(data.Date >= cutoff)].iloc[0][0])
        
        index = (data.index[data['Date'] == beg30]).tolist()

        data['Return30'] = np.NAN

        denom = 0

        for k in range(index[0],count):
            
            data['Return30'][k] = ((data['Close'][k]) / (data['Close'][denom]))-1

            denom = denom + 1


        #Rolling 90 day return.;
        cutoff1 =  data['Date'][0]+ datetime.timedelta(days=90)
        beg90 = (data[(data.Date >= cutoff1)].iloc[0][0])
        
        index1 = (data.index[data['Date'] == beg90]).tolist()

        data['Return90'] = np.NAN

        denom1 = 0

        for k1 in range(index1[0],count):
            
            data['Return90'][k1] = ((data['Close'][k1]) / (data['Close'][denom1]))-1

            denom1 = denom1 + 1
            

        #Rolling 180 day return.;
        cutoff2 =  data['Date'][0]+ datetime.timedelta(days=180)
        beg180 = (data[(data.Date >= cutoff2)].iloc[0][0])
        
        index2 = (data.index[data['Date'] == beg180]).tolist()

        data['Return180'] = np.NAN

        denom2 = 0

        for k2 in range(index2[0],count):
            
            data['Return180'][k2] = ((data['Close'][k2]) / (data['Close'][denom2]))-1

            denom2 = denom2 + 1


        #Rolling 270 day return.;
        cutoff3 =  data['Date'][0]+ datetime.timedelta(days=270)
        beg270 = (data[(data.Date >= cutoff3)].iloc[0][0])
        
        index3 = (data.index[data['Date'] == beg270]).tolist()

        data['Return270'] = np.NAN

        denom3 = 0

        for k3 in range(index3[0],count):
            
            data['Return270'][k3] = ((data['Close'][k3]) / (data['Close'][denom3]))-1

            denom3 = denom3 + 1


        #Rolling 365 day return.;
        cutoff4 =  data['Date'][0]+ datetime.timedelta(days=365)
        beg365 = (data[(data.Date >= cutoff4)].iloc[0][0])
        
        index4 = (data.index[data['Date'] == beg365]).tolist()

        data['Return365'] = np.NAN

        denom4 = 0

        for k4 in range(index4[0],count):
            
            data['Return365'][k4] = ((data['Close'][k4]) / (data['Close'][denom4]))-1

            denom4 = denom4 + 1


            
        data['Date'] = pd.to_datetime(data['Date'])
        mask = (data['Date'] > begdate) & (data['Date'] <= enddate)
        ReturnData1 = data.loc[mask]

        ReturnData = ReturnData1[['Date','Return30', 'Return90', 'Return180', 'Return270', 'Return365']]


        Avg30 = ReturnData['Return30'].mean()
        Vol30= ReturnData['Return30'].std()

        Avg90 = ReturnData['Return90'].mean()
        Vol90 = ReturnData['Return90'].std()

        Avg180 = ReturnData['Return180'].mean()
        Vol180 = ReturnData['Return180'].std()

        Avg270 = ReturnData['Return270'].mean()
        Vol270 = ReturnData['Return270'].std()

        Avg365 = ReturnData['Return365'].mean()
        Vol365 = ReturnData['Return365'].std()

        ReturnData.reset_index(drop=True, inplace=True)

        summary = [Avg30, Vol30, Avg90, Vol90, Avg180, Vol180, Avg270, Vol270, Avg365, Vol365]    
        
        return(ReturnData, summary)


    columns = ['Date']


    Return30_df = pd.DataFrame(columns=columns)
    Return90_df = pd.DataFrame(columns=columns)
    Return180_df = pd.DataFrame(columns=columns)
    Return270_df = pd.DataFrame(columns=columns)
    Return365_df = pd.DataFrame(columns=columns)



    ##merging

    for m in range(N):

        x, y= return_calc(assets[m])

        if (m==0):
            
            
            Return30_df['Date'] = x['Date'].values
            Return30_df[assets[m]] = x['Return30'].values
            

            Return90_df['Date'] = x['Date'].values
            Return90_df[assets[m]] = x['Return90'].values
   
            Return180_df['Date'] = x['Date'].values
            Return180_df[assets[m]] = x['Return180'].values
      
            Return270_df['Date'] = x['Date'].values
            Return270_df[assets[m]] = x['Return270'].values
       
            Return365_df['Date'] = x['Date'].values
            Return365_df[assets[m]] = x['Return365'].values

        else:

            subset_return30 = x[['Date', 'Return30']].copy()
            Return30_df = pd.merge(Return30_df,subset_return30, on='Date')
            Return30_df = Return30_df.rename(columns={'Return30': assets[m]})

            subset_return90 = x[['Date', 'Return90']].copy()
            Return90_df = pd.merge(Return90_df,subset_return90, on='Date')
            Return90_df = Return90_df.rename(columns={'Return90': assets[m]})

            subset_return180 = x[['Date', 'Return180']].copy()
            Return180_df = pd.merge(Return180_df,subset_return180, on='Date')
            Return180_df = Return180_df.rename(columns={'Return180': assets[m]})

            subset_return270 = x[['Date', 'Return270']].copy()
            Return270_df = pd.merge(Return270_df,subset_return270, on='Date')
            Return270_df = Return270_df.rename(columns={'Return270': assets[m]})

            subset_return365 = x[['Date', 'Return365']].copy()
            Return365_df = pd.merge(Return365_df,subset_return365, on='Date')
            Return365_df = Return365_df.rename(columns={'Return365': assets[m]})
            
        Return30_df.to_csv('return_data/Return30_df.csv')
        Return90_df.to_csv('return_data/Return90_df.csv')
        Return180_df.to_csv('return_data/Return180_df.csv')
        Return270_df.to_csv('return_data/Return270_df.csv')
        Return365_df.to_csv('return_data/Return365_df.csv')
        

