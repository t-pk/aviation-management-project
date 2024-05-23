from typing import Union
from django.contrib import admin
import logging
from django.utils import timezone
from aviation.forms import BookingForm, FlightForm
from .models import Airport, Flight, Aircraft, Booking, Passenger
from django.db.models import Count

logger = logging.getLogger(__name__)


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    """
    Lớp admin cho Flight.
    """

    form = FlightForm

    list_display: list[str] = [
        "id",
        "departure_airport",
        "arrival_airport",
        "departure_time",
        "arrival_time",
        "aircraft_code",
        "duration_time",
        "capacity",
        "avaiable_seat",
        "total_passenger",
    ]
    search_fields: list[str] = ["id", "aircraft__code"]
    date_hierarchy: str = "departure_time"

    list_filter: list[str] = ["departure_airport", "arrival_airport", "departure_time", "arrival_time"]
    list_per_page: int = 20

    def total_passenger(self, obj: Flight) -> int:
        """
        Tính tổng số hành khách đã đặt chỗ.
        Input:
            obj (Flight): flight.
        Output:
            int: Tổng số hành khách.
        """
        return obj.booking_set.aggregate(total_passengers=Count("passengers"))["total_passengers"]

    def avaiable_seat(self, obj: Flight) -> int:
        """
        Tính số ghế còn trống.
        Input:
            obj (Flight): chuyến bay.
        Output:
            int: Số ghế còn trống.
        """
        return (
            obj.aircraft.capacity - obj.booking_set.aggregate(total_passengers=Count("passengers"))["total_passengers"]
        )

    def capacity(self, obj: Flight) -> int:
        """
        Lấy sức chứa của máy bay.
        Input:
            obj (Flight): chuyến bay.
        Output:
            int: Sức chứa của máy bay.
        """
        return obj.aircraft.capacity

    @staticmethod
    def aircraft_code(obj: Flight) -> str:
        """
        Lấy mã của máy bay.
        Input:
            obj (Flight): chuyến bay.
        Output:
            str: Mã máy bay.
        """
        return obj.aircraft.code

    @staticmethod
    def duration_time(obj: Flight) -> timezone.timedelta:
        """
        Tính thời gian của chuyến bay.
        Input:
            obj (Flight): chuyến bay.
        Output:
            timezone.timedelta: Thời gian.
        """
        duration = obj.arrival_time - obj.departure_time
        return duration

    aircraft_code.short_description = "Aircraft Code"
    duration_time.short_description = "Duration"
    total_passenger.short_description = "Total Passenger Booked"

    def has_change_permission(self, request, obj: Union[Flight, None] = None) -> bool:
        """
        Xác định người dùng có quyền thay đổi chuyến bay hay không.
        Input:
            request (HttpRequest): request.
            obj (Union[Flight, None]): chuyến bay (nếu có).
        Output:
            bool: True/False.
        """
        logger.debug(
            f"has_change_permission request {request} obj {obj} user {request.user} is supper user {request.user.is_superuser}"
        )

        if obj and (obj.departure_time <= timezone.now() or obj.arrival_time <= timezone.now()):
            if request.user and request.user.is_superuser:
                return super().has_change_permission(request, obj)
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj: Union[Flight, None] = None) -> bool:
        """
        Xác định người dùng có quyền xóa chuyến bay hay không.
        Input:
            request (HttpRequest): request.
            obj (Union[Flight, None]): chuyến bay (nếu có).
        Output:
            bool: True/False.
        """
        logger.debug(f"request {request} obj {obj} user {request.user} is supper user {request.user.is_superuser}")

        if obj and (obj.departure_time <= timezone.now() or obj.arrival_time <= timezone.now()):
            if request.user and request.user.is_superuser:
                return super().has_delete_permission(request, obj)
            return False
        return super().has_delete_permission(request, obj)


