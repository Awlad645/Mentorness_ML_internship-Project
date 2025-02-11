

import warnings
import itertools
import numpy as np
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import pandas as pd
import statsmodels.api as sm
import matplotlib
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'

from google.colab import drive
drive.mount('/content/drive')

"""# Reading Data"""

df = pd.read_csv("/content/drive/MyDrive/Time Series Prediction/Super_Store_data (1).csv")
df.head()

"""# Extracting the Time Series"""

df.Category.unique()

"""We see that the dataset contains data for three product category, namely Furniture, Office supplies and technology. Lets first try to forecast sales of furnitures."""

df.shape

df.describe()

df['Order Date'].min(), df['Order Date'].max()

cols = ['Row ID', 'Order ID', 'Ship Date', 'Ship Mode', 'Customer ID', 'Customer Name', 'Segment', 'Country', 'City', 'State', 'Postal Code', 'Region', 'Product ID', 'Category', 'Sub-Category', 'Product Name', 'Quantity', 'Discount', 'Profit']

df.drop(cols, axis=1, inplace=True)
df.head()

# @title Sales

from matplotlib import pyplot as plt
df['Sales'].plot(kind='hist', bins=20, title='Sales')
plt.gca().spines[['top', 'right',]].set_visible(False)

df= df.sort_values('Order Date')
df.head()

df.shape

"""# Data Cleaning"""

df.isnull().sum()

df = df.groupby('Order Date')['Sales'].sum().reset_index()
df.head()

# @title Order Date vs Sales

from matplotlib import pyplot as plt
import seaborn as sns
def _plot_series(series, series_name, series_index=0):
  from matplotlib import pyplot as plt
  import seaborn as sns
  palette = list(sns.palettes.mpl_palette('Dark2'))
  xs = series['Order Date']
  ys = series['Sales']

  plt.plot(xs, ys, label=series_name, color=palette[series_index % len(palette)])

fig, ax = plt.subplots(figsize=(10, 5.2), layout='constrained')
df_sorted = df.sort_values('Order Date', ascending=True)
_plot_series(df_sorted, '')
sns.despine(fig=fig, ax=ax)
plt.xlabel('Order Date')
_ = plt.ylabel('Sales')

df.shape

"""## Setting date as index"""

df = df.set_index('Order Date')
df.index

"""## Resampling

Since our order dates are daily, we will resample it to monthly to somewhat smoothen it out
"""

import pandas as pd

# Assuming df is your DataFrame containing the 'Sales' column
# Convert the index to datetime index if it's not already
df.index = pd.to_datetime(df.index)

# Now, you can proceed with resampling
y = df['Sales'].resample('MS').mean()
y['2017':]

"""## Plotting the time series"""

y.plot(figsize=(15, 6))
plt.show()

"""Observations from above figure:

1. The time-series has seasonality pattern, sales are low at the beginning of the year and high at the end of the year.
2. There is an upward trend within any single year with low months in the mid of the year.

## Stationarity Check

We will try the following to ensure stationarity of the series:

1. Time series decomposition
2. ADF test

### Time series decomposition

Decomposition of a time series can be performed by considering the series as an additive or multiplicative combination of the base level, trend, seasonal index and the residual term
"""

from pylab import rcParams
rcParams['figure.figsize'] = 18, 8
decomposition = sm.tsa.seasonal_decompose(y, model='additive')
fig = decomposition.plot()
plt.show()

"""### ADF Test"""

from statsmodels.tsa.stattools import adfuller

def test_adfuller(data):
    res=adfuller(data,maxlag=16)
    labels=['ADF Test Statistic','p-value','#Lags Used','No. of obs. used']
    for label, value in zip(labels,res):
        print(label+':'+str(value))
    if res[1]<=0.05:
        print('H0 is rejected, series is stationary')
    else:
        print('Failed to reject H0, series is not stationary')

test_adfuller(y)

"""##### 1. The ADF test statistic is -2.4399517684865506, and the p-value is 0.1307762660460255. With a p-value greater than the typical significance levels (0.05 or 0.01), we fail to reject the null hypothesis (H0). Therefore, we do not have enough evidence to conclude that the series is stationary.

##### 2. The p-value being greater than 0.05 suggests that there is a significant probability that the non-stationarity observed in the series is due to random noise rather than a systematic pattern. Thus, the series likely exhibits some form of trend or seasonality.

##### 3. But! Here's where it gets interesting. The test also tells us it had to look back 11 periods to spot any changes in sales. That could mean there's something happening every 11 periods that affects sales. Maybe it's a seasonal promotion, or perhaps customers tend to buy more every 11 weeks. It's like spotting a pattern in the chaos.

## Trying Differencing

Lets see if differencing the series could make the series stationary
"""

