import logging
from django.http import HttpRequest, JsonResponse
from django.views import View
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Airport, Flight
from aviation.utils import calculate_fare, get_end_datetime, get_start_datetime

logger = logging.getLogger(__name__)


class BookingView(View):
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest):
        """
        lấy thông tin đặt chỗ.
        Input:
            request (HttpRequest): các tham số 'departure', 'arrival', 'departure_time', và 'quantity'.
        Output:
            JsonResponse: thông tin giá vé và danh sách các chuyến bay phù hợp.
        """
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Unauthorized"}, status=401)

        departure = request.GET.get("departure")
        arrival = request.GET.get("arrival")
        departure_time = request.GET.get("departure_time")
        quantity = request.GET.get("quantity")

        logger.debug(f"API get-booking-information query: {str(request.GET)}")

        departure_date = timezone.make_aware(timezone.datetime.strptime(departure_time, "%Y-%m-%d"))
        current_datetime = timezone.now().astimezone()
        departure_date = departure_date.replace(
            hour=current_datetime.hour, minute=current_datetime.minute, second=current_datetime.second
        )

        if departure_date.date() == current_datetime.date():
            start_datetime = departure_date
        else:
            start_datetime = get_start_datetime(departure_date)

        end_datetime = get_end_datetime(departure_date)

        matching_flights = Flight.objects.filter(
            departure_airport=departure,
            arrival_airport=arrival,
            departure_time__range=(start_datetime, end_datetime),
        )

        serialized_flights = [{"pk": flight.pk, "__str__": str(flight)} for flight in matching_flights]
        departure_airport = Airport.objects.get(pk=departure)
        arrival_airport = Airport.objects.get(pk=arrival)
        logger.debug(f"departure_airport: {departure_airport} {arrival_airport}")

        fare_information = calculate_fare(departure_airport, arrival_airport, quantity)
        fare_information.update({"flights": serialized_flights})

        return JsonResponse(fare_information, safe=False)
