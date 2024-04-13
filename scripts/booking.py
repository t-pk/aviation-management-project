import json
from django.utils import timezone
import random
from aviation.utils import calculate_distance_between_points

# Load passenger data from JSON
passenger_path = "./aviation/fixtures/0003_Passenger.json"
with open(passenger_path, "r") as json_file:
    passenger_data = json.load(json_file)

# Load flight data from JSON
flight_path = "./aviation/fixtures/0004_Flight.json"
with open(flight_path, "r") as json_file:
    flight_data = json.load(json_file)

airport_path = "./aviation/fixtures/0002_Airport.json"
with open(airport_path, "r") as json_file:
    airport_data = json.load(json_file)


def find_airport_by_code(pk):
    for airport in airport_data:
        if airport["pk"] == pk:
            return airport
    return None


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
        # Calculate the 1 fare
        fare = distance * 3000
        flight["fields"]["fare"] = fare


transformed_data = []


# Function to generate random booking data
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


# Iterate over each flight
i = 0
for flight in flight_data:
    # Randomly select number of bookings for each flight (between 5 and 10)
    num_bookings = random.randint(5, 20)

    for _ in range(num_bookings):
        i += 1
        # Randomly select number of passengers for each booking (between 1 and 5)
        num_passengers = random.randint(3, 5)

        # Randomly assign passengers to the booking
        passengers = random.sample(range(1, len(passenger_data) + 1), num_passengers)

        # If passenger has relation_id (passenger id), include it in the passengers list
        passengers_with_ids = []
        for passenger_id in passengers:
            for passenger in passenger_data:
                if passenger["pk"] == passenger_id:
                    passengers_with_ids.append(passenger_id)
                    break

        # Generate booking date (current date)
        current_datetime = timezone.datetime.now() - timezone.timedelta(weeks=random.randint(5, 16))
        booking_datetime = current_datetime.replace(
            hour=random.randint(0, 23), minute=random.randint(0, 59), second=random.randint(0, 59)
        )
        booking_date_str = booking_datetime.strftime("%Y-%m-%d %H:%M:%S")

        total_fare = flight["fields"]["fare"] * len(passengers_with_ids)
        # Generate booking data for the flight
        booking_data = generate_booking_data(flight, passengers_with_ids, booking_date_str, total_fare, i)
        transformed_data.append(booking_data)

# Save transformed data to JSON file
output_file_path = "./aviation/fixtures/0005_Booking.json"
with open(output_file_path, "w") as json_file:
    json.dump(transformed_data, json_file, indent=2)

print(f"Transformed data saved to {output_file_path}")
