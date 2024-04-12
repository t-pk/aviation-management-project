from datetime import datetime
import logging
from django.http import HttpRequest, JsonResponse
from django.views import View
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Airport, Flight
from aviation.utils import calculate_fare

logger = logging.getLogger(__name__)


class BookingView(View):
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        # Retrieve specific parameters from the GET request
        departure = request.GET.get("departure")
        arrival = request.GET.get("arrival")
        departure_time = request.GET.get("departure_time")
        quantity = request.GET.get("quantity")

        logger.debug(f"API get-booking-information query: {str(request.GET)}")

        departure_date = datetime.strptime(departure_time, "%Y-%m-%d")

        current_datetime = timezone.now()
        if departure_date.date() == current_datetime.date():
            start_datetime = departure_date.replace(
                hour=current_datetime.hour, minute=current_datetime.minute, second=current_datetime.second
            )
        else:
            start_datetime = departure_date.replace(hour=0, minute=0, second=0)

        end_datetime = departure_date.replace(hour=23, minute=59, second=59)

        matching_flights = Flight.objects.filter(
            departure_airport=departure,
            arrival_airport=arrival,
            departure_time__range=(start_datetime, end_datetime),
        )

        # Serialize flights to JSON
        serialized_flights = [{"pk": flight.pk, "__str__": str(flight)} for flight in matching_flights]
        departure_airport = Airport.objects.get(pk=departure)
        arrival_airport = Airport.objects.get(pk=arrival)
        logger.debug(f"departure_airport: {departure_airport} {arrival_airport}")

        fare_information = calculate_fare(departure_airport, arrival_airport, quantity)
        fare_information.update({"flights": serialized_flights})

        return JsonResponse(fare_information, safe=False)
