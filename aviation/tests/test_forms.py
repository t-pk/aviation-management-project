import json
from django.test import TestCase
from django.utils import timezone
from aviation.models import Passenger, Flight, Aircraft
from aviation.forms import BookingForm
from datetime import timedelta


class BookingFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.aircraft = Aircraft.objects.create(
            model="Boeing 747",
            capacity=300,
            code="ABC123"
        )

        cls.flight = Flight.objects.create(
            departure_airport="SGN",
            arrival_airport="HAN",
            departure_time=timezone.now(),
            arrival_time=timezone.now() + timedelta(hours=2),
            aircraft=cls.aircraft
        )
        cls.passenger1 = Passenger.objects.create(name="Tâm")
        cls.passenger2 = Passenger.objects.create(name="Nguyệt")
        cls.passenger3 = Passenger.objects.create(name="Như")

        cls.passenger1.relation = cls.passenger2
        cls.passenger1.save()
        cls.passenger2.relation = cls.passenger1
        cls.passenger2.save()

    def test_valid_form(self):
        form_data = {
            'departure': 'SGN',
            'arrival': 'HAN',
            'flight': self.flight.pk,
            'departure_time': timezone.now().date(),
            'total_passenger': 2,
            'passengers': [self.passenger1.pk, self.passenger2.pk],
            'total_amount': 200
        }
        form = BookingForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_form(self):
        form_data = {
            'departure': 'SGN',
            'arrival': 'HAN',
            'flight': self.flight.pk,
            'departure_time': timezone.now().date(),
            'total_passenger': 2,
            'passengers': [self.passenger1.pk, self.passenger2.pk],
            'total_amount': 200
        }
        form = BookingForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_flight(self):
        form_data = {
            'departure': 'SGN',
            'arrival': 'HAN',
            'departure_time': timezone.now().date(),
            'total_passenger': 2,
            'passengers': [self.passenger1.pk, self.passenger2.pk],
            'total_amount': 200
        }
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('flight', form.errors)

    def test_invalid_form_exceeding_pasengers(self):
        form_data = {
            'departure': 'SGN',
            'arrival': 'HAN',
            'flight': self.flight.pk,
            'departure_time': timezone.now().date(),
            'total_passenger':  1,
            'passengers': [self.passenger1.pk, self.passenger2.pk],
            'total_amount': 200
        }
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('passengers', form.errors)
