from data_source.robinhood import Robinhood

rob = Robinhood("mich.menning@gmail.com")
print(rob.get_buying_power())
print(rob.get_total_equity())
print("IBIO owns: ", rob.get_num_stock_own("IBIO"))
print("SPY owns: ", rob.get_num_stock_own("SPY"))
print("SPXS owns: ", rob.get_num_stock_own("SPXS"))
