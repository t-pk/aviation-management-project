# views.py
import json
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from math import radians, sin, cos, sqrt, atan2
from aviation.models import Booking, Flight

class BookingView(APIView):
  permission_classes =[IsAuthenticated]
  def post(self, request, format=None):
    departure_airport = request.data['departure_airport']
    print("departure_airport: ", departure_airport)

    return JsonResponse
  
class BookingFlightView(APIView):
    permission_classes =[IsAuthenticated]
    def post(self, request, format=None):
        departure_time_str = request.data['departure_time']
        departure_date = datetime.strptime(departure_time_str, "%Y-%m-%d")
        # Get start and end of departure date
        start_datetime = departure_date.replace(hour=0, minute=0, second=0)
        end_datetime = departure_date.replace(hour=23, minute=59, second=59)

        matching_flights = Flight.objects.filter(
            departure_airport = request.data['departure_airport'],
            arrival_airport = request.data['arrival_airport'],
            departure_time__range=(start_datetime, end_datetime)
        )

        # Construct JSON response data
        flights_data = []
        for flight in matching_flights:
            flight_data = {
                'id': flight.id,
                'departure_airport': flight.departure_airport,
                'arrival_airport': flight.arrival_airport,
                'departure_time': flight.departure_time.isoformat(),
                'arrival_time': flight.arrival_time.isoformat(),
                'aircraft_model': flight.aircraft.model
            }
            flights_data.append(flight_data)

        # Return JSON response
        return JsonResponse({'flights': flights_data})
    
def get_booking_data(self, booking_id):
    try:
        booking = Booking.objects.get(pk=booking_id)
        print(booking)
        data = {
            'departure_airport': booking.flight.departure_airport,
            'arrival_airport': booking.flight.arrival_airport,
            'departure_time': booking.flight.departure_time.strftime('%Y-%m-%d'),
            'flight_id': booking.flight.id
        }
        return JsonResponse(data)
    except Booking.DoesNotExist:
        return JsonResponse({'error': 'Booking not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def calculate_distance(request):
    if request.method == 'GET':
        departure_code = request.GET.get('departure_code')
        arrival_code = request.GET.get('arrival_code')
        total_passenger = int(request.GET.get('total_passenger'))

        # Load airport data from JSON file
        with open('./mock/airports.json') as airports_file:
            airport_data = json.load(airports_file)

        # Retrieve departure and arrival airport coordinates from JSON data
        departure_airport = next((airport for airport in airport_data if airport['code'] == departure_code), None)
        arrival_airport = next((airport for airport in airport_data if airport['code'] == arrival_code), None)

        if departure_airport is None or arrival_airport is None:
            return JsonResponse({'error': 'Invalid airport code'}, status=400)

        departure_lat = float(departure_airport['latitude'])
        departure_lon = float(departure_airport['longitude'])
        arrival_lat = float(arrival_airport['latitude'])
        arrival_lon = float(arrival_airport['longitude'])

        # Calculate distance using Haversine formula
        distance = calculate_distance_between_points(departure_lat, departure_lon, arrival_lat, arrival_lon)

        return JsonResponse({'distance': distance, 'fare': distance * 3000, 'total_fare': total_passenger * distance * 3000 })

    return JsonResponse({'error': 'Invalid request'}, status=400)

def calculate_distance_between_points(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
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
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = radius * c

    return round(distance)