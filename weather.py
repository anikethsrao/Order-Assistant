# Aniketh Rao 
# Weather in scarborough near Papa J's Scarborough
# Store location 4630 Kingston Rd, Scarborough, ON M1E 4Z4

# Library Imports
from datetime import datetime, timedelta
import pandas as pd
import requests
from requests.api import request

# Initialization
BASE_URL = "https://api.worldweatheronline.com/premium/v1/past-weather.ashx"
API_KEY = "8c311cade0ad48229a3184843212710"
Q = "M1E" # POSTAL CODE

# date format yyyy-MM-dd (Example: 2009-07-20 for 20 July 2009.)
MONTHS = {
    "Jan" : '01',
    "Feb" : '02',
    "Mar" : '03',
    "Apr" : '04',
    "May" : '05',
    "Jun" : '06',
    "Jul" : '07',
    "Aug" : '08',
    "Sep" : '09',
    "Oct" : '10',
    "Nov" : '11',
    "Dec" : '12'
}

# enddate yyyy-MM-dd (Example: 2009-07-22 for 22 July 2009.)
# If you wish to retrieve weather between two dates, use this  parameter to specify the ending date.
# Important: the enddate parameter must have the same month and year as the date parameter.

# tp Valid values: 1, 3 (default), 6, 12, 24
# Specifies the weather forecast time interval in hours.
# Options are: 1 hour, 3 hourly, 6 hourly, 12 hourly (day/night) or 24 hourly (day average).
FREQUENCY = 12

# format XML (default), JSON
FORMAT = "JSON"

# dataset = RetrieveByAttribute(API_KEY, Q, start_date, end_date, FREQUENCY).retrieve_hist_data()


def main():

    # Starting date 
    day = 16
    month = "Sep"
    year = 2019

    start_date = f'{year}-{MONTHS[month]}-{day}'

    # Weeks of data required
    WEEKS = 1

    for i in range(WEEKS):
        start_date, end_date = get_date_range(start_date)

        print(send_request(start_date, end_date))
        find_next_week(start_date)

    print("Program Executed")


def find_next_week(start):

    year, month, day = start.split('-')
    date = f'{day}/{get_month_from_index(month)}/{year}'

    print(f'date = {date}')

    dt = datetime.strptime(date, '%d/%b/%Y')
    start = dt - timedelta(days=dt.weekday())
    start = start + timedelta(days=7)

    day = start.strftime('%d')
    month = start.strftime('%b')
    year = start.strftime('%Y')

    return f'{year}-{MONTHS[month]}-{day}'


def get_date_range(start_date):

    start_year, month_numerical, start_day = start_date.split('-')

    start_month = get_month_from_index(month_numerical)
    
    date = f'{start_day}/{start_month}/{start_year}'
    dt = datetime.strptime(date, '%d/%b/%Y')
    start = dt - timedelta(days=dt.weekday())
    end = start + timedelta(days=6)

    end_day = end.strftime('%d')
    end_month = end.strftime('%b')
    end_year = end.strftime('%Y')

    start_date = f'{start_year}-{MONTHS[start_month]}-{start_day}'
    end_date = f'{end_year}-{MONTHS[end_month]}-{end_day}'

    return (start_date, end_date)


def send_request(start_date: str, end_date: str):
    requestURL = f"{BASE_URL}?key={API_KEY}&q={Q}&date={start_date}&enddate={end_date}&tp={FREQUENCY}&format={FORMAT}"

    print("Requesting...")
    r = requests.get(url=requestURL)
    if r.status_code == 200:
        print("Request Succeeded...")
        j = r.json()
        df = pd.json_normalize(j)
        fileExtention = '~/Documents/GitHub/Order-Assistant'
        fileName = 'WeatherData1.csv'
        df.to_csv(f'{fileExtention}/{fileName}')
        return f'Saved to file {fileName}'

    else:
        return 'request failed'


def get_month_from_index(index):
    return list(MONTHS.keys())[list(MONTHS.values()).index(index)]
main()