import json
from django import forms
from django.db import models
from django.contrib import admin
from datetime import datetime


class Flight(models.Model):
    departure_airport = models.CharField(max_length=100)
    arrival_airport = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    aircraft = models.ForeignKey("Aircraft", on_delete=models.CASCADE)
    class Meta:
        db_table = "aviation_flight"
    def __str__(self):
        return f"{self.aircraft.model} | {self.departure_time.time().strftime("%H:%M")} -> {self.arrival_time.time().strftime("%H:%M")}"

class FlightAdmin(admin.ModelAdmin):
    list_display = ['id', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'aircraft_model', 'duration_time']
    search_fields =  ['id', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'aircraft_id']
    list_filter = ['id', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'aircraft_id']

    def aircraft_model(self, obj):
        return obj.aircraft.model if obj.aircraft else ''  # Assuming model is a field in the Aircraft model

    def duration_time(self, obj):
        if obj.departure_time and obj.arrival_time:
            duration = obj.arrival_time - obj.departure_time
            return duration
        else:
            return None

class Aircraft(models.Model):
    model = models.CharField(max_length=100)
    capacity = models.IntegerField()
    class Meta:
        db_table = "aviation_aircraft"

class AircraftAdmin(admin.ModelAdmin):
    list_display = ['id', 'model', 'capacity']
    search_fields = ['id', 'model', 'capacity']
    list_filter = ['model', 'capacity']


class Passenger(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    class Meta:
        db_table = "aviation_passenger"
    def __str__(self):
        return f"{self.name} ({self.phone})"

class PassengerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone']
    search_fields =  ['id', 'name', 'email', 'phone']
    list_filter = ['name', 'email', 'phone']

class Booking(models.Model):
    flight = models.ForeignKey("Flight", on_delete=models.CASCADE)
    passengers = models.ManyToManyField(Passenger)
    booking_date = models.DateField()
    seat_number = models.CharField(max_length=10)
    class Meta:
        db_table = "aviation_booking"


class BookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        flights = Flight.objects.all()[:10]
        self.fields['flight'].queryset = flights
    
    # Load airport data from JSON file
    with open('./mock/airports.json') as airports_file:
        airport_data = json.load(airports_file)

    # Extract airport codes and names
    airport_choices = [(airport['code'], f"{airport['code']} - {airport['name']}") for airport in airport_data]

    # Set choices for departure and arrival fields
    departure = forms.ChoiceField(label="Departure", choices=airport_choices)
    arrival = forms.ChoiceField(label="Arrival", choices=airport_choices)
    departure_time = forms.DateField(label="Departure Date", widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Booking
        # exclude = ['flight']
        fields = ['departure', 'arrival', 'departure_time','flight', 'passengers', 'seat_number']

class BookingAdmin(admin.ModelAdmin):

    # exclude= ['flight']
    form = BookingForm
    filter_horizontal = ['passengers']
    class Media:
        js=("aviation/booking.js",)


class PaymentInformation(models.Model):
    item_description = models.CharField(max_length=100, default='Snack')  # Set default value to 'Snack'
    booking = models.OneToOneField("Booking", on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        db_table = "aviation_payment_information"


class ItemInformation(models.Model):
    item_description = models.CharField(max_length=100, default='Snack')  # Set default value to 'Snack'
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        db_table = "aviation_item_information"


class CarryOnItem(models.Model):
    item_description = models.CharField(max_length=100, default='Snack')  # Set default value to 'Snack'
    item = models.ForeignKey("ItemInformation", on_delete=models.CASCADE)
    flight = models.ForeignKey("Flight", on_delete=models.CASCADE)
    passenger = models.ForeignKey("Passenger", on_delete=models.CASCADE)
    item_quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        db_table = "aviation_carry_on_item"
