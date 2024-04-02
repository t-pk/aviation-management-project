from django.contrib import admin
from django.contrib import admin
from datetime import timedelta

from aviation.forms import BookingForm

from .models import Flight, Aircraft, Booking, Passenger

class FlightAdmin(admin.ModelAdmin):
    list_display = ['id', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'aircraft_code', 'duration_time']
    search_fields = ['id', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'aircraft_id', 'duration_time']
    list_filter = ['departure_airport', 'arrival_airport']

    def aircraft_code(self, obj):
        return obj.aircraft.code if obj.aircraft else ''

    def duration_time(self, obj):
        if obj.departure_time and obj.arrival_time:
            duration = obj.arrival_time - obj.departure_time
            return duration
        else:
            return None

class AircraftAdmin(admin.ModelAdmin):
    list_display = ['id', 'model', 'code', 'capacity']
    search_fields = ['id', 'model', 'code', 'capacity']
    list_filter = ['code', 'capacity']

class PassengerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone']
    search_fields = ['id', 'name', 'email', 'phone']
    list_filter = ['name', 'email', 'phone']

class BookingAdmin(admin.ModelAdmin):
    form = BookingForm
    filter_horizontal = ['passengers']
    list_display = ('id', 'get_departure_airport', 'get_arrival_airport', 'get_departure_time', 'get_arrival_time', 'get_passenger_names', 'booking_date')

    def get_departure_airport(self, obj):
        return obj.flight.departure_airport

    def get_arrival_airport(self, obj):
        return obj.flight.arrival_airport

    def get_passenger_names(self, obj):
        return ", ".join([passenger.name for passenger in obj.passengers.all()])

    def get_departure_time(self, obj):
        departure_time = obj.flight.departure_time + timedelta(hours=7)
        return departure_time.strftime('%Y-%m-%d %H:%M')

    def get_arrival_time(self, obj):
        arrival_time = obj.flight.arrival_time + timedelta(hours=7)
        return arrival_time.strftime('%Y-%m-%d %H:%M')

    get_departure_airport.short_description = 'Departure Airport'
    get_arrival_airport.short_description = 'Arrival Airport'
    get_passenger_names.short_description = 'Passenger Names'
    get_arrival_time.short_description = 'Arrival Time'
    get_passenger_names.short_description = 'Passenger Names'

    class Media:
        js = ("aviation/booking.js",)

admin.site.register(Flight, FlightAdmin)
admin.site.register(Aircraft, AircraftAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Passenger, PassengerAdmin)
