# views.py
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

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

