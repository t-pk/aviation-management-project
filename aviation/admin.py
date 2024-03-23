from django.contrib import admin

from .models import Flight, Aircraft, Booking, Passenger, PaymentInformation,  ItemInformation, CarryOnItem, AircraftAdmin, PassengerAdmin, FlightAdmin

admin.site.register(Flight, FlightAdmin)
admin.site.register(Aircraft, AircraftAdmin)
admin.site.register(Booking)
admin.site.register(Passenger, PassengerAdmin)
admin.site.register(PaymentInformation)
admin.site.register(ItemInformation)
admin.site.register(CarryOnItem)

