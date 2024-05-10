from django.utils.timezone import datetime
from math import radians, sin, cos, sqrt, atan2


def get_end_datetime(departure_time_instance: datetime):
    return departure_time_instance.replace(hour=23, minute=59, second=59)


def get_start_datetime(departure_time_instance: datetime):
    return departure_time_instance.replace(hour=0, minute=0, second=0)


def adjust_datetime(departure_time_instance: datetime):
    return departure_time_instance.replace(
        hour=departure_time_instance.hour, minute=departure_time_instance.minute, second=departure_time_instance.second
    )


def calculate_fare(departure_airport, arrival_airport, total_passenger):

    if departure_airport is None or arrival_airport is None:
        return {"error": "Invalid airport code"}

    departure_lat = float(departure_airport.latitude)
    departure_lon = float(departure_airport.longitude)
    arrival_lat = float(arrival_airport.latitude)
    arrival_lon = float(arrival_airport.longitude)

    distance = calculate_distance_between_points(departure_lat, departure_lon, arrival_lat, arrival_lon)

    fare = distance * 3000
    total_fare = int(total_passenger) * fare

    return {
        "distance": distance,
        "fare": fare,
        "total_fare": total_fare,
    }


def calculate_distance_between_points(lat1, lon1, lat2, lon2):
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    radius = 6371.0

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = radius * c
    return round(distance)
