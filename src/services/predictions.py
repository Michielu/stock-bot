import stocker as Stocker


def get_predictions(my_stocks_arr):
    i = 0
    prediction_info = {}
    num = len(my_stocks_arr)
    # print(my_stocks_arr)
    # for company in my_stocks_arr:
    #     print(company.get_data())

    for company in my_stocks_arr:
        # if(i > 10):
        #     break
        ti = company.get_ticker()
        # ti = company
        future_prediction = []
        try:
            future_prediction = Stocker.predict.tomorrow(ti)
        except:
            i += 1
            print("Error with ", ti)
            continue

        # todo: check if failed with user so it stops this

        # company.set_predictions(future_prediction)
        i = i+1
        prediction_info[ti] = future_prediction
        print(ti, " ", future_prediction)
        print("Done", i, "/", num)

    return prediction_info

# Predict = {ticker: [prediction, error %, date]}
# current= {ticker: current}


def calculate_ratio(predict, current):
    ratio_dic = {}
    for t in predict.keys():
        ratio = predict[t][0]/current[t]
        # print(t, " : ", ratio)
        # if ratio > 1.01:
        ratio_dic[t] = ratio
        # print("Ratio:", ratio)
    return ratio_dic

# Predict = {ticker: [prediction, error %, date]}
# current= {ticker: current}


def calculate_error(predict, current):
    error_dic = {}
    for t in predict.keys():
        ratio = predict[t][1]
        # print(t, " : ", ratio)
        # if ratio > 1.01:
        error_dic[t] = ratio
        # print("Ratio:", ratio)
    return error_dic


Predictions = {
    "get_predictions": get_predictions,
    "calculate_ratio": calculate_ratio
}
