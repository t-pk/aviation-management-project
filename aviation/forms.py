import json
from django import forms
from django.utils import timezone

from aviation.utils import get_airport
from .models import Booking, Flight


class BookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    airport_choices = [
        (airport["code"], f"{airport['code']} - {airport['city']} - {airport['name']}") for airport in get_airport()
    ]

    departure = forms.ChoiceField(
        label="Departure",
        choices=airport_choices,
        widget=forms.Select(attrs={"onchange": "get_booking_information(this.id);"}),
    )

    arrival = forms.ChoiceField(
        label="Arrival",
        choices=airport_choices,
        initial=airport_choices[1][0],
        widget=forms.Select(attrs={"onchange": "get_booking_information(this.id);"}),
    )

    departure_time = forms.DateField(
        label="Departure Time",
        widget=forms.DateInput(attrs={"type": "date", "onchange": "get_booking_information(this.id);", "min": timezone.now().date()}),
        initial=timezone.now().date(),

    )

    quantity = forms.IntegerField(
        label="Quantity",
        initial=0,
        min_value=1,
        widget=forms.NumberInput(attrs={"oninput": "get_booking_information();"}),
    )

    total_fare = forms.DecimalField(label="Total Fare", required=True, initial=0, min_value=0, widget=forms.NumberInput(attrs={'readonly': 'readonly'}))

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
            passenger_count = booking_instance.passengers.count()
            self.initial["quantity"] = passenger_count
        else:
            departure_instance = self.airport_choices[0][0]
            arrival_instance = self.airport_choices[1][0]
            departure_time_instance = timezone.now()

        self.initial["departure"] = departure_instance
        self.initial["arrival"] = arrival_instance
        self.initial["departure_time"] = departure_time_instance

        current_datetime = timezone.now()
        if departure_time_instance.date() == current_datetime.date():
            start_datetime = departure_time_instance.replace(hour=departure_time_instance.hour, minute=departure_time_instance.minute, second=departure_time_instance.second)
        else:
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
        flight_id = self.data.get("flight")

        if "flight" not in cleaned_data or cleaned_data["flight"] is None:
            if flight_id:
                try:
                    cleaned_data["flight"] = Flight.objects.get(pk=flight_id)
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

        return cleaned_data
