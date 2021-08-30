import os
from dotenv import load_dotenv

import codecs
import json
import requests
import folium

from geopy import distance
from flask import Flask

NEAREST_COFFEE_SHOPS_COUNT = 5


def load_coffee_shops(filepath):
    with open(filepath, "r", encoding="CP1251") as file:
        file_content = file.read()
        coffee_shops = json.loads(file_content)
    return coffee_shops


def fetch_coordinates(apikey, place):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    params = {"geocode": place, "apikey": apikey, "format": "json"}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    found_places = response.json()["response"]["GeoObjectCollection"]["featureMember"]
    most_relevant = found_places[0]
    lon, lat = most_relevant["GeoObject"]["Point"]["pos"].split(" ")
    return lon, lat


def get_processed_coffee_shops(coffee_shops, coords):
    processed_coffee_shops = []
    for coffee_shop in coffee_shops:
        coffee_coordinates = (
            f"{coffee_shop['Latitude_WGS84']} {coffee_shop['Longitude_WGS84']}"
        )
        processed_coffee_shop = {
            "title": coffee_shop["Name"],
            "longitude": coffee_shop["Longitude_WGS84"],
            "latitude": coffee_shop["Latitude_WGS84"],
            "distance": distance.distance(coffee_coordinates, coords).km,
        }
        processed_coffee_shops.append(processed_coffee_shop)
    return processed_coffee_shops


def get_coffee_distance(processed_coffee_shops):
    return processed_coffee_shops["distance"]


def get_coffee_shops_map_with_marks(coords, dedicated_coffee_shops):
    coffee_shops_map = folium.Map(location=coords, zoom_start=15)
    folium.Marker(
        location=coords,
        popup="Вы находитесь здесь",
        icon=folium.Icon(icon="cloud", color="red"),
    ).add_to(coffee_shops_map)
    for coffee_shop in dedicated_coffee_shops:
        location_five_coffee_shops = (
            folium.Marker(
                location=(coffee_shop["latitude"], coffee_shop["longitude"]),
                popup=coffee_shop["title"],
                icon=folium.Icon(icon="cloud"),
            )
        ).add_to(coffee_shops_map)
    return coffee_shops_map


def create_coffee_shops_map():
    with codecs.open("coordinates.html",encoding='utf-8', mode='r') as file:
        return file.read()


if __name__ == "__main__":
    load_dotenv()
    YANDEX_APIKEY = os.getenv("YANDEX_API_KEY")
    place = input("Где вы находитесь? ")
    filepath = "coffee.json"
    coffee_shops = load_coffee_shops(filepath)
    lon, lat = fetch_coordinates(YANDEX_APIKEY, place)
    processed_coffee_shops = get_processed_coffee_shops(coffee_shops, (lat, lon))
    sorted_processed_coffee_shops = sorted(
        processed_coffee_shops, key=get_coffee_distance
    )
    nearest_coffee_shops = sorted_processed_coffee_shops[:NEAREST_COFFEE_SHOPS_COUNT]
    coffee_shops_map = get_coffee_shops_map_with_marks((lat, lon), nearest_coffee_shops)
    create_coffee_shops_map()
    coffee_shops_map.save("coordinates.html")
    app = Flask(__name__)
    app.add_url_rule("/", "my_coffee_shops_map", create_coffee_shops_map)
    app.run("0.0.0.0")