@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    """
    Lớp admin cho Aircraft.
    """

    list_display: list[str] = ["id", "model", "code", "capacity"]
    search_fields: list[str] = ["id", "model", "code", "capacity"]
    list_filter: list[str] = ["model"]
    list_per_page: int = 20


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    """
    Lớp admin cho Airport.
    """

    list_display: list[str] = ["id", "code", "city", "name", "latitude", "longitude"]
    search_fields: list[str] = ["id", "code", "city", "name"]
    list_filter: list[str] = ["code", "city"]
    list_per_page: int = 20


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    """
    Lớp admin cho Passenger.
    """

    list_display: list[str] = ["id", "name", "date_of_birth", "sex", "email", "phone"]
    search_fields: list[str] = ["name", "email", "phone"]
    list_per_page: int = 20


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Lớp admin cho Booking.
    """

    form = BookingForm
    filter_horizontal = ["passengers"]
    search_fields = ["id", "passengers__name"]
    list_display: list[str] = (
        "id",
        "departure_airport",
        "arrival_airport",
        "aircraft_code",
        "departure_time",
        "arrival_time",
        "passenger_names",
        "quantity",
        "total_fare_with_vnd",
        "booking_date",
    )
    list_filter: list[str] = [
        "flight__departure_time",
        "flight__departure_airport",
        "flight__arrival_airport",
        "flight__aircraft__code",
    ]

    def get_queryset(self, request):
        """
        queryset danh sách booking.
        Input:
            request (HttpRequest): request.
        Output:
            QuerySet: booking.
        """
        queryset = super().get_queryset(request)
        return queryset.prefetch_related("passengers")

    date_hierarchy: str = "flight__departure_time"

    list_per_page: int = 20

    @staticmethod
    def departure_airport(obj: Booking) -> Airport:
        """
        sân bay khởi hành.
        Input:
            obj (Booking): booking.
        Output:
            Airport: Sân bay khởi hành.
        """
        return obj.flight.departure_airport

    @staticmethod
    def arrival_airport(obj: Booking) -> Airport:
        """
        sân bay đến.
        Input:
            obj (Booking): booking.
        Output:
            Airport: Sân bay đến.
        """
        return obj.flight.arrival_airport

    @staticmethod
    def passenger_names(obj: Booking) -> str:
        """
        ds tên của hành khách.
        Input:
            obj (Booking): booking.
        Output:
            str: ds tên hành khách.
        """
        return ", ".join([passenger.name for passenger in obj.passengers.all()])

    @staticmethod
    def aircraft_code(obj: Booking) -> str:
        """
        mã của máy bay.
        Input:
            obj (Booking): booking.
        Output:
            str: Mã máy bay.
        """
        return obj.flight.aircraft.code

    @staticmethod
    def departure_time(obj: Booking) -> str:
        """
        Lấy thời gian khởi hành của chuyến bay.
        Input:
            obj (Booking): booking.
        Output:
            str: Thời gian khởi hành.
        """
        departure_time = obj.flight.departure_time.astimezone()
        return departure_time.strftime("%Y-%m-%d %H:%M")

    @staticmethod
    def arrival_time(obj: Booking) -> str:
        """
        Lấy thời gian đến của chuyến bay.
        Input:
            obj (Booking): booking.
        Output:
            str: Thời gian đến.
        """
        arrival_time = obj.flight.arrival_time.astimezone()
        return arrival_time.strftime("%Y-%m-%d %H:%M")

    @staticmethod
    def quantity(obj: Booking) -> int:
        """
        số lượng hành khách.
        Input:
            obj (Booking): booking.
        Output:
            int: Số lượng hành khách.
        """
        return obj.passengers.count()

    @staticmethod
    def total_fare_with_vnd(obj: Booking) -> str:
        """
        Lấy tổng giá vé của booking (định dạng: VND).
        Input:
            obj (Booking): booking.
        Output:
            str: Tổng giá vé.
        """
        formatted_amount = "{:,.0f}".format(obj.total_fare)  # Định dạng với dấu phẩy cho phân cách hàng nghìn
        return f"{formatted_amount} VND"

    departure_airport.short_description = "Departure Airport"
    arrival_airport.short_description = "Arrival Airport"
    passenger_names.short_description = "Passenger Names"
    arrival_time.short_description = "Arrival Time"
    passenger_names.short_description = "Passenger Names"
    quantity.short_description = "Quantity"
    total_fare_with_vnd.short_description = "Total_fare"

    class Media:
        js = ("aviation/booking.js",)

    def has_change_permission(self, request, obj: Union[Booking, None] = None) -> bool:
        """
        Xác định người dùng có quyền thay đổi booking hay không.
        Input:
            request (HttpRequest): request hiện tại.
            obj (Union[Booking, None]): booking (nếu có).
        Output:
            bool: True/False.
        """
        logger.debug(
            f"has_change_permission request {request} obj {obj} user {request.user} is supper user {request.user.is_superuser}"
        )

        if obj and obj.flight and obj.flight.departure_time <= timezone.now():
            logger.debug(f"flight.departure_time = {obj.flight.departure_time} timezone.now() = {timezone.now()}")
            if request.user and request.user.is_superuser:
                return super().has_change_permission(request, obj)
            return False

        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj: Union[Booking, None] = None) -> bool:
        """
        Xác định người dùng có quyền xóa booking hay không.
        Input:
            request (HttpRequest): request hiện tại.
            obj (Union[Booking, None]): booking (nếu có).
        Output:
            bool: True/False.
        """
        logger.debug(
            f"has_delete_permission request {request} obj {obj} user {request.user} is supper user {request.user.is_superuser}"
        )

        if obj and obj.flight and obj.flight.departure_time <= timezone.now():
            logger.debug(f"flight.departure_time = {obj.flight.departure_time} timezone.now() = {timezone.now()}")
            if request.user and request.user.is_superuser:
                return super().has_delete_permission(request, obj)
            return False
        return super().has_delete_permission(request, obj)
