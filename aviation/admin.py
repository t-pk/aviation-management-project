from django.contrib import admin

from .models import Flight, Aircraft, Booking, Passenger, PaymentInformation,  ItemInformation, CarryOnItem, AircraftAdmin, PassengerAdmin

admin.site.register(Flight)
admin.site.register(Aircraft, AircraftAdmin)
admin.site.register(Booking)
admin.site.register(Passenger, PassengerAdmin)
admin.site.register(PaymentInformation)
admin.site.register(ItemInformation)
admin.site.register(CarryOnItem)

