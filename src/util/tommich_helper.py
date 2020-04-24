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


def get_roc(closing_price, history_closing, roc_length):

    # print("PC: ", closing_price,  history_roc)
    if roc_length < 0:
        return None

    if roc_length > len(history_closing):
        return 1

    else:
        return (closing_price/history_closing[-roc_length] - 1) * 100


def get_hl2(high, low):
    if low == 0:
        return None
    return round(high/low, 2)


TOMMICH_HELPER = {
    "get_sma_balance": get_sma_balance,
    "get_roc": get_roc,
    "get_hl2": get_hl2
}

# Tests
# print("hello")
# print("SMA: ", simple_moving_avg(data_set, 3))
