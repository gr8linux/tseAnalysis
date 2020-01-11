from tehran_stocks import Stocks,db,get_asset
import pandas as pd
pd.set_option('plotting.backend', 'pandas_bokeh')
import matplotlib.pyplot as plt
'''tseStock handle basic operations on TSE data fetch from 
    tehran-stocks library
    usage:
    mystock = tseStock('خودرو') # Load IKCO ticker 
    mystock.plot()              # Plot the close price column with pandas.plot function
'''
#TODO Import adjusted data form Tehran stock exchange
class tseStock():
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
            self.figsize=(800,400)
        else:
            self.figsize = (20,10)
        return self.figsize
    def ma(self,window=20):
        if(len(self.__price__.close)>window):
            try:
                self.__price__['MA' + str(window)]
            except KeyError:
                self.__price__['MA' + str(window)] = self.__price__.close.rolling(window).mean()
                return self.__price__['MA'+str(window)]
            else:
                #self.__price__['MA' + str(window)] = self.__price__.close.rolling(window).mean()
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



    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name


afra = tseStock('افرا','2019','2020')

#afra.ma(10).plot()
#afra.df.close.plot()
print(afra)
print(afra.close.head())
#afra.plot('2019','2020')

afra.close.plot(figsize=afra.figsize,legend=True)
afra.ma(20).plot(figsize=afra.figsize,legend=True)

afra.ma(50).plot(figsize=afra.figsize,legend=True)
afra.ma(200).plot(figsize=afra.figsize,legend=True,title="Afranet daily close with 3 SMA")

plt.show()


