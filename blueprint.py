from config.config import LOGGING_CONFIG, MKAD_CENTER, MKAD_RADIUS, YANDEX_API_KEY
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
import logging
import math
import requests

logging.basicConfig(**LOGGING_CONFIG)
mkad_blueprint = Blueprint("mkad", __name__)
API_HIT_COUNTER = 0
API_HIT_START_TIME = datetime.now()


def API_limit_checker() -> tuple[bool, str]:
    global API_HIT_COUNTER, API_HIT_START_TIME
    if datetime.now() - API_HIT_START_TIME > timedelta(days=1):
        API_HIT_COUNTER = 0
        API_HIT_START_TIME = datetime.now()
    if API_HIT_COUNTER >= 20000:
        return False, "API limit reached for the day"
    API_HIT_COUNTER += 1
    return True, ""


def get_coordinates(address: str, use_test_data=False) -> tuple:
    if use_test_data:
        return 55.7522, 37.6156
    base_url = 'https://geocode-maps.yandex.ru/1.x/'
    params = {
        "apikey": YANDEX_API_KEY,
        "geocode": address,
        "format": 'json'
    }
    response = requests.get(base_url, params=params)
    try:
        coords = response.json()[
            "response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
        lon, lat = map(float, coords.split())
        return lat, lon
    except (KeyError, IndexError, ValueError):
        logging.error(f"Failed to get coordinates for address: {address}")
        return None, None


def haversine_distance(point1: tuple, point2: tuple) -> float:
    lat1, lon1 = point1
    lat2, lon2 = point2
    R = 6371.0  # Radius of the Earth in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2)**2 + math.cos(math.radians(lat1))
         * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


def is_inside_mkad(lat: float, lon: float) -> bool:
    distance_to_center = haversine_distance((lat, lon), MKAD_CENTER)
    return distance_to_center <= MKAD_RADIUS


@mkad_blueprint.route('/distance', methods=['POST'])
def get_distance():
    proceed, error_message = API_limit_checker()
    if not proceed:
        return jsonify({"error": error_message}), 429
    address = request.json.get("address")
    if not address:
        return jsonify({"error": "No address provided"}), 400
    lat, lon = get_coordinates(address)
    if lat is None or lon is None:
        logging.error(
            f"Could not retrieve valid coordinates for address: {address}")
        return jsonify({"error": "Could not retrieve valid coordinates for the provided address."}), 500
    if is_inside_mkad(lat, lon):
        logging.info(f"The address '{address}' is inside the MKAD.")
        return jsonify({"message": "The address is inside the MKAD."}), 200
    else:
        distance_from_center = haversine_distance((lat, lon), MKAD_CENTER)
        distance_to_mkad = distance_from_center - MKAD_RADIUS
        logging.info(
            f"The address '{address}' is {distance_to_mkad:.2f} km away from the MKAD.")
        return jsonify({"message": f"The address is {distance_to_mkad:.2f} km away from the MKAD."}), 200
