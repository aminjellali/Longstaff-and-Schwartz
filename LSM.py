"""
Created on Sat Sep 12 14:05:58 2018

@author: Amin Jellali
@Email: amin.jellali@esprit.tn
"""

import numpy as np
from functions import simulate_paths
# one wants to test the LSM algorithm on the evolution of Laguerre base
# just change this import to the corresponding number of polynoms function in
# the functions file (includes only 2pol, 3pol, 4pol)
from functions import renderContinuationValues
import time as time_clock


begin = time_clock.time()
# Inputs
numberOfPaths =  100000
timePeriod = 2
numberOftimePeriods = 50
deltaT = timePeriod / numberOftimePeriods
S0 = 44
r = 0.06
sigma = 0.4
K =  40

print('Generating stock price matrix ...')
stock_price = simulate_paths(numberOfPaths, timePeriod,
                            numberOftimePeriods, sigma, r, S0)

print ('Calculating cash flow matrix...')
# At time t = N
cash_flow_matrix = np.zeros_like(stock_price)
for time in range (0,numberOftimePeriods + 1):
    for path_in_time in range (0, numberOfPaths):
        if K - stock_price[time][path_in_time] > 0:
            cash_flow_matrix[time][path_in_time] =(
            K - stock_price[time][path_in_time])
print('Entering loop...')
# starting the loop
for time in range (numberOftimePeriods-1, 0, -1):
    print('Remaining calculations: ',time)
    # fetch the last cash flow for in the money paths
    X = []
    Y = []
    for stock_p in range(0, numberOfPaths):
        if stock_price[time][stock_p] < K:
            X.append(stock_price[time][stock_p])
            for cash_flow_fetcher in range (time + 1, numberOftimePeriods + 1):
                if cash_flow_matrix[cash_flow_fetcher][stock_p] > 0:
                    Y.append( cash_flow_matrix[cash_flow_fetcher][stock_p]*
                             np.exp(-r *
                                    deltaT * (cash_flow_fetcher - time)))
                    break
                elif (cash_flow_matrix[cash_flow_fetcher][stock_p] == 0 and
                      cash_flow_fetcher == numberOftimePeriods) :
                    Y.append(0)
    # calculate the continuation values
    if len(X) > 1 and len(Y) > 1:
        continuation_values = renderContinuationValues (X, Y)
        # print(cash_flow_matrix)
        # generate the cash flow vector for time t
        # initialize the continuation values counter
        continuation_values_counter = -1
        # get the current cash_flow_vector of time
        cash_flow_vector = np.array([K - x
                                if x < K else 0 for x in stock_price[time]])
        # set a dynamic comparision loop to compare between the cash flow at
        # current time and the corresponding continuation value
        for cash_flow_index in range(0, numberOfPaths):
            if cash_flow_vector[cash_flow_index] > 0 :
                continuation_values_counter += 1
                # have an in the money path thus we campare continuation values
                # to current vector
                if(cash_flow_vector[cash_flow_index] >
                   continuation_values[continuation_values_counter]):
                    # we exercice immedietly thus we change all future values
                    # to zero
                    for sub_time in range(time + 1,numberOftimePeriods + 1 ):
                            cash_flow_matrix[sub_time][cash_flow_index] = 0
                else :
                    cash_flow_matrix[time][cash_flow_index] = 0

# calculate mean values
cashFlowMeanVector = [np.mean(x) for x in cash_flow_matrix ]
# discount mean values
DiscountedCashFlowVector = [ cashFlowMeanVector[i] *  np.exp(-r* deltaT * i)
                            for i in range(1,len(cashFlowMeanVector))]
# determine the value
summ=np.sum(DiscountedCashFlowVector)
# determine best stoping time
maxCashFlow = np.max(DiscountedCashFlowVector)
end = time_clock.time()
standard_error_vector = np.matrix(stock_price)
standard_error = np.mean(standard_error_vector.std(1)/np.sqrt(numberOfPaths))
print('######################################################################')
print('############################ Input Data ##############################')
print('######################################################################')
print('          ',"number of paths is: ",numberOfPaths)
print('          ',"time periode is: ",timePeriod)
print('          ',"number of exercice is: ",numberOftimePeriods)
print('          ',"step is : ",deltaT)
print('          ',"strike price is: ",K)
print('          ',"spot price is: ",S0)
print('          ',"intrest rate is: ",r)
print('          ',"volatility is: ",sigma)
print('          ',"number of polynoms is: ",3)
print('######################################################################')
print('########################### Final Values #############################')
print('######################################################################')
print('             ', " error is : ", standard_error )
print('          ',"max value is: ",maxCashFlow," at time: ",
      DiscountedCashFlowVector.index(maxCashFlow))
print('          ',"finale value is: ",summ)
print('          ',"execution time: ", end - begin, ' s')
print('######################################################################')
print('######################################################################')
print('###############################AJ#####################################')
