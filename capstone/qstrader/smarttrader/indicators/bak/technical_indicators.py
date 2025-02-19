#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provides some technical indicators for analysing stocks.

When I can I will add more.
If anyone wishes to contribute with new code or corrections/suggestions, feel
free.

Features:

    Relative Strength Index (RSI), ROC, MA envelopes
    Simple Moving Average (SMA), Weighted Moving Average (WMA), Exponential
    Moving Average (EMA)
    Bollinger Bands (BB), Bollinger Bandwidth, %B

Dependencies:

It requires numpy.
This module was tested under Windows with Python 2.7.3 and numpy 1.6.1.
"""

# Python 3 compatibility
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import numpy as np


def roc(prices, period=21):
    """
    The Rate-of-Change (ROC) indicator, a.k.a. Momentum, is a pure momentum
    oscillator that measures the percent change in price from one period to the
    next.
    The plot forms an oscillator that fluctuates above and below the zero line
    as the Rate-of-Change moves from positive to negative.
    ROC signals include centerline crossovers, divergences and
    overbought-oversold readings. Identifying overbought or oversold extremes
    comes natural to the Rate-of-Change oscillator.
    It can be used to measure the ROC of any data series, such as price or
    another indicator.
    Also known as PROC when used with price.

    ROC = [(Close - Close n periods ago) / (Close n periods ago)] * 100

    http://www.csidata.com/?page_id=797
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:rate_of_change_roc_a

    Input:
      prices ndarray
      period int > 1 and < len(prices) (optional and defaults to 21)

    Output:
      rocs ndarray

    Test:

     import numpy as np
    import technical_indicators as tai
     prices = np.array([11045.27, 11167.32, 11008.61, 11151.83, 10926.77,
    ... 10868.12, 10520.32, 10380.43, 10785.14, 10748.26, 10896.91, 10782.95,
    ... 10620.16, 10625.83, 10510.95, 10444.37, 10068.01, 10193.39, 10066.57,
    ... 10043.75])
     print(tai.roc(prices, period=12))
    [-3.84879682 -4.84888048 -4.52064339 -6.34389154 -7.85923013 -6.20834146
     -4.31308173 -3.24341092]
    """

    num_prices = len(prices)

    if num_prices < period:
        # show error message
        raise SystemExit('Error: num_prices < period')

    roc_range = num_prices - period

    rocs = np.zeros(roc_range)

    for idx in range(roc_range):
        rocs[idx] = ((prices[idx + period] - prices[idx]) / prices[idx]) * 100

    return rocs




def sma(prices, period):
    """
    Simple Moving Average (SMA) are used to smooth the data in an array to help
    eliminate noise and identify trends.
    In SMA, each value in the time period carries equal weight.

    They do not predict price direction, but can be used to identify the
    direction of the trend or define potential support and resistance levels.

    SMA = (P1 + P2 + ... + Pn) / K
    where K = n and Pn is the most recent price

    http://www.financialwebring.org/gummy-stuff/MA-stuff.htm

    http://www.csidata.com/?page_id=797
    http://stockcharts.com/school/doku.php?st=moving+average&id=chart_school:technical_indicators:moving_averages

    Input:
      prices ndarray
      period int > 1 and < len(prices)

    Output:
      smas ndarray

    Test:

     import numpy as np
     import technical_indicators as tai
     prices = np.array([22.27, 22.19, 22.08, 22.17, 22.18, 22.13, 22.23,
    ... 22.43, 22.24, 22.29, 22.15, 22.39, 22.38, 22.61, 23.36, 24.05, 23.75,
    ... 23.83, 23.95, 23.63, 23.82, 23.87, 23.65, 23.19, 23.10, 23.33, 22.68,
    ... 23.10, 22.40, 22.17])
     period = 10
     print(tai.sma(prices, period))
    [ 22.221  22.209  22.229  22.259  22.303  22.421  22.613  22.765  22.905
      23.076  23.21   23.377  23.525  23.652  23.71   23.684  23.612  23.505
      23.432  23.277  23.131]
    """

    num_prices = len(prices)

    if num_prices < period:
        # show error message
        raise SystemExit('Error: num_prices < period')

    sma_range = num_prices - period + 1

    smas = np.zeros(sma_range)

    # only required for the commented code below
    #k = period

    for idx in range(sma_range):
        # this is the code, but using np.mean below is faster and simpler
        #for period_num in range(period):
        #    smas[idx] += prices[idx + period_num]
        #smas[idx] /= k

        smas[idx] = np.mean(prices[idx:idx + period])

    return smas


def wma(prices, period):
    """
    Weighted Moving Average (WMA) is a type of moving average that assigns a
    higher weighting to recent price data.

    WMA = (P1 + 2 P2 + 3 P3 + ... + n Pn) / K
    where K = (1+2+...+n) = n(n+1)/2 and Pn is the most recent price after the
    1st WMA we can use another formula
    WMAn = WMAn-1 + w.(Pn - SMA(prices, n-1))
    where w = 2 / (n + 1)

    http://www.csidata.com/?page_id=797

    http://www.financialwebring.org/gummy-stuff/MA-stuff.htm

    http://www.investopedia.com/terms/l/linearlyweightedmovingaverage.asp

    http://fxtrade.oanda.com/learn/forex-indicators/weighted-moving-average

    Input:
      prices ndarray
      period int > 1 and < len(prices)

    Output:
      wmas ndarray

    Test:

     import numpy as np
     import technical_indicators as tai
     prices = np.array([77, 79, 79, 81, 83, 49, 55])
     period = 5
     print(tai.wma(prices, period))
    [ 80.73333333  70.46666667  64.06666667]
    """

    num_prices = len(prices)

    if num_prices < period:
        # show error message
        raise SystemExit('Error: num_prices < period')

    wma_range = num_prices - period + 1

    wmas = np.zeros(wma_range)

    k = (period * (period + 1)) / 2.0

    # only required for the commented code below
    #w = 2 / float(period + 1)

    for idx in range(wma_range):
        for period_num in range(period):
            weight = period_num + 1
            wmas[idx] += prices[idx + period_num] * weight
        wmas[idx] /= k

    # this is the code for the second formula, but I think the first is simpler
    # to understand
    #for idx in range(wma_range):
        #if idx == 0:
            #for period_num in range(period):
                #weight = period_num + 1
                #wmas[idx] += prices[idx + period_num] * weight
            #wmas[idx] /= k

        #else:
            #wmas[idx] = wmas[idx - 1] + w * \
                #(prices[idx + period - 1] - \
                 #sma(prices[idx - 1:idx + period - 1], period))

    return wmas


def ema(prices, period, ema_type=0):
    """
    Exponencial Moving Average (EMA) are used to smooth the data in an array to
    help eliminate noise and identify trends.
    Exponential moving averages reduce the lag by applying more weight to
    recent prices.
    The weighting applied to the most recent price depends on the number of
    periods in the moving average.

    They do not predict price direction, but can be used to identify the
    direction of the trend or define potential support and resistance levels.

    EMA type 0
    EMAn = w.Pn + (1 - w).EMAn-1
    EMAn = EMAn-1 + w.(Pn - EMAn-1)
    EMAn = w.Pn + w.(1 - w).Pn-1 + w.(1 - w)^2.Pn-2 + ... +
    w.(1 - w)^(n-1).P1 + w.(1 - w)^n.EMA0
    where w = 2 / (n + 1) and EMA0 = mean(oldest period)
    or
    EMAn = w.EMAn-1 + (1 - w).Pn
    where w = 1 - 2 / (n + 1) and Pn is the most recent price
    and EMA0 = mean(oldest period)

    EMA type 1
    The above formulas with EMA0 = P1 (oldest price)

    EMA type 2
    EMA = (Pn + w.Pn-1 + w^2.Pn-2 + w^3.Pn-3 + ... ) / K
    where K = 1 + w + w^2 + ... = 1 / (1 - w) and Pn is the most recent price
    and w = 2 / (N + 1)

    http://www.financialwebring.org/gummy-stuff/MA-stuff.htm

    http://www.csidata.com/?page_id=797
    http://stockcharts.com/school/doku.php?st=moving+average&id=chart_school:technical_indicators:moving_averages

    Input:
      prices ndarray
      period int > 1 and < len(prices)
      ema_type can be 0, 1 or 2

    Output:
      emas ndarray

    Tests:

     import numpy as np
     import technical_indicators as tai
     prices = np.array([22.27, 22.19, 22.08, 22.17, 22.18, 22.13, 22.23,
    ... 22.43, 22.24, 22.29, 22.15, 22.39, 22.38, 22.61, 23.36, 24.05, 23.75,
    ... 23.83, 23.95, 23.63, 23.82, 23.87, 23.65, 23.19, 23.10, 23.33, 22.68,
    ... 23.10, 22.40, 22.17])
     period = 10
     print(tai.ema(prices, period))
    [ 22.221       22.20809091  22.24116529  22.26640796  22.32887924
      22.51635574  22.79520015  22.96880013  23.12538192  23.27531248
      23.33980112  23.42711001  23.50763546  23.53351992  23.47106176
      23.40359598  23.39021489  23.26108491  23.23179675  23.08056097
      22.91500443]
     print(tai.ema(prices, period, 1))
    [ 22.27        22.25545455  22.22355372  22.21381668  22.20766819
      22.1935467   22.20017457  22.24196102  22.24160447  22.25040366
      22.23214845  22.26084873  22.2825126   22.34205576  22.52713653
      22.8040208   22.97601702  23.13128665  23.28014362  23.34375387
      23.43034408  23.51028152  23.53568488  23.47283308  23.40504525
      23.39140066  23.26205508  23.23259052  23.08121043  22.9155358 ]
     print(tai.ema(prices, period, 2))
    [ 22.28588695  22.174706    22.35085492  22.37470018  22.5672175
      23.21585701  23.89833692  23.77696963  23.82035739  23.9264279
      23.68389526  23.79525297  23.85640891  23.68752817  23.28045894
      23.13280996  23.29414649  22.79166223  23.04393782  22.51707883
      22.23310448]
    """

    num_prices = len(prices)

    if num_prices < period:
        # show error message
        raise SystemExit('Error: num_prices < period')

    if ema_type == 0:  # 1st value is the average of the period
        ema_range = num_prices - period + 1

        emas = np.zeros(ema_range)

        emas[0] = np.mean(prices[:period])

        w = 2 / float(period + 1)

        # only required for the 4th formula
        #w = 1 - 2 / float(period + 1)

        for idx in range(1, ema_range):
            emas[idx] = w * prices[idx + period - 1] + (1 - w) * emas[idx - 1]

            # or with the 2nd formula
            #emas[idx] = emas[idx - 1] + w * ((prices[idx + period - 1] -
            #                                 emas[idx - 1]))

            # or with the 4th formula
            #emas[idx] = w * emas[idx - 1] + (1 - w) * prices[idx + period - 1]

    elif ema_type == 1:  # 1st value is the 1st price
        ema_range = num_prices

        emas = np.zeros(ema_range)

        emas[0] = prices[0]

        w = 2 / float(period + 1)

        # only required for the 4th formula
        #w = 1 - 2 / float(period + 1)

        for idx in range(1, ema_range):
            emas[idx] = w * prices[idx] + (1 - w) * emas[idx - 1]

            # or with the 2nd formula
            #emas[idx] = emas[idx - 1] + w * (prices[idx] - emas[idx - 1])

            # or with the 4th formula
            #emas[idx] = w * emas[idx - 1] + (1 - w) * prices[idx]

    else:
        ema_range = num_prices - period + 1

        emas = np.zeros(ema_range)

        w = 2 / float(period + 1)

        k = 1 / float(1 - w)

        for idx in range(ema_range):
            for period_num in range(period):
                # this runs the prices backwards to comply with the formula
                emas[idx] += w**period_num * \
                    prices[idx + period - period_num - 1]
            emas[idx] /= k

    return emas


def ma_env(prices, period, percent, ma_type=0):
    """
    Moving Average Envelopes are percentage-based envelopes set above and below
    a moving average.
    They can be used as a trend following indicator.
    The envelopes can also be used to identify overbought and oversold levels
    when the trend is relatively flat.

    Upper Envelope: MA + (MA x percent)
    Lower Envelope: MA - (MA x percent)

    http://www.csidata.com/?page_id=797

    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:moving_average_envel

    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:bollinger_band_perce

    Input:
      prices ndarray
      period int > 1 and < len(prices)
      percent float > 0.00 and < 1.00
      ma_type 0=EMA type 0, 1=EMA type 1, 2=EMA type 2, 3=WMA, 4=SMA

    Output:
      ma_envs ndarray with upper, middle, lower bands, range and %B

    Test:

     import numpy as np
     import technical_indicators as tai
     prices = np.array([86.16, 89.09, 88.78, 90.32, 89.07, 91.15, 89.44,
    ... 89.18, 86.93, 87.68, 86.96, 89.43, 89.32, 88.72, 87.45, 87.26, 89.50,
    ... 87.90, 89.13, 90.70, 92.90, 92.98, 91.80, 92.66, 92.68, 92.30, 92.77,
    ... 92.54, 92.95, 93.20, 91.07, 89.83, 89.74, 90.40, 90.74, 88.02, 88.09,
    ... 88.84, 90.78, 90.54, 91.39, 90.65])
     period = 20
     print(tai.ma_env(prices, period, 0.1, 4))
    [[  97.57935      88.7085       79.83765      17.7417        0.35635537]
     [  97.95005      89.0455       80.14095      17.8091        0.50249872]
     [  98.164        89.24         80.316        17.848         0.4742268 ]
     [  98.3301       89.391        80.4519       17.8782        0.55196273]
     [  98.4588       89.508        80.5572       17.9016        0.47553291]
     [  98.65735      89.6885       80.71965      17.9377        0.58147644]
     [  98.7206       89.746        80.7714       17.9492        0.48295189]
     [  98.90375      89.9125       80.92125      17.9825        0.45926595]
     [  99.08855      90.0805       81.07245      18.0161        0.32512863]
     [  99.41965      90.3815       81.34335      18.0763        0.35055017]
     [  99.72325      90.6575       81.59175      18.1315        0.29607313]
     [  99.9493       90.863        81.7767       18.1726        0.42114502]
     [  99.9713       90.883        81.7947       18.1766        0.41401032]
     [  99.9944       90.904        81.8136       18.1808        0.37987327]
     [ 100.0868       90.988        81.8892       18.1976        0.30557876]
     [ 100.26775      91.1525       82.03725      18.2305        0.28648419]
     [ 100.30955      91.1905       82.07145      18.2381        0.40730942]
     [ 100.232        91.12         82.008        18.224         0.32330992]
     [ 100.2837       91.167        82.0503       18.2334        0.38828194]
     [ 100.37445      91.2495       82.12455      18.2499        0.46989025]
     [ 100.36565      91.2415       82.11735      18.2483        0.59088518]
     [ 100.2826       91.166        82.0494       18.2332        0.59948884]
     [ 100.15445      91.0495       81.94455      18.2099        0.54121385]]
    """

    num_prices = len(prices)

    if num_prices < period:
        # show error message
        raise SystemExit('Error: num_prices < period')

    ma_env_range = num_prices - period + 1

    # 3 bands, range and %B
    ma_envs = np.zeros((ma_env_range, 5))

    if 0 <= ma_type <= 2:  # EMAs
        ma = ema(prices, period, ema_type=ma_type)

    elif ma_type == 3:  # WMA
        ma = wma(prices, period)

    else:  # SMA
        ma = sma(prices, period)

    for idx in range(ma_env_range):
        # upper, middle, lower bands, range and %B
        ma_envs[idx, 0] = ma[idx] + (ma[idx] * percent)
        ma_envs[idx, 1] = ma[idx]
        ma_envs[idx, 2] = ma[idx] - (ma[idx] * percent)
        ma_envs[idx, 3] = ma_envs[idx, 0] - ma_envs[idx, 2]
        ma_envs[idx, 4] = (prices[idx] - ma_envs[idx, 2]) / ma_envs[idx, 3]

    return ma_envs


def bb(prices, period, num_std_dev=2.0):
    """
    Bollinger bands (BB) are volatility bands placed above and below a moving
    average.
    Volatility is based on the standard deviation, which changes as volatility
    increases and decreases.
    The bands automatically widen when volatility increases and narrow when
    volatility decreases.
    This dynamic nature of Bollinger Bands also means they can be used on
    different securities with the standard settings.
    For signals, Bollinger Bands can be used to identify M-Tops and W-Bottoms
    or to determine the strength of the trend.
    Signals derived from narrowing BandWidth are also important.

    Bollinger BandWidth is an indicator that derives from Bollinger Bands, and
    measures the percentage difference between the upper band and the lower
    band.
    BandWidth decreases as Bollinger Bands narrow and increases as Bollinger
    Bands widen.
    Because Bollinger Bands are based on the standard deviation, falling
    BandWidth reflects decreasing volatility and rising BandWidth reflects
    increasing volatility.

    %B quantifies a security's price relative to the upper and lower Bollinger
    Band. There are six basic relationship levels:
    %B equals 1 when price is at the upper band
    %B equals 0 when price is at the lower band
    %B is above 1 when price is above the upper band
    %B is below 0 when price is below the lower band
    %B is above .50 when price is above the middle band (20-day SMA)
    %B is below .50 when price is below the middle band (20-day SMA)

    They were developed by John Bollinger.
    Bollinger suggests increasing the standard deviation multiplier to 2.1 for
    a 50-period SMA and decreasing the standard deviation multiplier to 1.9 for
    a 10-period SMA.

    http://www.csidata.com/?page_id=797
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:bollinger_bands
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:bollinger_band_width
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:bollinger_band_perce

    Input:
      prices ndarray
      period int > 1 and < len(prices)
      num_std_dev float > 0.0 (optional and defaults to 2.0)

    Output:
      bbs ndarray with upper, middle, lower bands, bandwidth, range and %B

    Test:

     import numpy as np
     import technical_indicators as tai
     prices = np.array([86.16, 89.09, 88.78, 90.32, 89.07, 91.15, 89.44,
    ... 89.18, 86.93, 87.68, 86.96, 89.43, 89.32, 88.72, 87.45, 87.26, 89.50,
    ... 87.90, 89.13, 90.70, 92.90, 92.98, 91.80, 92.66, 92.68, 92.30, 92.77,
    ... 92.54, 92.95, 93.20, 91.07, 89.83, 89.74, 90.40, 90.74, 88.02, 88.09,
    ... 88.84, 90.78, 90.54, 91.39, 90.65])
     period = 20
     print(tai.bb(prices, period))
    [[  9.12919107e+01   8.87085000e+01   8.61250893e+01   5.82449423e-02
        5.16682146e+00   6.75671306e-03]
     [  9.19497209e+01   8.90455000e+01   8.61412791e+01   6.52300429e-02
        5.80844179e+00   5.07661263e-01]
     [  9.26132536e+01   8.92400000e+01   8.58667464e+01   7.55995881e-02
        6.74650724e+00   4.31816571e-01]
     [  9.29344497e+01   8.93910000e+01   8.58475503e+01   7.92797873e-02
        7.08689946e+00   6.31086945e-01]
     [  9.33114122e+01   8.95080000e+01   8.57045878e+01   8.49848539e-02
        7.60682430e+00   4.42420124e-01]
     [  9.37270110e+01   8.96885000e+01   8.56499890e+01   9.00563838e-02
        8.07702198e+00   6.80945403e-01]
     [  9.38972812e+01   8.97460000e+01   8.55947188e+01   9.25117832e-02
        8.30256250e+00   4.63143909e-01]
     [  9.42636418e+01   8.99125000e+01   8.55613582e+01   9.67861377e-02
        8.70228361e+00   4.15826692e-01]
     [  9.45630193e+01   9.00805000e+01   8.55979807e+01   9.95225220e-02
        8.96503854e+00   1.48579313e-01]
     [  9.47851634e+01   9.03815000e+01   8.59778366e+01   9.74461225e-02
        8.80732672e+00   1.93266744e-01]
     [  9.50411874e+01   9.06575000e+01   8.62738126e+01   9.67087637e-02
        8.76737475e+00   7.82660026e-02]
     [  9.49062071e+01   9.08630000e+01   8.68197929e+01   8.89956780e-02
        8.08641429e+00   3.22789193e-01]
     [  9.49015375e+01   9.08830000e+01   8.68644625e+01   8.84332063e-02
        8.03707509e+00   3.05526266e-01]
     [  9.48939343e+01   9.09040000e+01   8.69140657e+01   8.77834713e-02
        7.97986867e+00   2.26311285e-01]
     [  9.48594576e+01   9.09880000e+01   8.71165424e+01   8.50982021e-02
        7.74291521e+00   4.30661576e-02]
     [  9.46722663e+01   9.11525000e+01   8.76327337e+01   7.72280810e-02
        7.03953265e+00  -5.29486389e-02]
     [  9.45543042e+01   9.11905000e+01   8.78266958e+01   7.37753219e-02
        6.72760849e+00   2.48722001e-01]
     [  9.46761721e+01   9.11200000e+01   8.75638279e+01   7.80546993e-02
        7.11234420e+00   4.72660054e-02]
     [  9.45733946e+01   9.11670000e+01   8.77606054e+01   7.47286754e-02
        6.81278915e+00   2.01003516e-01]
     [  9.45322396e+01   9.12495000e+01   8.79667604e+01   7.19508503e-02
        6.56547911e+00   4.16304661e-01]
     [  9.45303313e+01   9.12415000e+01   8.79526687e+01   7.20906879e-02
        6.57766250e+00   7.52141243e-01]
     [  9.43672335e+01   9.11660000e+01   8.79647665e+01   7.02286710e-02
        6.40246702e+00   7.83328285e-01]
     [  9.41460689e+01   9.10495000e+01   8.79529311e+01   6.80194599e-02
        6.19313782e+00   6.21182512e-01]]
    """

    num_prices = len(prices)

    if num_prices < period:
        # show error message
        raise SystemExit('Error: num_prices < period')

    bb_range = num_prices - period + 1

    # 3 bands, bandwidth, range and %B
    bbs = np.zeros((bb_range, 6))

    simple_ma = sma(prices, period)

    for idx in range(bb_range):
        std_dev = np.std(prices[idx:idx + period])

        # upper, middle, lower bands, bandwidth, range and %B
        bbs[idx, 0] = simple_ma[idx] + std_dev * num_std_dev
        bbs[idx, 1] = simple_ma[idx]
        bbs[idx, 2] = simple_ma[idx] - std_dev * num_std_dev
        bbs[idx, 3] = (bbs[idx, 0] - bbs[idx, 2]) / bbs[idx, 1]
        bbs[idx, 4] = bbs[idx, 0] - bbs[idx, 2]
        bbs[idx, 5] = (prices[idx] - bbs[idx, 2]) / bbs[idx, 4]

    return bbs


