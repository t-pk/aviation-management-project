from django.contrib import admin

from .models import Flight, Aircraft, Booking, Passenger,  AircraftAdmin, PassengerAdmin, FlightAdmin, BookingAdmin

admin.site.register(Flight, FlightAdmin)
admin.site.register(Aircraft, AircraftAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Passenger, PassengerAdmin)
