import json
import random
from django.utils import timezone
from aviation.utils import calculate_distance_between_points

# file JSON chứa dữ liệu về hành khách
passenger_path = "./aviation/fixtures/0003_Passenger.json"

# data hành khách từ file JSON
with open(passenger_path, "r", encoding="utf-8", errors="ignore") as json_file:
    passenger_data = json.load(json_file)

# file JSON chứa dữ liệu về chuyến bay
flight_path = "./aviation/fixtures/0004_Flight.json"

# data về chuyến bay từ file JSON
with open(flight_path, "r", encoding="utf-8", errors="ignore") as json_file:
    flight_data = json.load(json_file)

# file JSON chứa dữ liệu về sân bay
airport_path = "./aviation/fixtures/0002_Airport.json"

# data về sân bay từ file JSON
with open(airport_path, "r", encoding="utf-8", errors="ignore") as json_file:
    airport_data = json.load(json_file)


# Hàm tìm sân bay dựa trên mã
def find_airport_by_code(pk):
    for airport in airport_data:
        if airport["pk"] == pk:
            return airport
    return None


# Tính toán giá vé cho mỗi chuyến bay dựa trên khoảng cách giữa hai sân bay
for flight in flight_data:
    departure_code = flight["fields"]["departure_airport"]
    arrival_code = flight["fields"]["arrival_airport"]
    departure_airport = find_airport_by_code(departure_code)
    arrival_airport = find_airport_by_code(arrival_code)

    if departure_airport and arrival_airport:
        departure_lat = departure_airport["fields"]["latitude"]
        departure_lon = departure_airport["fields"]["longitude"]
        arrival_lat = arrival_airport["fields"]["latitude"]
        arrival_lon = arrival_airport["fields"]["longitude"]

        distance = calculate_distance_between_points(departure_lat, departure_lon, arrival_lat, arrival_lon)
        fare = distance * 3000  # Giả sử giá vé là 3000 VND/km
        flight["fields"]["fare"] = fare

# Tạo dữ liệu đặt vé cho mỗi chuyến bay
transformed_data = []


def generate_booking_data(flight, passengers, booking_date, total_fare, i):
    return {
        "model": "aviation.booking",
        "pk": i,
        "fields": {
            "flight": flight["pk"],
            "passengers": passengers,
            "booking_date": booking_date,
            "total_fare": total_fare,
        },
    }


i = 0
for flight in flight_data:
    num_bookings = random.randint(3, 10)

    for _ in range(num_bookings):
        i += 1
        num_passengers = random.randint(3, 9)

        # Chọn ngẫu nhiên một số hành khách từ dữ liệu hành khách
        passengers = random.sample(range(1, len(passenger_data) + 1), num_passengers)
        passengers_with_ids = []

        # Tìm hành khách có ID trong danh sách hành khách đã chọn
        for passenger_id in passengers:
            for passenger in passenger_data:
                if passenger["pk"] == passenger_id:
                    passengers_with_ids.append(passenger_id)
                    break

        # Tạo dữ liệu đặt vé cho mỗi chuyến bay và hành khách
        current_datetime = timezone.datetime.now().astimezone() - timezone.timedelta(weeks=random.randint(5, 16))
        booking_datetime = current_datetime.replace(
            hour=random.randint(0, 23), minute=random.randint(0, 59), second=random.randint(0, 59)
        )
        booking_date_str = booking_datetime.strftime("%Y-%m-%d %H:%M:%S %z")

        total_fare = flight["fields"]["fare"] * len(passengers_with_ids)
        booking_data = generate_booking_data(flight, passengers_with_ids, booking_date_str, total_fare, i)
        transformed_data.append(booking_data)

# Lưu dữ liệu đặt vé vào file JSON
output_file_path = "./aviation/fixtures/0005_Booking.json"
with open(output_file_path, "w") as json_file:
    json.dump(transformed_data, json_file, indent=2)

print(f"Transformed data saved to {output_file_path}")
