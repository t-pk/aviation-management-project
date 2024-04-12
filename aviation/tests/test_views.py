from django.test import TestCase, Client
from django.utils import timezone
from aviation.models import Aircraft, Airport, Flight
from django.contrib.auth.models import User
from django.urls import reverse
import json

class BookingViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.aircraft = Aircraft.objects.create(model="Boeing 737", capacity=180, code="ABC123")
        self.airport1 = Airport.objects.create(code="SGN", city="HCM", name="ABC123", latitude=1.1, longitude=1.2)
        self.airport2 = Airport.objects.create(code="HAN", city="HAN", name="ABC122", latitude=2.1, longitude=2.2)

        # Create some sample flights
        self.departure_time = timezone.now() + timezone.timedelta(days=1)
        self.arrival_time =timezone.now() + timezone.timedelta(days=1, hours=2)

        self.flight = Flight.objects.create(
            departure_airport=self.airport1,
            arrival_airport=self.airport2,
            departure_time=timezone.now() + timezone.timedelta(days=1),
            arrival_time=timezone.now() + timezone.timedelta(days=1, hours=2),
            aircraft=self.aircraft,
        )

    def test_booking_view_get_invalid(self):
        query_params = {
            'departure': self.airport1.pk,
            'arrival': self.airport2.pk,
            'departure_time': self.departure_time.strftime("%Y-%m-%d"),
            'quantity': 1,
        }
        url = reverse('get_booking_information')  # Assuming the URL name is 'booking_view'
        response = self.client.get(url, query_params,  content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_booking_view_get_valid(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")

        query_params = {
            'departure': self.airport1.pk,
            'arrival': self.airport2.pk,
            'departure_time': self.departure_time.strftime("%Y-%m-%d"),
            'quantity': 1,
        }
        response = self.client.get(f"/aviation/get-booking-information/", query_params,  content_type="application/json")

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertIn('flights', response_data)
        self.assertIn('fare', response_data)
        self.assertEqual(len(response_data['flights']), 1)
        self.assertEqual(response_data['flights'][0]['pk'], self.flight.pk)
