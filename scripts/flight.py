import json
from datetime import datetime, timedelta, timezone
import random


# Function to format datetime with UTC offset
def format_datetime_with_utc_offset(dt):
    rounded_minute = int(((dt.minute + 7.5) // 15) * 15)
    if rounded_minute >= 60:
        dt += timedelta(hours=1)
        rounded_minute = 0
    formatted_date = dt.strftime("%Y-%m-%d %H:") + "{:02d}".format(rounded_minute) + ":00 +0000"
    return formatted_date


# Load airports data
input_file_path = "./mock/airports.json"
with open(input_file_path, "r") as json_file:
    original_data = json.load(json_file)

current_date_utc = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
transformed_data = []

# start time of current date
for obj in original_data:
    start_date = current_date_utc - timedelta(days=7)
    end_date = current_date_utc + timedelta(days=14)
    while start_date < end_date:
        number_of_flight = random.randint(1, 3)
        arrivals = [item for item in original_data if item["code"] != obj["code"]]
        for airport in arrivals:
            i = 0
            departure_time_min = 0.5
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
                arrival_time = start_date + timedelta(
                    hours=random_hours_arrival, minutes=random.choice([0, 15, 30, 45])
                )

                transformed_item = {
                    "model": "aviation.flight",
                    "pk": len(transformed_data) + 1,
                    "fields": {
                        "departure_airport": obj["code"],
                        "arrival_airport": airport["code"],
                        "departure_time": format_datetime_with_utc_offset(departure_time),
                        "arrival_time": format_datetime_with_utc_offset(arrival_time),
                        "aircraft_id": random.randint(1, 90),
                    },
                }
                transformed_data.append(transformed_item)

        start_date += timedelta(days=1)

# Save transformed data to JSON file
output_file_path = "./aviation/fixtures/0004_Flight.json"
with open(output_file_path, "w") as json_file:
    json.dump(transformed_data, json_file, indent=2)

print(f"Transformed data saved to {output_file_path}")
