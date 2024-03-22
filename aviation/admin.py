from django.contrib import admin

from .models import Flight, Aircraft, Booking, Passenger, PaymentInformation,  ItemInformation, CarryOnItems

admin.site.register(Flight)
admin.site.register(Aircraft)
admin.site.register(Booking)
admin.site.register(Passenger)
admin.site.register(PaymentInformation)
admin.site.register(ItemInformation)
admin.site.register(CarryOnItems)

