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


def get_price_change(high, low, past_price_change):
    if past_price_change == None or past_price_change < 2:
        return 0
    else:
        hl2 = get_hl2(high, low)
        if hl2 == None:
            print("Error getting hl2")
            return 0

        return (hl2/past_price_change - 1)*100


def get_hl2(high, low):
    if low == 0:
        return None
    return round(high/low, 2)


TOMMICH_HELPER = {
    "get_sma_balance": get_sma_balance,
    "get_price_change": get_price_change
}

# Tests
# print("hello")
# print("SMA: ", simple_moving_avg(data_set, 3))
