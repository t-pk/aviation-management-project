from django.urls import path
from .views import *
urlpatterns = [
    path('departure/',BookingView.as_view()),
    path('flights/',BookingFlightView.as_view()),
    path('bookings/<int:booking_id>/', get_booking_data, name='get_booking_data'),
    path('calculate-distance/', calculate_distance, name='calculate_distance'),
]