import pandas as pd
from datetime import date
import scipy.optimize as optimize
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches

pd.options.display.float_format = '{:.2%}'.format




def opt_port30(risk_free_rate):
    
    
    
    rfr30 = (pow((1+risk_free_rate), (30/365)))-1     #changing 

    df = pd.read_csv('return_data/Return30_df.csv', parse_dates=['Date']) #chancing
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    ##df['Date'] = pd.to_datetime(df['Date']).apply(lambda date: date.toordinal())
    df.set_index('Date', inplace=True)


    col_num = len(df.columns)
    row_num = len(df)
    col_names = df.columns.values.tolist()

    #base allocation = equal allocation to all assets
    eq_aloc = 1/col_num

    
    #defining an array for portfolio allocation 
    alloc_array = [eq_aloc] * col_num


##    #defining a 2 dimentional array for portfolio return calculations
##    portfolio_returns = np.zeros((col_num, row_num))
##
##
##    #creating 3 columns with as (assetreturn * allocation%)
##    for i in range(col_num):
##        for j in range(row_num):
##            portfolio_returns[i][j] = (df.iloc[ :, i ][j])*alloc_array[i]     
##
##    #converting the numpy array to a dataframe
##    df_port = pd.DataFrame(portfolio_returns.transpose(), columns = col_names)
##    df_port['Port_return'] = df_port.sum(axis=1)
##
##    #calculating the sharpe ration
##    port_avg_returns = (df_port['Port_return'].mean())
##    port_vol_returns = (df_port['Port_return'].std())
##
##    port_sharpe_ratio = ((port_avg_returns -rfr365)/port_vol_returns)
##
##    return(port_sharpe_ratio)


    #defining the optimization function
    def sharperatio(allocation_matrix):
        portfolio_returns = np.zeros((len(df.columns), len(df)))
        
        #creating 3 columns with as (assetreturn * allocation%)
        for i in range(col_num):
            for j in range(row_num):
                portfolio_returns[i][j] = (df.iloc[ :, i ][j])*allocation_matrix[i]

        #converting the numpy array to a dataframe
        df_port = pd.DataFrame(portfolio_returns.transpose(), columns = df.columns.values.tolist())
        df_port['Port_return'] = df_port.sum(axis=1)

        #calculating the sharpe ration
        port_avg_returns = (df_port['Port_return'].mean())
        port_vol_returns = (df_port['Port_return'].std())

        neg_port_sharpe_ratio = -1*((port_avg_returns -rfr30)/port_vol_returns) #intentionally creating negative sharpe ratio as we are minimizing 

        return(neg_port_sharpe_ratio)

    def con(t):
        return t.sum() - 1

    cons = ({'type':'eq', 'fun':con})

##    def con_real(alloc_array):
##        return np.sum(np.iscomplex(alloc_array))

##    cons = [{'type':'eq', 'fun': con},
##            {'type':'eq', 'fun': con_real}]


    ##results = sharperatio(alloc_array)
    zero_one = (0,1)
    bnds = col_num*[zero_one]

    opt = optimize.minimize(sharperatio, alloc_array, method='SLSQP', constraints= cons, bounds =bnds, tol=1e-10)

    #getting best allocation array
    best_alloc= opt.x

    #Sharpe ratio for best values
    best_sharpe = (sharperatio(best_alloc))*(-1) #multiplied by (-1) as the function calculates sharpe ratio in negative to be used in minimization problem

    
    plt.gca().axis("equal")
     
    def my_autopct(pct):
        return ('%1.1f%%' % pct) if pct > 2 else ''


    color_list = []
    
    for c in range(len(col_names)):
        color_list.append(plt.cm.Set3(c))

        
    #colors=[plt.cm.Set3(1)]
        
    pie = plt.pie(best_alloc, autopct=my_autopct, colors=color_list, shadow=True, startangle=90)


    labels = col_names
    handles = []
    for i, l in enumerate(labels):
##        handles.append(matplotlib.patches.Patch(color=plt.cm.Set3((i)/8.), label=l))
        handles.append(matplotlib.patches.Patch(color=color_list[i], label=l))
        
    plt.legend(handles,labels, bbox_to_anchor=(0.85,1.025), loc="upper left")

    plt.title("Optimal Portfolio Allocation (30 Day Returns)", fontsize=14)

    plt.figsize=(15,10)
    plt.text(0, -1.3, "Portfolio Sharpe Ratio= "+str(round(best_sharpe,2)), fontsize=13, color='green')
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.75)


    #draw circle
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    # Equal aspect ratio ensures that pie is drawn as a circle
    ##ax1.axis('equal')  
    plt.tight_layout()

    plt.savefig('Charts/optimal_portfolio/optimal_portfolio_30.png')
    plt.close()
    ##plt.show()


    #converting to perentage
    def Percent(fl):
        return '{:.2%}'.format(fl)

    best_alloc_per = list(map(Percent, best_alloc))
    print(best_alloc_per)
    

    
##    return(best_alloc_per, best_sharpe)



