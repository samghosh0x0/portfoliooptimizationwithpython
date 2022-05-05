# portfoliooptimizationwithpython
Portfolio Optimization and Trend Analysis with Python
Please register with https://www.coinapi.io/ and update key value in "data_coinapi.py" before running the scripts. 

If you are collecting data manually, you have to collect data from at least 366 days prior to the begining date for your analysis. This is required to calculate the 365-day returns. Save the data in "Data" folder as a .csv file. Please match the format with the existing .csv files. 



Files: 

 01Main.py: You can access all the modules from this file and update risk-free rate value. 
  
 data_coinapi.py : Simple program to receive data from Coinapi. This script is called from 01Main as a module. Please register with Coinapi and update the "key" value.
  
 'returncalculator.py' : Calculates rolling returns (30,90,180,270, and 365-day) and saves the data is the "return_data" folder. 
  
  
 Trendline Creators: 
  
  'trendline_30.py'
  'trendline_90.py'
  'trendline_180.py'
  'trendline_270.py'
  'trendline_365.py'
    
    - These files create various types of trendlines using the return data save in the "Charts" folder. 
    
    
 Optimizers: 
  'optimize_30.py'
  'optimize_90.py'
  'optimize_180.py'
  'optimize_270.py'
  'optimize_365.py'
      
      - These files calculate optimum portfolios, create charts and save the charts in the "Charts" folder. 
  



Folders:

  'Data': The 'data_coinapi.py' module saves collected data here. If the data is not available with Coinapi or you are doing analysis for fiat assets - save the data as a csv file here. 
  
  'return_data' : The 'returncalculator.py' module saves the calculated returns in this folder in .csv format. 
  
  'Charts' : All the charts created by trendline creators and optimizers are saved in this folder. 
  
