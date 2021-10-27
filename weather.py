# Aniketh Rao 
# Weather in scarborough near Papa J's Scarborough
# Store location 4630 Kingston Rd, Scarborough, ON M1E 4Z4
"""
# Library Imports
from WorldWeatherPy import HistoricalLocationWeather

# Initialization

BASE_URL = "https://api.worldweatheronline.com/premium/v1/past-weather.ashx"
API_KEY = "8c311cade0ad48229a3184843212710"
q = "M1E" # POSTAL CODE

# date format yyyy-MM-dd (Example: 2009-07-20 for 20 July 2009.)
start_date = "2021-07-11"

# enddate yyyy-MM-dd (Example: 2009-07-22 for 22 July 2009.)
# If you wish to retrieve weather between two dates, use this  parameter to specify the ending date.
# Important: the enddate parameter must have the same month and year as the date parameter.
end_date = "2021-07-18"

# tp Valid values: 1, 3 (default), 6, 12, 24
# Specifies the weather forecast time interval in hours.
# Options are: 1 hour, 3 hourly, 6 hourly, 12 hourly (day/night) or 24 hourly (day average).
FREQUENCY = 12

# format XML (default), JSON
FORMAT = "JSON"

#requestURL = f"{BASE_URL}?key={API_KEY}&q={q}&date={start_date}&enddate={end_date}&tp={FREQUENCY}&format={FORMAT}"

dataset = RetrieveByAttribute(API_KEY, q, start_date, end_date, FREQUENCY).retrieve_hist_data()
"""

from datetime import datetime, timedelta

month = "Sep"
day = 16
year = 2019
for i in range(100):
    date = f'{day}/{month}/{year}'
    dt = datetime.strptime(date, '%d/%b/%Y')
    start = dt - timedelta(days=dt.weekday())
    end = start + timedelta(days=6)
    print(f'week {i}')
    print(start.strftime('%d/%b/%Y'))
    print(end.strftime('%d/%b/%Y')) 

    

    start = start + timedelta(days=7)

    day = start.strftime('%d')
    month = start.strftime('%b')
    year = start.strftime('%Y')

print("Finished finding days")