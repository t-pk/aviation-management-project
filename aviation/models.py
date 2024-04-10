from django.db import models
from django.utils import timezone
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MaxLengthValidator,
    MinLengthValidator,
    EmailValidator,
)
from django.db.models import Count


class Flight(models.Model):
    departure_airport = models.ForeignKey("Airport", on_delete=models.CASCADE, related_name="departures")
    arrival_airport = models.ForeignKey("Airport", on_delete=models.CASCADE, related_name="arrivals")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    aircraft = models.ForeignKey("Aircraft", on_delete=models.CASCADE)

    class Meta:
        db_table = "aviation_flight"

    def __str__(self):
        num_booked_passengers = self.booking_set.aggregate(num_booked_passengers=Count("passengers"))[
            "num_booked_passengers"
        ]
        available_seats = self.aircraft.capacity - num_booked_passengers
        return f"{self.aircraft.code} | {self.departure_time.time().strftime('%H:%M')} | {self.arrival_time.time().strftime('%H:%M')} | {available_seats} (avail seats)"


class Aircraft(models.Model):
    model = models.CharField(max_length=100, validators=[MinLengthValidator(4), MaxLengthValidator(100)])
    capacity = models.IntegerField(validators=[MinValueValidator(100), MaxValueValidator(1000)])
    code = models.CharField(max_length=8, validators=[MinLengthValidator(3), MaxLengthValidator(8)])

    class Meta:
        db_table = "aviation_aircraft"

    def __str__(self):
        return f"{self.code} ({self.model})"


class Airport(models.Model):
    code = models.CharField(max_length=10, unique=True, validators=[MinLengthValidator(4), MaxLengthValidator(10)])
    city = models.CharField(max_length=100, unique=True, validators=[MinLengthValidator(4), MaxLengthValidator(100)])
    name = models.CharField(max_length=200, validators=[MinLengthValidator(4), MaxLengthValidator(200)])
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.code} - {self.name} ({self.city})"


class Passenger(models.Model):
    name = models.CharField(max_length=100, validators=[MinLengthValidator(6), MaxLengthValidator(100)])
    email = models.EmailField(null=True, blank=True, validators=[EmailValidator()])
    phone = models.CharField(max_length=20, null=True, blank=True, validators=[MaxLengthValidator(20)])
    citizen_identify_id = models.CharField(max_length=15, null=True, blank=True, validators=[MaxLengthValidator(15)])
    relation = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "aviation_passenger"

    def __str__(self):
        return f"{self.name} ({self.phone})"


class Booking(models.Model):
    flight = models.ForeignKey("Flight", on_delete=models.CASCADE)
    passengers = models.ManyToManyField(Passenger)
    booking_date = models.DateField(default=timezone.now)
    total_fare = models.DecimalField(default=0, max_digits=12, decimal_places=0, validators=[MinValueValidator(0)])

    class Meta:
        db_table = "aviation_booking"

    def __str__(self):
        return f"{self.id}"
