import pandas as pd


data = pd.read_csv('~/Documents/GitHub/Order-Assistant/WeatherData1.csv')
data = data['data.weather'][1]

print(data)
def parse(start, end):
    start_index = data.index(start)
    end_index = data[start_index:].index(end)
    final = data[start_index: start_index+end_index]
    return final

print(parse('avgTempC', ','))

# print(data)
# data.to_json()

#data_json = data['data.weather'].to_json()

# data_list = list(list(data['data.weather'])[0])

#print(type(data_list))
#print(data_list[0])
"""
for info in data['data.weather']:
    print(type(info))
"""