from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MaxLengthValidator,
    MinLengthValidator,
    EmailValidator,
)
from django.db.models import Count


def validate_date_of_birth(value: timezone.datetime):
    """
    Hàm kiểm tra ngày sinh.
    Input:
        value (timezone.datetime): Ngày sinh.
    Raises:
        ValidationError: ngày sinh > hiện tại.
    """
    if value > timezone.datetime.now().astimezone().date():
        raise ValidationError("Date of birth cannot be in the future")


class Airport(models.Model):
    """
    Class sân bay.
    Thuộc tính:
        id (AutoField): Khóa chính tự tăng.
        code (CharField): Mã sân bay, duy nhất.
        city (CharField): Thành phố của sân bay, duy nhất.
        name (CharField): Tên của sân bay.
        latitude (FloatField): Vĩ độ của sân bay.
        longitude (FloatField): Kinh độ của sân bay.
    """

    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True, validators=[MinLengthValidator(3), MaxLengthValidator(10)])
    city = models.CharField(max_length=100, unique=True, validators=[MinLengthValidator(4), MaxLengthValidator(100)])
    name = models.CharField(max_length=200, validators=[MinLengthValidator(4), MaxLengthValidator(200)])
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        db_table = "aviation_airport"

    def __str__(self):
        return f"{self.code} - {self.name} ({self.city})"


class Aircraft(models.Model):
    """
    Class máy bay.
    Thuộc tính:
        id (AutoField): Khóa chính tự tăng.
        model (CharField): Mô hình của máy bay.
        capacity (IntegerField): Sức chứa của máy bay.
        code (CharField): Mã của máy bay.
    """

    id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=100, validators=[MinLengthValidator(4), MaxLengthValidator(100)])
    capacity = models.IntegerField(validators=[MinValueValidator(100), MaxValueValidator(1000)])
    code = models.CharField(max_length=8, validators=[MinLengthValidator(3), MaxLengthValidator(8)])

    class Meta:
        db_table = "aviation_aircraft"

    def __str__(self):
        return f"{self.code} ({self.model})"


class Flight(models.Model):
    """
    Class chuyến bay.
    Thuộc tính:
        id (AutoField): Khóa chính tự tăng.
        departure_airport (ForeignKey): Sân bay khởi hành.
        arrival_airport (ForeignKey): Sân bay đến.
        departure_time (DateTimeField): Thời gian khởi hành.
        arrival_time (DateTimeField): Thời gian đến.
        aircraft (ForeignKey): Máy bay của chuyến bay.
    """

    id = models.AutoField(primary_key=True)
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)

    class Meta:
        db_table = "aviation_flight"

    def __str__(self):
        num_booked_passengers = self.booking_set.aggregate(num_booked_passengers=Count("passengers"))[
            "num_booked_passengers"
        ]
        available_seats = self.aircraft.capacity - num_booked_passengers
        return f"{self.aircraft.code} | {self.departure_time.astimezone().time().strftime('%H:%M')} | {self.arrival_time.astimezone().time().strftime('%H:%M')} | {available_seats} (avail seats)"


class Passenger(models.Model):
    """
    Class hành khách.
    Thuộc tính:
        id (AutoField): Khóa chính tự tăng.
        name (CharField): Tên của hành khách.
        date_of_birth (DateField): Ngày sinh của hành khách.
        sex (CharField): Giới tính của hành khách.
        email (EmailField): Email của hành khách.
        phone (CharField): Số điện thoại của hành khách.
        citizen_identify_id (CharField): Số chứng minh nhân dân của hành khách.
        relation (ForeignKey): Mối quan hệ với hành khách khác (nếu có).
    """

    id = models.AutoField(primary_key=True)

    class Sex(models.TextChoices):
        MALE = "M", "Nam"
        FEMALE = "F", "Nữ"
        OTHER = "O", "Khác"

    name = models.CharField(max_length=100, validators=[MinLengthValidator(6), MaxLengthValidator(100)])
    date_of_birth = models.DateField(null=False, validators=[validate_date_of_birth])
    sex = models.CharField(max_length=1, choices=Sex.choices, null=False)
    email = models.EmailField(null=True, blank=True, validators=[EmailValidator()])
    phone = models.CharField(max_length=20, null=True, blank=True, validators=[MaxLengthValidator(20)])
    citizen_identify_id = models.CharField(max_length=15, null=True, blank=True, validators=[MaxLengthValidator(15)])
    relation = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "aviation_passenger"

    def __str__(self):
        return f"{self.name} ({self.phone})"


class Booking(models.Model):
    """
    Class đặt chỗ.
    Thuộc tính:
        id (AutoField): Khóa chính tự tăng.
        flight (ForeignKey): Chuyến bay của đơn đặt chỗ.
        passengers (ManyToManyField): Danh sách hành khách.
        booking_date (DateTimeField): Ngày đặt chỗ.
        total_fare (DecimalField): Tổng giá vé.
    """

    id = models.AutoField(primary_key=True)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    passengers = models.ManyToManyField(Passenger)
    booking_date = models.DateTimeField(default=timezone.now)
    total_fare = models.DecimalField(default=0, max_digits=12, decimal_places=0, validators=[MinValueValidator(0)])

    class Meta:
        db_table = "aviation_booking"

    def __str__(self):
        return f"{self.id}"
