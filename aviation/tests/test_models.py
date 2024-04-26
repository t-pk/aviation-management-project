from django.test import TestCase
from aviation.models import Airport, Flight, Aircraft, Passenger, Booking
from django.utils import timezone


class FlightModelTest(TestCase):
    """Test module for Flight model"""

    @classmethod
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

    def test_flight_creation(self):
        """Test that a Flight object can be created successfully"""
        self.assertEqual(self.flight.departure_airport, self.airport1)
        self.assertEqual(self.flight.arrival_airport, self.airport2)

    def test_flight_update(self):
        """Test updating a Flight object"""
        new_departure_time = timezone.now() + timezone.timedelta(days=2)
        new_arrival_time = timezone.now() + timezone.timedelta(days=2, hours=3)

        self.flight.departure_time = new_departure_time
        self.flight.arrival_time = new_arrival_time
        self.flight.save()

        updated_flight = Flight.objects.get(pk=self.flight.pk)
        self.assertEqual(updated_flight.departure_time, new_departure_time)
        self.assertEqual(updated_flight.arrival_time, new_arrival_time)

    def test_flight_deletion(self):
        """Test deleting a Flight object"""
        flight_id = self.flight.pk
        self.flight.delete()

        with self.assertRaises(Flight.DoesNotExist):
            Flight.objects.get(pk=flight_id)

    def test_flight_retrieval(self):
        """Test retrieving a Flight object"""
        retrieved_flight = Flight.objects.get(pk=self.flight.pk)
        self.assertEqual(retrieved_flight, self.flight)


class AircraftModelTest(TestCase):
    """Test module for Aircraft model"""

    def setUp(self):
        self.aircraft = Aircraft.objects.create(model="Boeing 737", capacity=180, code="ABC123")

    def test_aircraft_creation(self):
        """Test creating a valid Aircraft object"""
        self.assertEqual(self.aircraft.model, "Boeing 737")
        self.assertEqual(self.aircraft.capacity, 180)
        self.assertEqual(self.aircraft.code, "ABC123")

    def test_aircraft_update(self):
        """Test updating a Aircraft object"""
        new_model = "Airbus A310"
        new_capacity = 200
        new_code = "VN-1002"

        self.aircraft.model = new_model
        self.aircraft.capacity = new_capacity
        self.aircraft.code = new_code
        self.aircraft.save()

        updated_aircraft = Aircraft.objects.get(pk=self.aircraft.pk)
        self.assertEqual(updated_aircraft.model, new_model)
        self.assertEqual(updated_aircraft.capacity, new_capacity)
        self.assertEqual(updated_aircraft.code, new_code)

    def test_aircraft_deletion(self):
        """Test deleting a Aircraft object"""
        aircraft_id = self.aircraft.pk
        self.aircraft.delete()

        with self.assertRaises(Aircraft.DoesNotExist):
            Aircraft.objects.get(pk=aircraft_id)

    def test_aircraft_retrieval(self):
        """Test retrieving a Aircraft object"""
        retrieved_aircraft = Aircraft.objects.get(pk=self.aircraft.pk)
        self.assertEqual(retrieved_aircraft, self.aircraft)


class AirportModelTest(TestCase):
    """Test module for Airport model"""

    def setUp(self):
        self.airport = Airport.objects.create(
            code="JFK",
            city="New York",
            name="John F. Kennedy International Airport",
            latitude=40.6413,
            longitude=-73.7781,
        )

    def test_airport_creation(self):
        """Test creating a valid Airport object"""
        self.assertEqual(self.airport.code, "JFK")
        self.assertEqual(self.airport.city, "New York")
        self.assertEqual(self.airport.name, "John F. Kennedy International Airport")
        self.assertAlmostEqual(self.airport.latitude, 40.6413)
        self.assertAlmostEqual(self.airport.longitude, -73.7781)

    def test_airport_update(self):
        """Test updating an Airport object"""
        new_code = "LAX"
        new_city = "Los Angeles"
        new_name = "Los Angeles International Airport"
        new_latitude = 33.9416
        new_longitude = -118.4085

        self.airport.code = new_code
        self.airport.city = new_city
        self.airport.name = new_name
        self.airport.latitude = new_latitude
        self.airport.longitude = new_longitude
        self.airport.save()

        updated_airport = Airport.objects.get(pk=self.airport.pk)
        self.assertEqual(updated_airport.code, new_code)
        self.assertEqual(updated_airport.city, new_city)
        self.assertEqual(updated_airport.name, new_name)
        self.assertAlmostEqual(updated_airport.latitude, new_latitude)
        self.assertAlmostEqual(updated_airport.longitude, new_longitude)

    def test_airport_deletion(self):
        """Test deleting an Airport object"""
        airport_id = self.airport.pk
        self.airport.delete()

        with self.assertRaises(Airport.DoesNotExist):
            Airport.objects.get(pk=airport_id)

    def test_airport_retrieval(self):
        """Test retrieving an Airport object"""
        retrieved_airport = Airport.objects.get(pk=self.airport.pk)
        self.assertEqual(retrieved_airport, self.airport)


