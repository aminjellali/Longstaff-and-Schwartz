# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 14:05:58 2018

@author: Amin Jellali
@Email: amin.jellali@esprit.tn
"""
import numpy as np

#### Laguerre base ####
def l_0():
    return 1


def l_1(x):
    return 1-x


def l_2(x):
    return (1/2)*(x**2-4*x+2)

def l_3(x):
    return (1/6)*(-x**3+9*x**2-18*x+6)

# used to simulate stock price paths
def simulate_paths(numberOfPaths, timePeriod, numberOftimePeriods, sigma,
                   r, S0):
    deltaT = timePeriod / numberOftimePeriods
    price = np.zeros((numberOftimePeriods + 1, numberOfPaths), np.float64) 
    price[0] = S0 
    for t in range(1, numberOftimePeriods + 1): 
     rand = np.random.standard_normal(numberOfPaths) 
     price[t] = price[t - 1] * np.exp((r - 0.5 * sigma ** 2) * deltaT + 
             sigma * np.sqrt(deltaT) * rand) 
    return price

# renders the solution of |αX - Y| = 0
# 3 polynoms
def renderContinuationValues(X, Y):
    # we apply the Lageurre-base polynom on the stock price vector at a
    # given time t to obtain a matrix P_X
    plynomMatrix = np.array([[l_0(), l_1(x), l_2(x)] for x in X])
    # multyply the stock prices matrix with it's transpose
    A = np.matmul(np.transpose(plynomMatrix), plynomMatrix)
    # multuply the discounted cashFlows vector at times of last one with
    # the transpose of P_X
    B = np.matmul(np.transpose(plynomMatrix), Y)
    # get the alpha* that give us the minimal distance:
    # minimal[(X*alpha-Y)^2]
    alphaStar = np.linalg.solve(A, B)
    # continuation values equation(6) of UCLA article
    conts = [alphaStar[0] * l_0() +
             alphaStar[1] * l_1(x) +
             alphaStar[2] * l_2(x)
             for x in X]
    return np.array(conts)


# renders the solution of |αX - Y| = 0
# 2 polynoms
def renderContinuationValues_2_poly_base(X, Y):
    # we apply the Lageurre-base polynom on the stock price vector at a
    # given time t to obtain a matrix P_X
    plynomMatrix = np.array([[l_0(), l_1(x)] for x in X])
    # multyply the stock prices matrix with it's transpose
    A = np.matmul(np.transpose(plynomMatrix), plynomMatrix)
    # multuply the discounted cashFlows vector at times of last one with
    # the transpose of P_X
    B = np.matmul(np.transpose(plynomMatrix), Y)
    # get the alpha* that give us the minimal distance:
    # minimal[(X*alpha-Y)^2]
    alphaStar = np.linalg.solve(A, B)
    # continuation values equation(6) of UCLA article
    conts = [alphaStar[0] * l_0() +
             alphaStar[1] * l_1(x)
             for x in X]
    return np.array(conts)


# renders the solution of |αX - Y| = 0
# 3 polynoms
def renderContinuationValues_4_poly_base(X, Y):
    # we apply the Lageurre-base polynom on the stock price vector at a
    # given time t to obtain a matrix P_X
    plynomMatrix = np.array([[l_0(), l_1(x), l_2(x), l_3(x) ] for x in X])
    # multyply the stock prices matrix with it's transpose
    A = np.matmul(np.transpose(plynomMatrix), plynomMatrix)
    # multuply the discounted cashFlows vector at times of last one with
    # the transpose of P_X
    B = np.matmul(np.transpose(plynomMatrix), Y)
    # get the alpha* that give us the minimal distance:
    # minimal[(X*alpha-Y)^2]
    alphaStar = np.linalg.solve(A, B)
    # continuation values equation(6) of UCLA article
    conts = [alphaStar[0] * l_0() +
             alphaStar[1] * l_1(x) +
             alphaStar[2] * l_2(x) +
             alphaStar[3] * l_3(x)
             for x in X]
    return np.array(conts)

