install python, pipenv, docker (docker-compose).
run source by command: ```python manage.py runserver```. should be port default 8000.

we use https://www.mockaroo.com/ to create mock data.


```bash
# setup enviroment to develop
pip install pipenv
pipenv shell

pipenv install
pipenv shell

# setup database
docker compose up

# need to create migration
python manage.py makemigrations
python manage.py migrate

# create 3 users and groups
python manage.py create_group_user
```


we have 3 users

```
#supper admin
username: admin
password: 123456

#ticketingstaff
username: ticketingstaff
password: ticketingstaff

#flightmanager
username: flightmanager
password: flightmanager
```

We also support running testcases with the command

```
 ./manage.py test
```

Running a specifict test case
```
test_models is file name.
python ./manage.py test aviation.tests.test_models
```

result run test
```
$ coverage run --source='.' manage.py test
Found 60 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
............DEBUG    has_change_permission request <WSGIRequest: GET '/aviationadmin/booking/'> obj 5 user test_user is supper user False
DEBUG    flight.departure_time = 2024-04-12 07:46:44.507003 timezone.now() = 2024-04-12 09:46:44.509755
.DEBUG    has_delete_permission request <WSGIRequest: GET '/aviationadmin/booking/'> obj 6 user test_user is supper user False
DEBUG    flight.departure_time = 2024-04-12 07:46:44.536226 timezone.now() = 2024-04-12 09:46:44.539359
...............DEBUG    Departure Time: 2024-04-12, Current Date: 2024-04-12, Same Date Check: True
DEBUG    flight information ABC123 | 09:46 | 11:46 | 180 (avail seats)
.DEBUG    Departure Time: 2024-04-12, Current Date: 2024-04-12, Same Date Check: True
DEBUG    flight information ABC123 | 09:46 | 11:46 | 180 (avail seats)
.DEBUG    Departure Time: 2024-04-12, Current Date: 2024-04-12, Same Date Check: True
.DEBUG    Departure Time: 2024-04-12, Current Date: 2024-04-12, Same Date Check: True
DEBUG    flight information ABC123 | 09:46 | 11:46 | 180 (avail seats)
.DEBUG    Departure Time: 2024-04-12, Current Date: 2024-04-12, Same Date Check: True
DEBUG    flight information ABC123 | 09:46 | 11:46 | 180 (avail seats)
.DEBUG    Departure Time: 2024-04-12, Current Date: 2024-04-12, Same Date Check: True
DEBUG    flight information ABC123 | 09:46 | 11:46 | 180 (avail seats)
.DEBUG    departure_airport HAN - ABC122 (HAN) arrival_airport HAN - ABC122 (HAN)
.DEBUG    departure_airport SGN - ABC123 (HCM) arrival_airport HAN - ABC122 (HAN)
.DEBUG    departure_airport SGN - ABC123 (HCM) arrival_airport HAN - ABC122 (HAN)
.DEBUG    departure_airport SGN - ABC123 (HCM) arrival_airport HAN - ABC122 (HAN)
.....................WARNING  Unauthorized: /aviation/get-booking-information/
.DEBUG    API get-booking-information query: <QueryDict: {'departure': ['77'], 'arrival': ['78'], 'departure_time': ['2024-04-13'], 'quantity': ['1']}>
DEBUG    departure_airport: SGN - ABC123 (HCM) HAN - ABC122 (HAN)
.
----------------------------------------------------------------------
Ran 60 tests in 2.519s

OK
Destroying test database for alias 'default'...
$ coverage report

Name                                  Stmts   Miss  Cover
---------------------------------------------------------
aviation/__init__.py                      0      0   100%
aviation/admin.py                       111     15    86%
aviation/apps.py                          4      0   100%
aviation/forms.py                        94     16    83%
aviation/migrations/0001_initial.py       8      0   100%
aviation/migrations/__init__.py           0      0   100%
aviation/models.py                       51      2    96%
aviation/tests/__init__.py                0      0   100%
aviation/tests/test_admins.py           126      0   100%
aviation/tests/test_forms.py             72      0   100%
aviation/tests/test_models.py           169      0   100%
aviation/tests/test_views.py             32      0   100%
aviation/urls.py                          3      0   100%
aviation/utils.py                        31      1    97%
aviation/views.py                        32      1    97%
config/__init__.py                        0      0   100%
config/settings.py                       28      0   100%
config/urls.py                            9      0   100%
manage.py                                12      2    83%
---------------------------------------------------------
TOTAL                                   782     37    95%
```

