from data_source.robinhood import Robinhood

rob = Robinhood("mich.menning@gmail.com")
print(rob.get_buying_power())
print(rob.get_total_equity())
print("IBIO owns: ", rob.get_num_stock_own("IBIO"))
print("SPY owns: ", rob.get_num_stock_own("SPY"))
print("SPXS owns: ", rob.get_num_stock_own("SPXS"))
print("SPXS stock info: ", rob.get_stock_info("SPXS"))

# Practice the buying and selling:
# print(rob.order_buy_market("CPHI", 1))
# print(rob.order_sell_market("IBIO", 1))
print(rob.order_sell_limit("IBIO", 1, 1.35))
print(rob.get_all_stock_info())


# After buy:
# {'LK': {'price': '4.390000', 'quantity': '4.00000000', 'average_buy_price': '6.2275', 'equity': '17.56', 'percent_change': '-29.51', 'equity_change': '-7.350000', 'type': 'adr', 'name': 'Luckin Coffee', 'id': '632edbd4-6fa3-41ad-b93f-f800243d88bd', 'pe_ratio': None, 'percentage': '2.66'},
# 'IBIO': {'price': '0.905000', 'quantity': '100.00000000', 'average_buy_price': '2.2800', 'equity': '90.50', 'percent_change': '-60.31', 'equity_change': '-137.500000', 'type': 'stock', 'name': 'iBio', 'id': '608f9563-f6b5-404f-a555-0f2ee635e4c7', 'pe_ratio': None, 'percentage': '13.72'},
# 'SPXS': {'price': '10.610000', 'quantity': '26.00000000', 'average_buy_price': '13.9517', 'equity': '275.86', 'percent_change': '-23.95', 'equity_change': '-86.884200','type': 'etp', 'name': 'Daily S&P 500 Bear 3X', 'id': '0dc6bd32-b849-48e1-9f80-badbfb306f5e', 'pe_ratio': None, 'percentage': '41.82'},
# 'UVXY': {'price': '42.610000', 'quantity': '3.00000000', 'average_buy_price': '50.1367', 'equity': '127.83', 'percent_change': '-15.01', 'equity_change': '-22.580100', 'type': 'etp', 'name': 'ProShares Ultra VIX Short-Term Futures ETF', 'id': '16543bbd-47df-4ff3-a743-11ff0901743f', 'pe_ratio': None, 'percentage': '19.38'},
# 'CPHI': {'price': '0.477500', 'quantity': '0.00000000', 'average_buy_price': '0.0000', 'equity': '0.00', 'percent_change': '0.00', 'equity_change': '0.000000', 'type': 'stock', 'name': 'China Pharma Holdings', 'id': '30fcef31-a871-46c1-afeb-ddb8d1ebc82b', 'pe_ratio': None, 'percentage': '0.00'}
# }
