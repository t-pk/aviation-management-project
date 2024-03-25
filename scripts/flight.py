import json
from datetime import datetime, timedelta, timezone
import random

current_date = datetime.now()
current_date_utc = current_date.astimezone(timezone.utc)

def format_datetime_with_utc_offset(dt):
    # Round the minutes to the nearest 15-minute interval
    rounded_minute = int(((dt.minute + 7.5) // 15) * 15)
    
    # Ensure that rounded_minute does not exceed 59
    if rounded_minute >= 60:
        dt += timedelta(hours=1)  # Add 1 hour
        rounded_minute = 0
    
    # Construct the formatted string with UTC offset
    formatted_date = dt.strftime('%Y-%m-%d %H:') + '{:02d}'.format(rounded_minute) + ':00 +0000'
    
    return formatted_date
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
        random_hours = random.uniform(0.5, 3)
        arrival_time = current_date_utc + timedelta(hours=random_hours)
        transformed_item = {
            "model": "aviation.flight",
            "pk": id,
            "fields": {
                "departure_airport": item["code"], 
                "arrival_airport":  airport["code"],
                "departure_time": format_datetime_with_utc_offset(current_date_utc),
                "arrival_time": format_datetime_with_utc_offset(arrival_time),
                "aircraft_id":  random.randint(1, 10),
            }
        }
        transformed_data.append(transformed_item)

# Save transformed data to a JSON file
output_file_path = "./aviation/fixtures/0003_Flight.json"
with open(output_file_path, "w") as json_file:
    json.dump(transformed_data, json_file, indent=2)

print(f"Transformed data saved to {output_file_path}")