class PassengerModelTest(TestCase):
    """Test module for Passenger model"""

    def setUp(self):
        self.passenger = Passenger.objects.create(
            name="John Doe",
            email="johndoe@example.com",
            phone="123456789",
            citizen_identify_id="ABC123",
            date_of_birth="2010-01-03",
            sex="F",
        )

    def test_passenger_creation(self):
        """Test creating a valid Passenger object"""
        self.assertEqual(self.passenger.name, "John Doe")
        self.assertEqual(self.passenger.email, "johndoe@example.com")
        self.assertEqual(self.passenger.phone, "123456789")
        self.assertEqual(self.passenger.citizen_identify_id, "ABC123")
        self.assertEqual(self.passenger.date_of_birth, "2010-01-03")
        self.assertEqual(self.passenger.sex, "F")

    def test_passenger_update(self):
        """Test updating a Passenger object"""
        new_name = "Jane Smith"
        new_email = "janesmith@example.com"
        new_phone = "987654321"
        new_citizen_identify_id = "XYZ789"

        self.passenger.name = new_name
        self.passenger.email = new_email
        self.passenger.phone = new_phone
        self.passenger.citizen_identify_id = new_citizen_identify_id
        self.passenger.save()

        updated_passenger = Passenger.objects.get(pk=self.passenger.pk)
        self.assertEqual(updated_passenger.name, new_name)
        self.assertEqual(updated_passenger.email, new_email)
        self.assertEqual(updated_passenger.phone, new_phone)
        self.assertEqual(updated_passenger.citizen_identify_id, new_citizen_identify_id)

    def test_passenger_deletion(self):
        """Test deleting a Passenger object"""
        passenger_id = self.passenger.pk
        self.passenger.delete()

        with self.assertRaises(Passenger.DoesNotExist):
            Passenger.objects.get(pk=passenger_id)

    def test_passenger_retrieval(self):
        """Test retrieving a Passenger object"""
        retrieved_passenger = Passenger.objects.get(pk=self.passenger.pk)
        self.assertEqual(retrieved_passenger, self.passenger)


class BookingModelTest(TestCase):
    """Test module for Booking model"""

    booking_date = timezone.now()

    def setUp(self):
        # Create passengers
        self.passenger = Passenger.objects.create(
            name="John Doe",
            email="johndoe@example.com",
            phone="123456789",
            citizen_identify_id="ABC123",
            date_of_birth="2010-01-03",
            sex="F",
        )

        self.aircraft = Aircraft.objects.create(model="Boeing 737", capacity=180, code="ABC123")

        self.airport1 = Airport.objects.create(code="SGN", city="HCM", name="ABC123", latitude=1.1, longitude=1.2)
        self.airport2 = Airport.objects.create(code="HAN", city="HAN", name="ABC122", latitude=2.1, longitude=2.2)
        self.flight1 = Flight.objects.create(
            departure_airport=self.airport1,
            arrival_airport=self.airport2,
            departure_time=timezone.now() + timezone.timedelta(days=1),
            arrival_time=timezone.now() + timezone.timedelta(days=1, hours=2),
            aircraft=self.aircraft,
        )
        self.flight2 = Flight.objects.create(
            departure_airport=self.airport2,
            arrival_airport=self.airport1,
            departure_time=timezone.now() + timezone.timedelta(days=1),
            arrival_time=timezone.now() + timezone.timedelta(days=1, hours=2),
            aircraft=self.aircraft,
        )
        # Create bookings
        self.booking1 = Booking.objects.create(
            flight=self.flight1, booking_date=self.booking_date, total_fare=2_000_000
        )
        self.booking1.passengers.add(self.passenger)

        self.booking2 = Booking.objects.create(
            flight=self.flight2, booking_date=self.booking_date, total_fare=2_500_000
        )
        self.booking2.passengers.add(self.passenger)

    def test_booking_creation(self):
        """Test creating a valid Booking object"""
        self.assertEqual(self.booking1.flight, self.flight1)
        self.assertEqual(self.booking1.booking_date, self.booking_date)
        self.assertEqual(self.booking1.total_fare, 2_000_000)
        self.assertEqual(self.booking1.passengers.count(), 1)
        self.assertEqual(self.booking1.passengers.first(), self.passenger)

        self.assertEqual(self.booking2.flight, self.flight2)
        self.assertEqual(self.booking2.booking_date, self.booking_date)
        self.assertEqual(self.booking2.total_fare, 2_500_000)
        self.assertEqual(self.booking2.passengers.count(), 1)
        self.assertEqual(self.booking2.passengers.first(), self.passenger)

    def test_booking_update(self):
        """Test updating a Booking object"""

        self.airport3 = Airport.objects.create(code="DLI", city="DLI", name="ABC123", latitude=1.1, longitude=1.2)
        self.airport4 = Airport.objects.create(code="HXN", city="HXN", name="ABC122", latitude=2.1, longitude=2.2)

        self.flight3 = Flight.objects.create(
            departure_airport=self.airport3,
            arrival_airport=self.airport4,
            departure_time=timezone.now() + timezone.timedelta(days=1),
            arrival_time=timezone.now() + timezone.timedelta(days=1, hours=2),
            aircraft=self.aircraft,
        )
        new_booking_date = timezone.now()
        new_total_fare = 3_500_000

        self.booking1.flight = self.flight3
        self.booking1.booking_date = new_booking_date
        self.booking1.total_fare = new_total_fare
        self.booking1.save()
        updated_booking = Booking.objects.get(pk=self.booking1.pk)
        self.assertEqual(updated_booking.flight, self.flight3)
        self.assertEqual(updated_booking.booking_date, new_booking_date)
        self.assertEqual(updated_booking.total_fare, new_total_fare)

    def test_booking_deletion(self):
        """Test deleting a Booking object"""
        booking_id = self.booking1.pk
        self.booking1.delete()

        with self.assertRaises(Booking.DoesNotExist):
            Booking.objects.get(pk=booking_id)

    def test_booking_retrieval(self):
        """Test retrieving a Booking object"""
        retrieved_booking = Booking.objects.get(pk=self.booking1.pk)
        self.assertEqual(retrieved_booking, self.booking1)
