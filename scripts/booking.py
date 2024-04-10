import json
from datetime import datetime, timedelta
import random
from math import radians, sin, cos, sqrt, atan2


def calculate_distance_between_points(lat1, lon1, lat2, lon2):
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # Radius of the Earth in kilometers
    radius = 6371.0

    # Calculate the change in coordinates
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Calculate the Haversine distance
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = radius * c
    return round(distance)


# Load passenger data from JSON
passenger_path = "./aviation/fixtures/0003_Passenger.json"
with open(passenger_path, "r") as json_file:
    passenger_data = json.load(json_file)

# Load flight data from JSON
flight_path = "./aviation/fixtures/0004_Flight.json"
with open(flight_path, "r") as json_file:
    flight_data = json.load(json_file)

airport_path = "./mock/airports.json"
with open(airport_path, "r") as json_file:
    airport_data = json.load(json_file)


def find_airport_by_code(code):
    for airport in airport_data:
        if airport["code"] == code:
            return airport
    return None


for flight in flight_data:
    departure_code = flight["fields"]["departure_airport"]
    arrival_code = flight["fields"]["arrival_airport"]
    departure_airport = find_airport_by_code(departure_code)
    arrival_airport = find_airport_by_code(arrival_code)

    if departure_airport and arrival_airport:
        departure_lat = departure_airport["latitude"]
        departure_lon = departure_airport["longitude"]
        arrival_lat = arrival_airport["latitude"]
        arrival_lon = arrival_airport["longitude"]

        distance = calculate_distance_between_points(departure_lat, departure_lon, arrival_lat, arrival_lon)
        # Calculate the 1 fare
        fare = distance * 3000
        flight["fields"]["fare"] = fare


transformed_data = []


# Function to generate random booking data
def generate_booking_data(flight, passengers, booking_date, total_fare):
    return {
        "model": "aviation.booking",
        "pk": flight["pk"],
        "fields": {
            "flight": flight["pk"],
            "passengers": passengers,
            "booking_date": booking_date,
            "total_fare": total_fare,
        },
    }


# # Function to find return flights
# def find_return_flights(arrival_airport, departure_time):
#     return_flights = []
#     for flight in flight_data:
#         if flight["fields"]["departure_airport"] == arrival_airport:
#             # Calculate the arrival date of the return flight (2 to 5 days after departure)
#             departure_time = datetime.strptime(flight["fields"]["departure_time"].split()[0], "%Y-%m-%d")
#             arrival_date = departure_time + timedelta(days=random.randint(2, 5))
#             return_flights.append({
#                 "flight": flight["pk"],
#                 "arrival_date": arrival_date.strftime("%Y-%m-%d")
#             })
#     return return_flights

# Iterate over each flight
for flight in flight_data:
    # Randomly select number of passengers for each flight (between 1 and 5)
    num_passengers = random.randint(3, 5)

    # Randomly assign passengers to the flight
    passengers = random.sample(range(1, len(passenger_data) + 1), num_passengers)

    # If passenger has relation_id (passenger id), include it in the passengers list
    passengers_with_ids = []
    for passenger_id in passengers:
        for passenger in passenger_data:
            if passenger["pk"] == passenger_id:
                passengers_with_ids.append(passenger_id)
                break

    # Generate booking date (current date)
    booking_date = datetime.now().strftime("%Y-%m-%d")
    total_fare = flight["fields"]["fare"] * len(passengers_with_ids)
    # Generate booking data for the flight
    booking_data = generate_booking_data(flight, passengers_with_ids, booking_date, total_fare)
    transformed_data.append(booking_data)
    # print(booking_data)  # Output the generated booking data

    # # Find return flights for the current flight
    # return_flights = find_return_flights(flight["fields"]["arrival_airport"], flight["fields"]["departure_time"])


# Save transformed data to JSON file
output_file_path = "./aviation/fixtures/0005_Booking.json"
with open(output_file_path, "w") as json_file:
    json.dump(transformed_data, json_file, indent=2)

print(f"Transformed data saved to {output_file_path}")
