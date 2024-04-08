import json
from django import forms
from django.utils import timezone
from .models import Booking, Flight


class BookingForm(forms.ModelForm):
    with open("./mock/airports.json") as airports_file:
        airport_data = json.load(airports_file)

    airport_choices = [
        (airport["code"], f"{airport['code']} - {airport['city']} - {airport['name']}") for airport in airport_data
    ]

    departure = forms.ChoiceField(
        label="Departure",
        choices=airport_choices,
        widget=forms.Select(attrs={"onchange": "get_booking_information();"}),
    )
    arrival = forms.ChoiceField(
        label="Arrival",
        choices=airport_choices,
        initial=airport_choices[1][0],
        widget=forms.Select(attrs={"onchange": "get_booking_information();"}),
    )

    departure_time = forms.DateField(
        label="Departure Time",
        widget=forms.DateInput(attrs={"type": "date", "onchange": "get_booking_information();"}),
        initial=timezone.now().date(),
    )

    quantity = forms.IntegerField(
        label="Quantity",
        initial=0,
        min_value=1,
        widget=forms.NumberInput(attrs={"onchange": "get_booking_information();"}),
    )

    flight = forms.ModelChoiceField(
        label="Flight",
        queryset=Flight.objects.none(),
        widget=forms.Select(attrs={"onchange": "get_booking_information();"}),
    )

    total_fare = forms.DecimalField(label="Total Fare", required=False, initial=0, min_value=0)

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

        if booking_instance:

            flight_instance = booking_instance.flight
            departure_instance = flight_instance.departure_airport
            arrival_instance = flight_instance.arrival_airport
            departure_time_instance = flight_instance.departure_time
            self.initial["flight"] = flight_instance.pk
        else:
            departure_instance = self.airport_choices[0][0]
            arrival_instance = self.airport_choices[1][0]
            departure_time_instance = timezone.now()

        self.initial["departure"] = departure_instance
        self.initial["arrival"] = arrival_instance
        self.initial["departure_time"] = departure_time_instance

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
        passengers = cleaned_data.get("passengers")
        quantity = cleaned_data.get("quantity")
        if passengers and passengers.count() != quantity:
            self.add_error(
                "passengers",
                forms.ValidationError("please check Quantity fields ."),
            )

        return cleaned_data
