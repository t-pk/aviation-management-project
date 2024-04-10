from datetime import datetime
import logging
from django import forms
from django.utils import timezone
from .models import Airport, Booking, Flight

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
        booking_instance = kwargs.pop("instance", None)

        airports = Airport.objects.all()

        airport_choices = [(airport.pk, f"{airport.code} - {airport.name}") for airport in airports]
        self.fields["departure"].choices = airport_choices
        self.fields["arrival"].choices = airport_choices

        if booking_instance and self.data.get("departure") is None:
            booking_instance.departure = booking_instance.flight.departure_airport
            booking_instance.arrival = booking_instance.flight.arrival_airport

            flight_instance = booking_instance.flight
            departure_instance = flight_instance.departure_airport
            arrival_instance = flight_instance.arrival_airport
            departure_time_instance = flight_instance.departure_time
            self.initial["flight"] = flight_instance.pk
            passenger_count = booking_instance.passengers.count()
            self.initial["quantity"] = passenger_count
            self.initial["departure"] = departure_instance.pk
            self.initial["arrival"] = arrival_instance.pk
            self.initial["departure_time"] = departure_time_instance
        else:
            departure_instance = self.data.get("departure", airport_choices[0][0])
            arrival_instance = self.data.get("arrival", airport_choices[1][0])
            departure_time_instance = self.data.get("departure_time", timezone.now())
            self.initial["departure"] = departure_instance
            self.initial["arrival"] = arrival_instance
            self.initial["departure_time"] = departure_time_instance

        current_datetime = timezone.now()
        logger.debug(
            f"booking_instance {booking_instance} current_datetime {current_datetime}, departure_time_instance = {departure_time_instance} departure_time_instance == current_datetime.date() {departure_time_instance == current_datetime.date()}"
        )
        if (
            departure_time_instance == current_datetime.date()
            or departure_time_instance.date() == current_datetime.date()
        ):
            start_datetime = departure_time_instance.replace(
                hour=departure_time_instance.hour,
                minute=departure_time_instance.minute,
                second=departure_time_instance.second,
            )
            logger.debug(f"start_datetime = {start_datetime}")
        else:
            if type(departure_time_instance) is str:
                departure_time_instance = datetime.strptime(departure_time_instance, "%Y-%m-%d")

            start_datetime = departure_time_instance.replace(hour=0, minute=0, second=0)
        end_datetime = departure_time_instance.replace(hour=23, minute=59, second=59)

        matching_flights = Flight.objects.filter(
            departure_airport=departure_instance,
            arrival_airport=arrival_instance,
            departure_time__range=(start_datetime, end_datetime),
        )

        self.fields["flight"].queryset = matching_flights

    def clean(self):
        cleaned_data = super().clean()
        booking_instance = self.instance
        passengers = cleaned_data.get("passengers")
        quantity = cleaned_data.get("quantity")
        flight = self.data.get("flight")
        passengers_selected = quantity or 0
        if "flight" not in cleaned_data or cleaned_data["flight"] is None:
            if flight:
                try:
                    flight = Flight.objects.get(pk=flight)
                    cleaned_data["flight"] = flight
                    errors = self.errors
                    if "flight" in errors:
                        errors.pop("flight")
                except Flight.DoesNotExist:
                    pass

        if passengers and passengers.count() != quantity:
            self.add_error(
                "passengers",
                forms.ValidationError("Please check the Quantity field."),
            )

        if passengers and flight:
            passenger_count = 0
            if booking_instance and booking_instance.id:
                booked_passenger = Booking.objects.get(id=booking_instance.id)
                passenger_count = booked_passenger.passengers.count()  # exists booked current on DB.
            available_seats = self.get_available_seats(flight) + passenger_count
            logger.debug(
                f"Class name: {self.__class__.__name__} func name {self.save.__name__} available_seats = {available_seats}, passengers_selected = {passengers_selected} passenger_count = {passenger_count}"
            )

            if passengers_selected > available_seats:
                raise forms.ValidationError(f"Only {available_seats - passenger_count} seats available on this flight.")

        return cleaned_data

    def get_available_seats(self, flight):
        logger.debug(f"flight information {flight}")
        if type(flight) is str:
            bookings = Booking.objects.filter(flight_id=flight)
            flight = Flight.objects.get(pk=flight)
        else:
            bookings = Booking.objects.filter(flight_id=flight.id)
        total_booked_seats = sum(booking.passengers.count() for booking in bookings)

        try:
            available_seats = flight.aircraft.capacity - total_booked_seats
        except Flight.DoesNotExist:
            available_seats = 0

        return available_seats


class FlightForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        departure_airport = cleaned_data.get("departure_airport")
        arrival_airport = cleaned_data.get("arrival_airport")
        logger.info(f"departure_airport {departure_airport} arrival_airport {arrival_airport}")

        if departure_airport == arrival_airport:
            raise forms.ValidationError("Departure and Arrival airports cannot be the same.")

        return cleaned_data
