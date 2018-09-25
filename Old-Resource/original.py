import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import pandas_datareader.data as web
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_model import ARIMA
from pandas.tseries.offsets import DateOffset
def prep_data():
    df = pd.read_csv("monthly-milk-production-pounds-p.csv")
    df.columns = ['Month', 'Milk in pounds per cow']
    df.drop(168,axis=0,inplace=True)
    df['Month'] = pd.to_datetime(df['Month'])
    df.set_index('Month', inplace=True)
    return df

def adf_check(series):
    result = adfuller(series)
    print(" Augmented Dicky-Fuller Test")
    labels = ['ADF Test Statistic', 'p-value', '# of lags', 'Num of observations used']

    for value, label in zip(result,labels):
        print(label+" : "+str(value))

    if result[1] <= 0.05:
        print("Against null hypothesis, reject")
        print("Data has no unit root and is stationary")
        return series.dropna()
    else:
        temp = series - series.shift(12)
        print "Fail to reject null hypothesis, differencing. . .\n"
        return adf_check(temp.dropna())

def draw_correlation(series):
    figure = plot_acf(series)
    figure_one = plot_pacf(series)
    plt.show()

def seasonal_ARIMA(df):
    model = sm.tsa.statespace.SARIMAX(df['Milk in pounds per cow'],order=(0,1,0), seasonal_order=(1,1,1,12))
    results = model.fit()
    print (results.summary())
    print results.resid
    future_date = [df.index[-1] + DateOffset(months=x) for x in range(0,24) ]
    future_df = pd.DataFrame(index=future_date[1:],columns=df.columns)
    final_df = pd.concat([df,future_df])
    final_df['Forecast'] = results.predict(start=168, end=188)
    final_df[2195:].dropna(subset=['Forecast'],inplace=True)
    print(final_df)
    final_df[['Milk in pounds per cow','Forecast']].plot(figsize=(12,8))
    plt.show()

if __name__ == '__main__':
    df = prep_data()
    #per year
    moving_average = df['Milk in pounds per cow'].rolling(12).mean()
    #per year
    standard_deviation = df['Milk in pounds per cow'].rolling(12).std()
    decomp = seasonal_decompose(df['Milk in pounds per cow'], freq=12)
    print df.describe()
    seasonal_ARIMA(df)
