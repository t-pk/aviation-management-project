from django import forms
from typing import Union, Dict
from django.http import HttpRequest
from django.utils.timezone import datetime
from django.db.models.query import QuerySet
from aviation.models import Airport, Booking, Flight
import logging
from django.utils import timezone

from aviation.utils import adjust_datetime, get_end_datetime, get_start_datetime

logger = logging.getLogger(__name__)

class BookingForm(forms.ModelForm):
    departure = forms.ChoiceField(
        label="Departure",
        widget=forms.Select(attrs={"onchange": "get_booking_information(this.id);"}),
    )

    arrival = forms.ChoiceField(
        label="Arrival",
        widget=forms.Select(attrs={"onchange": "get_booking_information(this.id);"}),
    )

    departure_time = forms.DateField(
        label="Departure Time",
        widget=forms.DateInput(
            attrs={"type": "date", "onchange": "get_booking_information(this.id);", "min": timezone.now().date()}
        ),
        initial=timezone.now().date(),
    )

    quantity = forms.IntegerField(
        label="Quantity",
        initial=0,
        min_value=1,
        widget=forms.NumberInput(attrs={"oninput": "get_booking_information();"}),
    )

    total_fare = forms.DecimalField(
        label="Total Fare",
        required=True,
        initial=0,
        min_value=0,
        widget=forms.NumberInput(attrs={"readonly": "readonly"}),
    )

    class Meta:
        model = Booking
        fields = [
            "departure",
            "arrival",
            "departure_time",
            "flight",
            "quantity",
            "passengers",
            "total_fare",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        booking_instance: Union[None, Booking] = kwargs.pop("instance", None)

        airports: QuerySet[Airport] = Airport.objects.all()

        airport_choices: list[tuple[int, str]] = [(airport.pk, f"{airport.code} - {airport.name}") for airport in airports]
        self.fields["departure"].choices = airport_choices
        self.fields["arrival"].choices = airport_choices
        current_datetime: datetime = timezone.now()

        if booking_instance and self.data.get("departure") is None:
            if self.initial == {}:
                booking_instance.departure = booking_instance.flight.departure_airport
                booking_instance.arrival = booking_instance.flight.arrival_airport
                return

            flight_instance: Flight = booking_instance.flight
            departure_instance: Airport = flight_instance.departure_airport
            arrival_instance: Airport = flight_instance.arrival_airport
            departure_time_instance: datetime = flight_instance.departure_time
            self.initial.update(
                {
                    "flight": flight_instance.pk,
                    "quantity": booking_instance.passengers.count(),
                    "departure": departure_instance.pk,
                    "arrival": arrival_instance.pk,
                    "departure_time": departure_time_instance,
                }
            )
        else:
            departure_instance: Union[int, str] = self.data.get("departure", airport_choices[0][0])
            arrival_instance: Union[int, str] = self.data.get("arrival", airport_choices[1][0])
            departure_time_instance: Union[datetime, str] = self.data.get("departure_time", current_datetime)
            self.initial.update(
                {
                    "departure": departure_instance,
                    "arrival": arrival_instance,
                    "departure_time": departure_time_instance,
                }
            )

        if isinstance(departure_time_instance, str):
            departure_time_instance = timezone.datetime.strptime(departure_time_instance, "%Y-%m-%d")

        logger.debug(
            f"Departure Time: {departure_time_instance.date()}, "
            f"Current Date: {current_datetime.date()}, "
            f"Same Date Check: {departure_time_instance.date() == current_datetime.date()}"
        )

        start_datetime: datetime = (
            adjust_datetime(departure_time_instance)
            if departure_time_instance.date() == current_datetime.date()
            else get_start_datetime(departure_time_instance)
        )

        end_datetime: datetime = get_end_datetime(departure_time_instance)

        matching_flights: QuerySet[Flight] = Flight.objects.filter(
            departure_airport=departure_instance,
            arrival_airport=arrival_instance,
            departure_time__range=(start_datetime, end_datetime),
        )

        self.fields["flight"].queryset = matching_flights

    def clean(self) -> Dict[str, Union[str, int]]:
        cleaned_data: Dict[str, Union[str, int]] = super().clean()
        booking_instance: Union[Booking, None] = self.instance
        passengers = cleaned_data.get("passengers")
        quantity: int = cleaned_data.get("quantity")
        flight: Union[str, None] = self.data.get("flight")

        passengers_selected: int = quantity or 0

        if not cleaned_data.get("flight"):
            if flight:
                if type(flight) is str:
                    cleaned_data["flight"] = Flight.objects.get(pk=flight)
                else:
                    cleaned_data["flight"] = Flight.objects.get(pk=flight.id)
                errors = self.errors
                errors.pop("flight", None)

        if passengers and passengers.count() != quantity:
            self.add_error(
                "passengers",
                forms.ValidationError(
                    f"Expected {quantity} passenger(s) based on the Quantity field, "
                    f"but found {passengers.count()} passenger(s)."
                ),
            )

        if passengers and flight:
            passenger_count: int = 0
            if booking_instance and booking_instance.id:
                booked_passenger: Booking = Booking.objects.get(id=booking_instance.id)
                passenger_count = booked_passenger.passengers.count()
            available_seats: int = self.get_available_seats(flight) + passenger_count

            if passengers_selected > available_seats:
                raise forms.ValidationError(f"Only {available_seats - passenger_count} seats available on this flight.")

        return cleaned_data

    def get_available_seats(self, flight: Union[str, Flight]) -> int:
        logger.debug(f"flight information {flight}")
        if type(flight) is str:
            bookings = Booking.objects.filter(flight_id=flight)
            flight = Flight.objects.get(pk=flight)
        else:
            bookings = Booking.objects.filter(flight_id=flight.id)
        total_booked_seats: int = sum(booking.passengers.count() for booking in bookings)
        available_seats: int = flight.aircraft.capacity - total_booked_seats if flight else 0
        return available_seats


class FlightForm(forms.ModelForm):
    request: Union[None, "HttpRequest"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def clean(self) -> Dict[str, Union[str, datetime]]:
        cleaned_data: Dict[str, Union[str, datetime]] = super().clean()
        departure_airport: Union[int, str] = cleaned_data.get("departure_airport")
        arrival_airport: Union[int, str] = cleaned_data.get("arrival_airport")
        logger.debug(f"departure_airport {departure_airport} arrival_airport {arrival_airport}")

        if departure_airport == arrival_airport:
            raise forms.ValidationError("Departure and Arrival airports cannot be the same.")

        return cleaned_data

    class Meta:
        model = Flight
        fields = [
            "departure_airport",
            "arrival_airport",
            "departure_time",
            "arrival_time",
            "aircraft",
        ]
