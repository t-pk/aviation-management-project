from django.utils.timezone import datetime
from math import radians, sin, cos, sqrt, atan2


def get_end_datetime(departure_time_instance: datetime):
    """
    Hàm trả về thời gian kết thúc của ngày cho một thời gian khởi hành cụ thể.
    Input:
        departure_time_instance (datetime): Thời gian khởi hành.
    Output:
        datetime: Thời gian kết thúc của ngày (23:59:59).
    """
    return departure_time_instance.replace(hour=23, minute=59, second=59)


def get_start_datetime(departure_time_instance: datetime):
    """
    Hàm trả về thời gian bắt đầu của ngày cho một thời gian khởi hành cụ thể.
    Input:
        departure_time_instance (datetime): Thời gian khởi hành.

    Output:
        datetime: Thời gian bắt đầu của ngày (00:00:00).
    """
    return departure_time_instance.replace(hour=0, minute=0, second=0)


def adjust_datetime(departure_time_instance: datetime):
    """
    Hàm điều chỉnh thời gian khởi hành giữ nguyên giờ, phút và giây.
    Input:
        departure_time_instance (datetime): Thời gian khởi hành.

    Output:
        datetime: Thời gian khởi hành được điều chỉnh.
    """
    return departure_time_instance.replace(
        hour=departure_time_instance.hour, minute=departure_time_instance.minute, second=departure_time_instance.second
    )


def calculate_fare(departure_airport, arrival_airport, total_passenger):
    """
    Hàm tính giá vé dựa trên khoảng cách giữa sân bay khởi hành và sân bay đến và số lượng hành khách.
    Input:
        departure_airport: Sân bay khởi hành.
        arrival_airport: Sân bay đến.
        total_passenger: Tổng số hành khách.

    Output:
        dict: Thông tin bao gồm khoảng cách, giá vé cho mỗi hành khách và tổng giá vé.
    """
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
    """
    Hàm tính khoảng cách giữa hai điểm dựa trên vĩ độ và kinh độ của chúng sử dụng công thức Haversine.
    Input:
        lat1: Vĩ độ điểm đầu.
        lon1: Kinh độ điểm đầu.
        lat2: Vĩ độ điểm cuối.
        lon2: Kinh độ điểm cuối.
    Output:
        float: Khoảng cách giữa hai điểm (km).
    """
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
