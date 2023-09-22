import csv
import json
import math
from collections import Counter

def main():

# 1. Считать из csv-файла количество остановок, вывести улицу, на которой больше всего остановок.
    try:
        with open('bus_stops.csv', encoding='windows-1251') as file_bus_stops:
                fields_string = file_bus_stops.readline()
                fields_string = file_bus_stops.readline()
                fields_list = fields_string.split(';')
                reader = csv.DictReader(file_bus_stops, fields_list, delimiter=';')
                bus_stop_list = [row for row in reader]
                street_list = [street['Описание места расположения объекта'].strip().split(',')[0] for street in bus_stop_list]
                print(f"Всего {len(bus_stop_list)} автобусных остановок. Больше всего остановок на ул. {Counter(street_list).most_common(1)[0][0]}")
    except FileNotFoundError:
        print('ОШИБКА: ФАЙЛА НЕТ В ДИРЕКТОРИИ')
    except (ValueError, IndexError) as error:
        print('ОШИБКА:', error)


#2. Определить, на каких станциях московского метро сейчас идёт ремонт эскалаторов и вывести на экран их названия.
    try:
        with open('subway_stops.json', encoding='windows-1251') as file_subway_stops:
            subway_stop_list = json.load(file_subway_stops)
            subway_stops_being_repaired = [stop['Name'] for stop in subway_stop_list if stop['RepairOfEscalators']]
            print(f"Ремонт эскалаторов на станциях: {'; '.join(subway_stops_being_repaired)}")
    except FileNotFoundError:
        print('ОШИБКА: ФАЙЛА НЕТ В ДИРЕКТОРИИ')
    except UnboundLocalError:
        print('ОШИБКА ПРИ ССЫЛАНИИ НА ОБЪЕКТ. ПРОВЕРИТЬ НАЛИЧИЕ ФАЙЛА В ДИРЕКТОРИИ.')
    except (ValueError, IndexError) as error:
        print('ОШИБКА:', error)


#3. Объединить наборы данных из предыдущих задач и посчитать, у какой станции метро больше всего остановок (в радиусе 0.5 км).
    try:
        subway_stop_with_most_bus_stops_name = ''
        max_bus_stop_amount = 0

        for subway_stop in subway_stop_list:
            subway_stop_latitude = float(subway_stop['Latitude_WGS84'])
            subway_stop_longitude = float(subway_stop['Longitude_WGS84'])
            bus_stop_counter = 0

            for bus_stop in bus_stop_list:
                bus_stop_latitude = float(bus_stop['Широта в WGS-84'])
                bus_stop_longitude = float(bus_stop['Долгота в WGS-84'])

                if abs(subway_stop_latitude - bus_stop_latitude) < 0.0045 and abs(subway_stop_longitude - bus_stop_longitude) < 0.008:
                    latitude_difference = subway_stop_latitude - bus_stop_latitude
                    longitude_difference = subway_stop_longitude - bus_stop_longitude
                    distance = math.hypot(latitude_difference * 111.19, longitude_difference * 62.66)

                    if distance <= 0.5:
                        bus_stop_counter += 1

                if bus_stop_counter > max_bus_stop_amount:
                    max_bus_stop_amount = bus_stop_counter
                    subway_stop_with_most_bus_stops_name = subway_stop['Name']

        print(f"Станция метро, вокруг которой больше всего остановок в радиусе 0,5 км - {subway_stop_with_most_bus_stops_name}")

    except UnboundLocalError:
        print('ОШИБКА ПРИ ССЫЛАНИИ НА ОБЪЕКТ. ПРОВЕРИТЬ НАЛИЧИЕ ФАЙЛА В ДИРЕКТОРИИ.')
    except (ValueError, IndexError) as error:
        print('ОШИБКА:', error)


if __name__ == '__main__':
    main()
