from django.test import TestCase, Client
from aviation.models import Aircraft, Booking, Flight
from datetime import datetime, timedelta
from django.contrib.auth.models import User


class TestBookingFlightView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")

    def test_valid_post_request(self):
        # Create test flight
        self.client.login(username="testuser", password="password123")
        aircraft = Aircraft.objects.create(model="Boeing 777", capacity=300, code="GHI789")

        flight = Flight.objects.create(
            departure_airport="SGN",
            arrival_airport="HAN",
            departure_time=datetime.now(),
            arrival_time=datetime.now(),
            aircraft=aircraft,
        )

        # Make post request
        response = self.client.post(
            f"/aviation/flights/",
            {
                "departure_airport": "SGN",
                "arrival_airport": "HAN",
                "departure_time": datetime.now().strftime("%Y-%m-%d"),
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue("flights" in response.json())

    # Add more test cases for invalid requests, missing data, etc.


class TestRetrieveBookingView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")

    def test_retrieve_existing_booking(self):
        # Create test booking
        aircraft = Aircraft.objects.create(model="Boeing 777", capacity=300, code="GHI789")

        flight = Flight.objects.create(
            departure_airport="SGN",
            arrival_airport="HAN",
            departure_time=datetime.now(),
            arrival_time=datetime.now(),
            aircraft=aircraft,
        )
        booking = Booking.objects.create(flight=flight)

        # Make get request
        response = self.client.get(f"/aviation/bookings/{booking.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("departure_airport" in response.json())
        self.assertEqual(response.json()["departure_airport"], "SGN")
        # Add more assertions for other fields

    # Add test cases for non-existent booking ID, etc.


class TestCalculateFaresView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")

    def test_valid_get_request(self):
        # Make get request with valid parameters
        response = self.client.get(
            f"/aviation/fares/", {"departure_code": "SGN", "arrival_code": "HAN", "total_passenger": 2}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue("distance" in response.json())
        self.assertTrue("fare" in response.json())
        self.assertTrue("total_fare" in response.json())

    def test_missing_parameters(self):
        # Test with missing parameters
        response = self.client.get(f"/aviation/fares/")
        self.assertEqual(response.status_code, 400)
        self.assertTrue("error" in response.json())

    def test_invalid_airport_code(self):
        # Test with invalid airport code
        response = self.client.get(
            f"/aviation/fares/", {"departure_code": "INVALID", "arrival_code": "HAN", "total_passenger": 2}
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue("error" in response.json())

    def test_invalid_passenger_count(self):
        # Test with invalid passenger count (non-integer value)
        response = self.client.get(
            f"/aviation/fares/", {"departure_code": "SGN", "arrival_code": "HAN", "total_passenger": "invalid"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue("error" in response.json())

    def test_negative_passenger_count(self):
        # Test with negative passenger count
        response = self.client.get(
            f"/aviation/fares/", {"departure_code": "SGN", "arrival_code": "HAN", "total_passenger": -2}
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue("error" in response.json())

    def test_zero_passenger_count(self):
        # Test with zero passenger count
        response = self.client.get(
            f"/aviation/fares/", {"departure_code": "SGN", "arrival_code": "HAN", "total_passenger": 0}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue("distance" in response.json())
        self.assertTrue("fare" in response.json())
        self.assertTrue("total_fare" in response.json())
