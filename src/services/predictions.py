import stocker as Stocker


def get_predictions(my_stocks_arr):
    i = 0
    prediction_info = {}
    for company in my_stocks_arr:
        if(i > 10):
            break
        future_prediction = Stocker.predict.tomorrow(company.get_ticker())
        company.set_predictions(future_prediction)
        i = i+1
        prediction_info[company.get_ticker()] = future_prediction
        print(company.get_ticker(), " ", future_prediction)

    return prediction_info

# Predict = {ticker: [prediction, error %, date]}
# current= {ticker: current}


def calculate_ratio(predict, current):
    ratio_dic = {}
    for t in predict.keys():
        ratio = predict[t][0]/current[t]
        print(t, " : ", ratio)
        if ratio > 1.01:
            ratio_dic[t] = ratio
        # print("Ratio:", ratio)
    return ratio_dic

# Predict = {ticker: [prediction, error %, date]}
# current= {ticker: current}


def calculate_error(predict, current):
    error_dic = {}
    for t in predict.keys():
        ratio = predict[t][1]
        print(t, " : ", ratio)
        if ratio > 1.01:
            error_dic[t] = ratio
        # print("Ratio:", ratio)
    return error_dic


Predictions = {
    "get_predictions": get_predictions,
    "calculate_ratio": calculate_ratio
}
