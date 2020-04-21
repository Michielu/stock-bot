import numpy as np

data_set = [1, 5, 7, 8, 2, 4, 12, 6, 92, 2, 0]


def simple_moving_avg(values, window):
    # window = len(values)
    weights = np.repeat(1.0, window)/window
    #if window is 3: weights = [.33,.33,.33]
    smas = np.convolve(values, weights, 'valid')
    return smas


def get_sma_balance(values):
    weight = 1/len(values)
    return sum(values)*weight


MOVING_AVERAGE = {
    "get_sma_balance": get_sma_balance
}

# Tests
# print("hello")
# print("SMA: ", simple_moving_avg(data_set, 3))
