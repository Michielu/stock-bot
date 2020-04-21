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


def get_price_change():
    #Assert(PChangeLength > 0, "'length' must be positive: " + PChangeLength);
    # def PriceChange = if ValueforPC[PChangeLength] != 0 then (ValueforPC / ValueforPC[PChangeLength] - 1) * 100 else 0;
    print('price change!')


def get_hl2(high, low):
    if low > 0:
        return -1
    return round(high/low, 2)


PARABOLIC_HELPER = {
    "get_sma_balance": get_sma_balance
}

# Tests
# print("hello")
# print("SMA: ", simple_moving_avg(data_set, 3))
