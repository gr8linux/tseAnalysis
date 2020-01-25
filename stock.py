from tehran_stocks import Stocks,db,get_asset
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
#pd.set_option('plotting.backend', 'pandas_bokeh')
import matplotlib.pyplot as plt
'''tseStock handle basic operations on TSE data fetch from 
    tehran-stocks library
    usage:
    mystock = tseStock('خودرو') # Load IKCO ticker 
    mystock.plot()              # Plot the close price column with pandas.plot function
'''
#TODO Import adjusted data form Tehran stock exchange
#TODO Developed based on mplfinance and add your extra feather
#TODO Build a better test module

class tseStock():
    ASSET_PATH = "/home/ali/Documents/books/tse/d/"
    def __init__(self,name,start_date=None,end_date=None):
        self.name = name
        self.__stock__ = get_asset(self.name)
        self.eps = self.__stock__.estimatedEps
        if(start_date!=None,end_date!=None):
            self.__price__ = self.__stock__.df.loc[start_date:end_date]
        else:
            self.__price__ = self.__stock__.df
    @property
    def figsize(self):
        if(pd.get_option('plotting.backend')== 'pandas_bokeh'):
            figsize=(800,400)
        else:
            figsize = (20,10)
        return figsize
    def ma(self,window=20):
        if(len(self.__price__.close)>window):
            try:
                self.__price__['MA' + str(window)]
            except KeyError:
                self.__price__['MA' + str(window)] = self.__price__.close.rolling(window).mean()
                return self.__price__['MA'+str(window)]
            else:
                return self.__price__['MA' + str(window)]
        else:
           return None
    def plot(self, start_date=None, end_date=None):
        if(start_date!=None and end_date!=None):
            self.close.loc[start_date:end_date].plot(figsize=(20,10),grid=True)
            plt.show()
        else:
            self.close.plot(figsize=(20,10),grid=True)
            plt.show()

    @property
    def close(self):
        return self.__price__.close

    @close.setter
    def close(self,close):
        self.__price__.close=close
    @property
    def mpl(self):
        return self.__stock__.mpl
    @staticmethod
    def asset_load(ticker=None, start=None, end=None, fullpath=None,source='rahavard'):
        # loading the data from rahavad365 .txt data file
        # rahavad generating a CSV format of the assets in daily time frame
        # ASSET_PATH is the root directory of asset files
        if(ticker==None and fullpath==None):
            return None
        if (fullpath == None):
            path = tseStock.ASSET_PATH + ticker + '_D_SH.txt'
        else:
            path = fullpath
        if(source == 'rahavard'):
            names = ["Ticker", "Per", "DATE", "TIME", "Open", "High", "Low", "Close", "Volume", "Openint","type", "id"]
        elif(source == 'tseclient'):
            names = ["Ticker","DATE","Open","High", "Low", "Close", "Volume", "Value", "Openint", "TradeCount", "Code", "Name_en", "Name", "Jdate", "Last_price"]

        asset = pd.read_csv(path, \
                            names=names, \
                            skiprows=1, usecols=["DATE", "Open", "High", "Low", "Close", "Volume", "Openint"], \
                            parse_dates=["DATE"], index_col=['DATE'])
        # asset_returns(asset)
        if (start != None and end != None):
            asset = asset[start:end]
        return asset

    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name

def stfinder():
    for i in Stocks.query.filter(Stocks.estimatedEps!=None).all():
        if(len(i.df.close)>0):
            if(i.estimatedEps/i.df.close.iloc[-1] > 0.2 ):
                print(f"{i.name} {i.estimatedEps/i.df.close.iloc[-1]:.2f}")
#stfinder()
df = None
steel = tseStock('فولاد','2017','2020')
df = tseStock.asset_load('FEOLAD')
df2 = tseStock.asset_load(fullpath='/home/ali/Documents/books/tse/d/Adjusted/افرا-ت.csv',source='tseclient')
df.Close.loc['2020'].plot()
df2.Close.loc['2020'].plot()

plt.show()
#mpf.plot(steel.mpl)
#afra.ma(10).plot()
#afra.df.close.plot()
#print(afra.__price__.info())
#print(afra.close.head())
#afra.plot('2018','2020')

#afra.close.plot(figsize=afra.figsize,legend=True)
#afra.ma(20).plot(figsize=afra.figsize,legend=True)

#afra.ma(50).plot(figsize=afra.figsize,legend=True)
#afra.ma(200).plot(figsize=afra.figsize,legend=True,title="Afranet daily close with 3 SMA")
#mpf.plot(afra.__price__)
#plt.show()


