import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
import statsmodels.api
import matplotlib.ticker as mtick
from scipy import stats
import numpy as np

def main1(risk_free_rate):
    
    pd.options.display.float_format = '{:.2%}'.format
    
    rfr30 = (pow((1+risk_free_rate), (30/365)))-1
                
    df = pd.read_csv('return_data/Return30_df.csv', parse_dates=['Date'])
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    df['Date'] = pd.to_datetime(df['Date']).apply(lambda date: date.toordinal())

    col_names = df.columns.values.tolist()

    #del col_names[0]
    col_names.pop(0)

    assets = col_names
    

    #creating correlation matrix
    df_cor = df.copy()
    df_cor.drop('Date', axis=1, inplace=True)
    corrMatrix = df_cor.corr()
    sns.heatmap(corrMatrix, annot=True).set_title("Correlation Matrix for Rolling 30 Day Returns", fontsize=14)
    plt.savefig('Charts/return30/corr_return30.png')
    ##plt.show()
    plt.savefig('Charts/return30/corr_return30.png')
    plt.close()
    
    #calculating average and volatility
    avg_returns = (df_cor.mean()).tolist()

    vol_returns = (df_cor.std()).tolist()

    

    #calculation for sharpe ratio
    avg_returnminusriskfree = ((df_cor - rfr30).mean()).tolist()

    
    
    sharperatio = [(x)/y for x, y in zip(map(float, avg_returnminusriskfree), map(float, vol_returns))]

    avg_df = pd.DataFrame(
        {'asset': assets,
         'average': avg_returns,
        })#.transpose()

    avg_df['average'] = 100* avg_df['average']

    vol_df = pd.DataFrame(
        {'asset': assets,
         'volatility': vol_returns
        })#.transpose()
    vol_df['volatility'] = 100* vol_df['volatility']

    sharperatio_pd = pd.DataFrame(
        {'asset': assets,
         'sharperatio': sharperatio
        })#.transpose()

    #calculations for upper and lower limits on trend charts
    max2_cols = []
    min2_cols = []
    #finding the 2nd max return value
    for asset in range(len(assets)):
        string = str(assets[asset])
        max2_c = min((df_cor[string].nlargest(2)).tolist())
        max2_cols.append(max2_c)
        

        min2_c = max((df_cor[string].nsmallest(2)).tolist())
        min2_cols.append(min2_c)

    #seeting upper and lower bounds for charts
    upper_bound = (max(max2_cols) + (abs(max(max2_cols)))*0.5)
    ##upper_bound = 2
    lower_bound = (min(min2_cols) - (abs(min(min2_cols)))*0.5)


