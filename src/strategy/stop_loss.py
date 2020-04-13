
sell_limit = -1


def stop_loss(account, data_df):
    # account.buy_stock("SPY", 4, 250)
    percentage_sell = .02  # 2% from max
    percentage_buy = .01  # 1%
    percentage_buy_more = .04

    bought_max_price = -1
    bought_num = 0
    # buy when stock goes up 1%
    # sell when max price go down 2%
    # later: buy more when up 5%

    last_price = -1
    lowest_price = -1  # for buying purposes
    for index, row in data_df.iterrows():
        current_price = row["Close"]
        if last_price == -1:
            last_price = current_price
            lowest_price = current_price
            continue

        # print(last_price, " --> ", current_price, "sell at: ",
            #   bought_max_price * (1-percentage_sell), "max: ", bought_max_price)
        if current_price < last_price:
            # Check to sell stock
            if bought_num != 0 and current_price < bought_max_price * (1-percentage_sell):
                # sell all
                print("Sell all!!!")
                # reset lowest_price or I'll continually buy when it goes up
                bought_max_price = -1
                lowest_price = current_price
            elif current_price < lowest_price:
                lowest_price = current_price
        elif current_price > last_price:
            # Check to buy stock
            if bought_num == 0 and current_price * (1-percentage_buy) < lowest_price:
                bought_num = 5
                bought_max_price = current_price
                print("buy first ones")
            if bought_num != 0 and current_price * (1-percentage_buy_more) < lowest_price:
                bought_num += 5
                print("Buy more!")

        # update last_price
        last_price = current_price
    return ""


Strategy = {
    "stop_loss": stop_loss
}
