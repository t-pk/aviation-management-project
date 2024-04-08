# Generated by Django 5.0.3 on 2024-04-08 09:26

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Aircraft",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "model",
                    models.CharField(
                        max_length=100,
                        validators=[
                            django.core.validators.MinLengthValidator(4),
                            django.core.validators.MaxLengthValidator(100),
                        ],
                    ),
                ),
                (
                    "capacity",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(100),
                            django.core.validators.MaxValueValidator(1000),
                        ]
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        max_length=8,
                        validators=[
                            django.core.validators.MinLengthValidator(3),
                            django.core.validators.MaxLengthValidator(8),
                        ],
                    ),
                ),
            ],
            options={
                "db_table": "aviation_aircraft",
            },
        ),
        migrations.CreateModel(
            name="Flight",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "departure_airport",
                    models.CharField(
                        max_length=4,
                        validators=[
                            django.core.validators.MinLengthValidator(2),
                            django.core.validators.MaxLengthValidator(4),
                        ],
                    ),
                ),
                (
                    "arrival_airport",
                    models.CharField(
                        max_length=4,
                        validators=[
                            django.core.validators.MinLengthValidator(2),
                            django.core.validators.MaxLengthValidator(4),
                        ],
                    ),
                ),
                ("departure_time", models.DateTimeField()),
                ("arrival_time", models.DateTimeField()),
                ("aircraft", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="aviation.aircraft")),
            ],
            options={
                "db_table": "aviation_flight",
            },
        ),
        migrations.CreateModel(
            name="Passenger",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "name",
                    models.CharField(
                        max_length=100,
                        validators=[
                            django.core.validators.MinLengthValidator(6),
                            django.core.validators.MaxLengthValidator(100),
                        ],
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, null=True, validators=[django.core.validators.EmailValidator()]
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True, max_length=20, null=True, validators=[django.core.validators.MaxLengthValidator(20)]
                    ),
                ),
                (
                    "citizen_identify_id",
                    models.CharField(
                        blank=True, max_length=15, null=True, validators=[django.core.validators.MaxLengthValidator(15)]
                    ),
                ),
                (
                    "relation",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="aviation.passenger"
                    ),
                ),
            ],
            options={
                "db_table": "aviation_passenger",
            },
        ),
        migrations.CreateModel(
            name="Booking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("booking_date", models.DateField(default=django.utils.timezone.now)),
                (
                    "total_fare",
                    models.DecimalField(
                        decimal_places=0,
                        default=0,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("flight", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="aviation.flight")),
                ("passengers", models.ManyToManyField(to="aviation.passenger")),
            ],
            options={
                "db_table": "aviation_booking",
            },
        ),
    ]
