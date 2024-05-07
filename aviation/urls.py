from django.urls import path
from .views import BookingView

urlpatterns = [
    path("get_booking_information/", BookingView.as_view(), name="get_booking_information"),
]
