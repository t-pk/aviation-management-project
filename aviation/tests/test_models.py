from django.test import TestCase
from aviation.models import Flight, Aircraft, Passenger, Booking
from django.utils import timezone


class FlightModelTest(TestCase):
    """Test module for Flight model"""

    @classmethod
    def setUp(self):
        self.aircraft = Aircraft.objects.create(model="Boeing 737", capacity=180, code="ABC123")
        self.flight = Flight.objects.create(
            departure_airport="SFO",
            arrival_airport="LAX",
            departure_time=timezone.now() + timezone.timedelta(days=1),
            arrival_time=timezone.now() + timezone.timedelta(days=1, hours=2),
            aircraft=self.aircraft,
        )

    def test_flight_creation(self):
        """Test that a Flight object can be created successfully"""
        self.assertEqual(self.flight.departure_airport, "SFO")
        self.assertEqual(self.flight.arrival_airport, "LAX")

    def test_flight_str_representation(self):
        """Test the string representation of a Flight object"""
        self.assertEqual(
            str(self.flight),
            f"{self.aircraft.code} | {self.flight.departure_time.time().strftime('%H:%M')} | {self.flight.arrival_time.time().strftime('%H:%M')}",
        )


class AircraftModelTest(TestCase):
    """Test module for Aircraft model"""

    def test_aircraft_creation(self):
        """Test that an Aircraft object can be created successfully"""
        aircraft = Aircraft.objects.create(model="A320", capacity=150, code="DEF456")
        self.assertEqual(aircraft.model, "A320")
        self.assertEqual(aircraft.capacity, 150)


class PassengerModelTest(TestCase):
    """Test module for Passenger model"""

    def test_passenger_creation(self):
        """Test that a Passenger object can be created successfully"""
        passenger = Passenger.objects.create(name="John Doe", email="john.doe@example.com", phone="1234567890")
        self.assertEqual(passenger.name, "John Doe")
        self.assertEqual(passenger.email, "john.doe@example.com")
        self.assertEqual(passenger.phone, "1234567890")


class BookingModelTest(TestCase):
    """Test module for Booking model"""

    @classmethod
    def setUp(self):
        self.aircraft = Aircraft.objects.create(model="Boeing 777", capacity=300, code="GHI789")
        self.flight = Flight.objects.create(
            departure_airport="JFK",
            arrival_airport="LHR",
            departure_time=timezone.now() + timezone.timedelta(days=2),
            arrival_time=timezone.now() + timezone.timedelta(days=2, hours=8),
            aircraft=self.aircraft,
        )
        self.passenger1 = Passenger.objects.create(name="Jane Smith", email="jane.smith@example.com")
        self.passenger2 = Passenger.objects.create(name="Michael Brown", phone="9876543210")
        self.booking = Booking.objects.create(flight=self.flight)
        self.booking.passengers.add(self.passenger1, self.passenger2)

    def test_booking_creation(self):
        """Test that a Booking object can be created successfully"""
        self.assertEqual(self.booking.flight, self.flight)
        self.assertEqual(self.booking.passengers.count(), 2)

    def test_booking_str_representation(self):
        """Test the string representation of a Booking object"""
        self.assertEqual(str(self.booking), f"{self.booking.id}")
