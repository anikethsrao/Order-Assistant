import pdfplumber
import json
import pandas as pd
from copy import deepcopy

# File path for weather data
weather_data_path = '~/Order-Assistant/WeatherData.csv'
data_columns = [
    'Begin', 
    'Delivery', 
    'End', 
    'Used', 
    'Cost', 
    '% of sales'
    ]

data = {}

# list of all items
drinks = {
    '591ml Pepsi': False,
    '591ml Diet Pepsi': False,
    '591ml Mountain Dew': False,
    '591ml Diet Mtn Dew': False,
    '591ml Aquafina': False,
    '591ml Dr Pepper': False,
    '591ml Mug Root Beer': False,
    '591ml Schw Gngr Ale': False,
    '591ml WCherry Pepsi': False,
    '591ml Crush Orange': False,
    '591ml Seven Up': False,
    '591ml Brsk IceT': False,
    '2Ltr Pepsi': False,
    '2Ltr Diet Pepsi': False,
    '2Ltr Mountain Dew': False,
    '2Ltr Dt Mtn Dew': False,
    '2Ltr Dr Pepper': False,
    '2Ltr Mug Root Beer': False,
    '2Ltr Schw Gngr Ale': False,
    '2Ltr Crush Orange': False,
    '2Ltr Brsk SwTea Lm': False,
    '2Ltr Seven Up': False,
    '355ml Pepsi': False,
    '355ml Diet Pepsi': False,
    '355ml Diet Mtn Dew': False,
    '355ml Dr Pepper': False,
    '355ml Schw Gngr Ale': False,
    '355ml Brsk SwTea Lm': False,
    '355ml Seven Up': False,
    '12oz Welch Gr Soda': False
}

cheese = {
    'Cheddar Cheese': False,
    'Three Cheese Blend': False,
    'String Cheese': False,
    'Agropur Cheese': False,
    '2 Cheese': False,
    '3 Cheese': False,
    'Feta Cheese': False,
    'Philly Whipped Cream Chee': False

}

dough = {
    'Dough Tray 10': False,
    'Dough Tray 12': False,
    'Dough Tray 14': False,
    'Dough Tray 16': False,
    'Chocolate Chip Cookie': False,
    'Choc Chip Brownie': False,
    'Cinnamon Pull Apart': False,
    'Thin Crust 14': False,
    'Gluten Free Crust': False
}

# There are two pepperonis in the log, needs work
meats = {
    'Pepperoni': False,
    'Bacon': False,
    'Salami': False,
    'Italian Sausage': False,
    'Anchovies': False,
    'Grilled Chicken': False,
    'Chicken Popper': False,
    'Salami': False,
    'Canadian Bacon': False,
    'Philly Cheesesteak': False,
    'Sliced Spicy Meatballs': False,
    'Meatball': False,
    'Beef': False,
    'Sausage': False,
    'Italian Sausage': False,
    'Roasted Wings': False,
    'Donair Topping': False
}

produce = {
    'Banana Peppers': False,
    'Black Olives': False,
    'Pineapple Lg Can': False,
    'Mushrooms': False,
    'Fresh Spinach': False,
    'Green Peppers': False,
    'Onions': False,
    'Tomatoes': False,
    'Banana Peppers': False,
    'Pepperoncini Peppers': False,
    'Jalapeno Peppers': False,
    'Green Olives': False
}

sauces = {
    'Bulk Ranch Sauce': False,
    'Pizza Sauce': False,
    'Jug Garlic Sauce': False,
    'Garlic Sauce Cups': False,
    'Pizza Sauce Cups': False,
    'Cheese Sauce Cups': False,
    'Ranch Sauce Cups': False,
    'Barbecue Sauce Cups': False,
    'Buffalo Sauce Cups': False,
    'Honey Must Sauce Cups': False,
    'Blue Cheese Sauce Cups': False,
    'Barbecue Sauce': False,
    'Garlic Parmesan Sauce Jug': False,
    'Buffalo Sauce': False,
    'Pouch Honey Chptl': False,
    'BBQ Bulk': False,
    'Alfredo Sauce': False,
    'Spinach Alfredo Sauce': False,
    'Cream Cheese Flavored Ici': False,
    'Creamy Garlic Dipping Cup': False,
    'Donair Sauce': False,
    'Hellman\'s Bulk Ranch': False
}

