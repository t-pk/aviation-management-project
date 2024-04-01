
import json
from django import forms
from django.db import models
from django.contrib import admin
from django.utils import timezone
from datetime import timedelta, datetime
from django.core.exceptions import ValidationError


class Flight(models.Model):
    departure_airport = models.CharField(max_length=100)
    arrival_airport = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    aircraft = models.ForeignKey("Aircraft", on_delete=models.CASCADE)
    class Meta:
        db_table = "aviation_flight"
    def __str__(self):
        return f"{self.aircraft.code} | {self.departure_time.time().strftime("%H:%M")} | {self.arrival_time.time().strftime("%H:%M")}"

class FlightAdmin(admin.ModelAdmin):
    list_display = ['id', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'aircraft_code', 'duration_time']
    search_fields =  ['id', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'aircraft_id']
    list_filter = ['id', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'aircraft_id']

    def aircraft_code(self, obj):
        return obj.aircraft.code if obj.aircraft else ''  # Assuming code is a field in the Aircraft model

    def duration_time(self, obj):
        if obj.departure_time and obj.arrival_time:
            duration = obj.arrival_time - obj.departure_time
            return duration
        else:
            return None

class Aircraft(models.Model):
    model = models.CharField(max_length=100)
    capacity = models.IntegerField()
    code = models.CharField(max_length=100)
    class Meta:
        db_table = "aviation_aircraft"

class AircraftAdmin(admin.ModelAdmin):
    list_display = ['id', 'model', 'code','capacity']
    search_fields = ['id', 'model', 'code' ,'capacity']
    list_filter = ['code', 'capacity']


class Passenger(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    citizen_identify_id = models.CharField(max_length=15, null=True, blank=True)
    relation= models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

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
    booking_date = models.DateField(default=timezone.now)
    total_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)  # Set default value to 0

    class Meta:
        db_table = "aviation_booking"

class BookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['flight'] = forms.ModelChoiceField(queryset=Flight.objects.all())
        self.fields['total_amount'].widget = forms.TextInput(attrs={'readonly': 'readonly'})

    # Load airport data from JSON file
    with open('./mock/airports.json') as airports_file:
        airport_data = json.load(airports_file)

    # Extract airport codes and names
    airport_choices = [(airport['code'], f"{airport['code']} - {airport['name']}") for airport in airport_data]

    # Set choices for departure and arrival fields
    departure = forms.ChoiceField(label="Departure", choices=airport_choices)
    arrival = forms.ChoiceField(label="Arrival", choices=airport_choices)
    departure_time = forms.DateField(
        label="Departure Date", 
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=timezone.now().date()
    )
    total_amount = forms.DecimalField(label="Total Amount", required=False, initial=0)
    total_passenger = forms.IntegerField(label="Total Passenger",initial=0, min_value=1)

    class Meta:
        model = Booking
        fields = ['departure', 'arrival', 'departure_time', 'flight','total_passenger', 'passengers', 'total_amount']

    def clean(self):
        cleaned_data = super().clean()
        passengers = cleaned_data.get('passengers')
        total_passenger = cleaned_data.get('total_passenger')
        print("cleaned_data.get('total_passenger')", cleaned_data.get('flight'))
        if passengers and passengers.count() != total_passenger:
            self.add_error('passengers', ValidationError("please check Total Passenger fields ."))

        return cleaned_data

class BookingAdmin(admin.ModelAdmin):

    # exclude= ['flight']
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
        js=("aviation/booking.js",)
