from module_obj.MyStock import MyStock

stock1 = MyStock("MMM", "3M Industry", "Manuafactorying")
stock1.add_stock_price(10)
stock1.add_stock_price(12)
stock1.add_stock_price(14)

print(stock1.get_history_price(), " equals [10, 12, 14]")
print(stock1.get_history_sma(), " equals [12]")

stock1.add_stock_price(16)
print(stock1.get_history_price(), " equals [10, 12, 14, 16]")
print(stock1.get_history_sma(), " equals [12, 14]")
