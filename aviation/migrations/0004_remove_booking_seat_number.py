# Generated by Django 5.0.3 on 2024-03-27 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("aviation", "0003_alter_booking_booking_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="booking",
            name="seat_number",
        ),
    ]