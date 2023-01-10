import csv
import json

city = {}

with open('worldcities.csv', 'r', encoding='utf8') as file:
    data = csv.reader(file, delimiter=';')
    a = 1
    for i in data:
        city[i[1]] = {'latitude': i[2], 'longitude': i[3]}

with open('city_coordinates', 'w', encoding='UTF8') as json_file:
    json.dump(city, json_file, indent=4)


print('ok')
