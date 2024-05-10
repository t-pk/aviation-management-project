from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from aviation.admin import AircraftAdmin, AirportAdmin, BookingAdmin, FlightAdmin, PassengerAdmin
from aviation.forms import BookingForm
from aviation.models import Airport, Flight, Aircraft, Booking, Passenger
from django.utils import timezone
from django.test import RequestFactory
from django.contrib.auth.models import User


class FlightAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.flight_admin = FlightAdmin(Flight, self.site)

        self.departure_time = timezone.now()
        self.arrival_time = self.departure_time + timezone.timedelta(hours=3)
        self.aircraft = Aircraft.objects.create(model="Boeing 737", capacity=180, code="ABC123")
        self.airport1 = Airport.objects.create(code="SGN", city="HCM", name="ABC123", latitude=1.1, longitude=1.2)
        self.airport2 = Airport.objects.create(code="HAN", city="HAN", name="ABC122", latitude=2.1, longitude=2.2)

        self.flight = Flight.objects.create(
            departure_airport=self.airport1,
            arrival_airport=self.airport2,
            departure_time=self.departure_time,
            arrival_time=self.arrival_time,
            aircraft=self.aircraft,
        )

        self.passenger1 = Passenger.objects.create(name="Thái", date_of_birth="2010-01-03", sex="F")
        self.passenger2 = Passenger.objects.create(name="Sang", date_of_birth="2010-01-03", sex="F")
        self.passenger3 = Passenger.objects.create(name="Bảo", date_of_birth="2010-01-03", sex="F")

        self.booking1 = Booking.objects.create(flight=self.flight)
        self.booking1.passengers.add(self.passenger1, self.passenger2)

        self.booking2 = Booking.objects.create(flight=self.flight)
        self.booking2.passengers.add(self.passenger3)

    def test_total_passenger(self):
        self.assertEqual(self.flight_admin.total_passenger(self.flight), 3)

    def test_aircraft_code(self):
        self.assertEqual(self.flight_admin.aircraft_code(self.flight), "ABC123")

    def test_duration_time(self):
        expected_duration = self.arrival_time - self.departure_time
        self.assertEqual(self.flight_admin.duration_time(self.flight), expected_duration)

    def test_list_display(self):
        list_display = self.flight_admin.get_list_display(None)
        self.assertEqual(
            list_display,
            [
                "id",
                "departure_airport",
                "arrival_airport",
                "departure_time",
                "arrival_time",
                "aircraft_code",
                "duration_time",
                "capacity",
                "avaiable_seat",
                "total_passenger",
            ],
        )

    def test_search_fields(self):
        search_fields = self.flight_admin.get_search_fields(None)
        self.assertEqual(
            search_fields,
            ["id", "aircraft__code"],
        )

    def test_list_filter(self):
        list_filter = self.flight_admin.get_list_filter(None)
        self.assertEqual(list_filter, ["departure_airport", "arrival_airport", "departure_time", "arrival_time"])


class AircraftAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = AircraftAdmin(Aircraft, self.site)

    def test_list_display(self):
        self.assertEqual(self.admin.list_display, ["id", "model", "code", "capacity"])

    def test_search_fields(self):
        self.assertEqual(self.admin.search_fields, ["id", "model", "code", "capacity"])

    def test_list_filter(self):
        self.assertEqual(self.admin.list_filter, ["model"])

    def test_list_per_page(self):
        self.assertEqual(self.admin.list_per_page, 20)


class AirportAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = AirportAdmin(Airport, self.site)

    def test_list_display(self):
        self.assertEqual(self.admin.list_display, ["id", "code", "city", "name", "latitude", "longitude"])

    def test_search_fields(self):
        self.assertEqual(self.admin.search_fields, ["id", "code", "city", "name"])

    def test_list_filter(self):
        self.assertEqual(self.admin.list_filter, ["code", "city"])

    def test_list_per_page(self):
        self.assertEqual(self.admin.list_per_page, 20)


class PassengerAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = PassengerAdmin(Passenger, self.site)

    def test_list_display(self):
        self.assertEqual(self.admin.list_display, ["id", "name", "date_of_birth", "sex", "email", "phone"])

    def test_search_fields(self):
        self.assertEqual(self.admin.search_fields, ["name", "email", "phone"])

    def test_list_per_page(self):
        self.assertEqual(self.admin.list_per_page, 20)


class BookingAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = BookingAdmin(Booking, self.site)
        self.aircraft = Aircraft.objects.create(model="Boeing 737", capacity=180, code="ABC123")
        self.airport1 = Airport.objects.create(code="SGN", city="HCM", name="ABC123", latitude=1.1, longitude=1.2)
        self.airport2 = Airport.objects.create(code="HAN", city="HAN", name="ABC122", latitude=2.1, longitude=2.2)

        self.flight = Flight.objects.create(
            departure_airport=self.airport1,
            arrival_airport=self.airport2,
            departure_time=timezone.now() + timezone.timedelta(days=1),
            arrival_time=timezone.now() + timezone.timedelta(days=5, hours=2),
            aircraft=self.aircraft,
        )
        self.passenger1 = Passenger.objects.create(name="Thái", date_of_birth="2010-01-03", sex="F")
        self.passenger2 = Passenger.objects.create(name="Thông", date_of_birth="2010-01-03", sex="F")
        self.booking = Booking.objects.create(flight=self.flight)
        self.booking.passengers.add(self.passenger1, self.passenger2)
        self.factory = RequestFactory()

    def test_form_assigned(self):
        self.assertEqual(self.admin.form, BookingForm)

    def test_filter_horizontal(self):
        self.assertEqual(self.admin.filter_horizontal, ["passengers"])

    def test_search_fields(self):
        self.assertEqual(self.admin.search_fields, ["id", "passengers__name"])

    def test_list_display(self):
        expected_list_display = [
            "id",
            "departure_airport",
            "arrival_airport",
            "aircraft_code",
            "departure_time",
            "arrival_time",
            "passenger_names",
            "quantity",
            "total_fare_with_vnd",
            "booking_date",
        ]
        actual_list_display = list(self.admin.list_display)
        self.assertEqual(actual_list_display, expected_list_display)

    def test_list_filter(self):
        expected_list_filter = [
            "flight__departure_time",
            "flight__departure_airport",
            "flight__arrival_airport",
            "flight__aircraft__code",
        ]
        self.assertEqual(self.admin.list_filter, expected_list_filter)

    def test_get_queryset(self):
        request = self.factory.get("/aviation/admin/booking/")
        qs = self.admin.get_queryset(request)
        self.assertIn("passengers", qs._prefetch_related_lookups)

    def test_departure_airport(self):
        self.assertEqual(self.admin.departure_airport(self.booking), self.airport1)

    def test_has_change_permission(self):
        user = User.objects.create(username="test_user")

        request = self.factory.get("aviation/admin/booking/")
        request.user = user

        self.flight.departure_time = timezone.now() - timezone.timedelta(hours=2)
        self.flight.save()
        self.assertFalse(self.admin.has_change_permission(request, self.booking))

    def test_has_delete_permission(self):
        user = User.objects.create(username="test_user")

        request = self.factory.get("aviation/admin/booking/")
        request.user = user

        self.flight.departure_time = timezone.now() - timezone.timedelta(hours=2)
        self.flight.save()
        self.assertFalse(self.admin.has_delete_permission(request, self.booking))

    def test_media(self):
        media = self.admin.media
        self.assertIn("aviation/booking.js", media._js)
