from django.urls import path
from .views import *
urlpatterns = [
    path('flights/',BookingFlightView.as_view()),
    path('bookings/<int:booking_id>/', get_booking_data, name='get_booking_data'),
    path('calculate-distance/', calculate_distance, name='calculate_distance'),
]