ydf=pd.DataFrame(y)
ydf.head()

ydf['First difference']=ydf['Sales']-ydf['Sales'].shift(1)
ydf['First seasonal difference']=ydf['Sales']-ydf['Sales'].shift(12)

ydf.head()

test_adfuller(ydf['First difference'].dropna())

test_adfuller(ydf['First seasonal difference'].dropna())

rcParams['figure.figsize'] = 18, 8
ydf['First difference'].plot(figsize=(13,9));

rcParams['figure.figsize'] = 18, 8
ydf['First seasonal difference'].plot(figsize=(13,9));

"""OBSERVATIONS:
    
- Seasonal differencing with 12 months period once removes the seasonality.

## ACF and PACF plots
"""

sm.graphics.tsa.plot_acf(ydf['First difference'].iloc[1:],lags=30);

sm.graphics.tsa.plot_pacf(ydf['First difference'].iloc[1:],lags=16);

sm.graphics.tsa.plot_acf(ydf['First seasonal difference'].iloc[12:],lags=30);

sm.graphics.tsa.plot_pacf(ydf['First seasonal difference'].iloc[12:],lags=16);

"""Obeservations:
    
1. From PACF plot, It looks like that using AR with lag 1 will be good for trend and AR with lag 0 for seasonality.
2. Similarly from ACF plot, it seems that MA with lag 1 will be good for trend and AR with lag 0 for seasonality.

## Implementing Sarimax

### Using grid search

Although we have an intution via differencing to use p=d=q=1 for Sarimax, Nonetheless lets try to use grid search to confirm or revise out initial guess.
"""

#Generating Triplets
p = d = q = range(0, 2)

pdq = list(itertools.product(p, d, q))

pdq

"""Note: To prevent overfitting, lets start with simpler seasonal parameters."""

seasonal_pdq=[(0,0,0,12),
              (0,1,0,12)]

"""### Train Test Split"""

train=y[:-15]
test=y[-15:]

for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(train,
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)
            results = mod.fit()
            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
        except:
            continue

"""#### We see that ARIMA(0, 1, 1)x(0, 1, 0, 12)12 - AIC:258.3790052353366

### Initializing best parameters
"""

mod = sm.tsa.statespace.SARIMAX(train,
                                order=(1, 1, 1),
                                seasonal_order=(0, 1, 0, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False
                                 )
results = mod.fit()
print(results.summary().tables[1])

"""## Checking Model Diagnostics"""

results.plot_diagnostics()
plt.show()

"""## Model Validation"""

pred=results.get_forecast(steps=8)
pred_ci=pred.conf_int()

ax=test.plot(label='observed')
pred.predicted_mean.plot(ax=ax,label='Predicted')
ax.fill_between(pred_ci.index,pred_ci.iloc[:,0],pred_ci.iloc[:,1],color='k',alpha=.25);

"""Conclusion: We see that our results are well within the confidence interval.

## MSE and RMSE Calculation
"""

test_forecast=pred.predicted_mean
mse_forecast=((test-test_forecast)**2).mean()
print('mse={}'.format(mse_forecast))

print('rmse={}'.format(np.sqrt(mse_forecast)))

y.min(),y.max()

"""In a time series with fluctuations in between (356.8, 1532.2), rmse with a value of 136 seems to be good.

# Future forecasts
"""

mod_final=sm.tsa.statespace.SARIMAX(y,order=(1,1,1),seasonal_order=(1,1,1,12),enforce_stationarity=False,enforce_invertibility=False)

results_f=mod_final.fit()

pred_f=results_f.get_forecast(steps=50)

pred_f_ci=pred_f.conf_int()

ax=y.plot(label='observed')
pred_f.predicted_mean.plot(ax=ax,label='forecast')
ax.fill_between(pred_f_ci.index,pred_f_ci.iloc[:,0],pred_f_ci.iloc[:,1],color='k',alpha=.25)
ax.set_xlabel('Date')
ax.set_ylabel('Co2 level')
plt.legend()
plt.show();

y_f=pred_f.predicted_mean

type(y_f)

y_f.to_csv('predictions.csv')
