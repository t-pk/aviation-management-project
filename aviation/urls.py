from django.urls import path
from .views import BookingFlightView, RetrieveBookingView, CalculateFaresView

urlpatterns = [
    path("flights/", BookingFlightView.as_view(), name="flights"),
    path("fares/", CalculateFaresView.as_view(), name="calculate_fares"),
    path(
        "bookings/<int:booking_id>/",
        RetrieveBookingView.as_view(),
        name="get_booking_data",
    ),
]
