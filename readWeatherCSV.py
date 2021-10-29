import pandas as pd


data = pd.read_csv('~/Documents/GitHub/Order-Assistant/WeatherData1.csv')
data=data.to_json()
for info in data['data.weather']:
    print(info)
