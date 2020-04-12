import stocker as Stocker


def get_predictions(my_stocks_arr):
    i = 0

    for company in my_stocks_arr:
        if(i > 5):
            break
        future_prediction = Stocker.predict.tomorrow(company.get_ticker())
        company.set_predictions(future_prediction)
        i = i+1
        print(company.get_ticker(), " ", future_prediction)

    return my_stocks_arr
