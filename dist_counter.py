import requests
import csv
from haversine import haversine, Unit


def get_object(object_name):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": object_name,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        print('No object')
        return None
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]

    toponym_coodrinates = toponym["Point"]["pos"]
    return list(map(float, toponym_coodrinates.split()))[::-1]


def get_dist(pos1, pos2):
    return haversine(pos1, pos2)


res = []
with open('to_pars_info_inp.csv', encoding='utf-8') as f:
    data = csv.DictReader(f, delimiter=',', quotechar='"')
    for i, row in enumerate(data):
        try:
            object_cords = get_object(f"улица {row['street']} {row['house_number']}")
        except Exception as er:
            res.append(res.append([row['floor'], row['floors_count'], row['rooms_count'], row['total_meters'], row['price'], row['district'], row['street'], row['house_number'], row['underground'], -1, -1]))
            continue
        #print(object_cords)
        try:
            dist_to_centre = get_dist(object_cords, (55.753544, 37.621202))
            dist_to_underground = get_dist(object_cords, get_object(f"Метро {row['underground']}"))
        except Exception as er:
            res.append(res.append([row['floor'], row['floors_count'], row['rooms_count'], row['total_meters'], row['price'], row['district'], row['street'], row['house_number'], row['underground'], -1, -1]))
            continue
        #print(dist_to_underground, dist_to_centre)
        #print((row['floor'], row['floors_count'], row['rooms_count'], row['total_meters'], row['price'], row['district'], row['street'], row['house_number'], row['underground'], dist_to_centre, dist_to_underground))
        print(i)
        res.append([row['floor'], row['floors_count'], row['rooms_count'], row['total_meters'], row['price'], row['district'], row['street'], row['house_number'], row['underground'], dist_to_centre, dist_to_underground])

print(*res, sep='\n')
with open('to_pars_info.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(
        csvfile, delimiter=',', quotechar='"',
        quoting=csv.QUOTE_MINIMAL,)
    writer.writerow(['', 'floor', 'floors_count', 'rooms_count', 'total_meters', 'price', 'district', 'street', 'house_number', 'underground'])
    for row in res:
        try:
            writer.writerow(row)
        except Exception as e:
            print(row, e)
