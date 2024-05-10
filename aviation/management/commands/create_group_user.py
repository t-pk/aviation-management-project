from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User


class Command(BaseCommand):
    help = "Creates a user and group with permissions"

    def handle(self, *args, **options):
        superuser = User.objects.create_superuser(username="admin", email="admin@gmail.com", password="123456")
        self.stdout.write(self.style.SUCCESS(f"Superuser '{superuser.username}' created successfully!"))

        all_permissions = Permission.objects.all()
        superuser.user_permissions.set(all_permissions)
        superuser.is_staff = True
        superuser.save()
        self.stdout.write(self.style.SUCCESS(f"Superuser '{superuser.username}' granted all permissions!"))

        user_flight_manager = User.objects.create_user(username="flightmanager", password="flightmanager")
        self.stdout.write(self.style.SUCCESS(f"User '{user_flight_manager.username}' created successfully!"))
        group_flight_manager, created = Group.objects.get_or_create(name="Flight Manager")

        add_flight_permission = Permission.objects.get(content_type__app_label="aviation", codename="add_flight")
        change_flight_permission = Permission.objects.get(content_type__app_label="aviation", codename="change_flight")
        delete_flight_permission = Permission.objects.get(content_type__app_label="aviation", codename="delete_flight")
        view_flight_permission = Permission.objects.get(content_type__app_label="aviation", codename="view_flight")

        add_airport_permission = Permission.objects.get(content_type__app_label="aviation", codename="add_airport")
        change_airport_permission = Permission.objects.get(
            content_type__app_label="aviation", codename="change_airport"
        )
        delete_airport_permission = Permission.objects.get(
            content_type__app_label="aviation", codename="delete_airport"
        )
        view_airport_permission = Permission.objects.get(content_type__app_label="aviation", codename="view_airport")

        add_aircraft_permission = Permission.objects.get(content_type__app_label="aviation", codename="add_aircraft")
        change_aircraft_permission = Permission.objects.get(
            content_type__app_label="aviation", codename="change_aircraft"
        )
        delete_aircraft_permission = Permission.objects.get(
            content_type__app_label="aviation", codename="delete_aircraft"
        )
        view_aircraft_permission = Permission.objects.get(content_type__app_label="aviation", codename="view_aircraft")

        group_flight_manager.permissions.add(
            add_flight_permission,
            change_flight_permission,
            delete_flight_permission,
            view_flight_permission,
            add_aircraft_permission,
            change_aircraft_permission,
            delete_aircraft_permission,
            view_aircraft_permission,
            add_airport_permission,
            change_airport_permission,
            delete_airport_permission,
            view_airport_permission,
        )

        user_flight_manager.groups.add(group_flight_manager)
        user_flight_manager.is_staff = True
        user_flight_manager.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"User '{user_flight_manager.username}' added to group 'Flight Manager' with permissions!"
            )
        )

        user_ticketing_staff = User.objects.create_user(username="ticketingstaff", password="ticketingstaff")
        self.stdout.write(self.style.SUCCESS(f"User '{user_ticketing_staff.username}' created successfully!"))

        group_ticketing_staff, created = Group.objects.get_or_create(name="Ticketing Staff")

        add_passenger_permission = Permission.objects.get(content_type__app_label="aviation", codename="add_passenger")
        change_passenger_permission = Permission.objects.get(
            content_type__app_label="aviation", codename="change_passenger"
        )
        delete_passenger_permission = Permission.objects.get(
            content_type__app_label="aviation", codename="delete_passenger"
        )
        view_passenger_permission = Permission.objects.get(
            content_type__app_label="aviation", codename="view_passenger"
        )

        add_booking_permission = Permission.objects.get(content_type__app_label="aviation", codename="add_booking")
        change_booking_permission = Permission.objects.get(
            content_type__app_label="aviation", codename="change_booking"
        )
        delete_booking_permission = Permission.objects.get(
            content_type__app_label="aviation", codename="delete_booking"
        )
        view_booking_permission = Permission.objects.get(content_type__app_label="aviation", codename="view_booking")

        group_ticketing_staff.permissions.add(
            add_passenger_permission,
            change_passenger_permission,
            delete_passenger_permission,
            view_passenger_permission,
            add_booking_permission,
            change_booking_permission,
            delete_booking_permission,
            view_booking_permission,
            view_flight_permission,
        )

        user_ticketing_staff.groups.add(group_ticketing_staff)
        user_ticketing_staff.is_staff = True
        user_ticketing_staff.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"User '{user_ticketing_staff.username}' added to group 'Ticketing Staff' with permissions!"
            )
        )
