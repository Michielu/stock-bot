
def test_account(my_account):
    my_account.print_summary()
    my_account.buy_stock("AAPL", 10, 100)
    my_account.print_summary()  # account value: 10000

    my_account.buy_stock("AAPL", 10, 200)
    my_account.print_summary()

    my_account.sell_stock("AAPL", 20, 100)
    my_account.print_summary()

    my_account.buy_stock("MSFT", 10, 100)
    my_account.print_summary()

    my_account.buy_stock("AAPL", 10, 50)
    my_account.print_summary()

    my_account.buy_stock("SPY", 4, 250)
    my_account.print_summary()
    return my_account.get_account_value() == 1100