##    print(max2_cols, min2_cols, upper_bound, lower_bound)
        
    
##    max2return = (df_cor.nlargest(2))[1]
##    print(max2return*100)
    

    # creating subplots for average returns, volatility and sharpe ratio

    fig, axes = plt.subplots(nrows=3, ncols=1)
    fig.tight_layout()

    #for average
    avg = avg_df.plot(ax=axes[0], x="asset", y='average', kind='bar', title ="Average Rolling 30 Day Return",figsize=(15,10), fontsize=12, rot=0, color='g', legend=False, zorder=3)
    avg.grid(axis='y', zorder=0)
    avg.set(xlabel=None)
    avg.set(ylabel='Avg. Rol. 30-d Ret')
    avg.yaxis.set_major_formatter(mtick.PercentFormatter())

    #creating data labels 
    for p1 in avg.patches:
        avg.annotate((str(round(p1.get_height(),2))+"%"), (p1.get_x() * 1.007, p1.get_height() * 1.05), color='black', fontsize=14)

    #for volatility
    vol = vol_df.plot(ax=axes[1], x="asset", y='volatility', kind='bar', title ="Votality of Rolling 30 Day Return",figsize=(15,10), fontsize=12, rot=0, color='r', legend=False,  zorder=3)
    vol.grid(axis='y', zorder=0)
    vol.set(xlabel=None)
    vol.set(ylabel='Vol of Rol. 30-d Ret.')
    vol.yaxis.set_major_formatter(mtick.PercentFormatter())

    #creating data labels 
    for p2 in vol.patches:
        vol.annotate((str(round(p2.get_height(),2))+"%"), (p2.get_x() * 1.007, p2.get_height() * 1.05), color='black', fontsize=14)


    #for avg/vol
    avgvol = sharperatio_pd.plot(ax=axes[2], x="asset", y='sharperatio', kind='bar', title ="Sharpe Ratio:30 day Returns ,Risk Free Rate: "+str("{:.2f}".format((risk_free_rate*100)))+"%",figsize=(15,10), fontsize=12, rot=0, color='b',legend=False,  zorder=3)
    avgvol.grid(axis='y', zorder=0)
    avgvol.set(xlabel=None)
    avgvol.set(ylabel='Sharpe Ratio')

    #creating data labels 
    for p3 in avgvol.patches:
        avgvol.annotate((str(round(p3.get_height(),2))), (p3.get_x() * 1.007, p3.get_height() * 1.05), color='black', fontsize=14)
        
    ##plt.show()

    plt.savefig('Charts/return30/return_vol_comparison.png')
    plt.close()

    slopes = []
    intercepts = []


    #loop for trend plots

    for j in range(len(assets)):
        
        ###multiplying return values with 100 to convert them in perceptage
        df[assets[j]] = df[assets[j]].apply(lambda x: x*100)
        
        #getting the trendline slops 
        slope, intercept, r_value, p_value, std_err = stats.linregress(df['Date'],df[assets[j]])

        slopes.append(slope)
        intercepts.append(intercept)
        ##print(slopes)
        
        
        #finding the second largest return for the asset 

        
        #creating trend plots
        g = sns.lmplot(data=df, x="Date", y=assets[j], truncate=False, scatter_kws={"s": 1}, lowess=True, height=5, aspect=1.5)
        g.fig.subplots_adjust(top=.9)

        #set upper and lower bound in the y axis (multiplied by 100 as values in percentage)
        g.set(ylim=(lower_bound*100, upper_bound*100))
        
        # iterate through the axes of the figure-level plot
        for ax in g.axes.flat:
            labels = ax.get_xticks() # get x labels
            new_labels = [date.fromordinal(int(label)) for label in labels] # convert ordinal back to datetime
            new_labels1 = [item.strftime("%B %d, %Y") for item in new_labels]
            ax.set_xticks(labels)
            ax.set_xticklabels(new_labels1, rotation=30, fontsize=8) # set new labels

        for ax in g.axes.flat:
            ax.yaxis.set_major_formatter(mtick.PercentFormatter())
            
        plt.title(assets[j]+":Trend in 30 Day Return")
        plt.ylabel("30 Day Return")
        plt.grid()
        #plt.show()
        plt.savefig('Charts/return30/'+assets[j]+'trend_return30.png')
        plt.close()


    ##print(slopes)

    ##print(intercepts)



    #comparing the trends

    x_values = df['Date'].tolist()


    recreated_tlines_df = pd.DataFrame({'Date':x_values})

    for l in range(len(assets)):
        y_list = []
        for m in range(len(x_values)):
            y_value = (((slopes[l])*(x_values[m]))+intercepts[l])

            y_list.append(y_value)
            
        recreated_tlines_df[assets[l]] = y_list
        
    recreated_tlines_df['Date_new'] = recreated_tlines_df['Date'].apply(lambda x: date.fromordinal(int(x)))
    recreated_tlines_df.drop('Date', axis=1, inplace=True)



    Normalized_trends =recreated_tlines_df.plot(x='Date_new', y=assets, kind="line", title ="Normalized Trend in Rolling 30-day Returns",figsize=(15,10), lw=4, fontsize=8, rot=0, legend=True, zorder=3)
    Normalized_trends.yaxis.set_major_formatter(mtick.PercentFormatter())
    Normalized_trends.grid(axis='y', zorder=0)
    Normalized_trends.set(xlabel=None)
    Normalized_trends.title.set_size(20)
    Normalized_trends.legend(prop={"size":14})
    Normalized_trends.tick_params(axis='both', which='major', labelsize=12)
    plt.xticks(rotation=30)
    ##plt.show()
    plt.savefig('Charts/return30/normalized_trends30.png')
    plt.close()





