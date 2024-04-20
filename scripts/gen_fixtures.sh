mkdir -p aviation/fixtures
python -m scripts.aircraft
python -m scripts.airport
python -m scripts.passenger
python -m scripts.flight
python -m scripts.booking


python manage.py loaddata 0001_Aircraft.json
python manage.py loaddata 0002_Airport.json
python manage.py loaddata 0003_Passenger.json
python manage.py loaddata 0004_Flight.json
python manage.py loaddata 0005_Booking.json