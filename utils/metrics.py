#!/usr/bin/env python

from math import sqrt
from utils import *
import sys

def MAE(observations, forecasts):
    """The MAE measure the average magnitude of the errors in a set of
    forecasts, without considering their direction.
    The MAE is a linear score which means that all the individual differences
    are equally in the average
    """
    msg("Calculate MAE")
    if len(observations) != len(forecasts):
        msg("Your result is not suitable")
        sys.exit()
    sum_error = 0.0
    m = len(observations)

    for iter in xrange(m):
        sum_error += abs(observations[iter]-forecasts[iter])

    return sum_error/m

def RMSE(observations, forecasts):
    """The RMSE is a quadratic scoring rule which measures the average
    magnitude of the error.
    The formula in words:
    the difference between forecast and corresponding observed values are each
    squared and then averaged over the sample.
    The RMSE is the most usefull when large errors are particularly undesirable
    """
    msg("Calculate RMSE")
    if len(observations) != len(forecasts):
        msg("The results is not suitable")
        sys.exit()
    square_error = 0.0
    m = len(observations)
    for iter in xrange(m):
        square_error += (observations[iter]-forecasts[iter])**2

    return sqrt(square_error/m)
    
