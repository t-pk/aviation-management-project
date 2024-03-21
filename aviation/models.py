from django.db import models

class Flight(models.Model):
    departure_airport = models.CharField(max_length=100)
    arrival_airport = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    aircraft = models.ForeignKey("Aircraft", on_delete=models.CASCADE)
    class Meta:
        db_table = "aviation_flight"


class Aircraft(models.Model):
    model = models.CharField(max_length=100)
    capacity = models.IntegerField()
    class Meta:
        db_table = "aviation_aircraft"


class Passenger(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    class Meta:
        db_table = "aviation_passenger"

class Booking(models.Model):
    flight = models.ForeignKey("Flight", on_delete=models.CASCADE)
    passenger = models.ForeignKey("Passenger", on_delete=models.CASCADE)
    booking_date = models.DateField()
    seat_number = models.CharField(max_length=10)
    class Meta:
        db_table = "aviation_booking"


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


class CarryOnItems(models.Model):
    item_description = models.CharField(max_length=100, default='Snack')  # Set default value to 'Snack'
    item = models.ForeignKey("ItemInformation", on_delete=models.CASCADE)
    flight = models.ForeignKey("Flight", on_delete=models.CASCADE)
    passenger = models.ForeignKey("Passenger", on_delete=models.CASCADE)
    item_quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        db_table = "aviation_carry_on_items"
