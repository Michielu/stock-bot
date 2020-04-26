import pandas as pd
import numpy as np

# Working with pandas dataframe
d = {'col1': [1, 2], 'col2': [3, 4]}
df = pd.DataFrame(data=d)
print(df)
print(df.dtypes)

df2 = pd.DataFrame(
    np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), columns=['a', 'b', 'c'])
print(df2)


timestamp = pd.Timestamp(1513393355, unit='s', tz="US/Central")
print("Time: ", timestamp)
print(timestamp.timetz(), type(timestamp.timetz()))
print(timestamp.timetz().hour, type(timestamp.timetz()))
print(timestamp.timetz().minute, type(timestamp.timetz()))
print("huh")
print(timestamp.hour, type(timestamp.timetz()))
print(timestamp.minute, type(timestamp.timetz()))
