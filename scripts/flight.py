import json
from datetime import datetime, timedelta, timezone
import random

current_date = datetime.now()
current_date_utc = current_date.astimezone(timezone.utc)
date_after_7_days = current_date_utc + timedelta(days=7)
id = 0
# Read original data from JSON file
input_file_path = "./mock/airports.json"
with open(input_file_path, "r") as json_file:
    original_data = json.load(json_file)

# Transform data into desired format
transformed_data = []
for idx, item in enumerate(original_data):
    for index, airport in enumerate(original_data):
        if(idx == index): continue
        # departure_time = 
        id+=1
        current_minute = date_after_7_days.minute
        rounded_minute = int(((current_minute + 7.5) // 15) * 15)  # Round to the nearest 15 minutes
        formatted_date = date_after_7_days.strftime('%Y-%m-%d %H:') + '{:02d}'.format(rounded_minute) + ':00 +0000'
        transformed_item = {
            "model": "aviation.flight",
            "pk": id,
            "fields": {
                "departure_airport": item["code"], 
                "arrival_airport":  airport["code"],
                "departure_time": formatted_date,
                "arrival_time": formatted_date,
                "aircraft_id":  random.randint(1, 10),
            }
        }
        transformed_data.append(transformed_item)

# Save transformed data to a JSON file
output_file_path = "./aviation/fixtures/0003_Flight.json"
with open(output_file_path, "w") as json_file:
    json.dump(transformed_data, json_file, indent=2)

print(f"Transformed data saved to {output_file_path}")
