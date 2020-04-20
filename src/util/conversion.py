# Converts dictionary to sheets
# Example:
# Input: {'SPY': ['1', '2', '3', '0.9625', 279.1000061035156, 0.0035829451025848748], 'AFZASD': ['12', '12', '12', '3', nan, nan]}
# Output: [['TICKER', 'CURRENT', 'PREDICTED', 'ERROR CHANCE', 'PREDICTED RATIO', 'ACTUAL', 'ACTUAL RATIO'], ['SPY', '96', '92.4', '4.652', '0.9625', 279.1000061035156, 0.34396272984814796], ['AFZASD', '167.9499969', '173.64', '5.587', '1.033879149', 'NA', 'NA']]


def dic_to_sheets(dic, keys):
    sheets_format = []
    sheets_format.append(keys)
    for key in dic.keys():
        projected = dic[key]
        temp_array = [key] + projected
        sheets_format.append(temp_array)

    print(sheets_format)
    return sheets_format

# [['TICKER', 'CURRENT', 'PREDICTED', 'ERROR CHANCE', 'PREDICTED RATIO', 'ACTUAL', 'ACTUAL RATIO'], ['MO', '40.90999985', '42.85', '8.599', '1.047421172', 'NA', 'NA'],['CLX', '195.6399994', '198.01', '2.886', '1.01211409', 'NA', 'NA']]


def convert_to_number(arr):
    for stock in arr[1:]:
        for index, el in enumerate(stock):
            try:
                stock[index] = float(el)
            except:
                print("FAIL:", el)

    return arr


Conversion = {
    "dic_to_sheets": dic_to_sheets,
    "convert_to_number": convert_to_number
}
