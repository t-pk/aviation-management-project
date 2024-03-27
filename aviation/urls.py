from django.urls import path
from .views import *
urlpatterns = [
    path('departure/',BookingView.as_view()),
    path('flights/',BookingFlightView.as_view()),
]