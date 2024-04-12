from django.test import TestCase
from django.utils import timezone

from aviation.forms import BookingForm, FlightForm
from aviation.models import Aircraft, Airport, Flight, Passenger

class BookingFormTest(TestCase):
    def setUp(self):
        self.aircraft = Aircraft.objects.create(model="Boeing 737", capacity=180, code="ABC123")
        self.airport1 = Airport.objects.create(code="SGN", city="HCM", name="ABC123", latitude=1.1, longitude=1.2)
        self.airport2 = Airport.objects.create(code="HAN", city="HAN", name="ABC122", latitude=2.1, longitude=2.2)

        self.flight = Flight.objects.create(
            departure_airport=self.airport1,
            arrival_airport=self.airport2,
            departure_time=timezone.now() + timezone.timedelta(days=1),
            arrival_time=timezone.now() + timezone.timedelta(days=1, hours=2),
            aircraft=self.aircraft,
        )
        self.flight.save()
        self.passenger1 = Passenger.objects.create(name="Tâm")
        self.passenger2 = Passenger.objects.create(name="Nguyệt")
        self.passenger3 = Passenger.objects.create(name="Như")

        self.passenger1.relation = self.passenger2
        self.passenger1.save()
        self.passenger2.relation = self.passenger1
        self.passenger2.save()
        self.booking_data = {
            'departure': self.airport1.pk,
            'arrival': self.airport2.pk,
            'departure_time': timezone.now(),
            'flight': self.flight,
            'quantity': 2,
            'passengers': [self.passenger1, self.passenger2],
            'total_fare': 2_700_000,
        }

    def test_booking_form_valid(self):
        form = BookingForm(data=self.booking_data)
        self.assertTrue(form.is_valid())

    def test_booking_form_invalid_by_quantity(self):
        invalid_data = self.booking_data.copy()
        invalid_data['quantity'] = 0
        form = BookingForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_booking_form_invalid_by_total_fare(self):
        invalid_data = self.booking_data.copy()
        invalid_data['total_fare'] = -1
        form = BookingForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_booking_form_invalid_by_flight(self):
        invalid_data = self.booking_data.copy()
        invalid_data['flight'] = None
        form = BookingForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_booking_form_invalid_by_departure(self):
        invalid_data = self.booking_data.copy()
        invalid_data['departure'] = None
        form = BookingForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_booking_form_invalid_by_arrival(self):
        invalid_data = self.booking_data.copy()
        invalid_data['arrival'] = None
        form = BookingForm(data=invalid_data)
        self.assertFalse(form.is_valid())


class FlightFormTestCase(TestCase):
    def setUp(self):
        self.aircraft = Aircraft.objects.create(model="Boeing 737", capacity=180, code="ABC123")
        self.airport1 = Airport.objects.create(code="SGN", city="HCM", name="ABC123", latitude=1.1, longitude=1.2)
        self.airport2 = Airport.objects.create(code="HAN", city="HAN", name="ABC122", latitude=2.1, longitude=2.2)

        self.valid_flight_data = {
            'departure_airport': self.airport1,
            'arrival_airport': self.airport2,
            'departure_time': timezone.now() + timezone.timedelta(days=1),
            'arrival_time': timezone.now() + timezone.timedelta(days=1, hours=2),
            'aircraft':self.aircraft,
        }
        self.invalid_flight_data = {
            'departure_airport': self.airport1,
            'arrival_airport': self.airport2,  
            'departure_time': timezone.now() + timezone.timedelta(days=1),
            'arrival_time': timezone.now() + timezone.timedelta(days=1, hours=2),
            'aircraft':self.aircraft,
        }

    def test_flight_form_valid(self):
        form = FlightForm(data=self.valid_flight_data)
        self.assertTrue(form.is_valid())

    def test_flight_form_invalid_by_airport(self):
        invalid_data = self.invalid_flight_data.copy()
        invalid_data['departure_airport'] = self.airport2
        form = FlightForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_flight_form_invalid_by_departure_time(self):
        invalid_data = self.invalid_flight_data.copy()
        invalid_data['departure_time'] = None
        form = FlightForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_flight_form_invalid_by_arrival_time(self):
        invalid_data = self.invalid_flight_data.copy()
        invalid_data['arrival_time'] = None
        form = FlightForm(data=invalid_data)
        self.assertFalse(form.is_valid())
