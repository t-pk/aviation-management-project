import unittest
from django.core.exceptions import ValidationError
from django.utils import timezone
from django import forms
from aviation.models import Booking  # Assuming models.py is in the same directory
from aviation.forms import BookingForm

# Mock airport data (replace with actual data if available)
mock_airports_data = [
    {"code": "SFO", "name": "San Francisco International Airport"},
    {"code": "LAX", "name": "Los Angeles International Airport"},
]


class BookingFormTest(unittest.TestCase):
    def setUp(self):
        self.form = BookingForm(initial={
            "id": 1,
            "departure": "SFO",
            "arrival": "LAX",
            "departure_time": timezone.now().date(),
            "total_passenger": 2,
        })

    def test_form_has_valid_fields(self):
        """
        Test that the form has the expected fields with correct types.
        """
        self.assertIsInstance(self.form.fields["departure"], forms.ChoiceField)
        self.assertIsInstance(self.form.fields["arrival"], forms.ChoiceField)
        self.assertIsInstance(self.form.fields["departure_time"], forms.DateField)
        self.assertIsInstance(self.form.fields["total_amount"], forms.DecimalField)
        self.assertIsInstance(self.form.fields["total_passenger"], forms.IntegerField)

    def test_form_initial_values(self):
        """
        Test that the form is correctly populated with initial values.
        """
        self.assertEqual(self.form.initial["departure"], "SFO")
        self.assertEqual(self.form.initial["arrival"], "LAX")
        self.assertEqual(self.form.initial["departure_time"], timezone.now().date())
        self.assertEqual(self.form.initial["total_passenger"], 2)

    # def test_form_is_valid_with_valid_data(self):
    #     """
    #     Test that the form validates correctly with valid data.
    #     """
    #     # Assuming a mock passenger list or relevant data structure
    #     mock_passengers = [{"id": 1, "name": "John Doe", "email": "john.doe@example.com"}, {"id": 2, "name": "John Doe1", "email": "john1.doe@example.com"}]
    #     self.form.instance.passengers.set(mock_passengers)  # Set passengers explicitly
    #     self.assertTrue(self.form.is_valid())

    # def test_form_is_invalid_with_inconsistent_passenger_count(self):
    #     """
    #     Test that the form raises an error if total_passenger doesn't match passengers count.
    #     """
    #     self.form.instance.passengers = [{"name": "John Doe", "email": "john.doe@example.com"}]
    #     with self.assertRaises(ValidationError) as cm:
    #         self.form.clean()
    #     self.assertEqual(
    #         cm.exception.message_dict,
    #         {"passengers": ["please check Total Passenger fields."]})

    # Add more tests for other validation rules as needed
