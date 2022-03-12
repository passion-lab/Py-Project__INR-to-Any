# Practical Problem 9 - Currency Converter
# Current Updates: USD -> any currency
# Upcoming Updates: any currency -> any currency

from bs4 import BeautifulSoup
from requests import get
from time import sleep, time
from datetime import datetime
from textwrap import fill
from shutil import get_terminal_size


update = False
print("Retrieving updated data from the X-RATES server ...", end="")

try:
    url = "https://www.x-rates.com/table/?from=INR&amount=1"
    status = get(url).status_code
    html = get(url).text
    data = []

    table = BeautifulSoup(html, 'html.parser').find_all('table')[1].find_all('tr')[1:]
    for item in table:
        data += item.get_text().split("\n\n")

    print("\rData retrieved successfully!")

    data = [item.split("\n")[1:-1] for item in data]
    data_v1 = ""
    for item in data:
        data_v1 += ",".join(item) + "\n"

    print("Updating the database ...", end="")
    sleep(1)

    with open("./currencyData.csv", "w") as file:
        file.write("_TIMESTAMP_," + str(datetime.now()) + "\n" + data_v1)

    print("\rDatabase updated!")
    update = True
except:
    print("\rDatabase not updated! Network can't be reached right now.")


with open("./currencyData.csv", "rt") as file:
    update_date = file.readline().strip("\n").split(",")
    file.seek(0)
    currency_data = file.read().split("\n")[1:-1]

if update is False:
    print(f"Working with last updated data ...\n[Last Updated: {update_date[1]}]\n\n")

country = ""
for index, item in enumerate(currency_data):
    country += f"[{index + 1}] {item.split(',')[0]};  "

# display available countries
print("{}".format(fill(text=country, width=get_terminal_size().columns - 2)))

print("\nConvert currency from Indian Rupees (INR) _________________________")
# 2. convert to?
while True:
    convert_to = input(" _To: ").strip()
    if convert_to.isdigit():
        convert_to = int(convert_to)
        if 0 < convert_to <= len(currency_data):
            break
        else:
            print("Option is out of range! Try again.")
            continue
    else:
        print("Not a valid input! Please type only available number corresponding to each country.")
        continue

# for which value?
while True:
    convert_val = input(f" _Enter value in {currency_data[convert_to - 1].split(',')[0]}: ").strip()
    if convert_val.isdigit():
        convert_val = float(convert_val)
        break
    else:
        print("Not a valid input! Please type only available number corresponding to each country.")
        continue

# conversion process=
convert_country = currency_data[convert_to - 1].split(',')[0]
convert_figure = float(currency_data[convert_to - 1].split(',')[1])

print(f"\n > {convert_val} Indian Rupees = {convert_figure * convert_val} {convert_country}")
# print(f" > {convert_val} {convert_country} = {convert_figure / convert_val} Indian Rupees.\n")

print("___\n-Thanks to X-RATES (www.x-rates.com) for providing database info!")
