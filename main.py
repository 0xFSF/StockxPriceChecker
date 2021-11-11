import os
from openpyxl import Workbook
from selenium import webdriver
import pandas as pd
from prices import Prices


def data():
    # Loads data from txt
    with open('data.txt', 'r') as file:
        txt = file.readlines()
    a = txt[0]
    b = txt[1]
    c = float(txt[2].replace("\n", ''))
    d = int(txt[3].replace("\n", ''))
    e = txt[4].replace("\n", '')
    f = txt[5].replace("\n", '')
    return [a, b, c, d, e, f]


def shoes(emai, passw, gbp, name, dat, driv, last_mont, current_mont):
    # Gets all needed data from sites
    df = pd.DataFrame(columns=['Product_name', 'SKU', 'Sizes', 'Quantity'])
    excel = pd.read_excel('shoes.xlsx', sheet_name=name)

    # Based on each row in excel sheet
    t = 0
    for index, row in excel.iterrows():
        sku = row['sku']
        value = row['price']

        prices = Prices(driv, sku, emai, passw, t, gbp, value, dat, last_mont, current_mont)
        stockx = prices.stockx()
        item_name = stockx[0]
        sizes = stockx[1]

        counter = sizes.count(",")
        counter += 1

        new_row = {'Product_name': item_name, 'SKU': sku, 'Sizes': sizes, 'Quantity': counter}
        df = df.append(new_row, ignore_index=True)
        print('\n' + item_name)
        print(sku)
        print(sizes)

        t += 1

    return df


print('data.txt:\n'
      '1. Put stockx email\n'
      '2. Put stockx password\n'
      '3. Put GBP exchange rate with "." format\n'
      '4. Put current date (if day <8 add to 30 or 31 based on last month)\n'
      '5. Put last month\n'
      '6. Put current month\n'
      '\n'
      'shoes.xlsx:\n'
      '1. Put sku\n'
      "2. Put discounted price\n"
      '\n'
      'Write anything if you want to start\n')
input()

try:
    os.remove("worth.xlsx")
except FileNotFoundError:
    pass
wb = Workbook()
wb.save(filename='worth.xlsx')
data = data()
email = data[0]
password = data[1]
kurs_gbp = data[2]
date = data[3]
last_month = data[4]
current_month = data[5]
sheets = pd.ExcelFile('shoes.xlsx').sheet_names
driver = webdriver.Chrome("C:/Users/dratw/Documents/Projekty/priceCompare/chromedriver.exe")
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source":
        "const newProto = navigator.__proto__;"
        "delete newProto.webdriver;"
        "navigator.__proto__ = newProto;"
})

# Based on each sheet in excel file
for i in range(len(pd.ExcelFile('shoes.xlsx').sheet_names)):
    stock = shoes(email, password, kurs_gbp, i, date, driver, last_month, current_month)
    with pd.ExcelWriter('worth.xlsx', engine='openpyxl', mode='a') as writer:
        stock.to_excel(writer, sheet_name=sheets[i])

writer.save()
writer.close()
