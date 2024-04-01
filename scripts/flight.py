import json
from datetime import datetime, timedelta, timezone
import random

# Function to format datetime with UTC offset
def format_datetime_with_utc_offset(dt):
    rounded_minute = int(((dt.minute + 7.5) // 15) * 15)
    if rounded_minute >= 60:
        dt += timedelta(hours=1)
        rounded_minute = 0
    formatted_date = dt.strftime('%Y-%m-%d %H:') + '{:02d}'.format(rounded_minute) + ':00 +0000'
    return formatted_date

# Load airports data
input_file_path = "./mock/airports.json"
with open(input_file_path, "r") as json_file:
    original_data = json.load(json_file)

# Current date in UTC
current_date_utc = datetime.now(timezone.utc)

# Start and end dates for generating flights
# start_date = current_date_utc - timedelta(days=10)  # 3 months before current date
# end_date = current_date_utc + timedelta(days=10)    # 3 months after current date

# Initialize list to store transformed data
transformed_data = []

# Generate flights for each day in the period
    
# start time of current date
start_date = current_date_utc.replace(hour=0, minute=0, second=0, microsecond=0)
end_date = start_date + timedelta(days=7)
    
while start_date < end_date:
    for obj in original_data:
        # random 8->10 flights for each day
        number_of_flight = random.randint(8,10)
        # random arrival_airports base on number of flight
        if number_of_flight > len(original_data):
            arrival_airports = [airport for airport in original_data if airport != obj]
        else:
            arrival_airports = random.sample([airport for airport in original_data if airport != obj], number_of_flight)
    
        for airport in arrival_airports:
            random_hours_departure = random.uniform(0, 24)  # Random departure hour between 0 and 24
            random_hours_arrival = random_hours_departure + random.uniform(0.5, 3)  # Random arrival hour after departure
        
            if random_hours_arrival >= 24:
                random_hours_arrival -= 24
            departure_time = start_date.replace(hour=int(random_hours_departure), minute=0, second=0, microsecond=0)
            arrival_time = start_date + timedelta(hours=random_hours_arrival)

            transformed_item = {
                "model": "aviation.flight",
                "pk": len(transformed_data) + 1,  # Generate unique primary key
                "fields": {
                    "departure_airport": obj["code"],
                    "arrival_airport":  airport["code"],
                    "departure_time": format_datetime_with_utc_offset(departure_time),
                    "arrival_time": format_datetime_with_utc_offset(arrival_time),
                    "aircraft_id":  random.randint(1, 50),
                }
            }
            transformed_data.append(transformed_item)
        
    start_date += timedelta(days=1)

# Save transformed data to JSON file
output_file_path = "./aviation/fixtures/0003_Flight.json"
with open(output_file_path, "w") as json_file:
    json.dump(transformed_data, json_file, indent=2)

print(f"Transformed data saved to {output_file_path}")
