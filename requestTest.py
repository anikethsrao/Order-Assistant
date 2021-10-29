import requests
import pandas as pd

URL = 'https://jsonplaceholder.typicode.com/todos/1'
r = requests.get(url=URL)

print(r)

j = r.json() # Check the JSON Response Content documentation below
print(j)
df = pd.json_normalize(j)
fileExtention = '~/Documents/GitHub/Order-Assistant'
fileName = 'test'
df.to_csv(f'{fileExtention}/{fileName}.csv')