seasoning = {
    'Italian Seasoning': False,
    'Seasoning Packets': False,
    'Parmesan': False,
    'Crushed Red Pepper': False,
    'Dustinator': False
}

boxes = {
    'Pizza Box 10': False,
    'Pizza Box 12': False,
    'Pizza Box 14': False,
    'Pizza Box 16': False,
    'Pizza Slice Box': False
}

category_dict = {
    'BEVERAGES': drinks,
    'CHEESE': cheese,
    'MEATS': meats,
    'PRODUCE': produce,
    'DOUGH': dough,
    'SAUCES': sauces,
    'SEASONS/FLOUR': seasoning,
    'BOXES': boxes
}


# Creates a josn with all the data : category { items { data { 'Begin' : 0.00, ... }}}
def logData(inventory, data_in, item, category):
    data = {}
    for i in range(len(data_columns)):
        try:
            x = float(data_in[i])
        except:
            x = 0.00

        data[data_columns[i]] = x

    if category in inventory:
        inventory[category][item] = data
    else:
        inventory[category] = {item: data}


def extrator(path: str) -> str:
    PAGES = 5
    date = 'date'
    category = ''
    category_name = ""
    detail_flag = False  # lets program know when to start recording values
    detail_counter = 0
    details = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
    word_count = 0
    inventory = {}

    for page_no in range(PAGES):
        with pdfplumber.open(path) as pdf:
            page = pdf.pages[page_no]
            text = page.extract_text()
        word = ''
        space_counter = 0
        prev_word = ""
        for character in text:
            if ord(character) != 160:  # 160 is the hex value for ' '
                word += character
                space_counter = 0

            elif len(word) > 0:
                word += ' '
                space_counter += 1

                # Word ends if there are more than one space between words
                if space_counter == 2:
                    word = word.strip()
                    word_count += 1

                    # A new category will only appear once all items have been read
                    if word in category_dict:  
                        for item in category:
                            if not category[item]:
                                print(f'** WARNING ** did not log {item}')
                                raise ValueError(f"{item} not found")
                        category_name = word # current category
                        category = category_dict[word]

                    # If the word exists in the category dict it is an item 
                    elif word in category:
                        detail_flag = True
                        if detail_counter == 6:
                            logData(inventory, details, prev_word, category_name)
                        prev_word = word
                        detail_counter = 0
                        category[word] = True

                    elif detail_counter > 5:
                        detail_flag = False

                    # Each item has 6 details that need to be saved
                    elif detail_flag and detail_counter < 6:
                        details[detail_counter] = word
                        detail_counter += 1

                    # The date will always be the 6th word on the first page 
                    elif page_no == 0 and word_count == 6:
                        try:
                            word = word.split(' \xad ')[0]
                            m, d, y = word.split('/')
                            date = ('-').join([y, m, d])
                        except:
                            pass

                    word = ''
                    space_counter = 0

    return date, inventory


# Extracts all weather data from a csv and returns json
def getWeatherData(path):

    data = pd.read_csv(path)
    full_info = {}
    day = data['0']
    temp = data['1']

    for i in range(100):
        full_info[day[i]] = temp[i]

    return full_info


# save data to file
def saveToFile(data, num):
    with open(f'data/data{num}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# Merges Data from pdfs and weather data into variable data
def mergeData(weather_data: dict, store_data: dict, date: str):
    try:
        store_data['AvgTempC'] = weather_data[date]
        print(weather_data[date])
    except KeyError:
        print(f'Date {date} has no weather data')
        store_data['AvgTempC'] = None
    
    data[date] = store_data


if __name__ == "__main__":
    # extract data from all data files and save it into one large JSON file
    weather_data = getWeatherData(weather_data_path)

    NUMBER_OF_FILES = 3

    for i in range(NUMBER_OF_FILES):
        file_no = i + 1
        store_data_file = f'StoreReports-{file_no}.pdf'
        # date, week_data = extrator(store_data_path + store_data_file)
        date, week_data = extrator(store_data_file)

        mergeData(weather_data, week_data, date)
        print(f'Added data {i}')

    print('Extraction Complete')

    saveToFile(data, 'FULL')
    print('Program Exocuted')

