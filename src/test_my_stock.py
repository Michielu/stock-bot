from module_obj.MyStock import MyStock
# TO test, change sma_window to 3 in MyStock
stock1 = MyStock("MMM", "3M Industry", "Manuafactorying")
stock1.add_stock_price(10, 12, 8)
stock1.add_stock_price(12, 14, 8)
stock1.add_stock_price(14, 16, 8)

print(stock1.get_history_price(), " equals [10, 12, 14]")
print(stock1.get_history_sma(), " equals [12]")

stock1.add_stock_price(16, 18, 8)
print(stock1.get_history_price(), " equals [10, 12, 14, 16]")
print(stock1.get_history_sma(), " equals [12, 14]")
