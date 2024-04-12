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
DEBUG    couldn't import psycopg 'c' implementation: No module named 'psycopg_c'
DEBUG    couldn't import psycopg 'binary' implementation: No module named 'psycopg_binary'
Found 32 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
DEBUG    Departure Time: 2024-04-12, Current Date: 2024-04-12, Same Date Check: True
DEBUG    flight information ABC123 | 03:51 | 05:51 | 180 (avail seats)
.DEBUG    Departure Time: 2024-04-12, Current Date: 2024-04-12, Same Date Check: True
DEBUG    flight information ABC123 | 03:51 | 05:51 | 180 (avail seats)
.DEBUG    Departure Time: 2024-04-12, Current Date: 2024-04-12, Same Date Check: True
.DEBUG    Departure Time: 2024-04-12, Current Date: 2024-04-12, Same Date Check: True
DEBUG    flight information ABC123 | 03:51 | 05:51 | 180 (avail seats)
.DEBUG    Departure Time: 2024-04-12, Current Date: 2024-04-12, Same Date Check: True
DEBUG    flight information ABC123 | 03:51 | 05:51 | 180 (avail seats)
.DEBUG    Departure Time: 2024-04-12, Current Date: 2024-04-12, Same Date Check: True
DEBUG    flight information ABC123 | 03:51 | 05:51 | 180 (avail seats)
.DEBUG    departure_airport HAN - ABC122 (HAN) arrival_airport HAN - ABC122 (HAN)
.DEBUG    departure_airport SGN - ABC123 (HCM) arrival_airport HAN - ABC122 (HAN)
.DEBUG    departure_airport SGN - ABC123 (HCM) arrival_airport HAN - ABC122 (HAN)
.DEBUG    departure_airport SGN - ABC123 (HCM) arrival_airport HAN - ABC122 (HAN)
.....................WARNING  Unauthorized: /aviation/get-booking-information/
.DEBUG    API get-booking-information query: <QueryDict: {'departure': ['45'], 'arrival': ['46'], 'departure_time': ['2024-04-13'], 'quantity': ['1']}>
DEBUG    departure_airport: SGN - ABC123 (HCM) HAN - ABC122 (HAN)
.
----------------------------------------------------------------------
Ran 32 tests in 1.756s

OK
Destroying test database for alias 'default'...

$ coverage report

Name                                  Stmts   Miss  Cover
---------------------------------------------------------
aviation/__init__.py                      0      0   100%
aviation/admin.py                       111     33    70%
aviation/apps.py                          4      0   100%
aviation/forms.py                        94     16    83%
aviation/migrations/0001_initial.py       8      0   100%
aviation/migrations/__init__.py           0      0   100%
aviation/models.py                       51      3    94%
aviation/tests/__init__.py                0      0   100%
aviation/tests/test_forms.py             72      0   100%
aviation/tests/test_models.py           169      0   100%
aviation/tests/test_views.py             31      0   100%
aviation/urls.py                          3      0   100%
aviation/utils.py                        31      2    94%
aviation/views.py                        33      1    97%
config/__init__.py                        0      0   100%
config/asgi.py                            4      4     0%
config/settings.py                       28      0   100%
config/urls.py                            9      0   100%
config/wsgi.py                            4      4     0%
manage.py                                12      2    83%
---------------------------------------------------------
TOTAL                                   664     65    90%
```

