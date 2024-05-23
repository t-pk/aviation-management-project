import json
from django.utils import timezone
import random


# Hàm định dạng datetime với offset UTC
def format_datetime_with_utc_offset(dt):
    rounded_minute = int(((dt.minute + 7.5) // 15) * 15)
    if rounded_minute >= 60:
        dt += timezone.timedelta(hours=1)
        rounded_minute = 0
    formatted_date = dt.strftime("%Y-%m-%d %H:") + "{:02d}".format(rounded_minute) + ":00 +0000"
    return formatted_date


# Đường dẫn đến file JSON chứa dữ liệu về sân bay
input_file_path = "./aviation/fixtures/0002_Airport.json"

# Đọc dữ liệu về sân bay từ file JSON
with open(input_file_path, "r", encoding="utf-8", errors="ignore") as json_file:
    original_data = json.load(json_file)

# Ngày hiện tại với offset UTC
current_date_utc = timezone.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
transformed_data = []

# Lặp qua từng sân bay
for obj in original_data:
    start_date = current_date_utc - timezone.timedelta(days=7)
    end_date = current_date_utc + timezone.timedelta(days=14)

    # Lặp qua từng ngày trong khoảng thời gian
    while start_date < end_date:
        number_of_flight = random.randint(1, 3)
        arrivals = [item for item in original_data if item["pk"] != obj["pk"]]

        # Lặp qua từng sân bay đến
        for airport in arrivals:
            i = 0
            departure_time_min = 0.5

            # Tạo số lượng chuyến bay ngẫu nhiên từ sân bay hiện tại đến sân bay đến
            while i < number_of_flight:
                i += 1
                departure_time_min += random.randint((i % 3) + 1, 4)
                random_hours_arrival = departure_time_min + random.uniform(1, 1.5)

                if random_hours_arrival >= 24:
                    random_hours_arrival -= 24
                random_minute = random.choice([0, 15, 30, 45])
                departure_time = start_date.replace(
                    hour=int(departure_time_min),
                    minute=random_minute,
                    second=0,
                    microsecond=0,
                )
                arrival_time = start_date + timezone.timedelta(
                    hours=random_hours_arrival, minutes=random.choice([0, 15, 30, 45])
                )

                transformed_item = {
                    "model": "aviation.flight",
                    "pk": len(transformed_data) + 1,
                    "fields": {
                        "departure_airport": obj["pk"],
                        "arrival_airport": airport["pk"],
                        "departure_time": format_datetime_with_utc_offset(departure_time),
                        "arrival_time": format_datetime_with_utc_offset(arrival_time),
                        "aircraft_id": random.randint(1, 90),
                    },
                }
                transformed_data.append(transformed_item)

        start_date += timezone.timedelta(days=1)

# Lưu dữ liệu về chuyến bay vào file JSON
output_file_path = "./aviation/fixtures/0004_Flight.json"
with open(output_file_path, "w") as json_file:
    json.dump(transformed_data, json_file, indent=2)

print(f"Transformed data saved to {output_file_path}")
