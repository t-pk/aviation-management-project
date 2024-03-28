mkdir ./aviation/fixtures
python ./scripts/aircraft.py
python ./scripts/passenger.py
python ./scripts/flight.py
python manage.py loaddata 0001_Aircraft.json
python manage.py loaddata 0002_Passenger.json
python manage.py loaddata 0003_Flight.json