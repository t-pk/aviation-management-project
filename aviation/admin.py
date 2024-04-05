from django.contrib import admin
from datetime import timedelta

from aviation.forms import BookingForm
from .models import Flight, Aircraft, Booking, Passenger


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "departure_airport",
        "arrival_airport",
        "departure_time",
        "arrival_time",
        "aircraft_code",
        "duration_time",
    ]
    search_fields = [
        "id",
        "departure_airport",
        "arrival_airport",
        "departure_time",
        "arrival_time",
        "aircraft_id",
        "duration_time",
    ]
    list_filter = ["departure_airport", "arrival_airport"]

    @staticmethod
    def aircraft_code(obj):
        return obj.aircraft.code if obj.aircraft else ""

    @staticmethod
    def duration_time(obj):
        if obj.departure_time and obj.arrival_time:
            duration = obj.arrival_time - obj.departure_time
            return duration
        else:
            return None

    aircraft_code.short_description = "Aircraft Code"
    duration_time.short_description = "Duration"


@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ["id", "model", "code", "capacity"]
    search_fields = ["id", "model", "code", "capacity"]
    list_filter = ["model"]


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "phone"]
    search_fields = ["id", "name", "email", "phone"]
    list_filter = ["name", "email", "phone"]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    form = BookingForm
    filter_horizontal = ["passengers"]
    list_display = (
        "id",
        "departure_airport",
        "arrival_airport",
        "departure_time",
        "arrival_time",
        "passenger_names",
        "total_passenger",
        "total_amount_with_vnd",
        "booking_date",
    )
    list_filter = ["flight__departure_airport", "flight__arrival_airport",  "flight__aircraft__code", "flight__departure_time"]

    @staticmethod
    def departure_airport(obj):
        return obj.flight.departure_airport

    @staticmethod
    def arrival_airport(obj):
        return obj.flight.arrival_airport

    @staticmethod
    def passenger_names(obj):
        return ", ".join([passenger.name for passenger in obj.passengers.all()])

    @staticmethod
    def departure_time(obj):
        departure_time = obj.flight.departure_time + timedelta(hours=7)
        return departure_time.strftime("%Y-%m-%d %H:%M")

    @staticmethod
    def arrival_time(obj):
        arrival_time = obj.flight.arrival_time + timedelta(hours=7)
        return arrival_time.strftime("%Y-%m-%d %H:%M")

    @staticmethod
    def total_passenger(obj):
        return obj.passengers.count()

    @staticmethod
    def total_amount_with_vnd(obj):
        formatted_amount = "{:,.0f}".format(obj.total_amount)  # Format with commas for thousands separators
        return f"{formatted_amount} VND"

    departure_airport.short_description = "Departure Airport"
    arrival_airport.short_description = "Arrival Airport"
    passenger_names.short_description = "Passenger Names"
    arrival_time.short_description = "Arrival Time"
    passenger_names.short_description = "Passenger Names"
    total_passenger.short_description = "Total Passenger"
    total_amount_with_vnd.short_description = "Total Amount"

    class Media:
        js = ("aviation/booking.js",)
