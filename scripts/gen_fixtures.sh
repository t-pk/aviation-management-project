mkdir -p aviation/fixtures
python ./scripts/aircraft.py
python ./scripts/airport.py
python ./scripts/passenger.py
python ./scripts/flight.py
python ./scripts/booking.py


python manage.py loaddata 0001_Aircraft.json
python manage.py loaddata 0002_Airport.json
python manage.py loaddata 0003_Passenger.json
python manage.py loaddata 0004_Flight.json
python manage.py loaddata 0005_Booking.json