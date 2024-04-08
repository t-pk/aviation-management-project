import json
from django import forms
from django.utils import timezone
from .models import Booking


class BookingForm(forms.ModelForm):
    with open("./mock/airports.json") as airports_file:
        airport_data = json.load(airports_file)

    airport_choices = [
        (airport["code"], f"{airport['code']} - {airport['city']} - {airport['name']}") for airport in airport_data
    ]

    departure = forms.ChoiceField(label="Departure", choices=airport_choices)
    arrival = forms.ChoiceField(label="Arrival", choices=airport_choices)
    departure_time = forms.DateField(
        label="Departure Date",
        widget=forms.DateInput(attrs={"type": "date"}),
        initial=timezone.now().date(),
    )
    total_amount = forms.DecimalField(label="Total Amount", required=False, initial=0)
    total_passenger = forms.IntegerField(label="Total Passenger", initial=0, min_value=1)

    class Meta:
        model = Booking
        fields = [
            "departure",
            "arrival",
            "departure_time",
            "flight",
            "total_passenger",
            "passengers",
            "total_amount",
        ]

    def clean(self):
        cleaned_data = super().clean()
        passengers = cleaned_data.get("passengers")
        total_passenger = cleaned_data.get("total_passenger")
        if passengers and passengers.count() != total_passenger:
            self.add_error(
                "passengers",
                forms.ValidationError("please check Total Passenger fields ."),
            )

        return cleaned_data
