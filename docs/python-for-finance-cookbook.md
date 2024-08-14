# Python for Finance Cookbook 2nd Edition

- [GitHub](https://github.com/PacktPublishing/Python-for-Finance-Cookbook-2E)

## Chapter 2

###  Converting prices to returns

There are two types of returns:

- Simple returns: They aggregate over assets—the simple return of a portfolio is the weighted sum of the returns of the individual assets in the portfolio. 

Simple returns are defined as:

Rt = (Pt - Pt-1)/Pt-1 = Pt/Pt-1 -1

- Log returns: They aggregate over time. It is easier to understand with the help of an example — the log return for a given month is the sum of the log returns of the days within that month.

Log returns are defined as:

rt = log(Pt/Pt-1) = log(Pt) - log(Pt-1)


### Adjusting the returns for inflation
- [cpi lib](https://palewi.re/docs/cpi/)
- [росстат](https://rosstat.gov.ru/statistics/price)

### Changing the frequency of time series data
The general rule of thumb for changing frequency can be broken down into the following:

- Multiply/divide the log returns by the number of time periods.
- Multiply/divide the volatility by the square root of the number of time periods.

For any process with independent increments (for example, the geometric Brownian motion), the variance of the logarithmic returns is proportional to time. For example, the variance of rt3 - rt1 is going to be the sum of the following two variances: rt2−rt1 and rt3−rt2, assuming t1≤t2≤t3. In such a case, when we also
assume that the parameters of the process do not change over time (homogeneity) we arrive at the proportionality of the variance to the length of the time interval. Which in practice means that the standard deviation (volatility) is proportional to the square root of time.

Realized volatility is frequently used for calculating the daily volatility using intraday returns.

The steps we need to take are as follows:

- Download the data and calculate the log returns
- Calculate the realized volatility over the months
- Annualize the values by multiplying by √12 , as we are converting from monthly values

### Different ways of imputing missing data

Two of the simplest approaches to imputing missing time series data are:

- Backward filling—fill the missing value with the next known value
- Forward filling—fill the missing value with the previous known value

Another possibility is to use interpolation, to which there are many different approaches.
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.interpolate.html


### Converting currencies

- [forex-python](https://github.com/MicroPyramid/forex-python)
- [theforexapi](https://theforexapi.com/)

### Different ways of aggregating trade data

There are some drawbacks of sampling financial time series by time:

- Time bars disguise the actual rate of activity in the market—they tend to oversample low activity periods (for example, noon) and undersample high activity periods (for example, close to market open and close).
- Nowadays, markets are more and more controlled by trading algorithms and bots, so they no longer follow human daylight cycles.
- Time-based bars offer poorer statistical properties (for example, serial correlation, heteroskedasticity, and non-normality of returns).
- Given that this is the most popular kind of aggregation and the easiest one to access, it can also be prone to manipulation (for example, iceberg orders).

Some of the alternatives they are using include:

- Tick bars—named after the fact that transactions/trades in financial markets are often referred to as ticks. For this kind of aggregation, we sample an OHLCV bar every time a predefined number of transactions occurs.
- Volume bars—we sample a bar every time a predefined volume (measured in any unit, for example, shares, coins, etc.) is exchanged.
- Dollar bars—we sample a bar every time a predefined dollar amount is exchanged. Naturally, we can use any other currency of choice.


## Chapter 4

### Outlier detection using rolling statistics

#### Winsorization
Another popular approach for treating outliers is winsorization. It is based on replacing outliers in data to limit their effect on any potential calculations. 
It’s easier to understand winsorization using an example. 
A 90% winsorization results in replacing the top 5% of values with the 95th percentile. 
Similarly, the bottom 5% is replaced using the value of the 5th percentile. 
We can find the corresponding winsorize function in the scipy library.

####  Hampel filter
Its goal is to identify and potentially replace outliers in a given series. 
It uses a centered sliding window of size 2x (given x observations before/after) to go over the entire series.
For each of the sliding windows, the algorithm calculates the median and the median absolute deviation (a form of a standard deviation).

Here are a few interesting anomaly/outlier detection libraries:
• https://github.com/datamllab/tods
• https://github.com/zillow/luminaire/
• https://github.com/signals-dev/Orion
• https://pycaret.org/anomaly-detection/
• https://github.com/linkedin/luminol—a library created by LinkedIn; unfortunately, it is not actively maintained anymore
• https://github.com/twitter/AnomalyDetection—this R package (created by Twitter) is quite famous and was ported to Python by some individual contributors

### Detecting changepoints in time series

We will use the CUSUM (cumulative sum) method to detect shifts of the means in a time series. The implementation used in the recipe has two steps:

1. Finding the changepoint—an iterative process is started by first initializing a changepoint in the middle of the given time series. Then, the CUSUM approach is carried out based on the selected point. 
The following changepoint is located where the previous CUSUM time series is either maximized or minimized (depending on the direction of the changepoint we want to locate). 
We continue this process until a stable changepoint is located or we exceed the maximum number of iterations.

2. Testing its statistical significance—a log-likelihood ratio test is used to test if the mean of the given time series changes at the identified changepoint. 
The null hypothesis states that there is no change in the mean of the series.

Some further remarks about the implementation of the algorithm:

- The algorithm can be used to detect both upward and downward shifts.
- The algorithm can find at most one upward and one downward changepoint.
- By default, the changepoints are only reported if the null hypothesis is rejected.
- Under the hood, the Gaussian distribution is used to calculate the CUSUM time series value and perform the hypothesis test.








