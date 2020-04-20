from data_source.sp500 import SP500
from data_source.predictions import Predictions
from data_source.current import Current
from module_obj.GoogleSheets import GoogleSheets


# Get SP500 in list
sp500Data = SP500["getSP500"]()
specific_stocks = []

industry = ["Information Technology", "Health Care", "Financials", "Communication Services",
            "Consumer Discretionary", "Industrials", "Consumer Staples", "Utilities", "Real Estate", "Energy", "Materials"]

choose_industry = industry[6]
# for company in sp500Data:
#     if company.get_industry() == choose_industry:
#         specific_stocks.append(company)


if len(specific_stocks) == 0:
    specific_stocks = sp500Data
else:
    print(len(specific_stocks), " of ", choose_industry)

# # TEST_STOCK = ["SPY", "CCI", "TFC", "NFLX"]
# # projected_price = Predictions["get_predictions"](TEST_STOCK)
projected_price = Predictions["get_predictions"](specific_stocks)

# projected_price = {'APD': [215.46, 5.118, '2020-04-16'], 'ALB': [60.23, 6.606, '2020-04-16'], 'AMCR': [9.21, 12.267, '2020-04-16'], 'AVY': [109.98, 6.216, '2020-04-16'], 'BLL': [67.84, 4.399, '2020-04-16'], 'CE': [
#     87.47, 19.697, '2020-04-16'], 'CF': [34.89, 29.832, '2020-04-16'], 'CTVA': [26.49, 8.303, '2020-04-16'], 'DOW': [39.42, 30.472, '2020-04-16'], 'DD': [47.17, 35.704, '2020-04-16'], 'EMN': [60.33, 23.698, '2020-04-16']}
print(projected_price)
current_price = Current["get_current_price_list"](projected_price.keys())
ratio_dict = Predictions["calculate_ratio"](projected_price, current_price)
print(len(ratio_dict), ratio_dict)

sheets_format = []
sheets_format.append(['TICKER', 'CURRENT', 'PREDICTED',
                      'ERROR CHANCE', 'PREDICTED RATIO', 'ACTUAL', 'ACTUAL RATIO'])

for key in projected_price.keys():
    projected = projected_price[key]
    sheets_format.append([key, current_price[key], projected[0],
                          projected[1], ratio_dict[key], 'NA', 'NA'])

# print("Sheets format: ", sheets_format)
projected_date = list(projected_price.values())[0][2]

gs = GoogleSheets()
gs.add_sheet(sheets_format, projected_date)

# gs.update_sheet("2020-04-17")

# [['Ticker', 'Current', 'Predicted'], [
#         'SPY', '280', '300'], ['APY', '240', '300']]
