from django.db import models
from django.utils import timezone

class Flight(models.Model):
    departure_airport = models.CharField(max_length=100)
    arrival_airport = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    aircraft = models.ForeignKey("Aircraft", on_delete=models.CASCADE)

    class Meta:
        db_table = "aviation_flight"

    def __str__(self):
        return f"{self.aircraft.code} | {self.departure_time.time().strftime('%H:%M')} | {self.arrival_time.time().strftime('%H:%M')}"

class Aircraft(models.Model):
    model = models.CharField(max_length=100)
    capacity = models.IntegerField()
    code = models.CharField(max_length=100)

    class Meta:
        db_table = "aviation_aircraft"


class Passenger(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    citizen_identify_id = models.CharField(max_length=15, null=True, blank=True)
    relation = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "aviation_passenger"

    def __str__(self):
        return f"{self.name} ({self.phone})"


class Booking(models.Model):
    flight = models.ForeignKey("Flight", on_delete=models.CASCADE)
    passengers = models.ManyToManyField(Passenger)
    booking_date = models.DateField(default=timezone.now)
    total_amount = models.DecimalField(default=0, max_digits=12, decimal_places=0)

    class Meta:
        db_table = "aviation_booking"
